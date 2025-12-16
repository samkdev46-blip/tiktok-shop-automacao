from moviepy.editor import VideoFileClip, vfx
import os
import time

# --- CONFIGURAÇÃO ---
PASTA_ORIGEM = "downloads"
PASTA_DESTINO = "videos_prontos"

print("🧼 Iniciando a Lavanderia de Vídeos...")

# 1. Cria a pasta de destino se não existir
if not os.path.exists(PASTA_DESTINO):
    os.makedirs(PASTA_DESTINO)

# 2. Lista os vídeos baixados
arquivos = [f for f in os.listdir(PASTA_ORIGEM) if f.endswith(".mp4")]

if not arquivos:
    print(f"❌ Nenhum vídeo encontrado na pasta '{PASTA_ORIGEM}'!")
else:
    print(f"📦 Encontrei {len(arquivos)} vídeos para processar.")
    
    contador = 1
    
    for arquivo in arquivos:
        caminho_original = os.path.join(PASTA_ORIGEM, arquivo)
        
        # Cria um nome novo e limpo (ex: produto_01.mp4)
        nome_novo = f"produto_viral_{contador}.mp4"
        caminho_final = os.path.join(PASTA_DESTINO, nome_novo)
        
        print(f"\n🔄 Processando: {arquivo}")
        print("   ⏳ Aplicando 'Truque de 1%' (Acelerando para tornar único)...")
        
        try:
            # Carrega o vídeo na memória
            video = VideoFileClip(caminho_original)
            
            # --- O TRUQUE MÁGICO ✨ ---
            # Acelera o vídeo em 1% (fator 1.01). 
            # Isso altera cada frame do vídeo, gerando um arquivo 100% novo pro algoritmo.
            video_unico = video.fx(vfx.speedx, 1.01)
            
            # Salva o novo vídeo (sem metadados antigos)
            # 'preset="ultrafast"' é para não fritar seu Dell
            video_unico.write_videofile(caminho_final, codec='libx264', audio_codec='aac', preset='ultrafast', verbose=False)
            
            # Libera a memória (Importante pro seu Dell!)
            video.close()
            video_unico.close()
            
            print(f"   ✅ Sucesso! Salvo como: {nome_novo}")
            contador += 1
            
        except Exception as e:
            print(f"   ❌ Erro ao processar esse vídeo: {e}")

    print("\n🏁 LAVANDERIA FECHADA! Todos os vídeos estão limpos.")
    print(f"👉 Verifique a pasta '{PASTA_DESTINO}'")