from flask import Flask, render_template, request, redirect, url_for, session

import random
import openpyxl
import pandas as pd
import os

app = Flask(__name__)
app.secret_key = '05a603cddbf379d782dde4f6c97d7b1cf80631942c136703'

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


def carregar_leaderboard():
    if os.path.exists('pontuacao.xlsx'):
        df = pd.read_excel('pontuacao.xlsx')
        df = df.sort_values(by='Pontuação', ascending=False)
        top10 = df.head(10)
        return top10.to_dict('records')  # Converta o DataFrame para uma lista de dicionários
    else:
        return None



@app.route("/", methods=["GET", "POST"])
def inserir_nome():
    nome = None
    leaderboard = carregar_leaderboard()  # Carrega o leaderboard
    print(leaderboard)
    print(type(leaderboard))

    if request.method == "POST":
        nome = request.form.get("nome")
        session['nome'] = nome
        session['vidas'] = 5
        return redirect(url_for("jogar"))
    
    return render_template("inserir_nome.html", nome=nome, leaderboard=leaderboard)





@app.route("/jogar", methods=["GET", "POST"])
def jogar():
    nome = session.get('nome')
    vidas = session.get('vidas', 5)
    pontos = session.get('pontos', 0)
    dica = session.get('dica', "")
    resultado = ""

    print(f"Vidas no início do jogo: {vidas}")

    familia_sorteada = session.get('familia_sorteada')

    if request.method == "GET" or not familia_sorteada:
        familia_sorteada = escolher_pais_aleatorio()
        dica = paises[familia_sorteada]
        session['dica'] = dica
        session['familia_sorteada'] = familia_sorteada

    if request.method == "POST":
        submit_button = request.form.get("submit")

        if submit_button == "palpite":
            palpite = request.form.get("palpite")
            
            if familia_sorteada:
                dica = paises[familia_sorteada]
                print('BORA POHA',dica,palpite.upper(), familia_sorteada,palpite.upper() == familia_sorteada)
                if palpite.upper() == familia_sorteada:
                    pontos += 1
                    session['pontos'] = pontos
                    resultado = f"Parabéns! Você acertou: {familia_sorteada}. Pontuação atual: {pontos}"
                else:
                    vidas -= 1
                    session['vidas'] = vidas
                    print(f"Vidas após perder uma vida: {vidas}")
                    if vidas == 0:
                        print("Todas as vidas perdidas. Reiniciando o jogo.")
                        session.pop('nome')
                        session.pop('vidas')
                        session.pop('pontos')
                        session.pop('dica')
                        session.pop('familia_sorteada')
                        
                        dados = {'Nome': [nome], 'Pontuação': [pontos]}

                        if os.path.exists('pontuacao.xlsx'):
                            df_anterior = pd.read_excel('pontuacao.xlsx')
                            df_atual = pd.DataFrame(data=dados)
                            df_final = pd.concat([df_anterior, df_atual], ignore_index=True)
                        else:
                            df_final = pd.DataFrame(data=dados)

                        df_final.to_excel('pontuacao.xlsx', index=False)
                        
                        return redirect(url_for("inserir_nome"))
                    else:
                        resultado = f"Errado! Você perdeu uma vida. Vidas restantes: {vidas}. A resposta correta era: {familia_sorteada}"



        elif submit_button == "proxima_pergunta":
            familia_sorteada = escolher_pais_aleatorio()
            dica = paises[familia_sorteada]
            session['dica'] = dica
            session['familia_sorteada'] = familia_sorteada

    return render_template("jogar.html", nome=nome, vidas=vidas, dica=dica, resultado=resultado)







def escolher_pais_aleatorio():
    familia_disponivel = [familia for familia in paises.keys() if familia not in familias_escolhidas]
    if not familia_disponivel:
        return None
    familia_sorteada = random.choice(familia_disponivel)
    familias_escolhidas.append(familia_sorteada)
    print('fs: ',familia_sorteada)
    print('f2: ',familias_escolhidas)
    return familia_sorteada

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
