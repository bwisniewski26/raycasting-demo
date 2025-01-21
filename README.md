# Textured Raycasting Example

This project demonstrates a simple implementation of textured raycasting using Python and Pygame. The code simulates a 3D environment by casting rays from the player's perspective and rendering walls with textures.

## Features

- Basic raycasting algorithm to simulate a 3D environment.
- Textured walls for a more realistic appearance.
- Player movement and rotation.
- Simple map representation using a string grid.

## Requirements

- Python 3.x
- Pygame

## Installation

1. Clone the repository:
   `git clone https://github.com/bwisniewski2/raycasting-demo`
2. Navigate to the project directory:
   `cd raycasting-demo`
3. Install the required dependencies:
   `pip install pygame`

## Usage

1. Run the script:
   `python textured_raycast.py`
2. Use arrow keys to move the player:
   - Left/Right arrows to rotate
   - Up/Down arrows to move forward/backwards

## Map representation

The map is represented as a string grid where each character corresponds to a tile:

- `W` - wall
- `M` - door
- ` ` - empty space

## Acknowledgements

This project was created using various online resources and tutorials on raycasting and Pygame. Special thanks to the contributors of these resources for their valuable insights and code snippets.
