import sys
import random
import numpy as np


def game_loop(difficulty):
    game_values = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0])
    
    print("Instructions: When asked for input, write the number of the tile you want to mark. 1 is the top left tile, 2 is the top middle tile, 3 is the top right tile, 4 is the middle left tile, and so on.")
    
    while(True):
        render(game_values)
        if check_win(game_values):
            print("CPU victory!")
            break
        
        user_input = get_input(game_values)
        game_values[user_input] = 1
        print(game_values)
        render(game_values)
        if check_win(game_values):
            print("Player victory!")
            break
        
        cpu_input = get_cpu_input(game_values, difficulty)
        game_values[cpu_input] = 2
        print(game_values)
        
    print("The game has ended. To replay, rerun the script.")



def render(value_array):
    # Using a character array to make the input look like the classic circles and crosses people are used to.
    # This is technically not necessary, and you could get used to playing with just the number array, but it looks better.
    symbol_array = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
    for i in range(9):
        if value_array[i] == 0:
            symbol_array[i] = ' '
        elif value_array[i] == 1:
            symbol_array[i] = 'X'
        elif value_array[i] == 2:
            symbol_array[i] = 'O'
        else:
            print("Something has gone wrong and the array keeping track of the game has been messed up.")
            sys.exit("Encountered fatal error. Quitting.")
            
    # Printing the game board to the terminal.
    print("\nCurrent state of the game:")
    print(" {} | {} | {}".format(symbol_array[0], symbol_array[1], symbol_array[2]))
    print("---+---+---")
    print(" {} | {} | {}".format(symbol_array[3], symbol_array[4], symbol_array[5]))
    print("---+---+---")
    print(" {} | {} | {}\n".format(symbol_array[6], symbol_array[7], symbol_array[8]))
    
def get_input(values):
    choice = -1
    while(True):
        try:
            choice = int(input("Choose your tile: "))
            if choice == 0:
                sys.exit("Emergency brakes!")
            elif choice < 0 or choice > 9:
                print("Please make a valid choice (a number from 1 to 9).")
            else:
                if values[choice-1] != 0:
                    print("That tile is already marked.")
                else:
                    break
        except ValueError:
            print("Please make a valid choice (a number from 1 to 9).")
    return choice-1

def get_cpu_input(values, randomness):
    # Major TODO.
    print("CPU choosing tile.")
    
    # Random choice
    if(random.randint(0, 9) < randomness):
        while(True):
            choice = random.randint(0, 8)
            if values[choice] == 0:
                return choice
                
    # "Intelligent" choice
    else:
        return 4
    
def check_win(values):

    # Winning Tic-Tac-Toe is a matter of getting three equal symbols in a row. The possible tile combinations are
    # 1-2-3 (top row)
    # 1-4-7 (left column)
    # 1-5-9 (up-left diagonal)
    # 2-5-8 (middle column)
    # 3-5-7 (up-right diagonal)
    # 3-6-9 (right column)
    # 4-5-6 (middle row)
    # 7-8-9 (bottom row)
    # Since there are only 8 combinations, it's simplest to simply check them all.
    # With larger boards, a more sophisticated approach would be appropriate.
    
    if values[0] != 0:
        # 1-2-3 combination
        if(values[0] == values[1] and values[0] == values[2]):
            return True
        # 1-4-7 combination
        if(values[0] == values[3] and values[0] == values[6]):
            return True
        # 1-5-9 combination
        if(values[0] == values[4] and values[0] == values[8]):
            return True
            
    if values[1] != 0:
        # 2-5-8 combination
        if(values[1] == values[4] and values[1] == values[7]):
            return True
            
    if values[2] != 0:
        # 3-5-7 combination
        if(values[2] == values[4] and values[2] == values[6]):
            return True
        # 3-6-9 combination
        if(values[2] == values[5] and values[2] == values[8]):
            return True
    
    if values[3] != 0:
        # 4-5-6 combination
        if(values[3] == values[4] and values[3] == values[5]):
            return True
    
    if values[6] != 0:
        # 7-8-9 combination
        if(values[6] == values[7] and values[6] == values[8]):
            return True
    
    # Due to the transitive property (if a == b and a == c, then b == c),
    # we only have to include two of the three possible equality checks in the if statements.
    
    return False


if __name__ == "__main__":
    print("This is Terminal Tic-Tac-Toe.")
    difficulty = -1
    while(True):
        try:
            difficulty = int(input("First, specify the CPU's level of chaos (0 - Perfect, 10 - Random): "))
            break
        except ValueError:
            print("That's not a valid number.")
    
    
    if difficulty > 10:
        print("That number is too high. Defaulting to 10.")
        difficulty = 10
    elif difficulty < 0:
        print("That number is too low. Defaulting to 0.")
        difficulty = 0
    
    game_loop(difficulty)
    