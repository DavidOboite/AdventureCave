import random
import sys

# Read files for game
def load_file(filename):
    data = []

    with open(filename,'r') as file:
        for line in file:
            line = line.strip()

            if line:
                data.append(line)

    return data
# Read hero party file
def load_party(filename):

    party = []

    with open(filename,'r') as file:
        for line in file:
            line = line.strip()
            if line:
                name, health, damage = line.split(',')
                party.append((name,int(health),int(damage)))
    return party

# Load Party files for game
def play_game(party_file):

    rooms = load_file('rooms.txt')
    monsters = load_file('monsters.txt')
    treasures = load_file('treasure.txt')

    print(f'Loading player data from {party_file}...')

    party = load_party(party_file)
    print('\n choose your hero: \n')

    for i, hero in enumerate(party, start = 1):
        print(f'{i}. {hero[0]}: {hero[1]}')
    while True:
        try:
            hero_choice = int(input('\n Choose your hero: '))

            if 1 <= hero_choice <= len(party):
                break
            else:
                print("Choose a valid hero number.")
        except ValueError:
            print("Numbers for hero index....Type 1,2,3, or 4.")

    selected = party[hero_choice -1]
    hero_name = selected[0]
    health =selected[1]
    bonus_damage = selected[2]

    print(f'\n You chose {hero_name} with {health} health and {bonus_damage} damage.')


# Set player stats and create empty inventory
    gold = 0
    inventory = []
# Player chicken meter
    exit_count = 0

# welcome player ask player if they would like to explore
    while True:
        choice = input('Welcome to Treasure Cave! Do you want to explore? (yes/no): ').lower()

        if choice == "yes":
            break

        elif choice == "no":
                print( "You likely chicken, come back when you brave enough!")
                return

        else: print("Please type yes or no only." )
# player explores or skips rooms in cave
    skip_room = False

    for room in rooms:

        print(f'\n You enter {room}')

        while True:
            choice = input("Explore this room? (yes/exit): ").lower()

            if choice == "yes":
                break
            elif choice == "exit":
                exit_count += 1
                print("You chickened out.")

                skip_room = True

                if exit_count >= 3:
                    while True:
                        quit_game = input("Do you want to quit the game? (yes/no): ").lower()

                        if quit_game == "yes":
                            print("Thank you for playing...Leaving game now")
                            return
                        elif quit_game == "no":
                            exit_count = 0
                            break
                        else: print("Please type yes or no only.")
                break
            else:
                print("Please type yes or exit only.")
        # Check if player skipped cave
        if  skip_room:
                skip_room = False
                continue

# Randomly select and generate cave events
        event = random.randint(1,3)

        if event == 1:
            monster = random.choice(monsters)

            print(f'A {monster} attacks!')

            damage = random.randint(5,20)
            damage = damage - ( bonus_damage // 5 )

            if damage < 1:
                damage = 1

            health -= damage

            print(f'You lose {damage} health.')

            if health <= 0:
                print('You died!')
                break

        elif event == 2:

            treasure = random.choice(treasures)

            inventory.append(treasure)

            found_gold = random.randint( 10, 50)

            gold += found_gold
            print(f'You found {treasure}')
            print(f'You found {found_gold} gold')

        else: print('Nothing happens.')

        print(f'Health: {health}')

        print( f'Gold: {gold}')


    if health > 0:
        print('\n Hooray!, You survived the Treasure Cave ALIVE!')
    else:
        print('\n GAME OVER')

    with open('savegame.txt', 'w') as save:

        save.write( f'Hero:{hero_name}\n')

        save.write(f'Gold:{gold}\n')

        save.write(f'Health:{health}\n')

        for item in inventory:
            save.write(f'Item:{item}\n')

    print('Game saved.')

if __name__ == '__main__':
    try:
        party_file = sys.argv[1]
        play_game(party_file)
    except IndexError:
        print('Missing party file')
    except FileNotFoundError:
        print('Something unexpected happened while running the game, please try again later.')