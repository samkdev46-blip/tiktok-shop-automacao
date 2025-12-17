import asyncio
from telethon import TelegramClient
from supabase import create_client, Client

# --- 1. DADOS DO TELEGRAM (Já testados) ---
api_id = 32858856          # Teu ID
api_hash = 'd17f8094408cde03f803b076748f5ef4'     # Tua Hash

# --- 2. DADOS DO SUPABASE (O Novo) ---
url_supabase = "https://cqvczuuonchjqpofjkyb.supabase.co" 
key_supabase = "sb_publishable_p_QeMSlZyBIMzuNsPq1BQg_PYm-byoE"

# Inicia as conexões
telegram = TelegramClient('anon', api_id, api_hash)
supabase: Client = create_client(url_supabase, key_supabase)

async def main():
    # 1. Envia msg no Telegram
    print("Enviando mensagem...")
    await telegram.send_message('me', 'Testando conexão com Banco de Dados! 🚀')
    
    # 2. Salva um registro no Supabase (Exemplo: criando um log)
    # IMPORTANTE: Você precisa ter uma tabela chamada 'logs' ou mudar o nome abaixo
    data = {"evento": "Bot Iniciado", "status": "Online"}
    
    try:
        response = supabase.table('logs').insert(data).execute()
        print("✅ Dados salvos no Supabase com sucesso!")
        print(response)
    except Exception as e:
        print(f"❌ Erro ao salvar no banco (Criou a tabela 'logs'?): {e}")

with telegram:
    telegram.loop.run_until_complete(main()) # <--- Recuado para a direita (Certo!)
  