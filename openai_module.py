import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def gerar_analise_de_treino(dados_treino):
    """Gera análise de treino personalizada usando o ChatGPT"""
    prompt = f"Crie uma análise detalhada de treino com os dados: {dados_treino}"
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        max_tokens=150
    )
    return {"analise": response.choices[0].text.strip()}
