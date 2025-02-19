from requests import get
from pprint import PrettyPrinter

# Constantes
BASE_URL = "https://pokeapi.co/api/v2/"
ALL_POKE = "pokemon/"

printer = PrettyPrinter()

def get_info():
    """
    Obtiene la lista de Pokémon desde la API.
    """
    try:
        # Obtener los datos de la API
        response = get(BASE_URL + ALL_POKE)
        response.raise_for_status()  # Lanza una excepción si la solicitud no fue exitosa
        data = response.json()

        # Extraer los nombres y números de los Pokémon
        poke_list = data["results"]
        return poke_list

    except Exception as e:
        print(f"Error fetching data from API: {e}")
        return []

def get_poke_info(poke_list):
    """
    Extrae el nombre y número de cada Pokémon.
    """
    poke_info = [
        {"name": poke["name"], "number": poke["url"].split("/")[-2]} for poke in poke_list
    ]
    return poke_info

def get_specific_pokemon(identifier):
    """
    Obtiene información detallada de un Pokémon específico por nombre o número.
    """
    try:
        # Hacer la solicitud a la API
        response = get(f"{BASE_URL}pokemon/{identifier}/")
        response.raise_for_status()  # Lanza una excepción si la solicitud no fue exitosa
        pokemon_data = response.json()

        # Extraer información relevante
        pokemon_info = {
            "name": pokemon_data["name"],
            "number": pokemon_data["id"],
            "types": [t["type"]["name"] for t in pokemon_data["types"]],
            "abilities": [a["ability"]["name"] for a in pokemon_data["abilities"]],
            "height": pokemon_data["height"],  # Altura en decímetros
            "weight": pokemon_data["weight"],
            "image_url": pokemon_data["sprites"]["front_default"],
            "stats": {s["stat"]["name"]: s["base_stat"] for s in pokemon_data["stats"]}
        }
        return pokemon_info

    except Exception as e:
        print(f"Error fetching data for Pokémon '{identifier}': {e}")
        return None

def fightPokemon():
    """
    Compara dos Pokémon en base a sus estadísticas y tipos.
    """
    poke1 = input("Ingrese el nombre o número del primer Pokémon: ").strip().lower()
    poke2 = input("Ingrese el nombre o número del segundo Pokémon: ").strip().lower()
    
    pokemon1 = get_specific_pokemon(poke1)
    pokemon2 = get_specific_pokemon(poke2)
    
    if not pokemon1 or not pokemon2:
        print("No se pudo obtener información de uno o ambos Pokémon.")
        return
    
    print(f"\n{pokemon1['name'].capitalize()} vs {pokemon2['name'].capitalize()}\n")
    
    # Sumar las estadísticas base de cada Pokémon
    total_stats1 = sum(pokemon1['stats'].values())
    total_stats2 = sum(pokemon2['stats'].values())
    
    print(f"Estadísticas totales:")
    print(f"{pokemon1['name'].capitalize()}: {total_stats1}")
    print(f"{pokemon2['name'].capitalize()}: {total_stats2}\n")
    
    # Evaluar el tipo de ventaja basado en el primer tipo de cada Pokémon
    type_advantage = {
        "fire": ["grass", "ice", "bug", "steel"],
        "water": ["fire", "ground", "rock"],
        "grass": ["water", "ground", "rock"],
        "electric": ["water", "flying"],
        "ice": ["grass", "ground", "flying", "dragon"],
        "fighting": ["normal", "ice", "rock", "dark", "steel"],
        "poison": ["grass", "fairy"],
        "ground": ["fire", "electric", "poison", "rock", "steel"],
        "flying": ["grass", "fighting", "bug"],
        "psychic": ["fighting", "poison"],
        "bug": ["grass", "psychic", "dark"],
        "rock": ["fire", "ice", "flying", "bug"],
        "ghost": ["psychic", "ghost"],
        "dragon": ["dragon"],
        "dark": ["psychic", "ghost"],
        "steel": ["ice", "rock", "fairy"],
        "fairy": ["fighting", "dragon", "dark"]
    }
    
    advantage1 = any(t in type_advantage.get(pokemon1['types'][0], []) for t in pokemon2['types'])
    advantage2 = any(t in type_advantage.get(pokemon2['types'][0], []) for t in pokemon1['types'])
    
    print("Ventaja por tipo:")
    if advantage1 and not advantage2:
        print(f"{pokemon1['name'].capitalize()} tiene ventaja sobre {pokemon2['name'].capitalize()} por tipo.")
        total_stats1 *= 1.1  # Aumentamos un 10%
    elif advantage2 and not advantage1:
        print(f"{pokemon2['name'].capitalize()} tiene ventaja sobre {pokemon1['name'].capitalize()} por tipo.")
        total_stats2 *= 1.1  # Aumentamos un 10%
    else:
        print("Ninguno tiene ventaja por tipo.")
    
    print("\nResultado del combate:")
    if total_stats1 > total_stats2:
        print(f"{pokemon1['name'].capitalize()} gana la batalla!")
    elif total_stats2 > total_stats1:
        print(f"{pokemon2['name'].capitalize()} gana la batalla!")
    else:
        print("¡Es un empate!")

def main():
    """
    Función principal del programa.
    """
    while True:
        print("\nMenú:")
        print("1. Buscar un Pokémon")
        print("2. Simular una batalla")
        print("3. Salir")
        choice = input("Seleccione una opción: ").strip()
        
        if choice == "1":
            search_input = input("Ingrese un nombre o número de Pokémon: ").strip().lower()
            specific_pokemon = get_specific_pokemon(search_input)
            if specific_pokemon:
                printer.pprint(specific_pokemon)
            else:
                print("Pokémon no encontrado.")
        elif choice == "2":
            fightPokemon()
        elif choice == "3":
            break
        else:
            print("Opción no válida. Inténtelo de nuevo.")

if __name__ == "__main__":
    main()
