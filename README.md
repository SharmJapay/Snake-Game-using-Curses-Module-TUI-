# Snake Game in Python

A classic **Snake game** built using **Python** and the built-in **Curses** terminal library. 

## Features

* **Terminal-based GUI**: Runs directly in your command line or terminal.
* **Smooth Controls**: Use standard arrow keys to steer the snake.
* **Score Tracking**: Tracks your current score as you eat food.
* **Dynamic Speed**: The game gets harder and faster as the snake grows.
* **Collision Detection**: Game over triggers if you hit the walls or yourself.

## Requirements

* Python 3.x
* A terminal that supports the `curses` module:
  * **Linux / macOS**: Built-in support by default.
  * **Windows**: Requires the `windows-curses` package.

## Installation & Setup

1. **Clone or download** this repository to your local machine.

2. **Install dependencies** (Windows users only):
   ```bash
   pip install windows-curses
   ```

3. **Navigate** to the project directory in your terminal.

## How to Play

Run the game script with Python:

```bash
python snake_game.py
```
*(Replace `snake.py` with your actual main script file name if it is different).*

### Controls

* **Up Arrow**: Move Up
* **Down Arrow**: Move Down
* **Left Arrow**: Move Left
* **Right Arrow**: Move Right
* **Q Key**: Quit Game

## Code Structure

* `snake_game.py`: Main game loop, input handling, and rendering logic.
* Handles screen initialization, game state updates, and clean terminal shutdown using curses wrappers.

## License

This project is open-source and free to use for practice and fun.