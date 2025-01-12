from flask import Flask, request, jsonify
from osm_module import get_osm_data
from openai_module import gerar_analise_de_treino
from groq_module import gerar_cardapio

app = Flask(__name__)

@app.route("/localizacao", methods=["GET"])
def localizacao():
    """
    Endpoint para buscar informacoes de uma localizacao usando OSM.
    Params:
        query (str): Nome ou endereco da localizacao.
    Returns:
        JSON: Dados formatados sobre a localizacao.
    """
    query = request.args.get("query")
    if not query:
        return jsonify({"error": "Parâmetro 'query' é obrigatório."}), 400

    data = get_osm_data(query)
    return jsonify(data)

@app.route("/analise", methods=["POST"])
def analise():
    """
    Endpoint para gerar uma analise de treino usando OpenAI.
    """
    body = request.get_json()
    treino = body.get("treino")

    if not treino:
        return jsonify({"error": "Treino não especificado."}), 400

    analise = gerar_analise_de_treino(treino)
    return jsonify({"analise": analise})

@app.route("/cardapio", methods=["GET"])
def cardapio():
    """
    Endpoint para gerar cardapio usando o modulo groq.
    """
    return jsonify({"cardapio": gerar_cardapio()})

if __name__ == "__main__":
    app.run(debug=True)

