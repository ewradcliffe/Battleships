import random

"""
Global variables
"""

X_AXIS = 10	
Y_AXIS = 5
fleet_size = 3

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
            random_x_axis = random.randint(0, X_AXIS-1)
            random_y_axis = random.randint(0, Y_AXIS-1)
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
    random_x_axis = random.randint(0, X_AXIS-1)
    random_y_axis = random.randint(0, Y_AXIS-1)
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


enemy_game_grid = generate_grid(X_AXIS, Y_AXIS)
friendly_game_grid = generate_grid(X_AXIS, Y_AXIS)
enemy_ships = add_ships(enemy_game_grid, fleet_size)
friendly_ships = add_ships(friendly_game_grid, fleet_size)

while fleet_size > 0:
    """
    Basic game loop.
    """
    display_enemy = display_battlespace('Enemy', enemy_ships)
    display_friend = display_battlespace('Friendly', friendly_ships)

    """Player shot"""
    x = int(input('Please guess the x axis: '))
    y = int(input('Please guess the y axis: '))
    enemy_ships, freindly_fire = take_shot(enemy_ships, x, y)

    """Enemy shot"""
    friendly_ships, enemy_fire  = enemy_shot(friendly_ships)
  

    if freindly_fire is True and enemy_fire is True:
        fleet_size -=1
        print('\nYou hit, the enemy hit.')
    elif freindly_fire is True and enemy_fire is False:
        fleet_size -=1
        print('\nYou hit, the enemy missed.')
    elif freindly_fire is False and enemy_fire is True:
        print('\nYou missed, the enemy hit.')
    elif freindly_fire is False and enemy_fire is False:
        print('\nYou missed, the enemy missed.')


