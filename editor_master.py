from moviepy.editor import VideoFileClip, AudioFileClip, ImageClip, CompositeVideoClip
import os

# --- ⚙️ CONFIGURAÇÃO DA FÁBRICA ---
PASTA_VIDEOS = "videos_prontos"
PASTA_AUDIO = "audios_narrecao"
ARQUIVO_AUDIO = "narracao_vendas.mp3" # O arquivo que o Antônio criou
PASTA_AVATAR = "avatar"
ARQUIVO_AVATAR = "boneco.png"         # A imagem que tiramos o fundo
PASTA_FINAL = "videos_finalizados"

print("🎬 LUZ, CÂMERA, AÇÃO! Iniciando a montagem final...")

# 1. Cria a pasta de entrega se não existir
if not os.path.exists(PASTA_FINAL):
    os.makedirs(PASTA_FINAL)

# 2. Carrega os Atores (Áudio e Avatar)
try:
    caminho_audio = os.path.join(PASTA_AUDIO, ARQUIVO_AUDIO)
    audio_clip = AudioFileClip(caminho_audio)
    
    caminho_avatar = os.path.join(PASTA_AVATAR, ARQUIVO_AVATAR)
    # Carrega o boneco
    avatar_clip = ImageClip(caminho_avatar)
    
    print("✅ Recursos carregados (Voz e Boneco prontos).")

except Exception as e:
    print(f"❌ ERRO FATAL: Não achei o áudio ou o boneco! Verifique se os arquivos existem.\nErro: {e}")
    exit()

# 3. Processa cada vídeo da pasta
arquivos_video = [f for f in os.listdir(PASTA_VIDEOS) if f.endswith(".mp4")]

if not arquivos_video:
    print("❌ Nenhum vídeo encontrado na pasta 'videos_prontos'!")
else:
    for video_nome in arquivos_video:
        try:
            print(f"\n🔨 Editando o vídeo: {video_nome}...")
            caminho_video = os.path.join(PASTA_VIDEOS, video_nome)
            
            # Carrega o vídeo original
            clip_video = VideoFileClip(caminho_video)
            
            # --- ✂️ AJUSTE DE TEMPO ---
            # O vídeo precisa ter o tamanho do áudio + uma folga
            duracao_audio = audio_clip.duration + 1.5 
            
            # Se o vídeo for curto, repete ele (loop)
            if clip_video.duration < duracao_audio:
                clip_video = clip_video.loop(duration=duracao_audio)
            else:
                # Se for longo, corta no tamanho do áudio
                clip_video = clip_video.subclip(0, duracao_audio)
            
            # Remove o som original do vídeo (para não brigar com a voz do Antônio)
            clip_video = clip_video.without_audio()
            
            # Adiciona a voz do Antônio
            clip_video = clip_video.set_audio(audio_clip)
            
            # --- 👾 POSICIONA O BONECO ---
            # Redimensiona o boneco e coloca no canto direito inferior
            boneco_final = (avatar_clip
                            .resize(height=250)
                            .set_position(("right", "bottom"))
                            .set_duration(clip_video.duration))
            
            # --- 🎞️ RENDERIZAÇÃO (Junta tudo) ---
            video_final = CompositeVideoClip([clip_video, boneco_final])
            
            nome_saida = f"FINAL_{video_nome}"
            caminho_saida = os.path.join(PASTA_FINAL, nome_saida)
            
            print("   ⏳ Renderizando... (Isso pode demorar um pouquinho)")
            
            # Preset 'ultrafast' para ser rápido
            video_final.write_videofile(
                caminho_saida, 
                codec='libx264', 
                audio_codec='aac', 
                preset='ultrafast', 
                verbose=False,
                logger=None 
            )
            
            print(f"   ✅ SUCESSO! Vídeo pronto em: {caminho_saida}")
            
        except Exception as e:
            print(f"   ❌ Erro ao editar {video_nome}: {e}")

    print("\n🏁 FIM! Verifique a pasta 'videos_finalizados'.")