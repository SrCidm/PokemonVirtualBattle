# Pokémon Battle Simulator

Welcome to the **Pokémon Battle Simulator**! This project uses **PyQt5** to create a graphical user interface (GUI) that allows you to search for Pokémon, view their stats, and simulate battles between two Pokémon. The application leverages the [PokéAPI](https://pokeapi.co/) to fetch Pokémon data and provides a fun and interactive way to explore the Pokémon universe.

---

## Features

- **Pokémon Search**: Enter the name or number of a Pokémon to retrieve detailed information, including its types, abilities, stats, and an image.
- **Battle Simulation**: Simulate turn-based battles between two Pokémon. The app calculates damage based on types, moves, and stats.
- **Interactive GUI**: A user-friendly interface designed with a Pokédex theme.
- **Asynchronous Moves Fetching**: Efficiently retrieves Pokémon moves using asynchronous requests.

---

## Requirements

To run this application, you need:

- **Python 3.7 or higher**.
- The following Python libraries:
  - `requests`
  - `PyQt5`
  - `aiohttp`
  - `asyncio`

You can install the dependencies by running:

```bash
pip install requests PyQt5 aiohttp
```
## Installation
1. Clone this repository:

```bash
git clone https://github.com/your-username/pokemon-battle-simulator.git
```
2. Navigate to the project directory:

```bash
cd pokemon-battle-simulator
```
3. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Run the script pokemonInfopyQt5Deep.py to start the application:

```bash
python pokemonInfopyQt5Deep.py
```

## How to Use the App
1. Search for a Pokémon:

    Enter the name or number of a Pokémon in the search bar.

    Click "Find Pokemon" to view its details, including stats, types, abilities, and an image.

2. Simulate a Battle:

    Click the "Virtual Battle" button.

    Enter the names or numbers of two Pokémon.

    Watch the battle unfold in a turn-based simulation, complete with    damage calculations and a battle log.

## Code Structure
    The project is organized as follows:

    get_specific_pokemon(identifier): Fetches detailed information about a specific Pokémon by name or number.

    get_pokemon_moves(identifier): Retrieves a list of moves for a Pokémon, filtering out moves without power.

    get_move_power(move_name): Fetches the power of a specific move from the API.

    PokedexApp: The main class that handles the GUI and application logic.

    simulate_battle(): Simulates a battle between two Pokémon.

    calculate_damage(attacker, defender, move): Calculates the damage of a move based on types and stats.

## Contributing
    Contributions are welcome! If you find any bugs or have suggestions for improvements, please open an issue or submit a pull request.

    Fork the repository.

    Create a new branch for your feature or bugfix.

    Commit your changes and push them to your fork.

    Open a pull request with a detailed description of your changes.

## License
    This project is licensed under the MIT License. See the LICENSE file for more details.

## Contact
    For any questions or feedback, feel free to reach out:

    Email: sergio.g.cid.m@gmail.com