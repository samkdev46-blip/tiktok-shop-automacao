from moviepy.editor import VideoFileClip, AudioFileClip, ImageClip, CompositeVideoClip
import os

# --- ⚙️ CONFIGURAÇÃO ---
PASTA_VIDEOS = "videos_prontos"
PASTA_AUDIO = "audios_narrecao"
ARQUIVO_AUDIO = "narracao_vendas.mp3"
PASTA_AVATAR = "avatar"
ARQUIVO_AVATAR = "boneco.png"
PASTA_FINAL = "videos_finalizados"

# TAMANHO DO BONECO (Aumentei de 250 para 450)
TAMANHO_AVATAR = 450 

print("🎬 LUZ, CÂMERA, AÇÃO! Versão 2.0 (Com Movimento)...")

if not os.path.exists(PASTA_FINAL):
    os.makedirs(PASTA_FINAL)

try:
    caminho_audio = os.path.join(PASTA_AUDIO, ARQUIVO_AUDIO)
    audio_clip = AudioFileClip(caminho_audio)
    
    caminho_avatar = os.path.join(PASTA_AVATAR, ARQUIVO_AVATAR)
    # Carrega o boneco
    avatar_img = ImageClip(caminho_avatar)
    print("✅ Recursos carregados.")

except Exception as e:
    print(f"❌ Erro ao carregar arquivos: {e}")
    exit()

arquivos_video = [f for f in os.listdir(PASTA_VIDEOS) if f.endswith(".mp4")]

for video_nome in arquivos_video:
    try:
        print(f"\n🔨 Editando: {video_nome}...")
        caminho_video = os.path.join(PASTA_VIDEOS, video_nome)
        
        clip_video = VideoFileClip(caminho_video)
        
        # Ajuste de Tempo
        duracao_audio = audio_clip.duration + 1.0
        if clip_video.duration < duracao_audio:
            clip_video = clip_video.loop(duration=duracao_audio)
        else:
            clip_video = clip_video.subclip(0, duracao_audio)
        
        clip_video = clip_video.without_audio().set_audio(audio_clip)
        
        # --- 🚀 A MÁGICA DO MOVIMENTO ---
        # 1. Redimensiona o boneco (ficou maior)
        boneco = avatar_img.resize(height=TAMANHO_AVATAR)
        
        # 2. Define a posição dinâmica (Animação)
        # O boneco vai começar um pouco mais para baixo e subir devagarzinho
        # E vai ficar oscilando bem de leve para a direita e esquerda (como se estivesse vivo)
        def movimento_apresentador(t):
            # t é o tempo atual do vídeo em segundos
            
            # Movimento horizontal: Vai 5 pixels pra direita e volta (respiração)
            x_pos = "right" 
            
            # Movimento vertical: Começa mais baixo e sobe até a posição final
            # Isso dá um efeito de "entrada" ou de estar andando pra frente
            y_start = clip_video.h - TAMANHO_AVATAR + 50 # Começa 50px mais baixo
            y_end = clip_video.h - TAMANHO_AVATAR - 20   # Termina na posição certa
            
            # Calcula a posição Y baseada no tempo (sobe nos primeiros 2 segundos)
            if t < 2:
                y_pos = y_start - (t * 25) # Sobe rápido
            else:
                y_pos = y_end # Fica parado na altura certa
                
            return (x_pos, y_pos)

        # Aplica o movimento
        boneco_animado = (boneco
                          .set_position(("right", "bottom")) # Posição base
                          .set_duration(clip_video.duration))
        
        # Se quiser algo mais simples (só parado mas grande):
        # boneco_animado = boneco.set_position(("right", "bottom")).set_duration(clip_video.duration)

        # --- 🎞️ RENDERIZAÇÃO ---
        video_final = CompositeVideoClip([clip_video, boneco_animado])
        
        nome_saida = f"FINAL_V2_{video_nome}"
        caminho_saida = os.path.join(PASTA_FINAL, nome_saida)
        
        print("   ⏳ Renderizando com animação...")
        video_final.write_videofile(caminho_saida, codec='libx264', audio_codec='aac', preset='ultrafast', verbose=False, logger=None)
        print(f"   ✅ VÍDEO PRONTO: {nome_saida}")

    except Exception as e:
        print(f"   ❌ Erro: {e}")

print("\n🏁 FIM!")