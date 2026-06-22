import cv2
import numpy as np


def interpolate(image: np.ndarray, size: int, method: int = cv2.INTER_LINEAR) -> np.ndarray:
    return cv2.resize(image, (size, size), interpolation=method)
