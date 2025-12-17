import streamlit as st
import os
import subprocess
import json
import time

# --- Configurações da Página ---
st.set_page_config(
    page_title="Fábrica de Vídeos Samk", 
    page_icon="🏭",
    layout="centered"
)

st.title("🏭 Fábrica de Vídeos 9.5")
st.write("Controle total: Texto, Volume e Música.")

# --- BOTÃO PARA ATUALIZAR A LISTA (Sincronia com Telegram) ---
if st.button("🔄 Verificar se chegaram vídeos novos"):
    st.rerun()

st.divider()

# --- 1. ROTEIRO ---
st.header("1️⃣ Roteiro (Voz do Antônio)")
texto_padrao = """Para tudo o que você está fazendo e olha isso! 
Eu encontrei o produto mais incrível do TikTok Shop e você precisa ver.
Ele resolve aquele problema chato do dia a dia em segundos.
O link com desconto exclusivo está na minha bio. 
Corre antes que acabe o estoque!"""

novo_roteiro = st.text_area("Texto do Locutor:", value=texto_padrao, height=120)

st.divider()

# --- 2. CONFIGURAÇÃO DE ÁUDIO ---
st.header("2️⃣ Configuração de Música")

col1, col2 = st.columns(2)

with col1:
    # Barrinha de Volume (0 a 100)
    vol_porcentagem = st.slider("🔊 Volume da Música (%)", 0, 100, 15)
    volume_real = vol_porcentagem / 100.0 

with col2:
    # Escolha da Origem
    modo_musica = st.radio("Origem da Música:", ["📂 Aleatória (Da Pasta)", "📤 Upload (Arquivo Único)"])

caminho_musica_temp = None

# Lógica de Upload
if modo_musica == "📤 Upload (Arquivo Único)":
    uploaded_file = st.file_uploader("Arraste seu MP3 aqui", type=["mp3", "wav"])
    if uploaded_file is not None:
        caminho_musica_temp = "temp_music_upload.mp3"
        with open(caminho_musica_temp, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success(f"Música '{uploaded_file.name}' carregada!")

st.divider()

# --- 3. PRODUÇÃO ---
st.header("3️⃣ Produção")
pasta_entrada = "videos_baixados"

# Verifica fila de vídeos
qtd = 0
if os.path.exists(pasta_entrada):
    qtd = len([f for f in os.listdir(pasta_entrada) if f.endswith(('.mp4','.webm','.mkv'))])

if qtd > 0:
    st.success(f"🎬 **{qtd}** vídeos na fila de espera.")
else:
    st.warning("💤 Fila vazia. O Espião (Telegram) ainda não baixou nada novo.")

if st.button("🚀 INICIAR PRODUÇÃO", type="primary"):
    if qtd == 0:
        st.error("Sem vídeos para editar!")
    else:
        # 1. Salva as configurações para o editor.py ler
        dados_config = {
            "texto": novo_roteiro,
            "volume": volume_real,
            "modo_musica": "upload" if modo_musica.startswith("📤") else "aleatorio",
            "caminho_musica_custom": caminho_musica_temp
        }
        
        with open("config_temp.json", "w", encoding="utf-8") as f:
            json.dump(dados_config, f, indent=4)
        
        # 2. Roda o Editor
        status = st.status("🤖 O Robô está trabalhando...", expanded=True)
        status.write("⏳ Iniciando motor de edição...")
        
        processo = subprocess.run(["python", "editor.py"], capture_output=True, text=True)
        
        # 3. Verifica resultado
        if processo.returncode == 0:
            status.update(label="✅ Sucesso! Vídeos gerados.", state="complete", expanded=False)
            st.success("Processamento concluído!")
            
            # Limpa arquivo temporário de música se usou upload
            if caminho_musica_temp and os.path.exists(caminho_musica_temp):
                try: os.remove(caminho_musica_temp)
                except: pass
            
            time.sleep(1)
            st.rerun() # Atualiza a página
        else:
            status.update(label="❌ Erro Fatal", state="error")
            st.error("Ocorreu um erro no editor.py:")
            st.code(processo.stderr)
            st.text("Log de saída:")
            st.text(processo.stdout)

st.divider()

# --- 4. GALERIA ---
st.header("📂 Vídeos Finalizados")
pasta_saida = "videos_finalizados"

if os.path.exists(pasta_saida):
    videos = [f for f in os.listdir(pasta_saida) if f.endswith(".mp4")]
    # Ordena por mais recente
    videos.sort(key=lambda x: os.path.getmtime(os.path.join(pasta_saida, x)), reverse=True)
    
    if not videos:
        st.info("Nenhum vídeo pronto ainda.")
        
    for v in videos:
        caminho_completo = os.path.join(pasta_saida, v)
        
        # Layout: Vídeo na esquerda, Botão na direita
        col_v, col_b = st.columns([0.7, 0.3])
        
        with col_v:
            st.subheader(f"📺 {v}")
            st.video(caminho_completo)
            
        with col_b:
            st.write(" ")
            st.write(" ")
            st.write(" ")
            with open(caminho_completo, "rb") as file:
                st.download_button(
                    label="⬇️ BAIXAR",
                    data=file,
                    file_name=v,
                    mime="video/mp4"
                )
        st.divider()
else:
    st.warning("A pasta de saída ainda não foi criada.")