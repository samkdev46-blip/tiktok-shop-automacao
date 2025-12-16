from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time

# --- CONFIGURAÇÃO INICIAL ---
print("Iniciando o Robô... (Se for a primeira vez, vai baixar o driver)")

# O 'ChromeDriverManager' verifica qual seu Chrome e baixa o driver correto sozinho
# Isso evita aquele erro chato de "versão do driver incompatível"
service = ChromeService(ChromeDriverManager().install())
options = webdriver.ChromeOptions()

# Cria a janela do navegador
navegador = webdriver.Chrome(service=service, options=options)

# --- AÇÃO! ---
try:
    # 1. Acessar o Google (só pra testar a conexão)
    navegador.get("https://www.google.com")
    print("Acessei o site!")

    # 2. Digitar algo na busca (simulando um humano)
    # Encontra a barra de pesquisa pelo nome 'q'
    campo_busca = navegador.find_element(By.NAME, "q") 
    campo_busca.send_keys("TikTok Shop Automation Python")
    
    print("Digitei a busca...")
    time.sleep(2) # Espera 2 segundos pra você ver acontecendo

    # 3. Pegar o título da página para provar que leu os dados
    titulo = navegador.title
    print(f"O título da página é: {titulo}")

    # Mantém aberto por 10 segundos antes de fechar
    print("Vou fechar em 10 segundos...")
    time.sleep(10)

except Exception as e:
    print(f"Deu um erro: {e}")

finally:
    # Fecha o navegador para não travar a memória RAM do seu Dell
    navegador.quit()
    print("Navegador fechado com sucesso.")
    