# Ralf Mouthaan
# Nanomation
# May 2026

import matplotlib.pyplot as plt
import numpy as np
from Utils import LithotagIterator

iterator = LithotagIterator()

fig, axes = plt.subplots(2, 5, figsize=(15, 6))
for ax in axes.flat:
    sample = next(iterator)
    ax.imshow(sample['img'], cmap='gray')
    ax.set_title(f"({sample['XVal']}, {sample['YVal']})  {sample['Width']}px")
    ax.axis('off')

plt.tight_layout()
plt.show()
