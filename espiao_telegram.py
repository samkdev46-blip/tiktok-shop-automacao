import asyncio
from telethon import TelegramClient
from supabase import create_client, Client

# ======================================================
# 🔐 ÁREA DE SEGURANÇA (PREENCHA AQUI)
# ======================================================

# 1. SUAS CHAVES DO TELEGRAM (Pegou no my.telegram.org)
API_ID = '32858856'       
API_HASH = 'd17f8094408cde03f803b076748f5ef4'
NOME_SESSAO = 'sessao_tiktok_shopping'

# 2. SUAS CHAVES DO SUPABASE (Pegou nas Configurações > API)
SUPABASE_URL = 'https://cqvczuuonchjqpofjkyb.supabase.co'
SUPABASE_KEY = 'sb_secret_Q3NNWeubYjD6Cglva2q4cQ_dcMVtGxl' 

# ======================================================

# Conecta ao Banco de Dados (O Cofre)
print("🔌 Conectando ao Cofre Supabase...")
try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
except Exception as e:
    print(f"❌ Erro ao conectar no Supabase: {e}")
    exit()

# Lista de Canais para Monitorar
canais_alvo = ['@ofertaschina', '@promocoesbrasil', '@aliexpressbr'] 

async def garimpar_e_salvar(produto_desejado):
    print(f"\n🕵️‍♂️ Iniciando caçada por: '{produto_desejado}'...")
    
    async with TelegramClient(NOME_SESSAO, API_ID, API_HASH) as client:
        # Loop pelos canais
        for canal in canais_alvo:
            print(f"   > Verificando canal: {canal}...")
            try:
                # Busca as mensagens (limite de 10 por canal pra testar)
                async for mensagem in client.iter_messages(canal, search=produto_desejado, limit=10):
                    if mensagem.text:
                        # Prepara os dados (tratamento básico)
                        titulo_bruto = mensagem.text[:100].replace('\n', ' ')
                        
                        dados_oferta = {
                            "titulo": titulo_bruto,
                            "preco": "A verificar", 
                            "link_afiliado": f"https://t.me/{canal.replace('@', '')}/{mensagem.id}",
                            "link_video": "pendente",
                            "canal_origem": canal
                        }

                        # --- O RITUAL DE GRAVAÇÃO ---
                        try:
                            # Tenta inserir. Se der erro, printa o erro.
                            resposta = supabase.table("ofertas").insert(dados_oferta).execute()
                            print(f"   ✅ SUCESSO! Oferta salva: {titulo_bruto[:30]}...")
                        except Exception as e_banco:
                            print(f"   ⚠️ O cofre rejeitou (talvez duplicado?): {e_banco}")

            except Exception as e:
                print(f"   ⚠️ Erro ao ler canal {canal}: {e}")

if __name__ == '__main__':
    # Pergunta no terminal o que você quer buscar
    termo = input("\n🔎 Digite o produto que você quer buscar (ex: relogio): ")
    
    # Roda o loop assíncrono
    loop = asyncio.get_event_loop()
    loop.run_until_complete(garimpar_e_salvar(termo))