import random

class Game_size:
    """
    Class to regulate the size of the game
    """
    def __init__(self, x_axis, y_axis, fleet_size):
        self.x_axis = x_axis
        self.y_axis = y_axis
        self.fleet_size = fleet_size

def generate_grid(x, y):
    """
    generates a list of lists based on x and y inputs.
    """
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
   

def add_ships(game_grid, ships):
    """
    Add ships to the grid. Randomly selects an index for the y axis and x axis and inserts an '0'
    """
    while ships > 0:
            random_x_axis = random.randint(0, size.x_axis-1)
            random_y_axis = random.randint(0, size.y_axis-1)
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

def enemy_shot(game_grid):
    random_x_axis = random.randint(0, size.x_axis-1)
    random_y_axis = random.randint(0, size.y_axis-1)
    received_fire = take_shot(game_grid, random_x_axis, random_y_axis)
    return received_fire
                 

def display_battlespace(side, grid):
    """
    Displays the game area in a viewer freindly format.
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

    print(f'{side} fleet')
    print(battlespace)
    return battlespace


def combat(fleet_size, enemy_ships, friendly_ships):
    """
    Loop for the main game
    """
    enemy_fleet_size = fleet_size
    friendly_fleet_size = fleet_size

    while enemy_fleet_size > 0 and friendly_fleet_size > 0:
        display_enemy = display_battlespace('Enemy', enemy_ships)
        display_friend = display_battlespace('Friendly', friendly_ships)

        """Player shot"""
        x = int(input('Please guess the x axis: '))
        y = int(input('Please guess the y axis: '))
        enemy_ships, freindly_fire = take_shot(enemy_ships, x, y)

        """Enemy shot"""
        friendly_ships, enemy_fire  = enemy_shot(friendly_ships)
    
        if freindly_fire is True and enemy_fire is True:
            enemy_fleet_size -=1
            friendly_fleet_size -=1
            print('\nYou hit, the enemy hit.')
        elif freindly_fire is True and enemy_fire is False:
            enemy_fleet_size -=1
            print('\nYou hit, the enemy missed.')
        elif freindly_fire is False and enemy_fire is True:
            print('\nYou missed, the enemy hit.')
            friendly_fleet_size -=1
        elif freindly_fire is False and enemy_fire is False:
            print('\nYou missed, the enemy missed.')

    return enemy_fleet_size, friendly_fleet_size

def choose_game(choice):
    """
    Function to select game size.
    """
    while choice > 3:
        print('Invalid choice. Please choose a number between 1 and 3.')
        choice = int(input('What size game would you like to play? '))

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
    else:
        print('error')
    return x_axis, y_axis, fleet_size

"""
Start of game here:
"""
print('Welcome to battleships. The game of daring combat on the high seas.')
print('Please select a game level to continue:')
print('\n1. Midshipman.\n2. Captain.\n3. Admiral.\n')
choice = int(input('What size game would you like to play? '))

x_axis, y_axis, fleet_size = choose_game(choice)
size = Game_size(x_axis, y_axis, fleet_size)

enemy_game_grid = generate_grid(size.x_axis, size.y_axis)
friendly_game_grid = generate_grid(size.x_axis, size.y_axis)
enemy_ships = add_ships(enemy_game_grid, size.fleet_size)
friendly_ships = add_ships(friendly_game_grid, size.fleet_size)

enemy_fleet_size, friendly_fleet_size = combat(size.fleet_size, enemy_ships, friendly_ships)
if enemy_fleet_size == 0 and friendly_fleet_size > 0:
    print('You won! You sunk the enemy fleet. Well done!')
elif enemy_fleet_size > 0 and friendly_fleet_size == 0:
    print('All your ships got sunk. You lost!')
elif enemy_fleet_size == 0 and friendly_fleet_size == 0:
    print('All the ships got sunk! Everyone loses!')