import ezdxf
from ezdxf.addons.drawing import RenderContext, Frontend
from ezdxf.addons.drawing.matplotlib import MatplotlibBackend
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import numpy as np
import io

def dxf_to_ndarray(doc: ezdxf.document.Drawing, width_px: int) -> np.ndarray:

    msp = doc.modelspace()
    fig = plt.figure()
    ax = fig.add_axes([0, 0, 1, 1])

    ctx = RenderContext(doc)
    backend = MatplotlibBackend(ax)
    Frontend(ctx, backend).draw_layout(msp, finalize=True)

    # Manually fill closed polylines
    for entity in msp:
        if entity.dxftype() == "LWPOLYLINE" and entity.is_closed:
            points = [(p[0], p[1]) for p in entity.get_points()]
            polygon = Polygon(points, closed=True, facecolor="white", edgecolor="white")
            ax.add_patch(polygon)
        elif entity.dxftype() == "POLYLINE" and entity.is_closed:
            points = [(v.dxf.location.x, v.dxf.location.y) for v in entity.vertices]
            polygon = Polygon(points, closed=True, facecolor="white", edgecolor="white")
            ax.add_patch(polygon)

    dpi = 100
    fig.set_size_inches(width_px / dpi, width_px / dpi)

    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=dpi)
    plt.close(fig)

    buf.seek(0)
    img_array = plt.imread(buf)
    img_array = img_array[..., :3].mean(axis=-1)
    img_array = (img_array > 0.5).astype(np.float32)
    return img_array