from math import factorial
import numpy as np


def _noll_to_nm(j: int) -> tuple:
    n = 0
    while (n + 1) * (n + 2) // 2 < j:
        n += 1
    j_start = n * (n + 1) // 2 + 1
    p = j - j_start
    if n % 2 == 0:
        if p == 0:
            return (n, 0)
        pair = (p + 1) // 2
        abs_m = 2 * pair
    else:
        pair = (p + 2) // 2
        abs_m = 2 * pair - 1
    m = abs_m if (j_start + p) % 2 == 0 else -abs_m
    return (n, m)


def _zernike_poly(n: int, m: int, rho: np.ndarray, theta: np.ndarray) -> np.ndarray:
    abs_m = abs(m)
    R = np.zeros_like(rho, dtype=float)
    for s in range((n - abs_m) // 2 + 1):
        coeff = ((-1)**s * factorial(n - s) /
                 (factorial(s) * factorial((n + abs_m) // 2 - s) * factorial((n - abs_m) // 2 - s)))
        R += coeff * rho**(n - 2 * s)
    if m == 0:
        return np.sqrt(n + 1) * R
    elif m > 0:
        return np.sqrt(2 * (n + 1)) * R * np.cos(m * theta)
    else:
        return np.sqrt(2 * (n + 1)) * R * np.sin(abs_m * theta)


def ApplyZernike(image: np.ndarray, *zernike_coeffs: float) -> np.ndarray:
    """Apply Zernike aberrations (Noll-indexed, starting Z1) to an intensity pattern."""
    height, width = image.shape[:2]

    y = np.linspace(-1, 1, height)
    x = np.linspace(-1, 1, width)
    X, Y = np.meshgrid(x, y)
    rho = np.sqrt(X**2 + Y**2)
    theta = np.arctan2(Y, X)

    phase = np.zeros((height, width), dtype=float)
    for j, coeff in enumerate(zernike_coeffs, start=1):
        if coeff != 0.0:
            n, m = _noll_to_nm(j)
            phase += coeff * _zernike_poly(n, m, rho, theta)

    field = np.sqrt(np.maximum(image.astype(float), 0.0))
    spectrum = np.fft.fftshift(np.fft.fft2(field))
    aberration = np.where(rho <= 1.0, np.exp(1j * phase), 1.0)
    aberrated_field = np.fft.ifft2(np.fft.ifftshift(spectrum * aberration))
    result = np.abs(aberrated_field)**2

    src_mean = image.mean()
    dst_mean = result.mean()
    if src_mean > 0 and dst_mean > 0:
        result *= src_mean / dst_mean

    return result.astype(image.dtype)
