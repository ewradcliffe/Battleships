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
                 

def display_battlespace(grid):
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

    return battlespace


game_grid = generate_grid(X_AXIS, Y_AXIS)

ships = add_ships(game_grid, fleet_size)

while fleet_size > 0:
    display = display_battlespace(ships)
    print(display)

    x = int(input('Please guess the x axis: '))
    y = int(input('Please guess the y axis: '))
    ships, outcome = take_shot(ships, x, y)
    if outcome == True:
        fleet_size -=1
        print('You hit')
    else:
        print('You missed')


