import os
from supabase import create_client, Client
import yt_dlp

# --- CONFIGURAÇÕES ---
# ⚠️ COLOQUE SUAS CHAVES REAIS AQUI EMBAIXO:
api_url = "https://cqvczuuonchjqpofjkyb.supabase.co"
api_key = "sb_publishable_p_QeMSlZyBIMzuNsPq1BQg_PYm-byoE"

# Pasta onde os vídeos vão ficar
pasta_downloads = "videos_baixados"

# Conecta ao Banco
try:
    supabase: Client = create_client(api_url, api_key)
except Exception as e:
    print(f"❌ Erro na conexão com o Supabase. Verifique URL e KEY. Detalhe: {e}")
    exit()

# Cria a pasta se não existir
if not os.path.exists(pasta_downloads):
    os.makedirs(pasta_downloads)

def baixar_videos():
    print("🚜 Iniciando o trator de downloads...")
    
    try:
        # 1. Busca apenas os que o 'ja_baixei' é FALSE (ou null)
        response = supabase.table('logs').select("*").eq('ja_baixei', False).execute()
        lista_videos = response.data
    except Exception as e:
        print(f"❌ Erro ao consultar o banco. A coluna 'ja_baixei' existe e é booleana? Erro: {e}")
        return
    
    if not lista_videos:
        print("💤 Nenhum vídeo novo na fila (tudo já foi baixado ou lista vazia).")
        return

    print(f"📦 Encontrei {len(lista_videos)} vídeos na fila!")

    # Configurações do yt-dlp
    ydl_opts = {
        'outtmpl': f'{pasta_downloads}/%(title)s.%(ext)s',
        'format': 'bestvideo+bestaudio/best',
        'quiet': True,
        'no_warnings': True,
        'ignoreerrors': True, # Se um vídeo der erro, pula pro próximo sem travar
    }

    # 2. Loop para baixar cada um
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        for item in lista_videos:
            link = item.get('status') # Pega o link da coluna status
            id_banco = item.get('id')
            
            if not link:
                print(f"⚠️ Item ID {id_banco} sem link no status. Pulando.")
                continue

            print(f"⬇️ Baixando ID {id_banco}: {link}...")
            
            try:
                # Tenta baixar
                ydl.download([link])
                
                # 3. Marca como FEITO no banco de dados
                supabase.table('logs').update({'ja_baixei': True}).eq('id', id_banco).execute()
                print(f"✅ Sucesso! Vídeo salvo e marcado no banco.")
                
            except Exception as e:
                print(f"❌ Falha ao baixar este vídeo: {e}")

if __name__ == "__main__":
    baixar_videos()