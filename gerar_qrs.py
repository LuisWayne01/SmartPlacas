import os
import requests
import qrcode

# URL base da sua API
API_URL = "http://localhost:5063"
BASE_DOMINIO_CLIENTE = f"{API_URL}/p"

# Pasta onde os QR codes serão salvos
PASTA_SAIDA = "imagens_qrcode"
os.makedirs(PASTA_SAIDA, exist_ok=True)

def buscar_placas_da_api():
    try:
        # Pergunta no terminal quantos IDs você quer gerar neste lote
        quantidade_desejada = input("Quantas placas você deseja gerar neste lote? ")
        
        print(f"Conectando à API para gerar {quantidade_desejada} placas...")
        
        # Envia o valor digitado para a API
        resposta = requests.post(f"{API_URL}/api/placas/gerar?qtd={quantidade_desejada}")
        
        if resposta.status_code == 200:
            return resposta.json()
        else:
            print("Erro ao gerar placas na API.")
            return []
    except Exception as e:
        print(f"Erro de conexão com a API (ela está rodando?): {e}")
        return []

def gerar_imagens():
    placas = buscar_placas_da_api()
    
    if not placas:
        print("Nenhuma placa encontrada.")
        return

    print(f"\nGerando QR codes para {len(placas)} placas...")

    for placa in placas:
        placa_id = placa["id"]
        
        # Link completo que vai dentro do QR Code e na tag NFC
        link_final = f"{BASE_DOMINIO_CLIENTE}/{placa_id}"
        
        # Configuração do QR Code (alta correção de erro para impressão)
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        qr.add_data(link_final)
        qr.make(fit=True)

        # Cria a imagem e salva
        img = qr.make_image(fill_color="black", back_color="white")
        caminho_arquivo = os.path.join(PASTA_SAIDA, f"placa_{placa_id}.png")
        img.save(caminho_arquivo)
        
        print(f"[OK] Placa {placa_id} salva em: {caminho_arquivo}")

    print(f"\n[SUCESSO] Todos os {len(placas)} QR codes foram salvos na pasta '{PASTA_SAIDA}'!")

if __name__ == "__main__":
    gerar_imagens()