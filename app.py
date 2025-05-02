from flask import Flask, render_template, request, jsonify
from langchain_openai import ChatOpenAI
import os

OPENAI_API_KEY = "sua chave aqui"

if not OPENAI_API_KEY:
    raise ValueError("A chave da OpenAI não foi configurada corretamente.")

app = Flask(__name__)

# Carrega o modelo OpenAI
def get_openai_model():
    return ChatOpenAI(
        model="gpt-4o",
        openai_api_key=OPENAI_API_KEY,
        temperature=0.2,
    )

# Instancia o modelo
model = get_openai_model()

# Menu e configuração de contexto da IA
parametros_de_configuração = """
Você é uma atendente virtual de uma lanchonete em Cruzília.
Seja simpática, responda de forma informal, e use emojis quando possível.
Pode mostrar o menu, explicar os preços e responder perguntas como se fosse uma conversa do WhatsApp.

Menu da Lanchonete:
- Hambúrguer: R$ 15,00
- Cachorro Quente: R$ 10,00
- Batata Frita: R$ 8,00
- Refrigerante: R$ 5,00
"""

# Log de conversa (começa vazio)
log_conversa = []

# Função que consulta o modelo com histórico
def consultar_oraculo(pergunta, log_conversa):
    contexto = parametros_de_configuração + "\n" + "\n".join(log_conversa)
    pergunta_com_contexto = f"{contexto}\nPergunta: {pergunta}"
    resposta = model.invoke(pergunta_com_contexto)
    return resposta.content

# Rota principal (HTML)
@app.route("/")
def home():
    return render_template("index.html")

# Rota de consulta (mensagem)
@app.route("/consulta", methods=["POST"])
def consulta():
    pergunta_usuario = request.form["pergunta"]
    resposta = consultar_oraculo(pergunta_usuario, log_conversa)

    log_conversa.append(f"Pergunta: {pergunta_usuario}")
    log_conversa.append(f"Resposta: {resposta}")

    return jsonify({"resposta": resposta})

if __name__ == "__main__":
    app.run(debug=True)
