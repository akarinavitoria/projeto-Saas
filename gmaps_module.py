import googlemaps
import os

gmaps = googlemaps.Client(key=os.getenv("GMAPS_API_KEY"))

def get_gmap_data(query):
    """Obtém dados de academias a partir do Google Maps"""
    results = gmaps.places(query=query, location=(-23.55052, -46.633308), radius=5000)
    academias = []
    for result in results.get("results", []):
        academia = {
            "name": result.get("name"),
            "address": result.get("vicinity"),
            "rating": result.get("rating"),
            "user_ratings_total": result.get("user_ratings_total"),
            "coordinates": result["geometry"]["location"],
            "photos": result.get("photos", []),
        }
        academias.append(academia)
    return academias
