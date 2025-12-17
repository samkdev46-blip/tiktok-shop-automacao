import os
import random
import subprocess
import json
import math # <--- Importante para a animação do boneco
from moviepy.editor import VideoFileClip, AudioFileClip, CompositeVideoClip, CompositeAudioClip, ImageClip

# --- ⚙️ CARREGA A PRANCHETA (CONFIGURAÇÕES DO APP) ---
ARQUIVO_CONFIG = "config_temp.json"

# Valores padrão (caso rode manual sem o app)
CONFIG = {
    "texto": "Olha só que incrível!",
    "volume": 0.15, # 15%
    "modo_musica": "aleatorio",
    "caminho_musica_custom": None
}

if os.path.exists(ARQUIVO_CONFIG):
    print(f"📄 Lendo configurações de: {ARQUIVO_CONFIG}")
    try:
        with open(ARQUIVO_CONFIG, "r", encoding="utf-8") as f:
            CONFIG = json.load(f)
    except Exception as e:
        print(f"⚠️ Erro ao ler config, usando padrão. Erro: {e}")

TEXTO_NARRACAO = CONFIG["texto"]
VOLUME_MUSICA = CONFIG["volume"] # O valor que vem da barrinha (0.0 a 1.0)

# --- CONFIGURAÇÕES DE PASTAS ---
pasta_entrada = "videos_baixados"
pasta_saida = "videos_finalizados"
pasta_musicas = "musicas_fundo"
pasta_avatar = "avatar"
arquivo_avatar = "boneco.png"
arquivo_narracao_temp = "narracao_temp.mp3"

# Tenta importar o blur
try:
    from moviepy.video.fx.gaussian_blur import gaussian_blur
except ImportError:
    gaussian_blur = None

# Garante pastas
for pasta in [pasta_saida, pasta_musicas, pasta_avatar]:
    if not os.path.exists(pasta):
        os.makedirs(pasta)

def gerar_narracao_antonio(texto):
    """Gera o áudio usando edge-tts"""
    print("🎙️ Gerando voz do Antônio...")
    try:
        subprocess.run([
            "edge-tts",
            "--text", texto,
            "--write-media", arquivo_narracao_temp,
            "--voice", "pt-BR-AntonioNeural"
        ], check=True)
        return True
    except Exception as e:
        print(f"❌ Erro voz: {e}")
        return False

def adicionar_avatar(video_clip):
    """Adiciona o boneco com ANIMAÇÃO (Entrada + Flutuação)"""
    caminho_completo_avatar = os.path.join(pasta_avatar, arquivo_avatar)
    if not os.path.exists(caminho_completo_avatar):
        print("⚠️ Boneco não encontrado. Pulando avatar.")
        return video_clip

    try:
        # Carrega e redimensiona
        boneco = ImageClip(caminho_completo_avatar).resize(height=400)
        boneco = boneco.set_duration(video_clip.duration)
        
        # --- A MÁGICA DO MOVIMENTO ---
        def movimento(t):
            # t = tempo atual em segundos
            
            # 1. POSIÇÃO HORIZONTAL (X)
            # Fica fixo na direita (com margem de 50px da borda)
            # 1080 é a largura do vídeo, boneco.w é a largura do boneco
            pos_x = 1080 - boneco.w - 50 
            
            # 2. ANIMAÇÃO DE ENTRADA (Sobe nos primeiros 1.5 segundos)
            altura_final = 1450 # Posição Y onde ele vai estacionar
            altura_inicial = 2000 # Começa escondido
            
            if t < 1.5:
                # Interpolação: vai de 2000 até 1450
                progresso = t / 1.5
                pos_y = altura_inicial - ((altura_inicial - altura_final) * progresso)
            else:
                # 3. MODO "VIVO" (Respiração)
                # Math.sin cria uma onda suave. Multiplico por 5 para mover só 5 pixels
                flutuacao = math.sin(t * 3) * 5 
                pos_y = altura_final + flutuacao

            return (pos_x, pos_y)

        # Aplica a função de movimento
        boneco = boneco.set_position(movimento)
        
        print("👤 Avatar animado adicionado!")
        return CompositeVideoClip([video_clip, boneco])

    except Exception as e:
        print(f"⚠️ Erro ao adicionar avatar: {e}")
        return video_clip

def montar_audio_final(duracao_necessaria):
    """Mistura Narração + Música (Controlada pelo Usuário)"""
    if not os.path.exists(arquivo_narracao_temp): return None
    audio_narracao = AudioFileClip(arquivo_narracao_temp)
    
    # --- LÓGICA DA MÚSICA ---
    bg_music = None
    
    # 1. Verifica se o usuário mandou uma música específica (Upload)
    if CONFIG["modo_musica"] == "upload" and CONFIG["caminho_musica_custom"]:
        if os.path.exists(CONFIG["caminho_musica_custom"]):
            print(f"🎵 Usando música personalizada: {CONFIG['caminho_musica_custom']}")
            bg_music = AudioFileClip(CONFIG["caminho_musica_custom"])
        else:
            print("⚠️ Música personalizada não encontrada. Tentando aleatória...")

    # 2. Se não tem personalizada (ou falhou), usa Aleatória
    if bg_music is None:
        arquivos = [f for f in os.listdir(pasta_musicas) if f.endswith(('.mp3', '.wav'))]
        if arquivos:
            escolhida = random.choice(arquivos)
            print(f"🎵 Usando música aleatória: {escolhida}")
            bg_music = AudioFileClip(os.path.join(pasta_musicas, escolhida))

    # 3. Processamento do Áudio
    if bg_music:
        try:
            # Loop
            if bg_music.duration < duracao_necessaria:
                n_loops = int(duracao_necessaria / bg_music.duration) + 1
                bg_music = bg_music.loop(n=n_loops)
            
            # Corta
            bg_music = bg_music.subclip(0, duracao_necessaria)
            
            # --- AQUI ESTÁ O CONTROLE DE VOLUME ---
            print(f"🔊 Aplicando volume: {int(VOLUME_MUSICA * 100)}%")
            bg_music = bg_music.volumex(VOLUME_MUSICA)
            
            # Mistura
            return CompositeAudioClip([audio_narracao, bg_music])
        except Exception as e:
            print(f"⚠️ Erro ao processar música: {e}")
            return audio_narracao
    else:
        print("⚠️ Sem música de fundo.")
        return audio_narracao

def processar_video(caminho_video):
    print(f"\n🎬 Processando: {os.path.basename(caminho_video)}")
    if not gerar_narracao_antonio(TEXTO_NARRACAO): return

    try:
        temp_audio = AudioFileClip(arquivo_narracao_temp)
        tempo_narracao = temp_audio.duration + 0.5
        temp_audio.close()

        clip = VideoFileClip(caminho_video).without_audio()

        if clip.duration < tempo_narracao: clip = clip.loop(duration=tempo_narracao)
        else: clip = clip.subclip(0, tempo_narracao)

        # Verticalização
        largura, altura = 1080, 1920
        fundo = clip.resize(height=altura)
        fundo = fundo.crop(x1=fundo.w/2-largura/2, x2=fundo.w/2+largura/2, width=largura, height=altura)
        if gaussian_blur: fundo = gaussian_blur(fundo, sigma=15)
        else: fundo = fundo.fl_image(lambda image: 0.3 * image) # Escurece se não tiver blur
        
        frente = clip.resize(width=largura).set_position("center")
        video_final = CompositeVideoClip([fundo, frente], size=(largura, altura))

        novo_audio = montar_audio_final(tempo_narracao)
        if novo_audio: video_final.audio = novo_audio

        video_final = adicionar_avatar(video_final)

        nome = os.path.splitext(os.path.basename(caminho_video))[0]
        saida = os.path.join(pasta_saida, f"FINAL_{nome}.mp4")
        
        video_final.write_videofile(saida, codec='libx264', audio_codec='aac', preset='ultrafast')
        
        clip.close()
        video_final.close()
        
    except Exception as e:
        print(f"❌ Erro fatal: {e}")

if __name__ == "__main__":
    if os.path.exists(pasta_entrada):
        arquivos = [f for f in os.listdir(pasta_entrada) if f.lower().endswith(('.mp4', '.mkv', '.webm'))]
        if arquivos:
            for arq in arquivos: processar_video(os.path.join(pasta_entrada, arq))
        else:
            print("💤 Pasta vazia.")
    
    # Limpa arquivos temporários no final
    if os.path.exists(arquivo_narracao_temp): 
        try: os.remove(arquivo_narracao_temp)
        except: pass