import pytest
from tetrimino import Tetrimino
from constants import SHAPES, getColors, getWhite, setWhite

@pytest.fixture
def tetrimino_instance():
    """Fixture to create a new Tetrimino instance."""
    return Tetrimino(5, 5)  # Initialize with x=5, y=5

def test_tetrimino_initial_position(tetrimino_instance):
    """Test that the Tetrimino initializes with the correct position."""
    assert tetrimino_instance.x == 5
    assert tetrimino_instance.y == 5

def test_tetrimino_shape_dimensions(tetrimino_instance):
    """Test that the Tetrimino has a valid shape."""
    shape = tetrimino_instance.shape
    assert len(shape) > 0  # Ensure shape is not empty
    assert all(len(row) > 0 for row in shape)  # Ensure all rows have a length

def test_tetrimino_shape_values(tetrimino_instance):
    """Test that the Tetrimino shape contains valid values."""
    shape = tetrimino_instance.shape
    colors = getColors()
    max_color_index = len(colors) - 1
    for row in shape:
        for cell in row:
            assert cell == 0 or (2 <= cell <= max_color_index)

def test_tetrimino_rotation(tetrimino_instance):
    """Test that the Tetrimino rotates correctly."""
    original_shape = [row[:] for row in tetrimino_instance.shape]
    tetrimino_instance.rotate()
    rotated_shape = tetrimino_instance.shape

    # Check dimensions after rotation
    assert len(original_shape) == len(rotated_shape[0])
    assert len(original_shape[0]) == len(rotated_shape)

def test_tetrimino_white_conversion():
    """Test the behavior of the Tetrimino when white points are used."""
    setWhite(8)  # Set white points to 8
    tetrimino = Tetrimino(0, 0)

    # Check that white points were used correctly
    assert getWhite() == 0  # Ensure white points were deducted
    assert any(cell == 1 for row in tetrimino.shape for cell in row)  # Check for a white block
