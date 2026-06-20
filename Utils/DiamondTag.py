# Ralf Mouthaan
# Nanomation
# July 2025
#
# Functions to generate a diamondtag

import ezdxf
import ezdxf.document
import numpy as np
from math import cos, sin, pi
from Utils.DxfConversion import dxf_to_ndarray

Params = {
    'Poly': True,
    'NoPolyArcPoints': 10,
    'NoPolyCirclePoints': 50,
    'FillFactor': 0.5,
    'NoUnencryptedBits': 18,
    'NoEncryptedBits': 24
    }

def _DrawDiamondtag(doc, XPos, YPos, Size, XVal, YVal):

    _DrawCaps(doc, XPos, YPos, Size)
    msgencrypted = _Encode(XVal, YVal)
    _DrawNumber(doc, XPos, YPos, Size, msgencrypted)

def _DrawCaps(doc, XPos, YPos, Size):

    if Params["Poly"]:
        _DrawPolyCaps(doc, XPos, YPos, Size)
    else:
        _DrawNonPolyCaps(doc, XPos, YPos, Size)

def _DrawPolyCaps(doc, XPos, YPos, Size):

    msp = doc.modelspace()

    ArcRadius = Params["FillFactor"]*Size

    # N Cap
    NCap = msp.add_lwpolyline([])
    _AppendPolyArc(NCap, XPos, YPos + Size*9.5, ArcRadius, 30, 150)
    _AppendPolyArc(NCap, XPos - Size, YPos + Size*7.5, ArcRadius, 150, 270)
    _AppendPolyArc(NCap, XPos + Size, YPos + Size*7.5, ArcRadius, -90, 30)
    NCap.closed = True

    # S Cap
    SCap = msp.add_lwpolyline([])
    _AppendPolyArc(SCap, XPos, YPos - Size*9.5, ArcRadius, 210, 330)
    _AppendPolyArc(SCap, XPos + Size, YPos - Size*7.5, ArcRadius, 330, 450)
    _AppendPolyArc(SCap, XPos - Size, YPos - Size*7.5, ArcRadius, 90, 210)
    SCap.closed = True

    # W cap
    WCap = msp.add_lwpolyline([])
    _AppendPolyArc(WCap, XPos - Size*5, YPos, ArcRadius, 150, 210)
    _AppendPolyArc(WCap, XPos - Size*4, YPos - Size*2, ArcRadius, -150, 30)
    _AppendPolyArc(WCap, XPos - Size*4, YPos, ArcRadius, -150, -210)
    _AppendPolyArc(WCap, XPos - Size*4, YPos + Size*2, ArcRadius, -30, 150)
    WCap.closed = True

    # E cap
    ECap = msp.add_lwpolyline([])
    _AppendPolyArc(ECap, XPos + Size*5, YPos, ArcRadius, -30, 30)
    _AppendPolyArc(ECap, XPos + Size*4, YPos + Size*2, ArcRadius, 30, 210)
    _AppendPolyArc(ECap, XPos + Size*4, YPos, ArcRadius, 30, -30)
    _AppendPolyArc(ECap, XPos + Size*4, YPos - Size*2, ArcRadius, 150, 330)
    ECap.closed = True

def _DrawNonPolyCaps(doc, XPos, YPos, Size):

    msp = doc.modelspace()

    ArcRadius = Params["FillFactor"]*Size

    # N Cap
    NCap_NArc = msp.add_arc((XPos, YPos + Size*9.5), ArcRadius, 30, 150)
    NCap_SWArc = msp.add_arc((XPos - Size, YPos + Size*7.5), ArcRadius, 150, -90)
    NCap_SEArc = msp.add_arc((XPos + Size, YPos + Size*7.5), ArcRadius, -90, 30)
    msp.add_line(NCap_NArc.end_point, NCap_SWArc.start_point)
    msp.add_line(NCap_NArc.start_point, NCap_SEArc.end_point)
    msp.add_line(NCap_SWArc.end_point, NCap_SEArc.start_point)

    # S Cap
    SCap_SArc = msp.add_arc((XPos, YPos - Size*9.5), ArcRadius, 210, 330)
    SCap_NWArc = msp.add_arc((XPos - Size, YPos - Size*7.5), ArcRadius, 450, 570)
    SCap_NEArc = msp.add_arc((XPos + Size, YPos - Size*7.5), ArcRadius, 330, 450)
    msp.add_line(SCap_SArc.start_point, SCap_NWArc.end_point)
    msp.add_line(SCap_SArc.end_point, SCap_NEArc.start_point)
    msp.add_line(SCap_NWArc.start_point, SCap_NEArc.end_point)

    # W cap
    WCap_WArc = msp.add_arc((XPos - Size*5, YPos), ArcRadius, 150, -150)
    WCap_NArc = msp.add_arc((XPos - Size*4, YPos + Size*2), ArcRadius, -30, 150)
    WCap_EArc = msp.add_arc((XPos - Size*4, YPos), ArcRadius, -210, -150)
    WCap_SArc = msp.add_arc((XPos - Size*4, YPos - Size*2), ArcRadius, -150, 30)
    msp.add_line(WCap_WArc.start_point, WCap_NArc.end_point)
    msp.add_line(WCap_NArc.start_point, WCap_EArc.start_point)
    msp.add_line(WCap_EArc.end_point, WCap_SArc.end_point)
    msp.add_line(WCap_SArc.start_point, WCap_WArc.end_point)

    # E cap
    ECap_EArc = msp.add_arc((XPos + Size*5, YPos), ArcRadius, -30, 30)
    ECap_NArc = msp.add_arc((XPos + Size*4, YPos + Size*2), ArcRadius, 30, 210)
    ECap_WArc = msp.add_arc((XPos + Size*4, YPos), ArcRadius, -30, 30)
    ECap_SArc = msp.add_arc((XPos + Size*4, YPos - Size*2), ArcRadius, 150, -30)
    msp.add_line(ECap_WArc.end_point, ECap_NArc.end_point)
    msp.add_line(ECap_NArc.start_point, ECap_EArc.end_point)
    msp.add_line(ECap_EArc.start_point, ECap_SArc.end_point)
    msp.add_line(ECap_SArc.start_point, ECap_WArc.start_point)

def _DrawCircle(doc, XPos, YPos, Size):

    if Params["Poly"]:
        _DrawPolyCircle(doc, XPos, YPos, Size)
    else:
        _DrawNonPolyCircle(doc, XPos, YPos, Size)

def _DrawPolyCircle(doc, XPos, YPos, Size):

    msp = doc.modelspace()

    circle = msp.add_lwpolyline([])
    dAngle = 360/(Params["NoPolyCirclePoints"] - 1)
    for i in range(0, Params["NoPolyCirclePoints"]):
        angle = i*dAngle/180*pi
        X = XPos + Size*cos(angle)
        Y = YPos + Size*sin(angle)
        circle.append_points([(X, Y)])
    circle.closed = True

def _DrawNonPolyCircle(doc, XPos, YPos, Size):

    msp = doc.modelspace()
    msp.add_circle((XPos, YPos), Size)

def _DrawNumber(doc, XPos, YPos, Size, msgencrypted):

    # First line
    if msgencrypted[0] == 1:
        _DrawCircle(doc, XPos - 2, YPos + 6, Params["FillFactor"]*Size)
    if msgencrypted[1] == 1:
        _DrawCircle(doc, XPos, YPos + 6, Params["FillFactor"]*Size)
    if msgencrypted[2] == 1:
        _DrawCircle(doc, XPos + 2, YPos + 6, Params["FillFactor"]*Size)

    # Second line
    if msgencrypted[3] == 1:
        _DrawCircle(doc, XPos - 3, YPos + 4, Params["FillFactor"]*Size)
    if msgencrypted[4] == 1:
        _DrawCircle(doc, XPos - 1, YPos + 4, Params["FillFactor"]*Size)
    if msgencrypted[5] == 1:
        _DrawCircle(doc, XPos + 1, YPos + 4, Params["FillFactor"]*Size)
    if msgencrypted[6] == 1:
        _DrawCircle(doc, XPos + 3, YPos + 4, Params["FillFactor"]*Size)

    # Third line
    if msgencrypted[7] == 1:
        _DrawCircle(doc, XPos - 2, YPos + 2, Params["FillFactor"]*Size)
    if msgencrypted[8] == 1:
        _DrawCircle(doc, XPos, YPos + 2, Params["FillFactor"]*Size)
    if msgencrypted[9] == 1:
        _DrawCircle(doc, XPos + 2, YPos + 2, Params["FillFactor"]*Size)

    # Fourth line
    if msgencrypted[10] == 1:
        _DrawCircle(doc, XPos - 3, YPos, Params["FillFactor"]*Size)
    if msgencrypted[11] == 1:
        _DrawCircle(doc, XPos - 1, YPos, Params["FillFactor"]*Size)
    if msgencrypted[12] == 1:
        _DrawCircle(doc, XPos + 1, YPos, Params["FillFactor"]*Size)
    if msgencrypted[13] == 1:
        _DrawCircle(doc, XPos + 3, YPos, Params["FillFactor"]*Size)

    # Fifth line
    if msgencrypted[14] == 1:
        _DrawCircle(doc, XPos - 2, YPos - 2, Params["FillFactor"]*Size)
    if msgencrypted[15] == 1:
        _DrawCircle(doc, XPos, YPos - 2, Params["FillFactor"]*Size)
    if msgencrypted[16] == 1:
        _DrawCircle(doc, XPos + 2, YPos - 2, Params["FillFactor"]*Size)

    # Sixth line
    if msgencrypted[17] == 1:
        _DrawCircle(doc, XPos - 3, YPos - 4, Params["FillFactor"]*Size)
    if msgencrypted[18] == 1:
        _DrawCircle(doc, XPos - 1, YPos - 4, Params["FillFactor"]*Size)
    if msgencrypted[19] == 1:
        _DrawCircle(doc, XPos + 1, YPos - 4, Params["FillFactor"]*Size)
    if msgencrypted[20] == 1:
        _DrawCircle(doc, XPos + 3, YPos - 4, Params["FillFactor"]*Size)

    # Seventh line
    if msgencrypted[21] == 1:
        _DrawCircle(doc, XPos - 2, YPos - 6, Params["FillFactor"]*Size)
    if msgencrypted[22] == 1:
        _DrawCircle(doc, XPos, YPos - 6, Params["FillFactor"]*Size)
    if msgencrypted[23] == 1:
        _DrawCircle(doc, XPos + 2, YPos - 6, Params["FillFactor"]*Size)

def _AppendPolyArc(polyline, XCentre, YCentre, Radius, Angle1, Angle2):

    dAngle = (Angle2 - Angle1)/(Params["NoPolyArcPoints"] - 1)
    for i in range(0, Params["NoPolyArcPoints"]):
        angle = (Angle1 + i*dAngle)/180*pi
        X = XCentre + Radius*cos(angle)
        Y = YCentre + Radius*sin(angle)
        polyline.append_points([(X, Y)])

def _GetGeneratorMatrix():

    G = np.array(
    [[1,	1,	0,	1,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0],
    [1,	0,	1,	0,	1,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0],
    [0,	1,	1,	0,	0,	1,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0],
    [1,	1,	1,	0,	0,	0,	1,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0],
    [1,	0,	0,	0,	0,	0,	0,	1,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	1,	0,	0],
    [0,	1,	0,	0,	0,	0,	0,	0,	1,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	1,	0,	0],
    [1,	1,	0,	0,	0,	0,	0,	0,	0,	1,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	1,	0,	0],
    [1,	0,	1,	0,	0,	0,	0,	0,	0,	0,	1,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	1,	0,	0],
    [0,	1,	1,	0,	0,	0,	0,	0,	0,	0,	0,	1,	0,	0,	0,	0,	0,	0,	0,	0,	0,	1,	0,	0],
    [1,	1,	1,	0,	0,	0,	0,	0,	0,	0,	0,	0,	1,	0,	0,	0,	0,	0,	0,	0,	0,	1,	0,	0],
    [1,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	1,	0,	0,	0,	0,	0,	0,	0,	0,	1,	0],
    [1,	1,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	1,	0,	0,	0,	0,	0,	0,	0,	1,	0],
    [1,	0,	1,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	1,	0,	0,	0,	0,	0,	0,	1,	0],
    [0,	1,	1,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	1,	0,	0,	0,	0,	0,	1,	0],
    [1,	1,	1,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	1,	0,	0,	0,	0,	1,	0],
    [1,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	1,	0,	0,	1,	1,	0],
    [1,	1,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	1,	0,	1,	1,	0],
    [1,	0,	1,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	1,	1,	1,	0]])

    G = np.transpose(G)

    return G

def _Encode(XVal, YVal):

    # Interleave bits while inverting order of y
    msg = np.zeros((Params["NoUnencryptedBits"], 1), dtype="uint8")
    for i in range(round(Params["NoUnencryptedBits"]/2)):
        msg[2*i + 0, 0] = (XVal >> (round(Params["NoUnencryptedBits"]/2) - i - 1)) & 1
        msg[2*i + 1, 0] = (YVal >> i) & 1

    # Use generator matrix to obtain encrytped message
    G = _GetGeneratorMatrix()
    msgencrypted = np.matmul(G, msg)
    msgencrypted = msgencrypted % 2
    msgencrypted = msgencrypted.squeeze().tolist()

    return msgencrypted


def CreateDiamondtag(XVal: int, YVal: int, Width: int) -> dict:

    doc = ezdxf.new(dxfversion="R2010")
    doc.layers.add("Diamondtags")
    _DrawDiamondtag(doc, 0.0, 0.0, 1.0, XVal, YVal)
    img = dxf_to_ndarray(doc, Width)

    return {
        'img':     img,
        'XVal':    XVal,
        'YVal':    YVal,
        'Bindata': _Encode(XVal, YVal),
    }
