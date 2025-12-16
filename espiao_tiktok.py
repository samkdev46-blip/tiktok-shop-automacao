from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# --- CONFIGURAÇÃO ---
HASHTAG = "tiktokmademebuyit" 

print("🕵️ Iniciando o Robô Espião (Modo Manual)...")

options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

try:
    navegador = webdriver.Chrome(options=options)
    
    print(f"🚀 Acessando a tag: #{HASHTAG}")
    navegador.get(f"https://www.tiktok.com/tag/{HASHTAG}")
    
    # --- A MUDANÇA ESTÁ AQUI 👇 ---
    print("\n" + "="*50)
    print("🛑 PAUSA OBRIGATÓRIA!")
    print("1. Vá no navegador aberto.")
    print("2. Resolva o CAPTCHA (quebra-cabeça) se aparecer.")
    print("3. Espere os vídeos carregarem na tela.")
    input("👉 Quando estiver vendo os vídeos, volte aqui e dê ENTER para continuar...")
    print("="*50 + "\n")
    # ----------------------------------
    
    print("⬇️ Rolando a página para pegar mais virais...")
    for i in range(5): # Aumentei pra 5 rolagens pra pegar mais coisa
        navegador.execute_script("window.scrollBy(0, 500);")
        time.sleep(2)
    
    print("🔎 Caçando links de vídeos...")
    elementos = navegador.find_elements(By.CSS_SELECTOR, 'a')
    
    links_encontrados = []
    for item in elementos:
        link = item.get_attribute('href')
        # Filtro reforçado pra pegar link de vídeo mesmo
        if link and "tiktok.com" in link and "/video/" in link:
            if link not in links_encontrados:
                links_encontrados.append(link)

    print(f"\n✅ AGORA SIM! Encontrei {len(links_encontrados)} vídeos:")
    print("-" * 40)
    for video in links_encontrados[:10]: # Mostra Top 10
        print(video)
    print("-" * 40)

    input("\nPressione ENTER no terminal para encerrar a missão...")

except Exception as e:
    print(f"\n❌ Erro: {e}")

finally:
    if 'navegador' in locals():
        navegador.quit()