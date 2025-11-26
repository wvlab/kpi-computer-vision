import numpy as np


def translation_2d(dx: float, dy: float) -> np.ndarray:
    """Returns a 3x3 translation matrix for 2D homogeneous coordinates."""
    return np.array(
        [
            [1, 0, dx],
            [0, 1, dy],
            [0, 0, 1],
        ],
    )


def scaling_2d(sx: float, sy: float) -> np.ndarray:
    """Returns a 3x3 scaling matrix."""
    return np.array(
        [
            [sx, 0, 0],
            [0, sy, 0],
            [0, 0, 1],
        ],
    )


def rotation_2d(angle_deg: float) -> np.ndarray:
    """Returns a 3x3 rotation matrix (counter-clockwise)."""
    rad = np.radians(angle_deg)
    c, s = np.cos(rad), np.sin(rad)
    return np.array(
        [
            [c, -s, 0],
            [s, c, 0],
            [0, 0, 1],
        ]
    )


def translation_3d(dx: float, dy: float, dz: float) -> np.ndarray:
    """Returns a 4x4 translation matrix for 3D homogeneous coordinates."""
    return np.array(
        [
            [1, 0, 0, dx],
            [0, 1, 0, dy],
            [0, 0, 1, dz],
            [0, 0, 0, 1],
        ],
    )


def rotation_3d_z(angle_deg: float) -> np.ndarray:
    """Returns a 4x4 rotation matrix around the Z axis."""
    rad = np.radians(angle_deg)
    c, s = np.cos(rad), np.sin(rad)
    return np.array(
        [
            [c, -s, 0, 0],
            [s, c, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ],
    )


def axonometric_projection(
    alpha_deg: float = 45, beta_deg: float = 35.264
) -> np.ndarray:
    """
    Returns a 4x4 Projection Matrix.
    Logic: Rotate around X, then Rotate around Y, then Orthographic projection (drop Z).
    """
    rad_a = np.radians(alpha_deg)
    rad_b = np.radians(beta_deg)

    rx = np.array(
        [
            [1, 0, 0, 0],
            [0, np.cos(rad_a), -np.sin(rad_a), 0],
            [0, np.sin(rad_a), np.cos(rad_a), 0],
            [0, 0, 0, 1],
        ]
    )

    ry = np.array(
        [
            [np.cos(rad_b), 0, np.sin(rad_b), 0],
            [0, 1, 0, 0],
            [-np.sin(rad_b), 0, np.cos(rad_b), 0],
            [0, 0, 0, 1],
        ]
    )

    ortho = np.array(
        [
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 1],
        ],
    )

    return ortho @ ry @ rx


def compose(*matrices: np.ndarray) -> np.ndarray:
    """
    Multiplies a chain of matrices.
    Order: compose(Last, ..., First) corresponds to Last @ ... @ First @ Vector.
    """
    result = matrices[0]
    for m in matrices[1:]:
        result = result @ m

    return result


def apply(points: np.ndarray, matrix: np.ndarray) -> np.ndarray:
    """
    Applies transformation matrix to the extended coordinate matrix.
    Points shape: (D+1, N)
    Matrix shape: (D+1, D+1)
    """
    return matrix @ points
