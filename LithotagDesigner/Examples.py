# Ralf Mouthaan
# Nanomation
# July 2025
#
# Example script showing how to generate a DXF file with a grid of lithotags or diamondtags.

import ezdxf
import LithoTag
import DiamondTag
import ImageExports

def DrawLithotagsDXF():

    # Parameters
    dx = 25
    dy = 25

    # Create a new DXF document.
    doc = ezdxf.new(dxfversion="R2010")

    # Generate grid of lithotags
    doc.layers.add("Lithotags")
    for i in range(1, 11):
        for j in range (1, 11):
            LithoTag.DrawLithotag(doc, i*dx, j*dy, 1.0, i, j)

    # Save DXF document
    doc.saveas("Lithotag Test.dxf")

def DrawDiamondtagsDXF():

    # Parameters
    dx = 50
    dy = 50

    # Create a new DXF document.
    doc = ezdxf.new(dxfversion="R2010")

    # Generate grid of lithotags
    doc.layers.add("Diamondtags")
    for i in range(6, 7):
        for j in range (6, 7):
            DiamondTag.DrawDiamondtag(doc, i*dx, j*dy, 1.0, i, j)

    # Save DXF document
    doc.saveas("Outputs\Diamondtag Test (6, 6).dxf")

def DrawLithotagsDXF():

    # Can also be used to create others
    
    # Parameters
    dx = 50
    dy = 50

    # Create a new DXF document.
    doc = ezdxf.new(dxfversion="R2010")

    # Generate grid of lithotags
    doc.layers.add("Lithotags")
    for i in range(1, 11):
        for j in range (1, 11):
            LithoTag.DrawLithotag(doc, i*dx, j*dy, 1.0, i, j)

    ImageExports.Export(doc, "Outputs\Export Example.png")

def WriteChipTXT():

    Name = "41 x 41 Opto"
    TagStyle = "Lithotag" # "Diamondtag" alternatively
    Optical = 1
    SEM = 0
    LinkZill = 0
    WireBond = 0
    TagSpacing = 20 # in um
    TagInterval = 1 # Label interval
    numTagsX = 201
    numTagsY = 201
    Left_TAG = 0
    Bottom_TAG = 0
    Left_CAD = 3000
    Bottom_CAD = 3000

    with open(Name + ".txt", "w") as file:
        file.write("Name = " + Name + "\n")
        file.write("TagStyle = " + TagStyle + "\n")
        file.write("Optical = " + str(Optical) + "\n")
        file.write("SEM = " + str(SEM) + "\n")
        file.write("LinkZill = " + str(LinkZill) + "\n")
        file.write("WireBond = " + str(WireBond) + "\n")
        file.write("TagSpacing = " + str(TagSpacing) + "\n")
        file.write("TagInterval = " + str(TagInterval) + "\n")
        file.write("numTagsX = " + str(numTagsX) + "\n")
        file.write("numTagsY = " + str(numTagsY) + "\n")
        file.write("Left_TAG = " + str(Left_TAG) + "\n")
        file.write("Bottom_TAG = " + str(Bottom_TAG) + "\n")
        file.write("Left_CAD = " + str(Left_CAD) + "\n")
        file.write("Bottom_CAD = " + str(Bottom_CAD) + "\n")