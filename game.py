class Player:
    def __init__(self):
        self.health = 100
        self.inventory = []

class Game:
    def __init__(self):
        self.player = Player()
        self.is_running = True

    def game_loop(self):
        while self.is_running:
            self.show_menu()
            choice = input("> ").lower()
            self.handle_input(choice)

    def show_menu(self):
        print("\n=== NEO-WASTELAND ===")
        print("1. Look around")
        print("2. Check inventory")
        print("3. Check health")
        print("q. Quit")

    def handle_input(self, choice):
        if choice == 'q':
            self.is_running = False
        elif choice == '1':
            print("You see a desolate wasteland...")
        elif choice == '2':
            print(f"Inventory: {self.player.inventory}")
        elif choice == '3':
            print(f"Health: {self.player.health}")

def main():
    game = Game()
    game.game_loop()

if __name__ == "__main__":
    main()