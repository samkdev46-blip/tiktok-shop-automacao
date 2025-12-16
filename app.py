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
st.set_page_config(page_title="Fábrica de Virais 5.2 (Memória Fixa)", page_icon="🧠", layout="wide")

st.title("🧠 Fábrica de Virais (Correção de Memória)")
st.markdown("---")

# --- 🧠 INICIALIZAR MEMÓRIA (SESSION STATE) ---
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

            # 📏 Formato Vertical
            if clip_video.w > clip_video.h:
                st.write("⚠️ Ajustando para Vertical...")
                clip_video = clip_video.resize(height=1920)
                clip_video = clip_video.crop(x1=clip_video.w/2 - 540, y1=0, width=1080, height=1920)

            # 👾 Avatar Animado
            st.write("2️⃣ Adicionando Avatar...")
            TAMANHO_AVATAR = 450
            boneco = avatar_img.resize(height=TAMANHO_AVATAR)

            def movimento_apresentador(t):
                y_start = clip_video.h - TAMANHO_AVATAR + 100
                y_end = clip_video.h - TAMANHO_AVATAR - 50
                if t < 1.5:
                    y_pos = y_start - (t * (100/1.5))
                else:
                    y_pos = y_end
                return ("right", y_pos)

            boneco_animado = (boneco
                            .set_position(movimento_apresentador)
                            .set_duration(clip_video.duration))

            # Renderiza
            st.write("3️⃣ Renderizando...")
            video_final = CompositeVideoClip([clip_video, boneco_animado])
            
            output_path = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4").name
            
            video_final.write_videofile(
                output_path, codec='libx264', audio_codec='aac', preset='ultrafast', logger=None
            )
            
            status.update(label="✅ Pronto!", state="complete", expanded=False)
            return output_path

        except Exception as e:
            st.error(f"❌ Erro: {e}")
            return None

# --- 🗣️ FUNÇÃO ASYNC VOZ ---
async def gerar_voz_antonio(texto, arquivo_saida):
    comunicador = edge_tts.Communicate(texto, "pt-BR-AntonioNeural")
    await comunicador.save(arquivo_saida)

# --- 📂 BARRA LATERAL ---
st.sidebar.header("1. Configuração do Avatar 👾")
tipo_avatar = st.sidebar.radio("Avatar:", ["Padrão", "Upload"], horizontal=True)

arquivo_avatar_final = None # Variável para guardar o caminho decidido

if tipo_avatar == "Padrão":
    if os.path.exists("avatar/boneco.png"):
        arquivo_avatar_final = "avatar/boneco.png"
        st.sidebar.success("✅ Avatar Padrão OK")
    else:
        st.sidebar.error("❌ Faltando 'avatar/boneco.png'")
else:
    uploaded_avatar = st.sidebar.file_uploader("Subir Imagem", type=["png"])
    if uploaded_avatar:
        tfile_av = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
        tfile_av.write(uploaded_avatar.read())
        arquivo_avatar_final = tfile_av.name

st.sidebar.markdown("---")
st.sidebar.header("2. Configuração do Áudio 🔊")
tipo_audio = st.sidebar.radio("Áudio:", ["Padrão", "Upload", "Voz IA (Antônio)"])

arquivo_audio_final = None # Variável para guardar o caminho decidido

if tipo_audio == "Padrão":
    if os.path.exists("audios_narrecao/narracao_vendas.mp3"):
        arquivo_audio_final = "audios_narrecao/narracao_vendas.mp3"
        st.sidebar.success("✅ Áudio Padrão OK")
    
elif tipo_audio == "Upload":
    uploaded_audio = st.sidebar.file_uploader("Subir MP3", type=["mp3"])
    if uploaded_audio:
        tfile_au = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        tfile_au.write(uploaded_audio.read())
        arquivo_audio_final = tfile_au.name

elif tipo_audio == "Voz IA (Antônio)":
    texto_usuario = st.sidebar.text_area("Texto do Narrador:", "Esse produto é incrível!")
    
    # Botão para gerar
    if st.sidebar.button("🎙️ Gerar Voz"):
        if texto_usuario:
            try:
                tfile_tts = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
                asyncio.run(gerar_voz_antonio(texto_usuario, tfile_tts.name))
                # SALVA NA MEMÓRIA PERMANENTE
                st.session_state['audio_gerado_path'] = tfile_tts.name 
                st.rerun() # Recarrega para atualizar o player
            except Exception as e:
                st.sidebar.error(f"Erro: {e}")

    # Verifica se já existe áudio na memória
    if st.session_state['audio_gerado_path']:
        st.sidebar.audio(st.session_state['audio_gerado_path'])
        st.sidebar.success("✅ Áudio Gerado e Salvo!")
        arquivo_audio_final = st.session_state['audio_gerado_path']
    else:
        st.sidebar.warning("⚠️ Clique em 'Gerar Voz' acima.")

# --- 🖥️ ABAS ---
aba_manual, aba_auto = st.tabs(["📤 Upload Manual", "🎰 Busca Aleatória"])

with aba_manual:
    st.header("Manual")
    video_upload = st.file_uploader("Vídeo MP4", type=["mp4"])
    if st.button("🚀 Processar Manual"):
        if video_upload and arquivo_avatar_final and arquivo_audio_final:
            tfile_video = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") 
            tfile_video.write(video_upload.read())
            resultado = processar_video_viral(tfile_video.name, arquivo_audio_final, arquivo_avatar_final)
            if resultado:
                st.video(resultado)
        else:
            st.error("⚠️ Faltando Arquivos! Verifique Áudio e Avatar na esquerda.")

with aba_auto:
    st.header("Automático")
    termo = st.text_input("Produto")
    if st.button("🎲 Sortear e Criar"):
        # Agora checamos as variáveis finais, que buscam da memória se necessário
        if arquivo_avatar_final and arquivo_audio_final and termo:
            termo_opt = f"{termo} review"
            st.info(f"🔎 Buscando: {termo_opt}")
            
            if not os.path.exists("downloads"): os.makedirs("downloads")
            
            try:
                ydl_opts = {'default_search': 'ytsearch5', 'quiet': True, 'ignoreerrors': True, 'no_warnings': True}
                lista = []
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(termo_opt, download=False)
                    if 'entries' in info:
                        for v in info['entries']:
                            if v and v.get('duration') and v['duration'] < 180:
                                lista.append(v)
                
                if lista:
                    escolhido = random.choice(lista)
                    st.success(f"Vídeo: {escolhido.get('title')}")
                    v_url = escolhido['webpage_url']
                    path_down = f"downloads/{escolhido['id']}.mp4"
                    
                    if not os.path.exists(path_down):
                        with yt_dlp.YoutubeDL({'format':'best[ext=mp4]', 'outtmpl':path_down, 'quiet':True}) as ydl:
                            ydl.download([v_url])
                            
                    if os.path.exists(path_down):
                        res = processar_video_viral(path_down, arquivo_audio_final, arquivo_avatar_final)
                        if res: st.video(res)
                else:
                    st.warning("Nenhum vídeo curto achado.")
            except Exception as e:
                st.error(f"Erro: {e}")
        else:
            st.error("⚠️ Faltando Avatar ou Áudio (Gere a voz primeiro!)")