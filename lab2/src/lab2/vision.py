import cv2
import numpy as np
from typing import Tuple, List


def load_image(path: str) -> np.ndarray:
    img = cv2.imread(path)
    if img is None:
        raise FileNotFoundError(f"Could not find image at {path}")

    return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)


def apply_blur(img: np.ndarray, k_size: int) -> np.ndarray:
    if k_size % 2 == 0:
        k_size += 1

    return cv2.GaussianBlur(img, (k_size, k_size), 0)


def segment_color(
    img: np.ndarray,
    h_min: int,
    h_max: int,
    s_min: int,
    s_max: int,
    v_min: int,
    v_max: int,
) -> np.ndarray:
    hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
    lower = np.array([h_min, s_min, v_min])
    upper = np.array([h_max, s_max, v_max])
    mask = cv2.inRange(hsv, lower, upper)
    return mask


def morphological_ops(
    binary: np.ndarray, op_type: str, k_size: int, iterations: int
) -> np.ndarray:
    if k_size < 1:
        return binary
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (k_size, k_size))

    if op_type == "close":
        return cv2.morphologyEx(
            binary, cv2.MORPH_CLOSE, kernel, iterations=iterations
        )
    elif op_type == "open":
        return cv2.morphologyEx(
            binary, cv2.MORPH_OPEN, kernel, iterations=iterations
        )

    return binary


def find_buildings(
    binary_map: np.ndarray, min_area: float, max_area: float
) -> Tuple[int, List[np.ndarray]]:
    contours, _ = cv2.findContours(
        binary_map, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )

    filtered = []
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if min_area <= area <= max_area:
            filtered.append(cnt)

    return len(filtered), filtered
