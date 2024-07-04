import random

class GameSize:
    """
    Class to regulate the size of the game
    """
    def __init__(self, x_axis, y_axis, fleet_size):
        self.x_axis = x_axis
        self.y_axis = y_axis
        self.fleet_size = fleet_size

    """
    Function to select game size.
    """
    def choose_game(choice):

        if choice == 1:
            x_axis = 5
            y_axis = 3
            fleet_size = 1 
        elif choice == 2:
            x_axis = 10
            y_axis = 5
            fleet_size = 3 
        elif choice == 3:
            x_axis = 20
            y_axis = 10
            fleet_size = 5
        elif choice == 4:
            print('Thanks for playing. See you next time!')
            quit()
            
        return x_axis, y_axis, fleet_size

    """
    Generates a list of lists based on x and y axis generated above.
    """
    def generate_grid(x, y):

        y_axis = []
        i = 0
        while y > i:
            i +=1
            x_axis = []
            j = 0
            while x > j:
                x_axis.append('^')
                j +=1
            y_axis.append(x_axis)

        return y_axis

    """
    Add ships to the grid. Randomly selects an index for the y axis and x axis and inserts an '0'
    """
    def add_ships(game_grid, ships, x_axis, y_axis):

        while ships > 0:
                random_x_axis = random.randint(0, x_axis-1)
                random_y_axis = random.randint(0, y_axis-1)
                if game_grid[random_y_axis][random_x_axis] == '0':
                    continue
                else:
                    game_grid[random_y_axis][random_x_axis] = '0'
                    ships -= 1

        return game_grid


def take_shot(game_grid, x, y):
    """
    Function to resolve player shot. 
    Takes player guess of x and y axis and compares them with the grid.
    """

    if game_grid[y-1][x-1] == '0':
        game_grid[y-1][x-1] = 'x'
        return game_grid, True
    else:
        game_grid[y-1][x-1] = '.'
        return game_grid, False


def enemy_shot(game_grid, x_axis, y_axis):
    """
    Function for enemy shooting. Picks a grid square at random.
    """
    random_x_axis = random.randint(0, x_axis-1)
    random_y_axis = random.randint(0, y_axis-1)
    received_fire = take_shot(game_grid, random_x_axis, random_y_axis)
    return received_fire
                 

def display_battlespace(grid):
    """
    Displays the game area in a viewer friendly format.
    Adds a newline if not present
    Extracts lists and concatinates them together in a string.
    """
    battlespace = ''
    for item in grid:
        if '\n' not in item:
            item.append('\n')

    for part in grid:
        for wave in part:
            battlespace = battlespace + wave

    return battlespace

def hide_fleet(fleet):
    """
    Hides the ships on the enemy grid.
    """
    copy_enemy_ships =[]

    for line in fleet:
            x = line.copy()
            copy_enemy_ships.append(x)
    
    for ship in copy_enemy_ships:
        for section in ship:
            x = 0
            if section == '0':
                ship.remove('0')
                ship.insert(x, '^')
                x += 1
   
    return copy_enemy_ships

def combat(fleet_size, enemy_ships, friendly_ships, x_axis, y_axis):
    """
    Loop for the main game
    """
    enemy_fleet_size = fleet_size
    friendly_fleet_size = fleet_size

    while enemy_fleet_size > 0 and friendly_fleet_size > 0:
        hidden = hide_fleet(enemy_ships)
        hidden_enemy = display_battlespace(hidden)
        display_enemy = display_battlespace(enemy_ships)
        
        display_friend = display_battlespace(friendly_ships)

        """
        Uncomment the print statement below to see where the enemy ships are located.
        print(display_enemy)
        """
        print(display_enemy)
        print('Enemy Fleet:')
        print(hidden_enemy)
        print('Friendly Fleet:')
        print(display_friend)

        """Player shot"""
        player_shot_valid = False
        while player_shot_valid == False:
            x = input('Please guess the x axis: ')
            y = input('Please guess the y axis: ')
            if x.isnumeric() and y.isnumeric():
                x = int(x)
                y =int(y)
                if x <= 0 or x > x_axis:
                    print(f'X axis guess out of range. Please guess between 1 and {x_axis}.')
                elif y <= 0 or y > y_axis:
                    print(f'Y axis guess out of range. Please guess between 1 and {y_axis}.')
                else:
                    player_shot_valid = True
            else:
                print('Guess must be a number. Not a letter or special character')


        enemy_ships, friendly_fire = take_shot(enemy_ships, x, y)

        """Enemy shot"""
        friendly_ships, enemy_fire  = enemy_shot(friendly_ships, x_axis, y_axis)
    
        if friendly_fire is True and enemy_fire is True:
            enemy_fleet_size -=1
            friendly_fleet_size -=1
            print('\nYou hit, the enemy hit.')
        elif friendly_fire is True and enemy_fire is False:
            enemy_fleet_size -=1
            print('\nYou hit, the enemy missed.')
        elif friendly_fire is False and enemy_fire is True:
            print('\nYou missed, the enemy hit.')
            friendly_fleet_size -=1
        elif friendly_fire is False and enemy_fire is False:
            print('\nYou missed, the enemy missed.')

    return enemy_fleet_size, friendly_fleet_size

def main_game():
    play = True
    while play:
        print("Welcome to battleships. The game of daring combat on the high seas.\n")
        print('Please select a game level to continue:')
        print('\n1. Midshipman.\n2. Captain.\n3. Admiral.\n4. Quit')

        game_selection = False
        while game_selection == False:
            choice = input('\nWhat size game would you like to play? ')
            if choice.isnumeric():
                choice = int(choice)
                if choice < 1 or choice > 4:
                    print('Invalid choice. Please choose a number between 1 and 4.')
                else:
                    game_selection = True
            else:
                    print('Error. Please enter a number')

        x_axis, y_axis, fleet_size = GameSize.choose_game(choice)
        print(f'\nTo shoot, please enter coordinates.\n\nPlease guess between 1 and {x_axis} for the x axis, and 1 and {y_axis} for the y axis.\n')
                    
        """Generate a sea each for player and enemy"""
        enemy_sea = GameSize.generate_grid(x_axis, y_axis)
        friendly_sea = GameSize.generate_grid(x_axis, y_axis)

        """Add ships to player and enemy seas"""
        enemy_ships = GameSize.add_ships(enemy_sea, fleet_size, x_axis, y_axis)
        friendly_ships = GameSize.add_ships(friendly_sea, fleet_size, x_axis, y_axis)

        """Resolve combat"""
        enemy_fleet_size, friendly_fleet_size = combat(fleet_size, enemy_ships, friendly_ships, x_axis, y_axis)

        """Track combat. game ends when one player looses all their ships."""       
        if enemy_fleet_size == 0 and friendly_fleet_size > 0:
            print('You won! You sunk the enemy fleet. Well done!')
        elif enemy_fleet_size > 0 and friendly_fleet_size == 0:
            print('All your ships got sunk. You lost!')
        elif enemy_fleet_size == 0 and friendly_fleet_size == 0:
            print('All the ships got sunk! Everyone loses!')

        """Check to see if player wants to play again"""
        play_again = input("\nPress any key to play again, or enter 'Q' to quit: ")
        if play_again.lower() == 'q':
            print("\nThanks for playing. Goodbye!")
            play = False       

"""
Start of game here:
"""
main_game()


