# Ralf Mouthaan
# Nanomation
# May 2026
# 
# Turning a dxf to a numpy array

import ezdxf
from LithotagDesigner.LithoTag import DrawLithotag
import random
import Utils
import matplotlib.pyplot as plt
import numpy as np
import deeptrack as dt

import sys
print(sys.executable)

tagsize = 150
wavelengths = np.linspace(450e-9, 700e-9, 5)

# Create a DXF with a lithotag
doc = ezdxf.new(dxfversion="R2010")
doc.layers.add("Lithotags")
i = random.randint(0, 100)
j = random.randint(0, 100)
DrawLithotag(doc, 0, 0, 1.0, i, j)

# Convert DXF to an ndarray
img = Utils.dxf_to_ndarray(doc, tagsize)
