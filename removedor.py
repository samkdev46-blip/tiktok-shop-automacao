from rembg import remove
from PIL import Image
import io

# Nome da imagem que você baixou do Google/Gemini
entrada = "boneco_com_fundo.jpg" 
saida = "avatar/boneco.png" # Salva já na pasta certa

print(f"✂️ Removendo fundo de {entrada}...")

try:
    # Abre a imagem original
    with open(entrada, 'rb') as i:
        input_image = i.read()
    
    # Mágica da IA que remove o fundo
    output_image = remove(input_image)
    
    # Salva o PNG transparente
    with open(saida, 'wb') as o:
        o.write(output_image)
        
    print(f"✅ SUCESSO! Imagem salva sem fundo em: {saida}")

except Exception as e:
    print(f"❌ Erro: {e}")