import numpy as np

def hexagon(radius: float) -> np.ndarray:
    angles = np.linspace(0, 2*np.pi, 7)
    x = radius * np.cos(angles)
    y = radius * np.sin(angles)
    z = np.ones_like(x)
    
    return np.vstack((x, y, z))

def pyramid(base_size: float, height: float) -> tuple[np.ndarray, list[list[int]]]:
    h_iso = base_size * (3**0.5) / 2

    matrix_corners = np.array([
        [0, 0, height, 1],
        [-base_size/2, -h_iso/3, 0, 1],
        [base_size/2, -h_iso/3, 0, 1],
        [0, 2*h_iso/3, 0, 1],
    ]).T 
    
    edges = [
        [0, 1], [0, 2], [0, 3],
        [1, 2], [2, 3], [3, 1],
    ]
    
    return matrix_corners, edges
