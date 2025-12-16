import asyncio
import edge_tts  # <--- CORRIGIDO AQUI (Linha 2)
import os

# --- CONFIGURAÇÃO ---
PASTA_AUDIO = "audios_narrecao"
NOME_ARQUIVO_AUDIO = "narracao_vendas.mp3"

TEXTO_VENDAS = """
Para tudo o que você está fazendo e olha isso! 
Eu encontrei o produto mais incrível do TikTok Shop e você precisa ver.
Ele resolve aquele problema chato do dia a dia em segundos.
O link com desconto exclusivo está na minha bio. 
Corre antes que acabe o estoque!
"""

VOZ_ESCOLHIDA = "pt-BR-AntonioNeural"

print("🎙️ Iniciando o Locutor IA...")

if not os.path.exists(PASTA_AUDIO):
    os.makedirs(PASTA_AUDIO)

caminho_final = os.path.join(PASTA_AUDIO, NOME_ARQUIVO_AUDIO)

async def gerar_narracao():
    print(f"📖 Lendo o texto e gerando áudio com a voz: {VOZ_ESCOLHIDA}...")
    
    # <--- CORRIGIDO AQUI EMBAIXO TAMBÉM (Linha 28)
    communicate = edge_tts.Communicate(TEXTO_VENDAS, VOZ_ESCOLHIDA)
    
    await communicate.save(caminho_final)
    print(f"\n✅ SUCESSO! Áudio de vendas criado em: {caminho_final}")
    print("🎧 Pode abrir a pasta e ouvir o resultado!")

try:
    asyncio.run(gerar_narracao())
except Exception as e:
    print(f"❌ Erro ao gerar áudio: {e}")