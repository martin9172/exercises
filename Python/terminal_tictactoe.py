"""
- Terminal Tic-Tac-Toe -

This is a Python script that contains a version of the classic pen-and-paper game Tic-Tac-Toe which can be played in the terminal.
This script provides a single-player experience.

(Full description here later)

TODOs and improvements/extensions:

# Implement rotation and mirroring during choice generation in a way that actually works!

# Links to read: 
    https://stackoverflow.com/questions/7466429/generate-a-list-of-all-unique-tic-tac-toe-boards 
    https://stackoverflow.com/questions/6160231/efficient-algorithm-for-counting-unique-states-of-tic-tac-toe

- Add pydocs to all functions.
- Make the game replayable without the script ending.
- Switch to a 2D array for the game grid.
- Change hardcoded functions to make them dynamic.
- Enable extra grid sizes (from 3x3 to 7x7 to start).
"""

import sys
import random
import pickle
import numpy as np



def initialize():
    # Function that loads the CPU's choices from a file.
    # If that fails, it instead generates the choices itself, and saves them to a file.
    smart_choice = {}
    
    try:
        smart_choice = pickle.load(open("choices3x3.pkl", "rb"))
        return smart_choice
    except FileNotFoundError:
        print("Failed to find choices3x3.pkl. Without it, the CPU won't know how to intelligently play the game. Generating the file now.")
    except:
        sys.exit("An unknown error has occurred while trying to initialize the CPU player. Quitting.")
    
    generate_choices(np.array([0, 0, 0, 0, 0, 0, 0, 0, 0]), smart_choice, 4)
    
    #print("\nThe dictionary has been created. Here it is:")
    #print(smart_choice)
    #print("\n")
    
    pickle.dump(smart_choice, open('choices3x3.pkl', 'wb'), pickle.HIGHEST_PROTOCOL)
    
    return smart_choice
    
    
def generate_choices(game_state, smart_choice, severity):
    # This recursive function tests every possible next CPU move. The recursion terminates when a win state, draw state or loss state is reached.
    # Each of these states are weighted with points, which is an integer which can be positive, zero or negative. Loss states have negative score.
    # Before recursion can occur, the function checks if the current state already exists in the smart_choice dictionary as a rotation or mirror.
    # This saves storage space. It calls itself 81 times, 9 times per player choice, in principle. However, it does check if each tile is actually
    # available, so it doesn't overwrite anything, and it obviously can't actually ever be called 81 times. (It's 72, then 42, then 30, then 6.) 
    # It also checks if the player wins if they choose that tile, and won't try to make its 9 choices in that case.
    
    # Check for win state (CPU win)
    if check_win(game_state):
        #print("+ + This resulted in a CPU win: {}".format(game_state))
        return 3 * 3**severity
    
    # Check for draw (will never happen in a 3x3 game, but is here in case of expansion
    if check_draw(game_state):
        #print("+ + This resulted in a draw.")
        return 0
    
    result_arr = np.array([-100000, -100000, -100000, -100000, -100000, -100000, -100000, -100000, -100000])
    
    for i in range(9):
        if game_state[i] != 0:
            continue
        
        new_state = np.copy(game_state)
        new_state[i] = 1    
        
        # Check for win state (player win)
        if check_win(new_state):
            #print("- - This resulted in a player win: {}".format(new_state))
            result_arr[i] = -5 * 3**severity
            continue
        
        # Check for draw state
        if check_draw(new_state):
            #print("- - This resulted in a draw.")
            result_arr[i] = 0
            continue
        
        choice_points = np.array([-100000, -100000, -100000, -100000, -100000, -100000, -100000, -100000, -100000])
        
        """
        # I should look into a better way to check these 8 mutations...
        if tuple(new_state) in smart_choice:
            #print("Debug: {} already exists in the dictionary.".format(new_state))
            continue
        elif tuple(rotate_array(new_state)) in smart_choice:
            #print("Debug: A version of {} already exists in the dictionary, as {}. (90 degree rotation)".format(new_state, rotate_array(new_state)))
            continue
        elif tuple(rotate_array(rotate_array(new_state))) in smart_choice:
            #print("Debug: A version of {} already exists in the dictionary, as {}. (180 degree rotation)".format(new_state, rotate_array(rotate_array(new_state))))
            continue
        elif tuple(rotate_array(rotate_array(rotate_array(new_state)))) in smart_choice:
            #print("Debug: A version of {} already exists in the dictionary, as {}. (270 degree rotation)".format(new_state, rotate_array(rotate_array(rotate_array(new_state)))))
            continue
        elif tuple(mirror_array(new_state)) in smart_choice:
            #print("Debug: A version of {} already exists in the dictionary, as {}. (Mirror)".format(new_state, mirror_array(new_state)))
            continue
        elif tuple(mirror_array(rotate_array(new_state))) in smart_choice:
            #print("Debug: A version of {} already exists in the dictionary, as {}. (Mirror, 90 degree rotation)".format(new_state, mirror_array(rotate_array(new_state))))
            continue
        elif tuple(mirror_array(rotate_array(rotate_array(new_state)))) in smart_choice:
            #print("Debug: A version of {} already exists in the dictionary, as {}. (Mirror, 180 degree rotation)".format(new_state, mirror_array(rotate_array(rotate_array(new_state)))))
            continue
        elif tuple(mirror_array(rotate_array(rotate_array(rotate_array(new_state))))) in smart_choice:
            #print("Debug: A version of {} already exists in the dictionary, as {}. (Mirror, 270 degree rotation)".format(new_state, mirror_array(rotate_array(rotate_array(rotate_array(new_state))))))
            continue
        else:
        """
        if(True):
        
            #print("Making choices for {}:".format(new_state))
        
            for j in range(9):
                if new_state[j] != 0:
                    continue
                
                copy_state = np.copy(new_state)
                copy_state[j] = 2
                
                #print("+ Checking choice of {}".format(copy_state))
                
                choice_points[j] = generate_choices(copy_state, smart_choice, severity-1)
        
        #print("* * * * The collected results for all CPU choices in {} are: {}".format(new_state, choice_points))
        
        results = np.argmax(choice_points)
        smart_choice[tuple(new_state)] = results
        #print("Debug: Added {} to the dictionary with tile choice {}. ({} points)".format(new_state, results, choice_points[results]))
        
        summary = 0
        for j in range(9):
            if choice_points[j] == -100000:
                continue
            summary += choice_points[j]
            
        result_arr[i] = summary
    
    #print("The collected results for all player choices in {} are: {}".format(game_state, result_arr))
    retval = 0
    for i in range(9):
        if result_arr[i] == -100000:
            continue
        retval += result_arr[i]
    
    #print("* The point sum for all the choices in {} is {}.".format(game_state, retval))
    return retval
    

def game_loop(difficulty, cpu_logic):
    game_values = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0])
    
    print("Instructions: When asked for input, write the number of the tile you want to mark. 1 is the top left tile, 2 is the top middle tile, 3 is the top right tile, 4 is the middle left tile, and so on.")
    
    while(True):
        render(game_values)
        if check_win(game_values):
            print("CPU victory!")
            break
        if check_draw(game_values):
            print("This game was a draw!")
            break
        
        user_input = get_input(game_values)
        game_values[user_input] = 1
        print(game_values)
        render(game_values)
        if check_win(game_values):
            print("Player victory!")
            break
        if check_draw(game_values):
            print("This game was a draw!")
            break
        
        cpu_input = get_cpu_input(game_values, difficulty, cpu_logic)
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

def get_cpu_input(values, randomness, cpu_logic):
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
        if tuple(values) in cpu_logic:
            return cpu_logic[tuple(values)]
        elif tuple(rotate_array(values)) in cpu_logic:
            return rotate_result(cpu_logic[tuple(rotate_array(values))])
        elif tuple(rotate_array(rotate_array(values))) in cpu_logic:
            return rotate_result(rotate_result(cpu_logic[tuple(rotate_array(rotate_array(values)))]))
        elif tuple(rotate_array(rotate_array(rotate_array(values)))) in cpu_logic:
            return rotate_result(rotate_result(rotate_result(cpu_logic[tuple(rotate_array(rotate_array(rotate_array(values))))])))
        elif tuple(mirror_array(values)) in cpu_logic:
            return mirror_result(cpu_logic[tuple(mirror_array(values))])
        elif tuple(mirror_array(rotate_array(values))) in cpu_logic:
            return mirror_result(rotate_result(cpu_logic[tuple(mirror_array(rotate_array(values)))]))
        elif tuple(mirror_array(rotate_array(rotate_array(values)))) in cpu_logic:
            return mirror_result(rotate_result(rotate_result(cpu_logic[tuple(mirror_array(rotate_array(rotate_array(values))))])))
        elif tuple(mirror_array(rotate_array(rotate_array(rotate_array(values))))) in cpu_logic:
            return mirror_result(rotate_result(rotate_result(rotate_result(cpu_logic[tuple(mirror_array(rotate_array(rotate_array(rotate_array(values)))))]))))
        
        # We should never get here.
        sys.exit("PANIC: This game state isn't known at all, so the CPU doesn't know what to do! Choice generation has gone wrong!")
        

def rotate_result(number):
    # Helper function that "rotates" the CPU tile choice counter-clockwise.
    if number == 0:
        return 6
    if number == 1:
        return 3
    if number == 2:
        return 0
    if number == 3:
        return 7
    if number == 4:
        return 4
    if number == 5:
        return 1
    if number == 6:
        return 8
    if number == 7:
        return 5
    if number == 8:
        return 2
    return -1

def mirror_result(number):
    # Helper function that "mirrors" the CPU tile choice horizontally.
    if number == 0:
        return 2
    if number == 1:
        return 1
    if number == 2:
        return 0
    if number == 3:
        return 5
    if number == 4:
        return 4
    if number == 5:
        return 3
    if number == 6:
        return 8
    if number == 7:
        return 7
    if number == 8:
        return 6
    return -1

def rotate_array(values):
    # Currently hardcoded, but should be possible to make dynamic for any "nxn" array.
    # This function rotates the grid 90 degrees clockwise.
    
    new_values = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0])
    
    new_values[0] = values[6]
    new_values[1] = values[3]
    new_values[2] = values[0]
    new_values[3] = values[7]
    new_values[4] = values[4]
    new_values[5] = values[1]
    new_values[6] = values[8]
    new_values[7] = values[5]
    new_values[8] = values[2]
    
    return new_values

def mirror_array(values):
    # Currently hardcoded, but should be possible to make dynamic for any "nxn" array.
    # This function mirrors the grid from left to right.
    
    new_values = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0])
    
    new_values[0] = values[2]
    new_values[1] = values[1]
    new_values[2] = values[0]
    new_values[3] = values[5]
    new_values[4] = values[4]
    new_values[5] = values[3]
    new_values[6] = values[8]
    new_values[7] = values[7]
    new_values[8] = values[6]
    
    return new_values






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
    
def check_draw(values):
    # This function simply checks if every tile is filled.
    # It is always called after the check_win function, so it doesn't have to check for any winning game states.
    
    draw = True
    
    for i in range(9):
        if values[i] == 0:
            draw = False
            break
            
    return draw


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
    
    cpu_choices = initialize()
    game_loop(difficulty, cpu_choices)
    