import streamlit as st
import PIL.Image 

# --- 🚑 VACINA ANTI-ERRO ---
if not hasattr(PIL.Image, 'ANTIALIAS'):
    PIL.Image.ANTIALIAS = PIL.Image.LANCZOS
# ---------------------------

from moviepy.editor import VideoFileClip, AudioFileClip, ImageClip, CompositeVideoClip
import tempfile
import os
import yt_dlp
import random
import edge_tts
import asyncio

# --- 🎨 CONFIGURAÇÃO VISUAL ---
st.set_page_config(page_title="Fábrica de Virais 6.0 (Cookies)", page_icon="🍪", layout="wide")

st.title("🍪 Fábrica de Virais (Modo Desbloqueio)")
st.markdown("---")

# --- 🧠 MEMÓRIA ---
if 'audio_gerado_path' not in st.session_state:
    st.session_state['audio_gerado_path'] = None

# --- ⚙️ FUNÇÃO DE PROCESSAMENTO ---
def processar_video_viral(caminho_video_bruto, caminho_audio, caminho_avatar):
    with st.status("🏗️ Processando vídeo...", expanded=True) as status:
        try:
            st.write("1️⃣ Carregando arquivos...")
            clip_video = VideoFileClip(caminho_video_bruto)
            audio_clip = AudioFileClip(caminho_audio)
            avatar_img = ImageClip(caminho_avatar)

            # ✂️ Ajuste de Tempo
            duracao_final = audio_clip.duration + 1.0 
            if clip_video.duration < duracao_final:
                clip_video = clip_video.loop(duration=duracao_final)
            else:
                clip_video = clip_video.subclip(0, duracao_final)

            clip_video = clip_video.without_audio().set_audio(audio_clip)

            # 📏 Vertical
            if clip_video.w > clip_video.h:
                clip_video = clip_video.resize(height=1920)
                clip_video = clip_video.crop(x1=clip_video.w/2 - 540, y1=0, width=1080, height=1920)

            # 👾 Avatar
            TAMANHO_AVATAR = 450
            boneco = avatar_img.resize(height=TAMANHO_AVATAR)

            def movimento_apresentador(t):
                y_start = clip_video.h - TAMANHO_AVATAR + 100
                y_end = clip_video.h - TAMANHO_AVATAR - 50
                if t < 1.5: return ("right", y_start - (t * (100/1.5)))
                else: return ("right", y_end)

            boneco_animado = (boneco.set_position(movimento_apresentador).set_duration(clip_video.duration))
            
            output_path = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4").name
            CompositeVideoClip([clip_video, boneco_animado]).write_videofile(
                output_path, codec='libx264', audio_codec='aac', preset='ultrafast', logger=None
            )
            
            status.update(label="✅ Pronto!", state="complete", expanded=False)
            return output_path
        except Exception as e:
            st.error(f"❌ Erro: {e}")
            return None

# --- 🗣️ VOZ ---
async def gerar_voz_antonio(texto, arquivo_saida):
    await edge_tts.Communicate(texto, "pt-BR-AntonioNeural").save(arquivo_saida)

# --- 🍪 CONFIGURAÇÃO DO CAÇADOR (A MÁGICA) ---
def get_ydl_opts(download=False, output_path=None):
    # Procura o arquivo cookies.txt na pasta
    usar_cookies = 'cookies.txt' if os.path.exists('cookies.txt') else None
    
    opts = {
        'quiet': True, 
        'ignoreerrors': True, 
        'no_warnings': True,
        'cookiefile': usar_cookies # <--- AQUI ESTA O SEGREDO
    }
    
    if download:
        opts['format'] = 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'
        opts['outtmpl'] = output_path
    else:
        opts['default_search'] = 'ytsearch5'
    return opts

# --- 📂 INTERFACE ---
st.sidebar.header("Avatar & Áudio")
tipo_avatar = st.sidebar.radio("Avatar:", ["Padrão", "Upload"], horizontal=True)
arquivo_avatar_final = "avatar/boneco.png" if tipo_avatar == "Padrão" and os.path.exists("avatar/boneco.png") else None

if tipo_avatar == "Upload":
    up_av = st.sidebar.file_uploader("Img Avatar", type=["png"])
    if up_av:
        t = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
        t.write(up_av.read())
        arquivo_avatar_final = t.name

st.sidebar.markdown("---")
tipo_audio = st.sidebar.radio("Áudio:", ["Padrão", "Upload", "Voz IA"])
arquivo_audio_final = "audios_narrecao/narracao_vendas.mp3" if tipo_audio == "Padrão" and os.path.exists("audios_narrecao/narracao_vendas.mp3") else None

if tipo_audio == "Upload":
    up_au = st.sidebar.file_uploader("Audio MP3", type=["mp3"])
    if up_au:
        t = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        t.write(up_au.read())
        arquivo_audio_final = t.name

if tipo_audio == "Voz IA":
    txt = st.sidebar.text_area("Texto:", "Produto top!")
    if st.sidebar.button("🎙️ Gerar Voz"):
        try:
            t = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
            asyncio.run(gerar_voz_antonio(txt, t.name))
            st.session_state['audio_gerado_path'] = t.name
            st.rerun()
        except Exception as e: st.error(e)
    
    if st.session_state['audio_gerado_path']:
        st.sidebar.audio(st.session_state['audio_gerado_path'])
        arquivo_audio_final = st.session_state['audio_gerado_path']

# --- ABAS ---
aba_manual, aba_auto = st.tabs(["Manual", "Automático (Cookies 🍪)"])

with aba_manual:
    v_up = st.file_uploader("Vídeo", type=["mp4"])
    if st.button("🚀 Processar") and v_up and arquivo_avatar_final and arquivo_audio_final:
        t = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
        t.write(v_up.read())
        res = processar_video_viral(t.name, arquivo_audio_final, arquivo_avatar_final)
        if res: st.video(res)

with aba_auto:
    st.header("Caçador com Cookies")
    
    # Aviso visual se o cookie foi carregado
    if os.path.exists('cookies.txt'):
        st.success("🍪 Arquivo de Cookies detectado! Modo desbloqueado ativo.", icon="✅")
    else:
        st.warning("⚠️ 'cookies.txt' não encontrado. O YouTube pode bloquear o download.", icon="🚨")

    termo = st.text_input("Produto")
    if st.button("🎲 Sortear") and termo and arquivo_avatar_final and arquivo_audio_final:
        st.info(f"🔎 Buscando: {termo} review...")
        
        if not os.path.exists("downloads"): os.makedirs("downloads")
        
        try:
            # 1. Busca
            lista = []
            with yt_dlp.YoutubeDL(get_ydl_opts(download=False)) as ydl:
                info = ydl.extract_info(f"{termo} review", download=False)
                if 'entries' in info:
                    for v in info['entries']:
                        if v and v.get('duration') and v['duration'] < 180:
                            lista.append(v)
            
            # 2. Download e Processamento
            if lista:
                escolhido = random.choice(lista)
                st.success(f"Vídeo: {escolhido.get('title')}")
                path_down = f"downloads/{escolhido['id']}.mp4"
                
                if not os.path.exists(path_down):
                    # Tenta baixar usando os cookies configurados
                    with yt_dlp.YoutubeDL(get_ydl_opts(download=True, output_path=path_down)) as ydl:
                        ydl.download([escolhido['webpage_url']])
                
                if os.path.exists(path_down):
                    res = processar_video_viral(path_down, arquivo_audio_final, arquivo_avatar_final)
                    if res: st.video(res)
            else:
                st.warning("Nada encontrado.")
        except Exception as e:
            st.error(f"Erro no download: {e}")