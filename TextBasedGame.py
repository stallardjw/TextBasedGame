import random

# TextBasedGame.py
# Jonathan Stallard
# December 2024

# Room and Item Setup
rooms = {
    "Crash Site": {"east": "Cryo Chamber", "item": None},
    "Observation Deck": {"south": "Cryo Chamber", "item": "Stellar Core"},
    "Cryo Chamber": {"north": "Observation Deck", "west": "Crash Site", "east": "Control Room", "south": "Botanical Lab", "item": "Frozen Relic"},
    "Control Room": {"west": "Cryo Chamber", "south": "Data Core", "item": "Holo-Key"},
    "Botanical Lab": {"north": "Cryo Chamber", "south": "Generator Room", "item": "Bioluminescent Orb"},
    "Data Core": {"north": "Control Room", "south": "AI Chamber", "item": "Quantum Chip"},
    "Generator Room": {"north": "Botanical Lab", "east": "AI Chamber", "item": "Plasma Cell"},
    "AI Chamber": {"west": "Generator Room", "north": "Data Core", "item": None},  # Villain's room
}

# Puzzle Bank
puzzle_bank = [
    {"question": "What is the capital city of France?", "answer": "paris"},
    {"question": "What is the largest mammal in the world?", "answer": "blue whale"},
    {"question": "How many continents are there on Earth?", "answer": "7"},
    {"question": "What is the chemical symbol for water?", "answer": "h2o"},
    {"question": "Which planet is known as the Red Planet?", "answer": "mars"},
    {"question": "Who painted the Mona Lisa?", "answer": "leonardo da vinci"},
    {"question": "What is the smallest prime number?", "answer": "2"},
    {"question": "What is the fastest land animal?", "answer": "cheetah"},
    {"question": "How many colors are there in a rainbow?", "answer": "7"},
    {"question": "Which ocean is the largest?", "answer": "pacific"},
    {"question": "What comes next in the sequence: 2, 4, 8, 16, ...?", "answer": "32"},
    {"question": "If you multiply me by any number, the result is always the same. What am I?", "answer": "0"},
    {"question": "I am not alive but I grow. I have no lungs, but I need air. What am I?", "answer": "fire"},
    {"question": "The more you take away from me, the bigger I get. What am I?", "answer": "hole"},
    {"question": "I speak without a mouth and hear without ears. I have no body, but I come alive with wind. What am I?", "answer": "echo"},
    {"question": "What has keys but can't open locks?", "answer": "piano"},
    {"question": "What has to be broken before you can use it?", "answer": "egg"},
    {"question": "I’m tall when I’m young, and I’m short when I’m old. What am I?", "answer": "candle"},
    {"question": "What has one eye but can’t see?", "answer": "needle"},
    {"question": "What can you hold in your left hand but not in your right?", "answer": "your right hand"},
]
random.shuffle(puzzle_bank)  # Shuffle puzzles for random assignment to rooms


# Game State
current_room = "Crash Site"
inventory = []
puzzle_index = 0  


# Functions

def assign_puzzles():
    """
    Assign puzzles sequentially from the shuffled puzzle bank to rooms with items.
    """
    global puzzle_index
    for room, details in rooms.items():
        if details.get("item"):
            rooms[room]["puzzle"] = puzzle_bank[puzzle_index]
            puzzle_index = (puzzle_index + 1) % len(puzzle_bank)  # Cycle through puzzles


def show_instructions():
    """
    Display the game's objective and available commands.
    """
    print("\nWelcome to 'Lost in the Celestial Labyrinth'!")
    print("Objective: Solve puzzles and collect all 6 energy cores to power your escape pod.")
    print("Avoid Eris, the rogue AI Sentinel, until you have all cores.")
    print("\nCommands:")
    print("- Move: 'go [direction]' (north, south, east, west)")
    print("- Collect an item: 'get [item]' ")
    print("- Quit the game: 'exit'\n")


def show_status():
    """
    Display the player's current status, including their location, inventory, and items in the room.
    """
    print(f"\nYou are in the {current_room}.")
    print(f"Inventory: {inventory}")
    item = rooms[current_room].get("item")
    if item:
        print(f"You see a {item}.")
    print("-" * 30)


def solve_puzzle(room):
    """
    Handle puzzle-solving for the current room.
    """
    puzzle = rooms[room].get("puzzle")
    if not puzzle:
        return True  # No puzzle in this room

    print(f"\nTo collect the item, solve this puzzle:\n{puzzle['question']}")
    print("Type 'exit' to leave the puzzle.")
    attempts = 0

    while True:
        answer = input("Your answer: ").strip().lower()
        if answer == puzzle["answer"].lower():
            print("Correct! You can now collect the item.")
            return True
        elif answer == "exit":
            print("You have exited the puzzle. The item remains in the room.")
            return False
        else:
            print("Incorrect.")
            attempts += 1
            if attempts >= 3:
                if input("Would you like a new question? (yes/no): ").strip().lower() == "yes":
                    global puzzle_index
                    puzzle = puzzle_bank[puzzle_index]
                    puzzle_index = (puzzle_index + 1) % len(puzzle_bank)  # Cycle through puzzles
                    rooms[room]["puzzle"] = puzzle
                    print(f"New puzzle: {puzzle['question']}")
                    attempts = 0


def main():
    """
    Main function to handle the game loop, player actions, and win/lose conditions.
    """
    global current_room, inventory

    assign_puzzles()
    show_instructions()

    while True:
        show_status()
        action = input("Enter your move: ").strip().lower()

        if action == "exit":
            print("\nYou have exited the game. Thanks for playing!")
            break
        elif action.startswith("go "):
            direction = action.split(" ")[1]
            if direction in rooms[current_room]:
                current_room = rooms[current_room][direction]
            else:
                print("You can't go that way!")
        elif action.startswith("get "):
            item = rooms[current_room].get("item")
            if item and action == f"get {item.lower()}":
                if solve_puzzle(current_room):
                    inventory.append(item)
                    rooms[current_room]["item"] = None
                    print(f"You collected the {item}.")
                else:
                    print("You must solve the puzzle to collect the item!")
            else:
                print("There is no such item to collect here.")
        else:
            print("Invalid command. Please try again.")

        if current_room == "AI Chamber":
            if len(inventory) == 6:
                print("\nCongratulations! You've collected all energy cores and powered your escape pod!")
                print("You successfully escaped the Celestial Labyrinth!")
            else:
                print("\nEris, the rogue AI Sentinel, captures you!")
                print("NOM NOM...GAME OVER!")
            break


# Start the game
if __name__ == "__main__":
    main()
