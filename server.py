from flask import Flask, jsonify, request
from groq_module import gerar_cardapio
from openai_module import gerar_analise_de_treino
from gmaps_module import get_gmap_data
import os

app = Flask(__name__)

@app.route('/academias', methods=['GET'])
def listar_academias():
    """Rota para listar academias usando dados do Google Maps"""
    query = request.args.get('query', 'academia perto de mim')
    academias = get_gmap_data(query)
    return jsonify(academias)

@app.route('/analise', methods=['POST'])
def analise_treino():
    """Gera análise personalizada de treino"""
    dados_treino = request.json
    analise = gerar_analise_de_treino(dados_treino)
    return jsonify(analise)

@app.route('/cardapio', methods=['GET'])
def cardapio():
    """Retorna cardápio gerado pelo Groq"""
    cardapio = gerar_cardapio()
    return jsonify(cardapio)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
