import requests

def get_osm_data(query):
    """
    Consulta a API do Nominatim (OpenStreetMap) para buscar informacoes sobre uma localizacao.
    Args:
        query (str): Nome ou endereco da localizacao.
    Returns:
        dict: Dados formatados sobre a localizacao (nome, coordenadas, etc.).
    """
    url = f"https://nominatim.openstreetmap.org/search?q={query}&format=json&addressdetails=1"
    response = requests.get(url, headers={"User-Agent": "academy-review-project"})

    if response.status_code == 200 and response.json():
        data = response.json()[0]  # Pega o primeiro resultado relevante
        return {
            "name": data.get("display_name"),
            "coordinates": {
                "latitude": float(data["lat"]),
                "longitude": float(data["lon"]),
            },
            "address": data.get("address", {})
        }
    return {"error": "Localizacao nao encontrada."}