# Ralf Mouthaan
# Nanomation
# July 2025
#
# Scripts to export designs as SVGs, PDFs or PNGs
# https://ezdxf.readthedocs.io/en/stable/tutorials/image_export.html

import ezdxf
from ezdxf.addons.drawing import Frontend, RenderContext, svg, layout, config, pymupdf

def Export(doc, Filename):

    # Get modelspace
    msp = doc.modelspace()

    # Create the render context
    context = RenderContext(doc) 

    # Create the backend
    if Filename.lower().endswith(".svg"):
        backend = svg.SVGBackend()   
    elif Filename.lower().endswith(".pdf"):
        backend = pymupdf.PyMuPdfBackend()
    elif Filename.lower().endswith(".png"):
        backend = pymupdf.PyMuPdfBackend()

    # Set color policy
    cfg = config.Configuration(background_policy=config.BackgroundPolicy.WHITE, 
                               color_policy=config.ColorPolicy.BLACK)

    # Create front end
    frontend = Frontend(context, backend, config = cfg)

    # Draw modelspace
    frontend.draw_layout(msp)

    # auto-detect page size and 2mm margins on all sides
    page = layout.Page(0, 0, layout.Units.mm, margins=layout.Margins.all(2))

    # Exports
    if Filename.lower().endswith(".svg"):

        # SVG export
        svg_string = backend.get_string(page, settings=layout.Settings(scale=1, fit_page=False))
        with open(Filename, "wt", encoding="utf8") as fp:
            fp.write(svg_string)

    elif Filename.lower().endswith(".pdf"):

        # PDF export
         pdf_bytes = backend.get_pdf_bytes(page)
         with open(Filename, "wb") as fp:
            fp.write(pdf_bytes)

    elif Filename.lower().endswith(".png"):

        png_bytes = backend.get_pixmap_bytes(page, fmt="png", dpi=96)
        with open(Filename, "wb") as fp:
            fp.write(png_bytes)
