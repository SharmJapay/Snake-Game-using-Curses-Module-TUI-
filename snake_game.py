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
    curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_GREEN)

    green_black = curses.color_pair(1)
    white_blue = curses.color_pair(2)
    red_white = curses.color_pair(3)
    black_green = curses.color_pair(4)

    black = curses.COLOR_BLACK
    white = curses.COLOR_WHITE

    colors = {
        "Green_Black": green_black,
        "White_Blue": white_blue,
        "Red_White": red_white,
        "Black_Green": black_green,
        "Black": black,
        "White": white,
    }

    return colors


def get_centered_x_position(screen_width, string_text):
    """Gets the value of the centered x-position of a string

    Arguments
        screen_width [int] - the width of the screen
        string_text [str] - the string used for the calculation of centered x-position

    Returns
        centered_x_position [int] - the calculated value of the centered x-position
    """

    centered_x_position = (screen_width - len(string_text)) // 2

    return centered_x_position


def display_game_over(game_screen_window, screen_width, game_score):
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
    x_position = max(0, get_centered_x_position(screen_width, game_over_text))

    try:
        game_screen_window.clear()
        game_screen_window.addstr(4, x_position, game_over_text, curses.A_BOLD)
        game_screen_window.refresh()
    except curses.error:
        pass


def display_game_score(game_screen_window, screen_width, game_score, colors):
    """Displays the Game Score

    Arguments
        game_screen_window [window] - The initialized game screen window
        screen_width [int] - the width of the screen
        game_score [int] - Value of final game score
        colors [list] - A list of all the colors initialized

    Returns
        None
    """

    game_score_text = f"GAME SCORE: {game_score} "
    x_position = max(0, get_centered_x_position(screen_width, game_score_text))

    try:
        # Move to row 0 and erase only that row's contents
        game_screen_window.move(0, 0)
        game_screen_window.clrtoeol()
        game_screen_window.addstr(0, x_position, game_score_text, colors["Black_Green"])
        game_screen_window.refresh()
    except curses.error:
        pass


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


def create_header_screen_window(screen_width, colors):
    """Create the header screen window in the screen

    Arguments
        screen_width [int] - the width of the screen
        colors [list] - A list of all the colors initialized

    Returns
        header_screen_window [window] - the initialized header screen window created
    """

    header_height, header_width = 7, screen_width
    position_y, position_x = 0, 0
    bg_color, border_color = colors["White_Blue"], colors["White"]

    # Create Header Window with its specifications
    header_screen_window = create_window(
        header_height,
        header_width,
        position_y,
        position_x,
        bg_color,
        border_color,
    )

    # Define all the texts you want to display
    header_text_greeting = "Welcome to Snake Game using Curses Python Module"
    header_text_controller = "(Controllers) : Up ↑, Down ↓, Left ←, Right →"
    header_text_start_game = "(Start Game) : ENTER Key"
    header_text_quit_game = "(Quit Game) : Q or ESC Key"

    header_text_list = [
        header_text_greeting,
        header_text_controller,
        header_text_start_game,
        header_text_quit_game,
    ]

    for index, text in enumerate(header_text_list):
        header_screen_window.addstr(
            index + 1,
            get_centered_x_position(screen_width, text),
            text,
            curses.A_BOLD,
        )

    return header_screen_window


def create_game_screen_window(screen_height, screen_width, colors):
    """Create the game screen window in the screen

    Arguments
        screen_height [int] - the height of the screen
        screen_width [int] - the width of the screen
        colors [list] - A list of all the colors initialized

    Returns
        game_screen_window [window] - the initialized game screen window created
    """

    game_screen_height, game_screen_width = screen_height - 7, screen_width
    position_y, position_x = 7, 0
    bg_color, border_color = colors["Green_Black"], colors["Green_Black"]

    game_screen_window = create_window(
        game_screen_height,
        game_screen_width,
        position_y,
        position_x,
        bg_color,
        border_color,
    )

    return game_screen_window


def start_snake_game(game_screen_window, colors):
    """Starts the game

    Arguments
        game_screen_window [window] - The initialized game screen window
        colors [list] - A list of all the colors initialized

    Return
        None
    """

    # SNAKE GAME VARIABLES (Game Score, Snake, Position, Direction, Speed, Food and Position)

    # Initialize game screen: height and width
    game_screen_height, game_screen_width = game_screen_window.getmaxyx()

    # Initialize the starting 'GAME SCORE'
    game_score = 0

    # Initialize the starting 'SNAKE POSITION' within inner window boundaries (tuple)
    snake_position = (game_screen_height // 2, game_screen_width // 2)

    # Initialize the 'SNAKE CHARACTER' (head, body, tail) sequence (list of tuples)
    snake = [
        (snake_position[0], snake_position[1]),
        (snake_position[0], snake_position[1] - 1),
        (snake_position[0], snake_position[1] - 2),
    ]

    # Initialize the starting 'SNAKE MOVEMENT DIRECTION' (right)
    snake_direction = curses.KEY_RIGHT

    # Initialize the starting 'SNAKE SPEED'
    snake_speed = 200
    game_screen_window.timeout(snake_speed)

    # Initialize the starting 'SNAKE FOOD POSITION' safely within inner bounds (tuple)
    snake_food = (
        random.randint(1, game_screen_height - 2),
        random.randint(1, game_screen_width - 2),
    )

    # Wrap the starting 'SNAKE FOOD' draw in a try/except to prevent Windows add_wch errors
    try:
        game_screen_window.addch(snake_food[0], snake_food[1], "0")
    except curses.error:
        pass

    # GAME LOOP EXECUTION - Loops until the snake hits a wall or its own body
    while True:
        game_screen_window.attron(colors["Green_Black"])
        game_screen_window.border()
        game_screen_window.attroff(colors["Green_Black"])

        display_game_score(game_screen_window, game_screen_width, game_score, colors)

        # Capture User Key Pressed Value
        key = game_screen_window.getch()

        # Stops the game once 'Q' or 'ESC' is pressed
        if key in (ord("q"), ord("Q"), ord("\x1b"), 27):
            break

        if key != -1:
            # Prevent reversing directly into yourself
            valid_down = key == curses.KEY_DOWN and snake_direction != curses.KEY_UP
            valid_up = key == curses.KEY_UP and snake_direction != curses.KEY_DOWN
            valid_left = key == curses.KEY_LEFT and snake_direction != curses.KEY_RIGHT
            valid_right = key == curses.KEY_RIGHT and snake_direction != curses.KEY_LEFT

            if valid_down or valid_up or valid_left or valid_right:
                snake_direction = key

        # Create the 'SNAKE HEAD' based on the current forward cell
        snake_head = (snake[0][0], snake[0][1])

        # Validate movement when Keypad Arrows are Pressed
        if snake_direction == curses.KEY_RIGHT or snake_direction == 454:
            snake_head = (snake[0][0], snake[0][1] + 1)

        elif snake_direction == curses.KEY_LEFT or snake_direction == 452:
            snake_head = (snake[0][0], snake[0][1] - 1)

        elif snake_direction == curses.KEY_UP or snake_direction == 450:
            snake_head = (snake[0][0] - 1, snake[0][1])

        elif snake_direction == curses.KEY_DOWN or snake_direction == 456:
            snake_head = (snake[0][0] + 1, snake[0][1])

        # Insert new snake head at 0 index of snake
        snake.insert(0, snake_head)

        # Break loop BEFORE drawing if snake head collides with boundaries or its own body
        # Row 1 is the floor boundary to preserve the Score text on Row 0
        if (
            snake[0][0] <= 1
            or snake[0][0] >= game_screen_height - 1
            or snake[0][1] <= 0
            or snake[0][1] >= game_screen_width - 1
            or snake[0] in snake[1:]
        ):
            break

        # Process feeding mechanics
        # Check if the SNAKE ate the SNAKE FOOD
        if snake[0] == snake_food:

            # Increment the game score by 1
            game_score += 1
            display_game_score(
                game_screen_window, game_screen_width, game_score, colors
            )

            # Increase snake speed
            if game_score % 3 == 0 and snake_speed >= 1:
                snake_speed -= snake_speed * 0.20
                game_screen_window.timeout(int(snake_speed))

            # Remove Current SNAKE FOOD
            snake_food = None

            while snake_food is None:
                # Create New SNAKE FOOD
                new_snake_food = (
                    random.randint(1, game_screen_height - 2),
                    random.randint(1, game_screen_width - 2),
                )

                # Validate that the new snake food position is not hitting any part of the Snake
                snake_food = new_snake_food if new_snake_food not in snake else None

            # Wrap the new 'SNAKE FOOD' draw in a try/except to prevent Windows add_wch errors
            try:
                game_screen_window.addch(snake_food[0], snake_food[1], "0")
            except curses.error:
                pass

        else:
            # Remove the Snake Tail (last tuple in the snake)
            tail = snake.pop()

            # Wrap the 'SNAKE TAIL' deletion draw in a try/except to prevent Windows add_wch errors
            try:
                game_screen_window.addch(tail[0], tail[1], " ")
            except curses.error:
                pass

        # Wrap the new 'SNAKE HEAD' draw in a try/except to prevent Windows add_wch errors
        try:
            game_screen_window.addch(
                snake_head[0], snake_head[1], curses.ACS_BLOCK, colors["Green_Black"]
            )
        except curses.error:
            pass

    # If game loop breaks, display game over
    display_game_over(game_screen_window, game_screen_width, game_score)


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

    ending_text_list = [ending_message_1, ending_message_2]
    index_list = [4, 6]

    game_screen_window.clear()

    for index, item in enumerate(ending_text_list):
        game_screen_window.addstr(
            index_list[index],
            get_centered_x_position(screen_width, item),
            item,
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
    header_screen_window = create_header_screen_window(screen_width, colors)
    header_screen_window.refresh()

    # Create a Game Screen Window
    game_screen_window = create_game_screen_window(screen_height, screen_width, colors)
    game_screen_window.refresh()

    # Enable keypad and specials keys capture and turn off input blocking
    game_screen_window.keypad(True)
    game_screen_window.nodelay(True)

    while True:
        key = game_screen_window.getch()

        if key in (ord("\n"), ord("\r"), curses.KEY_ENTER):
            game_screen_window.clear()
            start_snake_game(game_screen_window, colors)

        elif key in (ord("q"), ord("Q"), ord("\x1b"), 27):
            break

    atexit.register(end_program, game_screen_window, screen_width)


if __name__ == "__main__":
    curses.wrapper(main)
