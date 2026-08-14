"""Snake game built with Python and Curses Modules"""

import curses
import random
import atexit
import time


def get_initialize_colors():
    """Initialize colors for this game

    Returns
        colors [list] - A list of all the colors initialized
    """

    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLUE)
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_WHITE)

    green_black = curses.color_pair(1)
    white_blue = curses.color_pair(2)
    red_white = curses.color_pair(3)

    black = curses.COLOR_BLACK
    white = curses.COLOR_WHITE

    colors = {
        "Green_Black": green_black,
        "White_Blue": white_blue,
        "Red_White": red_white,
        "Black": black,
        "White": white,
    }

    return colors


def get_centered_position_x(screen_width, string_text):
    """Gets the value of the centered x-position of a string

    Arguments
        screen_width [int] - the width of the screen
        string_text [str] - the string used for the calculation of centered x-position

    Returns
        centered_position_x [window] - the calculated value of the centered x-position
    """

    centered_position_x = (screen_width - len(string_text)) // 2
    return centered_position_x


def show_game_over_display(game_screen_window, screen_width, game_score):
    """Displays the Game Over once the game conditions are met

    Arguments
        game_screen_window [window] - The initialized game screen window
        screen_width [int] - the width of the screen
        game_score [int] - Value of final game score

    Returns
        None
    """

    game_over_text = (
        f"Game Over. You're Score is {game_score}. (Press ENTER Key to try again)..."
    )

    game_screen_window.clear()
    game_screen_window.addstr(
        4,
        get_centered_position_x(screen_width, game_over_text),
        game_over_text,
        curses.A_BOLD | curses.A_STANDOUT,
    )
    game_screen_window.refresh()


def show_game_score_display(game_screen_window, screen_width, game_score):
    """Displays the Game Score

    Arguments
        game_screen_window [window] - The initialized game screen window
        screen_width [int] - the width of the screen
        game_score [int] - Value of final game score

    Returns
        None
    """

    game_score_text = f"GAME SCORE: {game_score} "

    game_screen_window.clear()
    game_screen_window.addstr(
        0,
        get_centered_position_x(screen_width, game_score_text),
        game_score_text,
        curses.A_BOLD,
    )
    game_screen_window.refresh()


def create_window(
    screen_height, screen_width, position_y, position_x, bg_color, border_color
):
    """Create New Window

    Arguments
        screen_height [int] - the height of the screen
        screen_width [int] - the width of the screen
        position_y [int] - the position of y (row)
        position_x [int] - the position of x (column)
        bg_color [str] - defined color for window background
        border_color [str] - defined color for window border

    Returns
        created_window [window] - the created new window
    """
    created_window = curses.newwin(screen_height, screen_width, position_y, position_x)
    created_window.bkgd(" ", bg_color)

    created_window.attron(border_color)
    created_window.border()
    created_window.attroff(border_color)

    return created_window


def show_header_screen_window(screen_height, screen_width, colors):
    """Displays the header screen window in the screen

    Arguments
        screen_height [int] - the height of the screen
        screen_width [int] - the width of the screen
        colors [list] - A list of all the colors initialized

    Returns
        None
    """

    header_height, header_width = (screen_height // 5), screen_width
    position_y, position_x = 0, 0

    # Create Header Window with its specifications
    header_screen_window = create_window(
        header_height,
        header_width,
        position_y,
        position_x,
        colors["White_Blue"],
        colors["White"],
    )

    # Define all the texts you want to display
    header_text_greeting = "Welcome to Snake Game using Curses Python Module"
    header_text_controller = (
        "Controllers: Up Arrow ↑, Down Arrow ↓, Left Arrow ←, Right Arrow →"
    )
    header_text_start_game = "Start Game: ENTER Key"
    header_text_quit_game = "Quit Game: Q or ESC Key"

    header_screen_window.addstr(
        1,
        get_centered_position_x(screen_width, header_text_greeting),
        header_text_greeting,
        curses.A_BOLD,
    )
    header_screen_window.addstr(
        2,
        get_centered_position_x(screen_width, header_text_controller),
        header_text_controller,
        curses.A_BOLD,
    )
    header_screen_window.addstr(
        3,
        get_centered_position_x(screen_width, header_text_start_game),
        header_text_start_game,
        curses.A_BOLD,
    )
    header_screen_window.addstr(
        4,
        get_centered_position_x(screen_width, header_text_quit_game),
        header_text_quit_game,
        curses.A_BOLD,
    )

    header_screen_window.refresh()


def start_snake_game(game_screen_window, screen_height, screen_width):
    """Starts the game

    Arguments
        game_screen_window [window] - The initialized game screen window
        screen_height [int] - the height of the screen
        screen_width [int] - the width of the screen
        colors [list] - A list of all the colors initialized
    Return
        None
    """

    # INITIALIZE SNAKE GAME VARIABLES
    # (Game Score, Character, Position, Movement Direction, Speed, Food, Food Position)

    # Initialize the starting 'GAME SCORE' and display at the center of the window
    game_score = 0
    show_game_score_display(game_screen_window, screen_width, game_score)

    # Initialize the random starting 'SNAKE POSITION' (tuple)
    snake_position = (
        screen_height // random.randint(2, 4),
        screen_width // random.randint(2, 4),
    )

    # Initialize the 'SNAKE CHARACTER' based on the initialize position (list of tuples)
    snake = [
        (snake_position[0], snake_position[1]),
        (snake_position[0], snake_position[1] - 1),
        (snake_position[0], snake_position[1] - 2),
    ]

    # Initialize the 'SNAKE HEAD'
    snake_head = (snake[0][0], snake[0][1])

    # Initialize the starting 'SNAKE MOVEMENT DIRECTION' (right)
    snake_direction = curses.KEY_RIGHT

    # Initialize the starting 'SNAKE SPEED'
    snake_speed = 100
    game_screen_window.timeout(snake_speed)

    # Initialize the random starting 'SNAKE FOOD POSITION' (tuple)
    snake_food = (
        screen_height // random.randint(2, 4),
        screen_width // random.randint(2, 4),
    )

    # Initialize the 'SNAKE FOOD' based on the initialize food position
    game_screen_window.addch(snake_food[0], snake_food[1], "0")

    # GAME LOOP EXECUTION
    # Loops until the snake hits a wall or its own body
    while True:

        # Create the Snake
        game_screen_window.addch(snake_head[0], snake_head[1], curses.ACS_BLOCK)

        # Break the Game Loop if the snake head collides with the wall or if it hits its body
        if (
            snake[0][0] in (0, screen_height)
            or snake[0][1] in (0, screen_width)
            or snake[0] in snake[1:]
        ):
            break

        # Capture User Key Pressed Value
        key_pressed = game_screen_window.getch()

        # Stops the game once 'Q' or 'ESC' is pressed
        if key_pressed in (ord("q"), ord("Q"), ord("\x1b"), 27):
            break

        if key_pressed != -1:
            snake_direction = key_pressed

        # Validate movement when Keypad Arrows are Pressed
        if snake_direction == curses.KEY_RIGHT or snake_direction == 454:
            snake_head = (snake[0][0], snake[0][1] + 1)

        elif snake_direction == curses.KEY_LEFT or snake_direction == 452:
            snake_head = (snake[0][0], snake[0][1] - 1)

        elif snake_direction == curses.KEY_UP or snake_direction == 450:
            snake_head = (snake[0][0] - 1, snake[0][1])

        elif snake_direction == curses.KEY_DOWN or snake_direction == 456:
            snake_head = (snake[0][0] + 1, snake[0][1])

        # Validate that new snake head is not equal to index 1 of snake
        if snake_head != snake[1]:
            # Insert new snake head at 0 index of snake
            snake.insert(0, snake_head)

        else:
            error_text = "Error: You cannot do reverse turns!"

            game_screen_window.clear()
            game_screen_window.addstr(
                4,
                get_centered_position_x(screen_width, error_text),
                error_text,
                curses.A_BOLD | curses.A_STANDOUT,
            )
            game_screen_window.refresh()

            time.sleep(2)
            break

        # Check if the SNAKE ate the SNAKE FOOD
        if snake[0] == snake_food:

            # Increase snake speed by 10%
            # game_screen_window.timeout(int(snake_speed * 0.10))

            # Increment the game score by 1
            game_score += 1
            show_game_score_display(game_screen_window, screen_width, game_score)

            # Remove Current SNAKE FOOD
            snake_food = None

            while snake_food is None:
                # Create New SNAKE FOOD
                new_snake_food = (
                    screen_height // random.randint(2, 4),
                    screen_width // random.randint(2, 4),
                )

                # Validate that the new snake food position is not hitting any part of the Snake
                if new_snake_food in snake:
                    new_snake_food = None

                else:
                    snake_food = new_snake_food

            # Display snake food based on the new food position
            game_screen_window.addch(snake_food[0], snake_food[1], "0")

        else:
            # Remove the tail or the last tuple in the snake
            tail = snake.pop()
            game_screen_window.addch(tail[0], tail[1], " ")

    # If game loop breaks, display game over
    show_game_over_display(game_screen_window, screen_width, game_score)


def end_program(game_screen_window, screen_width):
    """Displayed before the program is terminated

    Arguments
        typing_screen_window [window]: The initialized typing screen window
        screen_size [list]: A list of height and width of screen

    Returns
        None
    """

    ending_message_1 = "Thank you for trying this Snake Game"
    ending_message_2 = "This program will now end..."

    game_screen_window.clear()

    game_screen_window.addstr(
        4,
        get_centered_position_x(screen_width, ending_message_1),
        ending_message_1,
    )
    game_screen_window.addstr(
        6,
        get_centered_position_x(screen_width, ending_message_2),
        ending_message_2,
    )
    game_screen_window.refresh()

    time.sleep(2)


def main(stdscr):
    """Function where the snake game is called and run

    Arguments
        stdscr: The automatically initialized main window object of curses (stdscr).

    Returns
        None
    """
    # Initialize screen and set cursor visibility to hidden
    curses.initscr()
    curses.curs_set(0)

    # Turn off key echoing and enable cbreak mode for instant key processing
    curses.noecho()
    curses.cbreak()

    # Initialize clearing of the screen
    stdscr.clear()

    # Initialize colors
    colors = get_initialize_colors()

    # Initialize the screen height (rows) and screen width (columns)
    screen_height, screen_width = stdscr.getmaxyx()

    # Create a Header Screen Window
    show_header_screen_window(screen_height, screen_width, colors)

    # Create a Game Screen Window
    game_screen_height, game_screen_width = screen_height - 7, screen_width
    position_y, position_x = 7, 0

    game_screen_window = create_window(
        game_screen_height,
        game_screen_width,
        position_y,
        position_x,
        colors["Black"],
        colors["Black"],
    )

    # Enable keypad and specials keys capture and turn off input blocking
    game_screen_window.keypad(True)
    game_screen_window.nodelay(True)

    while True:
        key_pressed = game_screen_window.getch()

        if key_pressed in (ord("\n"), ord("\r"), curses.KEY_ENTER):
            game_screen_window.clear()

            start_snake_game(game_screen_window, screen_height, screen_width)
        elif key_pressed in (ord("q"), ord("Q"), ord("\x1b"), 27):
            break

    atexit.register(end_program, game_screen_window, screen_width)


if __name__ == "__main__":
    curses.wrapper(main)
