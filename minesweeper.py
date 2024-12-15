import os
from model.game_model import GameModel
from controller.game_controller import GameController
from view.gui_view import GUIView
from view.text_view import TextView
from tkinter import Tk
from test_validator import TestValidator

os.environ['TK_SILENCE_DEPRECATION'] = '1'

def main():
    """
    Main function to initialize and start the Minesweeper game.
    
    Precondition:
        - All required modules must be imported
        - All required files must be in correct directories
    Postcondition:
        - Game is initialized with user-selected settings
        - Appropriate view and controller are created
        - Game starts in selected mode
    Invariant:
        - Game configuration remains consistent with user selections
        - Test mode and difficulty settings are mutually exclusive
    
    Maps to: main() and __init__ setup in original minesweeper.py
    """
    # Ask if user wants to enter testing mode with test board validation
    while True:
        print("Would you like to enter testing mode? (yes/no)")
        user_input = input().strip().lower()
        if user_input in ['yes', 'no']:
            testing_mode = (user_input == 'yes')
            break
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")

    if not testing_mode:
        print("You have selected normal mode of the game.")

    test_board = None
    if testing_mode:
        while test_board is None:
            print("Enter test board filename (CSV format):")
            filename = input().strip()
            test_board = TestValidator.read_test_board(filename)
            if test_board is None:
                while True:
                    print("Would you like to try another file? (yes/no)")
                    retry_input = input().strip().lower()
                    if retry_input in ['yes', 'no']:
                        retry = (retry_input == 'yes')
                        break
                    else:
                        print("Invalid input. Please enter 'yes' or 'no'.")
                if not retry:
                    testing_mode = False
                    print("Exiting testing mode. You are now in normal mode of the game.")
                    break
            else:
                while True:
                    print("Would you like to play with this board layout? (yes/no)")
                    play_input = input().strip().lower()
                    if play_input in ['yes', 'no']:
                        play = (play_input == 'yes')
                        break
                    else:
                        print("Invalid input. Please enter 'yes' or 'no'.")
                if not play:
                    print("Exiting testing mode. You are now in normal mode of the game.")
                    testing_mode = False
                    break

    if testing_mode and test_board:
        game_model = GameModel("beginner")
        game_model.initialize_test_board(test_board)
    else:
        print("Select difficulty:")
        print("1. Beginner\t\t2. Intermediate\t\t3. Expert")
        difficulty_map = {
            '1': 'beginner',
            '2': 'intermediate',
            '3': 'expert'
        }
        while True:
            difficulty_level = input("Enter difficulty (1/2/3): ").strip()
            if difficulty_level in difficulty_map:
                difficulty = difficulty_map[difficulty_level]
                break
            else:
                print("Invalid input. Please enter '1', '2', or '3'.")
        game_model = GameModel(difficulty)
        game_model.initialize_board()

    print("Select game mode:")
    print("1. GUI")
    print("2. Text")
    while True:
        mode = input("Enter mode (1/2): ").strip()
        if mode in ['1', '2']:
            break
        else:
            print("Invalid input. Please enter '1' for GUI or '2' for Text mode.")

    if mode == '1':
        tk = Tk()
        tk.title("Minesweeper")
        controller = GameController(game_model, None, test_board, testing_mode)
        gui_view = GUIView(tk, game_model, controller)
        controller.view = gui_view
        tk.mainloop()
    elif mode == '2':
        controller = GameController(game_model, None, test_board, testing_mode)
        text_view = TextView(game_model, controller)
        controller.view = text_view
        text_view.run()
    else:
        print("Invalid mode! Exiting game.")
        exit()

if __name__ == "__main__":
    main()