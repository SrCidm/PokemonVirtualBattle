from requests import get
from PyQt5.QtWidgets import (
    QApplication, QLabel, QLineEdit, QPushButton, QVBoxLayout, 
    QWidget, QHBoxLayout, QFrame, QMessageBox, QInputDialog
)
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt
import sys
import requests
from io import BytesIO
import random
import aiohttp
import asyncio

# Constantes
BASE_URL = "https://pokeapi.co/api/v2/"
ALL_POKE = "pokemon"
        # Tabla de ventajas de tipo
type_advantage = {
            "normal": {
                "normal": 1, "fire": 1, "water": 1, "grass": 1, "electric": 1, "ice": 1, "fighting": 1,
                "poison": 1, "ground": 1, "flying": 1, "psychic": 1, "bug": 1, "rock": 0.5, "ghost": 0,
                "dragon": 1, "dark": 1, "steel": 0.5, "fairy": 1
            },
            "fire": {
                "normal": 1, "fire": 0.5, "water": 0.5, "grass": 2, "electric": 1, "ice": 2, "fighting": 1,
                "poison": 1, "ground": 1, "flying": 1, "psychic": 1, "bug": 2, "rock": 0.5, "ghost": 1,
                "dragon": 0.5, "dark": 1, "steel": 2, "fairy": 1
            },
            "water": {
                "normal": 1, "fire": 2, "water": 0.5, "grass": 0.5, "electric": 1, "ice": 1, "fighting": 1,
                "poison": 1, "ground": 2, "flying": 1, "psychic": 1, "bug": 1, "rock": 2, "ghost": 1,
                "dragon": 0.5, "dark": 1, "steel": 1, "fairy": 1
            },
            "grass": {
                "normal": 1, "fire": 0.5, "water": 2, "grass": 0.5, "electric": 1, "ice": 1, "fighting": 1,
                "poison": 0.5, "ground": 2, "flying": 0.5, "psychic": 1, "bug": 0.5, "rock": 2, "ghost": 1,
                "dragon": 0.5, "dark": 1, "steel": 0.5, "fairy": 1
            },
            "electric": {
                "normal": 1, "fire": 1, "water": 2, "grass": 0.5, "electric": 0.5, "ice": 1, "fighting": 1,
                "poison": 1, "ground": 0, "flying": 2, "psychic": 1, "bug": 1, "rock": 1, "ghost": 1,
                "dragon": 1, "dark": 1, "steel": 1, "fairy": 1
            },
            "ice": {
                "normal": 1, "fire": 0.5, "water": 0.5, "grass": 2, "electric": 1, "ice": 0.5, "fighting": 1,
                "poison": 1, "ground": 2, "flying": 2, "psychic": 1, "bug": 1, "rock": 1, "ghost": 1,
                "dragon": 2, "dark": 1, "steel": 0.5, "fairy": 1
            },
            "fighting": {
                "normal": 2, "fire": 1, "water": 1, "grass": 1, "electric": 1, "ice": 2, "fighting": 1,
                "poison": 1, "ground": 1, "flying": 0.5, "psychic": 0.5, "bug": 0.5, "rock": 2, "ghost": 0,
                "dragon": 1, "dark": 2, "steel": 2, "fairy": 0.5
            },
            "poison": {
                "normal": 1, "fire": 1, "water": 1, "grass": 2, "electric": 1, "ice": 1, "fighting": 1,
                "poison": 0.5, "ground": 0.5, "flying": 1, "psychic": 1, "bug": 1, "rock": 0.5, "ghost": 0.5,
                "dragon": 1, "dark": 1, "steel": 0, "fairy": 2
            },
            "ground": {
                "normal": 1, "fire": 2, "water": 1, "grass": 0.5, "electric": 2, "ice": 1, "fighting": 1,
                "poison": 2, "ground": 1, "flying": 0, "psychic": 1, "bug": 1, "rock": 2, "ghost": 1,
                "dragon": 1, "dark": 1, "steel": 2, "fairy": 1
            },
            "flying": {
                "normal": 1, "fire": 1, "water": 1, "grass": 2, "electric": 0.5, "ice": 1, "fighting": 2,
                "poison": 1, "ground": 1, "flying": 1, "psychic": 1, "bug": 2, "rock": 0.5, "ghost": 1,
                "dragon": 1, "dark": 1, "steel": 0.5, "fairy": 1
            },
            "psychic": {
                "normal": 1, "fire": 1, "water": 1, "grass": 1, "electric": 1, "ice": 1, "fighting": 2,
                "poison": 2, "ground": 1, "flying": 1, "psychic": 0.5, "bug": 1, "rock": 1, "ghost": 0,
                "dragon": 1, "dark": 0, "steel": 0.5, "fairy": 1
            },
            "bug": {
                "normal": 1, "fire": 0.5, "water": 1, "grass": 0.5, "electric": 1, "ice": 1, "fighting": 0.5,
                "poison": 0.5, "ground": 1, "flying": 0.5, "psychic": 2, "bug": 1, "rock": 1, "ghost": 0.5,
                "dragon": 1, "dark": 2, "steel": 0.5, "fairy": 0.5
            },
            "rock": {
                "normal": 1, "fire": 2, "water": 1, "grass": 2, "electric": 1, "ice": 2, "fighting": 0.5,
                "poison": 1, "ground": 0.5, "flying": 2, "psychic": 1, "bug": 2, "rock": 1, "ghost": 1,
                "dragon": 1, "dark": 1, "steel": 0.5, "fairy": 1
            },
            "ghost": {
                "normal": 0, "fire": 1, "water": 1, "grass": 1, "electric": 1, "ice": 1, "fighting": 1,
                "poison": 1, "ground": 1, "flying": 1, "psychic": 2, "bug": 1, "rock": 1, "ghost": 2,
                "dragon": 1, "dark": 0, "steel": 1, "fairy": 1
            },
            "dragon": {
                "normal": 1, "fire": 1, "water": 1, "grass": 1, "electric": 1, "ice": 1, "fighting": 1,
                "poison": 1, "ground": 1, "flying": 1, "psychic": 1, "bug": 1, "rock": 1, "ghost": 1,
                "dragon": 2, "dark": 1, "steel": 0.5, "fairy": 0
            },
            "dark": {
                "normal": 1, "fire": 1, "water": 1, "grass": 1, "electric": 1, "ice": 1, "fighting": 0.5,
                "poison": 1, "ground": 1, "flying": 1, "psychic": 2, "bug": 1, "rock": 1, "ghost": 2,
                "dragon": 1, "dark": 0.5, "steel": 1, "fairy": 0.5
            },}
def get_specific_pokemon(identifier):
    """
    Obtiene información detallada de un Pokémon específico por nombre o número.
    """
    try:
        response = get(f"{BASE_URL}pokemon/{identifier}/")
        response.raise_for_status()
        pokemon_data = response.json()

        # Extraer las estadísticas del Pokémon
        stats = {stat["stat"]["name"]: stat["base_stat"] for stat in pokemon_data["stats"]}

        pokemon_info = {
            "name": pokemon_data["name"],
            "number": pokemon_data["id"],
            "types": [t["type"]["name"] for t in pokemon_data["types"]],
            "abilities": [a["ability"]["name"] for a in pokemon_data["abilities"]],
            "height": pokemon_data["height"],
            "weight": pokemon_data["weight"],
            "image_url": pokemon_data["sprites"]["front_default"],
            "back_image_url": pokemon_data["sprites"].get("back_default", ""),
            "stats": stats,
        }
        return pokemon_info
    except Exception as e:
        print(f"Error fetching data for Pokémon '{identifier}': {e}")
        return None

async def fetch_move(session, move_url):
    """Obtiene los detalles de un movimiento y verifica si tiene 'power'."""
    async with session.get(move_url) as response:
        move_data = await response.json()
        if move_data.get("power") and move_data["power"] > 0:
            return move_data["name"]  # Solo devuelve el nombre si tiene power
        return None

async def get_pokemon_moves_async(identifier):
    """Obtiene los movimientos de un Pokémon que tienen 'power' usando solicitudes asíncronas."""
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{BASE_URL}pokemon/{identifier}/") as response:
            pokemon_data = await response.json()

            # Obtener todas las URLs de movimientos
            move_urls = [move["move"]["url"] for move in pokemon_data["moves"]]

            # Hacer todas las peticiones en paralelo
            tasks = [fetch_move(session, url) for url in move_urls]
            moves = await asyncio.gather(*tasks)

            # Filtrar None (movimientos sin power)
            return [move for move in moves if move]

def get_pokemon_moves(identifier):
    """Función de entrada para ejecutar la versión asíncrona."""
    return asyncio.run(get_pokemon_moves_async(identifier))

def get_move_power(move_name):
    """Obtiene el poder de un movimiento desde la API."""
    try:
        response = get(f"{BASE_URL}move/{move_name}/")
        response.raise_for_status()
        move_data = response.json()
        return move_data.get("power", 0)  # Si no tiene poder, devuelve 0
    except Exception as e:
        print(f"Error retrieving move details {move_name}: {e}")
        return 0  # Valor por defecto en caso de error

class PokedexApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Pokemon Battle Simulator")
        self.setGeometry(100, 100, 400, 600)

        # Aplicar estilo Pokédex
        self.setStyleSheet("""
                           QInputDialog {
                                background-color: black;
                                border: 2px solid black;
                                border-radius: 5px;
                                padding: 5px;
                            }
                            QPushButton {
                                background-color: red;
                                color: white;
                                border: 2px solid white;
                                border-radius: 10px;
                                padding: 10px;
                            }
                            QPushButton:hover {
                                background-color: #000;  /* Color al pasar el ratón */
                            }
                            QPushButton:pressed {
                                background-color: #000;  /* Color cuando el botón es presionado */
                            }
                            """
                            "color: black; background-color: red; border: 2px solid black; padding: 10px; border-radius: 5px;")

        self.layout = QVBoxLayout()

        self.header = QLabel("Pokemon Battle Simulator", self)
        self.header.setFont(QFont("Arial", 20, QFont.Bold))
        self.header.setAlignment(Qt.AlignCenter)
        self.header.setStyleSheet("color: white; background-color: black; padding: 5px; border-radius: 10px;")
        self.layout.addWidget(self.header)

        self.search_input = QLineEdit(self)
        self.search_input.setPlaceholderText("Enter the name or number of the Pokemon")
        self.search_input.setStyleSheet("background-color: white; border: 2px solid black; border-radius: 5px; padding: 5px;")
        self.layout.addWidget(self.search_input)

        self.search_button = QPushButton("Find Pokemon", self)
        self.search_button.setStyleSheet("background-color: black; color: white; border-radius: 5px; padding: 5px;")
        self.search_button.clicked.connect(self.search_pokemon)
        self.layout.addWidget(self.search_button)

        # Botón para simular batalla
        self.battle_button = QPushButton("Virtual Battle", self)
        self.battle_button.setStyleSheet("background-color: black; color: white; border-radius: 5px; padding: 5px;")
        self.battle_button.clicked.connect(self.simulate_battle)
        self.layout.addWidget(self.battle_button)

        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setStyleSheet("background-color: white")
        self.layout.addWidget(self.image_label)

        self.info_frame = QFrame(self)
        self.info_frame.setStyleSheet("background-color: white; border-radius: 10px; padding: 10px;")
        self.info_layout = QVBoxLayout()

        self.info_label = QLabel(self)
        self.info_label.setFont(QFont("Arial", 12))
        self.info_label.setAlignment(Qt.AlignCenter)
        self.info_label.setStyleSheet("background-color: white")
        self.info_layout.addWidget(self.info_label)

        self.info_frame.setLayout(self.info_layout)
        self.layout.addWidget(self.info_frame)

        # Layout para las imágenes de batalla
        self.battle_layout = QHBoxLayout()
        self.layout.addLayout(self.battle_layout)

        self.setLayout(self.layout)
        

    def search_pokemon(self):
        identifier = self.search_input.text().strip().lower()
        pokemon = get_specific_pokemon(identifier)
        if pokemon:
            image_url = pokemon["image_url"]
            pixmap = self.get_pixmap_from_url(image_url)
            self.image_label.setPixmap(pixmap)

            info_text = (f"<b>Name:</b> {pokemon['name'].capitalize()}<br>"
                         f"<b>Number:</b> {pokemon['number']}<br>"
                         f"<b>Types:</b> {', '.join(pokemon['types'])}<br>"
                         f"<b>Height:</b> {pokemon['height']} decímetros<br>"
                         f"<b>Weight:</b> {pokemon['weight']} hectogramos<br>"
                         f"<b>Abilitys:</b> {', '.join(pokemon['abilities'])}")
            self.info_label.setText(info_text)
        else:
            self.image_label.clear()
            self.info_label.setText("<b>Pokemon not found</b>")

    def simulate_battle(self):
        self.clear_battle_layout()

        poke1, ok1 = QInputDialog.getText(self, "Pokémon 1", "Enter the name or number of the first Pokémon:")
        poke2, ok2 = QInputDialog.getText(self, "Pokémon 2", "Enter the name or number of the second Pokémon:")

        if not ok1 or not ok2:
            return

        pokemon1 = get_specific_pokemon(poke1.strip().lower())
        pokemon2 = get_specific_pokemon(poke2.strip().lower())

        if not pokemon1 or not pokemon2:
            QMessageBox.warning(self, "Error", "Could not retrieve information for one or both Pokémon.")
            return

        moves1 = get_pokemon_moves(poke1.strip().lower())
        moves2 = get_pokemon_moves(poke2.strip().lower())

        if moves1 is None or moves2 is None:
            QMessageBox.warning(self, "Error", "The moves for one or both Pokémon could not be retrieved.")
            return

        self.show_battle_images(pokemon1, pokemon2)

        # Simular batalla por turnos
        battle_log = []  # Para almacenar los eventos de la batalla
        hp1 = pokemon1["stats"].get("hp", 100)  # Usar HP real si está disponible
        hp2 = pokemon2["stats"].get("hp", 100)

        while hp1 > 0 and hp2 > 0:
            # Turno del Pokémon 1
            move1 = random.choice(moves1)
            damage1 = self.calculate_damage(pokemon1, pokemon2, move1)
            hp2 -= damage1
            battle_log.append(f"{pokemon1['name'].capitalize()} use {move1}. It causes {damage1} damage!")

            if hp2 <= 0:
                break

            # Turno del Pokémon 2
            move2 = random.choice(moves2)
            damage2 = self.calculate_damage(pokemon2, pokemon1, move2)
            hp1 -= damage2
            battle_log.append(f"{pokemon2['name'].capitalize()} use {move2}. It causes {damage2} damage!")

        # Mostrar el resultado de la batalla
        winner = pokemon1 if hp1 > hp2 else pokemon2 if hp2 > hp1 else None
        self.show_winner(winner)

        # Mostrar el registro de la batalla
        battle_log_text = "\n".join(battle_log)
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Battle Log")
        msg_box.setText(battle_log_text)
        msg_box.setStyleSheet("""background-color: red; color: white; border: 2px solid red;""")
        btn_ok = msg_box.addButton("Accept", QMessageBox.AcceptRole)
        btn_ok.setStyleSheet("background-color: black; color: white; border-radius: 5px; padding: 5px;")
        msg_box.exec_()

    def clear_battle_layout(self):
        """
        Limpia el layout de batalla anterior.
        """
        while self.battle_layout.count():
            item = self.battle_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

    def show_battle_images(self, pokemon1, pokemon2):
        """
        Muestra las imágenes de los Pokémon en batalla con fondo blanco.
        """
        # Crear un contenedor para el primer Pokémon
        container1 = QVBoxLayout()
        container1_widget = QWidget()  # Widget para el contenedor
        container1_widget.setLayout(container1)
        container1_widget.setStyleSheet("background-color: white; border: 2px solid black; border-radius: 10px; padding: 10px;")  # Fondo blanco

        if pokemon1["back_image_url"]:
            pixmap1 = self.get_pixmap_from_url(pokemon1["back_image_url"])
            label1 = QLabel(self)
            label1.setPixmap(pixmap1)
            container1.addWidget(label1)

        # Mostrar nombre y número del primer Pokémon
        info1 = QLabel(f"{pokemon1['name'].capitalize()} (#{pokemon1['number']})", self)
        info1.setAlignment(Qt.AlignCenter)
        info1.setStyleSheet("background-color: white; color: black; font-weight: bold;")  # Fondo blanco y texto negro
        container1.addWidget(info1)

        # Crear un contenedor para el segundo Pokémon
        container2 = QVBoxLayout()
        container2_widget = QWidget()  # Widget para el contenedor
        container2_widget.setLayout(container2)
        container2_widget.setStyleSheet("background-color: white; border: 2px solid black; border-radius: 10px; padding: 10px;")  # Fondo blanco

        if pokemon2["image_url"]:
            pixmap2 = self.get_pixmap_from_url(pokemon2["image_url"])
            label2 = QLabel(self)
            label2.setPixmap(pixmap2)
            container2.addWidget(label2)

        # Mostrar nombre y número del segundo Pokémon
        info2 = QLabel(f"{pokemon2['name'].capitalize()} (#{pokemon2['number']})", self)
        info2.setAlignment(Qt.AlignCenter)
        info2.setStyleSheet("background-color: white; color: black; font-weight: bold;")  # Fondo blanco y texto negro
        container2.addWidget(info2)

        # Agregar los contenedores al layout de batalla
        self.battle_layout.addWidget(container1_widget)  # Agregar el widget del contenedor
        self.battle_layout.addWidget(container2_widget)  # Agregar el widget del contenedor
  
    def determine_winner(self, pokemon1, pokemon2, moves1, moves2):
        """Simulación de batalla más realista."""

        # Simulación simplificada por turnos (ejemplo básico)
        hp1 = sum(pokemon1["stats"].values())  # Puntos de salud iniciales (simplificado)
        hp2 = sum(pokemon2["stats"].values())

        while hp1 > 0 and hp2 > 0:
            # Turno del pokemon1
            move1 = random.choice(moves1)  # Elige un movimiento aleatorio
            damage1 = self.calculate_damage(pokemon1, pokemon2, move1)
            hp2 -= damage1

            if hp2 <= 0:
                break  # pokemon1 gana

            # Turno del pokemon2
            move2 = random.choice(moves2)  # Elige un movimiento aleatorio
            damage2 = self.calculate_damage(pokemon2, pokemon1, move2)
            hp1 -= damage2

            if hp1 <= 0:
                break  # pokemon2 gana

        if hp1 > hp2:
            return pokemon1
        elif hp2 > hp1:
            return pokemon2
        else:
            return None  # Empate
        
    def calculate_damage(self, attacker, defender, move):
        """Calcula el daño de un movimiento de manera más realista."""
        try:
            # Obtener el poder del movimiento
            power = get_move_power(move)

            # Si el movimiento no tiene poder, es un movimiento de estado y no hace daño
            if power is None or power == 0:
                return 0

            # Obtener el tipo del movimiento
            move_response = get(f"{BASE_URL}move/{move}/")
            move_response.raise_for_status()
            move_data = move_response.json()
            move_type = move_data.get("type", {}).get("name", "normal")  # Usa "normal" como tipo por defecto si no se encuentra

            # Obtener los tipos del defensor
            defender_types = defender.get("types", [])

            # Calcular el multiplicador de tipo
            type_multiplier = 1
            for defender_type in defender_types:
                type_multiplier *= type_advantage.get(move_type, {}).get(defender_type, 1)

            # Estadísticas del atacante y defensor
            attack = attacker["stats"].get("attack", 50)  # Ataque del atacante
            defense = defender["stats"].get("defense", 50)  # Defensa del defensor

            # Factor aleatorio entre 0.85 y 1.0 para simular variabilidad
            random_factor = random.uniform(0.85, 1.0)

            # Fórmula de daño simplificada (similar a los juegos de Pokémon)
            damage = (((2 * 50 / 5 + 2) * power * (attack / defense) / 50 + 2) * type_multiplier * random_factor)

            return int(damage) if damage > 0 else 1  # Mínimo 1 de daño

        except Exception as e:
            print(f"Error calculating the move damage. {move}: {e}")
            return 10  # Daño por defecto en caso de error


    def show_winner(self, winner):
        """
        Muestra la imagen del Pokémon ganador.
        """
        if winner:
            pixmap = self.get_pixmap_from_url(winner["image_url"])
            self.image_label.setPixmap(pixmap)
            msg_box = QMessageBox(self)
            msg_box.setWindowTitle("Winner")
            msg_box.setText(f"{winner['name'].capitalize()} Win the Battle!")
            msg_box.setStyleSheet("""
                background-color: red;
                color: white;
                border: 2px solid red;
            """)
            btn_ok = msg_box.addButton("Accept", QMessageBox.AcceptRole)
            btn_ok.setStyleSheet("background-color: black; color: white; border-radius: 5px; padding: 5px;")
            msg_box.exec_()
        else:
            msg_box = QMessageBox(self)
            msg_box.setWindowTitle("Draw")
            msg_box.setText(f"the battle ended in a draw!")
            msg_box.setStyleSheet("""
                background-color: red;
                color: white;
                border: 2px solid red;
            """)
            btn_ok = msg_box.addButton("Accept", QMessageBox.AcceptRole)
            btn_ok.setStyleSheet("background-color: black; color: white; border-radius: 5px; padding: 5px;")
            msg_box.exec_()

    def get_pixmap_from_url(self, url):
        """
        Obtiene un QPixmap desde una URL.
        """
        response = requests.get(url)
        image = QPixmap()
        image.loadFromData(BytesIO(response.content).read())
        return image

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PokedexApp()
    window.show()
    sys.exit(app.exec_())

