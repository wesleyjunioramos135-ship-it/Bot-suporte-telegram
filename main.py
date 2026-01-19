import logging
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

# --- CONFIGURAÇÕES ---
TOKEN = "SEU_TOKEN_AQUI"
ID_DO_GRUPO = -1001234567890  # Coloque o ID do seu grupo aqui (com o -100)
TEMPO_ENTRE_MENSAGENS = 3600  # Tempo em segundos (ex: 3600 = 1 hora)

# Mensagem de cobrança
TEXTO_COBRANCA = (
    "🚨 **ATENÇÃO MEMBROS** 🚨\n\n"
    "Para permanecer no grupo, é OBRIGATÓRIO compartilhar o link abaixo!\n"
    "O sistema está monitorando membros inativos.\n\n"
    "👉 t.me/SEU_LINK_AQUI\n\n"
    "Quem não ajudar o grupo a crescer será removido em breve!"
)

# Configuração de Logs (importante para a Square Cloud)
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def enviar_cobranca(context: ContextTypes.DEFAULT_TYPE):
    """Função que envia a mensagem no grupo."""
    try:
        await context.bot.send_message(
            chat_id=ID_DO_GRUPO,
            text=TEXTO_COBRANCA,
            parse_mode='Markdown'
        )
        logging.info("Mensagem de cobrança enviada com sucesso.")
    except Exception as e:
        logging.error(f"Erro ao enviar cobrança: {e}")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando para iniciar o bot e verificar se está online."""
    await update.message.reply_text("Bot de Gerenciamento Online! 🚀")

def main():
    application = ApplicationBuilder().token(TOKEN).build()

    # Adiciona o JobQueue para enviar mensagens automaticamente
    job_queue = application.job_queue
    # Envia a primeira mensagem 10 segundos após ligar
    job_queue.run_once(enviar_cobranca, 10)
    # Envia repetidamente a cada X segundos
    job_queue.run_repeating(enviar_cobranca, interval=TEMPO_ENTRE_MENSAGENS, first=10)

    application.add_handler(CommandHandler("start", start))

    print("Bot rodando...")
    application.run_polling()

if __name__ == '__main__':
    main()
  
