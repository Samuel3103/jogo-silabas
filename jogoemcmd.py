import random
import openpyxl
import pandas as pd
import os

# Abra o arquivo XLSX
caminho_arquivo = r"SILABAS.xlsx"
workbook = openpyxl.load_workbook(caminho_arquivo)
sheet = workbook.active
paises = {}

# Itere pelas linhas da planilha e adicione ao dicionário
for row in sheet.iter_rows(min_row=2, values_only=True):
    silaba = row[0]
    palavra = row[1]
    paises[silaba] = palavra

# Lista para controlar quais famílias silábicas já foram escolhidas
familias_escolhidas = []

def escolher_pais_aleatorio():
    familia_disponivel = [familia for familia in paises.keys() if familia not in familias_escolhidas]
    if not familia_disponivel:
        return None
    familia_sorteada = random.choice(familia_disponivel)
    familias_escolhidas.append(familia_sorteada)
    return familia_sorteada

def main():
    nome = input("Digite seu nome: ")
    vidas = vidas_iniciais
    pontos = 0
    
    print("Bem-vindo ao Jogo de Adivinhação de Família Silábica,", nome + "!")
    print("Você tem", vidas, "vidas.")
    
    while vidas > 0:
        pais_alvo = escolher_pais_aleatorio()
        if pais_alvo is None:
            print("Você esgotou todas as famílias silábicas disponíveis. Fim de jogo!")
            break
            
        dica = paises[pais_alvo]
        
        print("\nDica:", dica)
        palpite = input("Digite o nome do país: ")
        
        if palpite.upper() == pais_alvo:
            pontos += 1
            print("Parabéns! Você acertou:", pais_alvo)
            print("Pontuação atual:", pontos)
        else:
            vidas -= 1
            if vidas == 0:
                print("Você perdeu todas as vidas. Fim de jogo!")
            else:
                print("Errado! Você perdeu uma vida. Vidas restantes:", vidas)
                print("A resposta correta era:", pais_alvo)
    
    # Salvar nome e pontuação em um arquivo XLSX
    dados = {'Nome': [nome], 'Pontuação': [pontos]}
    
    if os.path.exists('pontuacao.xlsx'):
        df_anterior = pd.read_excel('pontuacao.xlsx')
        df_atual = pd.DataFrame(data=dados)
        df_final = pd.concat([df_anterior, df_atual], ignore_index=True)
    else:
        df_final = pd.DataFrame(data=dados)
    
    df_final.to_excel('pontuacao.xlsx', index=False)
    print("\nNome e pontuação salvas no arquivo pontuacao.xlsx")

if __name__ == "__main__":
    vidas_iniciais = 5
    main()
