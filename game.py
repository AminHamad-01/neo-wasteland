import random

class Player:
    def __init__(self):
        self.health = 100
        self.energy = 100
        self.inventory = []
        self.credits = 50
        self.weapon = "Rusty Blade"

    def take_damage(self, amount):
        self.health = max(0, self.health - amount)
        return self.health > 0

    def use_energy(self, amount):
        if self.energy >= amount:
            self.energy -= amount
            return True
        return False

class Enemy:
    def __init__(self, name, health, damage):
        self.name = name
        self.health = health
        self.damage = damage

class Game:
    def __init__(self):
        self.player = Player()
        self.is_running = True
        self.enemies = [
            Enemy("Rogue Bot", 30, 10),
            Enemy("Cyber Ghoul", 40, 15),
            Enemy("Data Wraith", 25, 20)
        ]

    def game_loop(self):
        while self.is_running and self.player.health > 0:
            self.show_menu()
            choice = input("> ").lower()
            self.handle_input(choice)

    def show_menu(self):
        print("\n=== NEO-WASTELAND ===")
        print(f"Health: {self.player.health} | Energy: {self.player.energy} | Credits: {self.player.credits}")
        print("1. Explore")
        print("2. Check inventory")
        print("3. Rest (restore energy)")
        print("4. Status")
        print("q. Quit")

    def handle_input(self, choice):
        if choice == 'q':
            self.is_running = False
        elif choice == '1':
            self.explore()
        elif choice == '2':
            self.show_inventory()
        elif choice == '3':
            self.rest()
        elif choice == '4':
            self.show_status()

    def explore(self):
        if not self.player.use_energy(10):
            print("Too tired to explore. Rest first!")
            return
            
        if random.random() < 0.4:  # 40% chance of enemy encounter
            enemy = random.choice(self.enemies)
            self.combat(enemy)
        else:
            self.find_item()

    def combat(self, enemy):
        print(f"\nA {enemy.name} appears!")
        while enemy.health > 0 and self.player.health > 0:
            print(f"\nYour Health: {self.player.health} | Enemy Health: {enemy.health}")
            print("1. Attack")
            print("2. Run")
            choice = input("What will you do? > ")
            
            if choice == '1':
                damage = random.randint(15, 25)
                enemy.health -= damage
                print(f"You deal {damage} damage!")
                
                if enemy.health > 0:
                    if not self.player.take_damage(enemy.damage):
                        print("You have been defeated!")
                        return
                    print(f"Enemy hits you for {enemy.damage} damage!")
            elif choice == '2':
                if random.random() < 0.5:
                    print("You escaped!")
                    return
                print("Couldn't escape!")
                if not self.player.take_damage(enemy.damage):
                    print("You have been defeated!")
                    return
        
        if enemy.health <= 0:
            reward = random.randint(10, 30)
            self.player.credits += reward
            print(f"Victory! You earned {reward} credits!")

    def find_item(self):
        items = ["Med Kit", "Energy Cell", "Scrap Metal", "Data Crystal"]
        item = random.choice(items)
        self.player.inventory.append(item)
        print(f"You found: {item}")

    def show_inventory(self):
        print("\nInventory:")
        print(f"Weapon: {self.player.weapon}")
        for item in self.player.inventory:
            print(f"- {item}")

    def rest(self):
        if self.player.credits >= 10:
            self.player.credits -= 10
            self.player.energy = min(100, self.player.energy + 50)
            print("Rested. Energy restored.")
        else:
            print("Need 10 credits to rest!")

    def show_status(self):
        print(f"\nHealth: {self.player.health}")
        print(f"Energy: {self.player.energy}")
        print(f"Credits: {self.player.credits}")
        print(f"Current Weapon: {self.player.weapon}")

def main():
    game = Game()
    game.game_loop()

if __name__ == "__main__":
    main()