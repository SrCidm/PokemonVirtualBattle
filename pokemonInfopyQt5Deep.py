from requests import get
from PyQt5.QtWidgets import (
    QApplication, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QHBoxLayout, QFrame, QMessageBox, QInputDialog
)
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt
import sys
import requests
from io import BytesIO

# Constantes
BASE_URL = "https://pokeapi.co/api/v2/"
ALL_POKE = "pokemon/"

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
            "stats": stats  # Agregar las estadísticas
        }
        return pokemon_info
    except Exception as e:
        print(f"Error fetching data for Pokémon '{identifier}': {e}")
        return None

class PokedexApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Simulator Battle of Pokemon")
        self.setGeometry(100, 100, 400, 600)

        # Aplicar estilo Pokédex
        self.setStyleSheet("background-color: red; border: 5px solid black; border-radius: 15px;")

        self.layout = QVBoxLayout()

        self.header = QLabel("Simulator Battle of Pokemon", self)
        self.header.setFont(QFont("Arial", 20, QFont.Bold))
        self.header.setAlignment(Qt.AlignCenter)
        self.header.setStyleSheet("color: white; background-color: black; padding: 10px; border-radius: 10px;")
        self.layout.addWidget(self.header)

        self.search_input = QLineEdit(self)
        self.search_input.setPlaceholderText("Ingrese el nombre o número de Pokémon")
        self.search_input.setStyleSheet("background-color: white; border: 2px solid black; border-radius: 5px; padding: 5px;")
        self.layout.addWidget(self.search_input)

        self.search_button = QPushButton("Find Pokemon", self)
        self.search_button.setStyleSheet("background-color: black; color: white; border-radius: 5px; padding: 5px;")
        self.search_button.clicked.connect(self.search_pokemon)
        self.layout.addWidget(self.search_button)

        # Botón para simular batalla
        self.battle_button = QPushButton("Simulator Battle", self)
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
                         f"<b>High:</b> {pokemon['height']} decímetros<br>"
                         f"<b>Weight:</b> {pokemon['weight']} hectogramos<br>"
                         f"<b>Abilitys:</b> {', '.join(pokemon['abilities'])}")
            self.info_label.setText(info_text)
        else:
            self.image_label.clear()
            self.info_label.setText("<b>Pokemon not found</b>")

    def simulate_battle(self):
        """
        Simula una batalla entre dos Pokémon.
        """
        # Limpiar el layout de batalla anterior
        self.clear_battle_layout()

        # Obtener los nombres o números de los Pokémon
        poke1, ok1 = QInputDialog.getText(self, "Pokémon 1", "<span style='color:black;background-color:white;'>Ingrese el nombre o número del primer Pokémon:</span>")
        poke2, ok2 = QInputDialog.getText(self, "Pokémon 2", "<span style='color:black;background-color:white;'>Ingrese el nombre o número del segundo Pokémon:</span>")

        if not ok1 or not ok2:
            return

        # Obtener información de los Pokémon
        pokemon1 = get_specific_pokemon(poke1.strip().lower())
        pokemon2 = get_specific_pokemon(poke2.strip().lower())

        if not pokemon1 or not pokemon2:
            QMessageBox.warning(self, "Error", "No se pudo obtener información de uno o ambos Pokémon.")
            return

        # Mostrar imágenes de la batalla
        self.show_battle_images(pokemon1, pokemon2)

        # Determinar el ganador
        winner = self.determine_winner(pokemon1, pokemon2)
        self.show_winner(winner)

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

    def determine_winner(self, pokemon1, pokemon2):
        """
        Determina el ganador de la batalla basado en las estadísticas.
        """
        total_stats1 = sum(pokemon1["stats"].values())
        total_stats2 = sum(pokemon2["stats"].values())

        if total_stats1 > total_stats2:
            return pokemon1
        elif total_stats2 > total_stats1:
            return pokemon2
        else:
            return None  # Empate

    def show_winner(self, winner):
        """
        Muestra la imagen del Pokémon ganador.
        """
        if winner:
            pixmap = self.get_pixmap_from_url(winner["image_url"])
            self.image_label.setPixmap(pixmap)
            msg_box = QMessageBox(self)
            msg_box.setWindowTitle("Ganador")
            msg_box.setText(f"{winner['name'].capitalize()} gana la batalla!")
            msg_box.setStyleSheet("""
                background-color: red;
                color: white;
                border: 2px solid red;
            """)
            btn_ok = msg_box.addButton("Aceptar", QMessageBox.AcceptRole)
            btn_ok.setStyleSheet("background-color: black; color: white; border-radius: 5px; padding: 5px;")
            msg_box.exec_()
        else:
            msg_box = QMessageBox(self)
            msg_box.setWindowTitle("Empate")
            msg_box.setText(f"Termino la batalla en empate")
            msg_box.setStyleSheet("""
                background-color: red;
                color: white;
                border: 2px solid red;
            """)
            btn_ok = msg_box.addButton("Aceptar", QMessageBox.AcceptRole)
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
