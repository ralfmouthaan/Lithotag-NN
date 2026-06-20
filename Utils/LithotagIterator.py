import random
from Utils.LithoTag import CreateLithotag
from Utils.Zernike import ApplyZernike

# --- Parameters ---
SIZE_MIN          = 30     # minimum image size (pixels)
SIZE_MAX          = 150    # maximum image size (pixels)
NUM_ZERNIKES      = 11     # number of Zernike terms applied (Z2 through Z(NUM_ZERNIKES+1))
ZERNIKE_MIN       = -1.0   # minimum Zernike coefficient (waves)
ZERNIKE_MAX       =  1.0   # maximum Zernike coefficient (waves)


class LithotagIterator:

    def __iter__(self):
        return self

    def __next__(self) -> dict:
        size  = random.randint(SIZE_MIN, SIZE_MAX)
        xval  = random.randint(0, 100)
        yval  = random.randint(0, 100)

        result = CreateLithotag(xval, yval, size)

        # Z1 (piston) has no effect on intensity; randomise Z2 onward
        coeffs = [0.0] + [random.uniform(ZERNIKE_MIN, ZERNIKE_MAX)
                          for _ in range(NUM_ZERNIKES)]
        result['img']    = ApplyZernike(result['img'], *coeffs)
        result['coeffs'] = coeffs

        return result
