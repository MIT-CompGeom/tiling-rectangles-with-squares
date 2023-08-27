"""
Rectangle Packing with Squares

This software solves via brute force the problem of completely filling (tiling)
a rectangular board of given dimensions using nonoverlapping squares of
specified allowed sizes.

Dependencies: numpy

Functions:
    - create_board(n, m): Creates a board of size n x m filled with zeros
      (represented as a numpy array).
    - find_zero(board): Finds the position of the first zero in the board.
    - check_right(board, i, j, size): Checks whether there's enough space to fit a square of specified size.
    - fill_square(board, i, j, size, name): Fills (or unfills) a square on the board.
    - find_square(board, i, j): Finds the size of the existing square with top-left corner (i,j).
    - pack(board_height, board_width, allowed_pieces): Initializes a board and packs via pack_board.
    - pack_board(board, allowed_pieces, counter): Recursive function that tries to pack the board with the allowed pieces.
    - full_packing_search(max_height, max_width, allowed_pieces): Tries to pack boards of sizes from 2x2 to max_height x max_width.
    - check_packing(board, allowed_pieces): Checks that the board is a perfect packing using only specified square sizes.
    - check_packings(boards, allowed_pieces): Checks a list of packings, and returns maximum square size used.
    - board_to_svg(board, cell_size=10): Renders a board as an SVG drawing (as a string).
    - save_packings(successful_packings, output_dir='output'): Saves all packings to SVG files in the specified directory.
    - latex_table(answers): Prints a LaTeX table of which packings were possible (used in the paper).
    - undecomposable(answers): Returns a list of sizes of packings that cannot be decomposed into smaller packings via a single line cut.

Usage:
    Define the allowed pieces and then call the full_packing_search function with desired max dimensions.
"""

import math, os
import numpy as np
import xml.etree.ElementTree as ET

def create_board(n,m):
    """Create an empty board with n rows and m columns"""
    board = np.zeros((n,m))
    return board

def find_zero(board):
    """Finds the leftmost topmost 0, if any"""
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 0:
                return i, j
    return None

def check_right(board, i, j, size):
    """Checks whether there are size 0's to the right of position (i,j), including (i,j) itself.
    Because we process rows in order, if these cells are 0, the entire square of this size should be 0.
    """
    if i + size > len(board) or j + size > len(board[0]):
        return False
    for k in range(size):
        if board[i][j+k] != 0:
            return False
    return True

def fill_square(board, i, j, size, name):
    """Fills a square of specified size with entries name starting at top-left location (i,j)"""
    if i + size > len(board) or j + size > len(board[0]):
        raise RuntimeError("error square out of bounds")
    for a in range(size):
        for b in range(size):
            if board[i+a][j+b] != 0 != name:
                # This should never happen because we process rows in order and call check_right before this
                raise RuntimeError("error square overlap")
            board[i+a][j+b] = name

def find_square(board, i, j):
    """Finds the size of the square with top-left corner (i,j), and checks that it's really a square"""
    height, width = board.shape
    name = board[i][j]
    # Compute size by walking right
    size = 1
    while j + size < width:
        if board[i][j+size] != name: break
        size += 1
    # Verify entire square is there
    for vi in range(i, i+size):
        for vj in range(j, j+size):
            if vi >= height or board[vi][vj] != name:
                raise RuntimeError(f"incomplete square starting at {i},{j} width {size}")
    # Verify square doesn't extend lower
    for vj in range(j, j+size):
        if i+size+1 < height and board[i+size+1][vj] == name:
            raise RuntimeError(f"tall rectangular square starting at {i},{j} width {size}")
    return size

def pack_board(board, allowed_pieces, counter, successful_packings):
    """Recursive function used by pack that tries to pack the board with the allowed pieces.

    `counter` keeps tracks of the number of placed pieces.
    `successful_packings` should be a list; it will accumulate all found packings.
    """
    current_location = find_zero(board)
    if current_location is None:
        successful_packings.append(board.copy())
        return True
    counter += 1
    for size in allowed_pieces:
        if check_right(board,current_location[0], current_location[1], size):
            fill_square(board, current_location[0], current_location[1], size, counter)
            if pack_board(board, allowed_pieces, counter, successful_packings):
                return True
            fill_square(board, current_location[0], current_location[1], size, 0)
    return False

def pack(board_height, board_width, allowed_pieces, successful_packings):
    """Initializes a board and packs via pack_board."""
    board = create_board(board_height, board_width)
    counter = 0
    return pack_board(board, allowed_pieces, counter, successful_packings)

def full_packing_search(max_height, max_width, allowed_pieces):
    """Tries to pack boards of sizes from 2x2 to max_height x max_width."""
    answers = np.zeros((max_height, max_width))
    successful_packings = []
    for i in range(2, max_height):
        for j in range(2, max_width):
            # Save half the time by skipping taller-than-wide rectangles
            if i > j:
                answers[i][j] = answers[j][i]
            else:
                print(f'Solving {i} x {j}...', end=' ')
                answers[i][j] = solved = int(pack(i, j, allowed_pieces, successful_packings))
                if solved:
                    max_size = check_packing(successful_packings[-1], allowed_pieces)
                    print('SUCCESS with largest square of', max_size)
                else:
                    print('FAILED!')
    return (answers, successful_packings)

def check_packing(board, allowed_pieces):
    """Check that board is a perfect packing using only specified square sizes
    Returns the maximum-size square used.
    """
    height, width = board.shape
    # Ensure entire board is filled
    for i in range(height):
        for j in range(width):
            if board[i][j] == 0:
                print(board)
                raise RuntimeError(f"{i},{j} isn't filled")
    # Ensure board is a set of squares by repeatedly removing from a copy
    copy = board.copy()
    max_size = 0
    for i in range(height):
        for j in range(width):
            if copy[i][j] == 0: continue  # already erased
            try:
                size = find_square(copy, i, j)
                if size not in allowed_pieces:
                    raise RuntimeError(f"forbidden size {size}")
                if size > max_size: max_size = size
                fill_square(copy, i, j, size, 0)
            except RuntimeError:
                print(board)
                raise
    return max_size

def check_packings(successful_packings, allowed_pieces):
    """Check a list of packings, and return maximum size used"""
    return max(
        check_packing(packing, allowed_pieces)
        for packing in successful_packings
    )

# Base color_palette based on:
# https://coolors.co/8a1c7c-429ea6-fcd757-f24236
color_palette = {
  2: ['#8A1C7C'],
  3: ['#429EA6'],
  5: ['#FCD757'],
  7: ['#F24236'],
}
# Make a 50% lighter version of each color for checkerboarding.
for colors in color_palette.values():
  rgb = colors[0].lstrip('#')
  rgb = tuple(int(rgb[i:i+2], 16) for i in [0, 2, 4])
  colors.append('#%02x%02x%02x' % tuple(int(0.5*val + 0.5*255) for val in rgb))

def board_to_svg(board, cell_size=10):
    """Renders a board as an SVG drawing (as a string)."""
    global max_color
    height, width = board.shape
    stroke_width = 2
    svg_width = width * cell_size + stroke_width
    svg_height = height * cell_size + stroke_width
    svg = ET.Element('svg', xmlns="http://www.w3.org/2000/svg",
        width=str(svg_width), height=str(svg_height),
        viewBox=f'{-stroke_width/2} {-stroke_width/2} {svg_width} {svg_height}')

    colors = [[0] * width for _ in range(height)]
    copy = board.copy()
    for i in range(height):
        for j in range(width):
            if copy[i][j] == 0: continue  # already erased
            size = find_square(copy, i, j)
            fill_square(copy, i, j, size, 0)

            # Assign color with greedy algorithm: first color not used by neighbors
            used_colors = set()
            if j > 0: used_colors.add(colors[i][j-1])
            if i > 0:
                for sj in range(j, j+size):
                    used_colors.add(colors[i-1][sj])
            for color in color_palette[size]:
                if color not in used_colors: break
            else:
                print('bad coloring', color)
            fill_square(colors, i, j, size, color)

            ET.SubElement(svg, 'rect',
                {'stroke-width': str(stroke_width)}, stroke="black",
                x=str(j * cell_size), y=str(i * cell_size),
                width=str(size * cell_size), height=str(size * cell_size),
                fill=color)
                #fill="hsl({}, 80%, 60%)".format(color * 30))
    return ET.tostring(svg, encoding="unicode")

def save_packings(successful_packings, output_dir='output'):
    """Saves all packings to SVG files in the specified directory."""
    os.makedirs(output_dir, exist_ok=True)
    count = 0
    for packing in successful_packings:
        i, j = packing.shape
        # Don't bother outputting easy packings
        if math.gcd(i, j) > 1: continue
        count += 1
        svg = board_to_svg(packing)
        with open(os.path.join(output_dir, f'{i}x{j}.svg'), 'w') as f:
            f.write(svg)
    print('Output packings:', count)

def latex_table(answers):
    """Prints a LaTeX table of which packings were possible (used in the paper)."""
    height, width = answers.shape
    print(r'\begin{tabular}{r' + 'c' * (width - 2) + '}')
    print('&'.join(['  '] + [str(j).rjust(2) for j in range(2, width)]) + r'\\')
    for i in range(2, height):
        row = [str(i).rjust(2)]
        for j in range(2, width):
            if answers[i][j] > 0.5:
                row.append(r'\T')
            else:
                row.append('  ')
        print('&'.join(row) + r'\\')
    print(r'\end{tabular}')

def undecomposable(answers):
    """Returns a list of sizes of packings that cannot be decomposed into smaller packings via a single line cut."""
    height, width = answers.shape
    decomposable = create_board(height, width)
    check = (7, 13)
    for i1 in range(2, height):
        for j1 in range(2, width):
            if answers[i1][j1] == 0:
                decomposable[i1][j1] = 999999  # don't list unsolvable instances as undecomposable
                continue
            for i2 in range(2, height):
                if answers[i2][j1] == 0: continue
                if i1+i2 == check[0] and j1 == check[1]: print(f'{check[0]}x{check[1]} = {i1}+{i2} x {j1}')
                if i1+i2 < height: decomposable[i1+i2][j1] += 1
            for j2 in range(2, width):
                if answers[i1][j2] == 0: continue
                if i1 == check[0] and j1+j2 == check[1]: print(f'{check[0]}x{check[1]} = {i1} x {j1}+{j2}')
                if j1+j2 < width: decomposable[i1][j1+j2] += 1
    undecomposable = []
    for i in range(2, height):
        for j in range(2, width):
            if decomposable[i][j] == 0:
                undecomposable.append((i,j))
    return undecomposable

allowed_pieces = [2,3,5,7,11,13,17,19]  # only need prime sizes
answers, successful_packings = full_packing_search(20, 20, allowed_pieces)
print(answers)
latex_table(answers)
#pack(7, 20, allowed_pieces, successful_packings)
#pack(7, 21, allowed_pieces, successful_packings)
max_size = check_packings(successful_packings, allowed_pieces)
print('Maximum square size:', max_size)
print('Packings found:', len(successful_packings))
save_packings(successful_packings)
print('Undecomposable:', ', '.join('%sx%s' % pair for pair in undecomposable(answers)))
