from telethon import TelegramClient

# --- COLA AQUI OS TEUS DADOS ---
api_id = 32858856          # Substitui pelo teu número (sem aspas)
api_hash = 'd17f8094408cde03f803b076748f5ef4' # Substitui pela tua hash (mantém as aspas)
phone = '+5521995392046'   # Teu número com código do país (+55) e DDD

# Cria a sessão (isso vai criar um arquivo .session na pasta)
client = TelegramClient('anon', api_id, api_hash)

async def main():
    # Envia uma mensagem para ti mesmo ("Saved Messages")
    await client.send_message('me', 'Olá, Mestre! A automação começou. 🤖')
    print("Mensagem enviada! Verifica o teu Telegram.")

with client:
    client.loop.run_until_complete(main())