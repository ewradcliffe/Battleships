import colorama
import os
import random
from colorama import Fore
colorama.init(autoreset=True)
"""
This piece of code is taken from the Colorama lesson by
Tech with Tim (https://www.youtube.com/watch?v=u51Zjlnui4Y)
"""


class GameSize:
    """
    Class to regulate the size of the game
    """
    def __init__(self, x_axis, y_axis, fleet_size):
        self.x_axis = x_axis
        self.y_axis = y_axis
        self.fleet_size = fleet_size

    def choose_game(choice):
        """
        Select game size.
        """
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
            y_axis = 5
            fleet_size = 5
        elif choice == 4:
            print('Thanks for playing. See you next time!')
            quit()

        return x_axis, y_axis, fleet_size

    def generate_grid(x, y):
        """
        Generates a list of lists based on x and y axis generated above.
        """
        y_axis = []
        i = 0
        while y > i:
            i += 1
            x_axis = []
            j = 0
            while x > j:
                x_axis.append(Fore.BLUE + '^')
                j += 1
            y_axis.append(x_axis)

        return y_axis

    def add_ships(game_grid, ships, x_axis, y_axis):
        """
        Add ships to the grid.
        Randomly selects an index for the y axis and x axis and inserts an '0'
        """
        while ships > 0:
            random_x_axis = random.randint(0, x_axis-1)
            random_y_axis = random.randint(0, y_axis-1)
            if game_grid[random_y_axis][random_x_axis] == Fore.WHITE + '0':
                continue
            else:
                game_grid[random_y_axis][random_x_axis] = Fore.WHITE + '0'
                ships -= 1

        return game_grid


def clear_screen():
    """
    Function to clear previous rounds from terminal.
    From https://stackoverflow.com/questions/2084508/
    clear-the-terminal-in-python
    """
    os.system("cls" if os.name == "nt" else "clear")


def player_shot(game_grid, x_axis, y_axis):
    """
    Function to resolve player shot.
    Asks player to guess coordinates of x an y axis.
    Also gives player opportunity to return to main menu.
    """
    invalid_guess = True
    while invalid_guess:
        x = input('Please guess the x axis: ')
        if x.lower() == 'm':
            main_game()

        y = input('Please guess the y axis: ')
        if y.lower() == 'm':
            main_game()

        """
        Clear screen in case invalid data is entered
        Needed to prevent errors in Heroku.
        """
        clear_screen()
        if x.isnumeric() and y.isnumeric():
            x = int(x)
            y = int(y)
            if x <= 0 or x > x_axis:
                print('X axis guess out of range.'
                      f' Please guess between 1 and {x_axis}.')
            elif y <= 0 or y > y_axis:
                print('Y axis guess out of range.'
                      f' Please guess between 1 and {y_axis}.')
            else:
                invalid_guess = False

        else:
            print('Guess must be a number.'
                  ' Not a letter or special character')

    """
    Takes player guess of x and y axis and deducts one
    to compare with index positions in list.
    """
    if game_grid[y-1][x-1] == Fore.WHITE + '0':
        game_grid[y-1][x-1] = Fore.RED + 'x'
        return game_grid, True
    else:
        game_grid[y-1][x-1] = Fore.WHITE + '.'
        return game_grid, False


def enemy_shot(game_grid, x_axis, y_axis):
    """
    Function for enemy shooting. Picks a grid square at random.
    """
    random_shot = True
    while random_shot:
        random_x_axis = random.randint(1, x_axis)
        random_y_axis = random.randint(1, y_axis)
        if game_grid[random_y_axis - 1][random_x_axis - 1] == Fore.WHITE + '0':
            game_grid[random_y_axis - 1][random_x_axis - 1] = Fore.RED + 'x'
            random_shot = False
            return game_grid, True
        elif game_grid[random_y_axis - 1][
                random_x_axis - 1] == Fore.BLUE + '^':
            game_grid[random_y_axis - 1][random_x_axis - 1] = Fore.WHITE + '.'
            random_shot = False
            return game_grid, False
        else:
            random_shot = True


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
    copy_enemy_ships = []

    for line in fleet:
        x = line.copy()
        copy_enemy_ships.append(x)

    for ship in copy_enemy_ships:
        index = 0
        for section in ship:
            if section == Fore.WHITE + '0':
                ship.remove(Fore.WHITE + '0')
                ship.insert(index, Fore.BLUE + '^')
            index += 1

    return copy_enemy_ships


def combat(fleet_size, enemy_ships, friendly_ships, x_axis, y_axis):
    """
    Function for resolving combat.
    Runs until one side looses all their ships.
    Starts by clearing menu from terminal.
    """
    clear_screen()

    enemy_fleet_size = fleet_size
    friendly_fleet_size = fleet_size

    while enemy_fleet_size > 0 and friendly_fleet_size > 0:
        hidden = hide_fleet(enemy_ships)
        hidden_enemy = display_battlespace(hidden)
        display_enemy = display_battlespace(enemy_ships)
        display_friend = display_battlespace(friendly_ships)

        print('To shoot, please enter coordinates.'
              f'\nPlease guess between 1 and {x_axis} '
              f'for the x axis, and 1 and {y_axis} for the y axis.\n'
              f'Or enter "M" to return to the Menu.\n')

        """
        Uncomment print statement below to print
        grid which displays enemy ship.
        print(display_enemy)
        """
        print('Enemy Fleet:')
        print(hidden_enemy)
        print('Friendly Fleet:')
        print(display_friend)

        """Player shot"""
        enemy_ships, friendly_fire = player_shot(enemy_ships, x_axis, y_axis)

        """Enemy shot"""
        friendly_ships, enemy_fire = enemy_shot(friendly_ships, x_axis, y_axis)

        """Clear previous rounds from terminal"""
        clear_screen()

        if friendly_fire is True and enemy_fire is True:
            enemy_fleet_size -= 1
            friendly_fleet_size -= 1
            print('You hit, the enemy hit.\n')
        elif friendly_fire is True and enemy_fire is False:
            enemy_fleet_size -= 1
            print('You hit, the enemy missed.\n')
        elif friendly_fire is False and enemy_fire is True:
            print('You missed, the enemy hit.\n')
            friendly_fleet_size -= 1
        elif friendly_fire is False and enemy_fire is False:
            print('You missed, the enemy missed.\n')

    return enemy_fleet_size, friendly_fleet_size


def main_game():
    """
    Function containing the game.
    Starts by clearing previous rounds from terminal.
    """
    clear_screen()

    play = True
    while play:
        print('Welcome to battleships.'
              ' The game of daring combat on the high seas.\n')
        print('Please select a game level to continue:')
        print('\n1. Midshipman.\n2. Captain.\n3. Admiral.\n4. Quit')

        invalid_input = True
        while invalid_input:
            choice = input('\nWhat size game would you like to play? ')
            try:
                choice = int(choice)
                if choice < 1 or choice > 4:
                    print('Invalid choice.'
                          ' Please choose a number between 1 and 4.')
                else:
                    invalid_input = False
            except ValueError:
                print('Error. Please enter a number.'
                      'Not a letter or special character')

        clear_screen()
        x_axis, y_axis, fleet_size = GameSize.choose_game(choice)

        """Generate a sea each for player and enemy"""
        enemy_sea = GameSize.generate_grid(x_axis, y_axis)
        friendly_sea = GameSize.generate_grid(x_axis, y_axis)

        """Add ships to player and enemy seas"""
        enemy_ships = GameSize.add_ships(enemy_sea, fleet_size, x_axis, y_axis)
        friendly_ships = GameSize.add_ships(
            friendly_sea, fleet_size, x_axis, y_axis)

        """Resolve combat"""
        enemy_fleet_size, friendly_fleet_size = combat(
                fleet_size, enemy_ships, friendly_ships, x_axis, y_axis)

        """Track combat. game ends when one player looses all their ships."""
        if enemy_fleet_size == 0 and friendly_fleet_size > 0:
            print('You won! You sunk the enemy fleet. Well done!')
        elif enemy_fleet_size > 0 and friendly_fleet_size == 0:
            print('All your ships got sunk. You lost!')
        elif enemy_fleet_size == 0 and friendly_fleet_size == 0:
            print('All the ships got sunk! Everyone loses!')

        """Check to see if player wants to play again"""
        play_again = input('\nPress any key to play again'
                           ' or enter "Q" to quit: ')
        if play_again.lower() == 'q':
            print("\nThanks for playing. Goodbye!")
            play = False


if __name__ == "__main__":
    """
    Start of game here:
    """
    main_game()
