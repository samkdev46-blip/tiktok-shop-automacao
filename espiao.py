import asyncio
from telethon import TelegramClient, events
from supabase import create_client, Client

# --- 1. CONFIGURAÇÕES DO TELEGRAM ---
api_id = 32858856           # <--- SEU ID AQUI
api_hash = 'd17f8094408cde03f803b076748f5ef4' # <--- SUA HASH AQUI

# --- 2. CONFIGURAÇÕES DO SUPABASE ---
url_supabase = "https://cqvczuuonchjqpofjkyb.supabase.co"  # <--- SUA URL AQUI
key_supabase = "sb_publishable_p_QeMSlZyBIMzuNsPq1BQg_PYm-byoE"           # <--- SUA KEY AQUI

# Inicia as conexões
client = TelegramClient('anon', api_id, api_hash)
supabase: Client = create_client(url_supabase, key_supabase)

print("🕵️‍♂️ Espião V2 (Filtro de Ouro) iniciado...")

# Lista do que queremos caçar
palavras_chave = ['tiktok.com', 'instagram.com', 'youtube.com', 'youtu.be', 'douyin.com']

@client.on(events.NewMessage)
async def handler(event):
    try:
        texto_msg = event.text or "" # Garante que é texto
        chat = await event.get_chat()
        nome_chat = chat.title if hasattr(chat, 'title') else "Privado"
        
        # O FILTRO MÁGICO 🧙‍♂️
        # Verifica se alguma das palavras chave está no texto (em minúsculo)
        tem_link = any(palavra in texto_msg.lower() for palavra in palavras_chave)

        if tem_link:
            print(f"💎 OURO ENCONTRADO em: {nome_chat}")
            
            # Salva no Banco
            data = {
                "evento": f"Link de: {nome_chat}",
                "status": texto_msg # Salva o link completo
            }
            supabase.table('logs').insert(data).execute()
            print("✅ Link salvo no Banco!")
            
        else:
            # Só mostra no terminal, mas NÃO salva no banco
            print(f"🗑️ Ignorado (sem link) em: {nome_chat}")

    except Exception as e:
        print(f"❌ Erro: {e}")

with client:
    client.run_until_disconnected()