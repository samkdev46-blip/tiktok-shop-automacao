import yt_dlp
import os

# --- MIRA RECALIBRADA 🎯 ---
# Adicionamos "shorts" para forçar o algoritmo do YouTube a trazer verticais
TERMO = "tiktok shop finds shorts" 
QTD = 5  # Aumentei para 5 para garantir que pegue bons

print(f"🕵️ Iniciando operação de DOWNLOAD: '{TERMO}'")
print("🚫 Filtro ativado: Rejeitando vídeos longos (acima de 60s)...")

# 1. Cria a pasta
pasta_destino = "downloads"
if not os.path.exists(pasta_destino):
    os.makedirs(pasta_destino)

# 2. Configura a bazuca com TRAVA DE SEGURANÇA
ydl_opts = {
    'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best', 
    'outtmpl': f'{pasta_destino}/%(title)s.%(ext)s', 
    'noplaylist': True,
    'quiet': False,
    
    # --- O SEGREDO ESTÁ AQUI 👇 ---
    # Isso diz: "Se a duração for maior que 60 segundos, PULE!"
    'match_filter': yt_dlp.utils.match_filter_func("duration < 61"),
    'ignoreerrors': True, # Se pular um vídeo longo, não trava o robô
}

try:
    print(f"🚀 Buscando vídeos curtos de '{TERMO}'...")
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        # Buscamos um pouco mais (10) porque alguns serão filtrados pelo tempo
        ydl.download([f"ytsearch10:{TERMO}"])

    print(f"\n✅ SUCESSO! Verifique a pasta '{pasta_destino}'. Agora só deve ter vídeo curto!")

except Exception as e:
    print(f"❌ Deu ruim: {e}")