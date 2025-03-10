import click
from PIL import Image


def generate_chessboard(rows, cols, square_size=50):
    """
    Generate a black and white chessboard image

    Parameters:
    size (int): Number of squares on each side (e.g., 8 for standard chess board)
    square_size (int): Pixel size of each square (default: 50)

    Returns:
    PIL.Image: Generated chessboard image
    """
    # Calculate total image size
    rows_size = rows * square_size
    cols_size = cols * square_size

    # Create new white image
    # board = Image.new('RGB', (rows_size, cols_size), 'white')
    board = Image.new('RGB', (cols_size, rows_size), 'white')

    # Get pixel access object
    pixels = board.load()

    # Fill in black squares
    for i in range(cols_size):
        for j in range(rows_size):
            # Calculate which square this pixel belongs to
            square_x = i // square_size
            square_y = j // square_size

            # If sum of coordinates is odd, make it black
            if (square_x + square_y) % 2 == 1:
                pixels[i, j] = (0, 0, 0)  # Black color

    return board


@click.command()
@click.option("-out", "--output", "output",
              required=True, type=str, default="chessboard.jpg",
              help="select output directory for measurements")
@click.option("-r", "--rows", "rows",
              required=True, type=int)
@click.option("-c", "--cols", "cols",
              required=True, type=int)
@click.option("-sq", "--square", "square_size",
              required=True, type=int)
def main(output, rows, cols, square_size):
    board = generate_chessboard(rows, cols, square_size)
    board.save(output)
    print(f"Chessboard saved as {output}")


if __name__ == '__main__':
    main()
