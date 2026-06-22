# Ralf Mouthaan
# Nanomation
# July 2025
#
# Functions to generate a lithotag

import random
import numpy as np
import ezdxf
from math import sqrt, sin, cos, pi
from Utils.DxfConversion import dxf_to_ndarray
from Utils.Zernike import ApplyZernike

Params = {
    'Poly': True,
    'NoPolyArcPoints': 10,
    'NoPolyCirclePoints': 50,
    'FillFactor': 0.5,
    'NoLithotagRings': 3,
    'NoCheckBits': 3,
    'NoMessageBits': 32
    }

_SIZE_MIN          = 30
_SIZE_MAX          = 150
_NUM_ZERNIKES      = 11
_ZERNIKE_MAX       =  0.75
_TIP_TILT_MAX      =  5.0
_DEFOCUS_MAX       =  5.0
_READ_NOISE_MIN    =  1.0
_READ_NOISE_MAX    =  5.0
_BIAS_MIN          =  0.0
_BIAS_MAX          = 50.0
_ILLUM_MIN         = 100.0
_ILLUM_MAX         = 255.0

def _DrawLithotag(doc, XPos: float, YPos : float, Scale: float, XVal: int, YVal: int):

    _DrawSpine(doc, XPos, YPos, Scale)
    _DrawXVal(doc, XPos, YPos, Scale, XVal)
    _DrawYVal(doc, XPos, YPos, Scale, YVal)
    _DrawXCheck(doc, XPos, YPos, Scale, XVal)
    _DrawYCheck(doc, XPos, YPos, Scale, YVal)

def _DrawSpine(doc, XPos, YPos, Scale):

    if Params["Poly"]:
        _DrawPolySpine(doc, XPos, YPos, Scale)
    else:
        _DrawNonPolySpine(doc, XPos, YPos, Scale)

def _DrawNonPolySpine(doc, XPos, YPos, Scale):

    msp = doc.modelspace()

    SpineLength = Scale * Params["NoLithotagRings"]
    CapRadius = Scale * Params["FillFactor"] * (sqrt(3) - 1)

    # Spine Caps
    N_Cap  = msp.add_arc((XPos, YPos + 2*SpineLength), CapRadius, -180, 0, False)
    SE_Cap = msp.add_arc((XPos + sqrt(3)*SpineLength, YPos -SpineLength), CapRadius, 60, -120, False)
    S_Cap  = msp.add_arc((XPos, YPos - 2*SpineLength), CapRadius, 0, 180, False)
    SW_Cap = msp.add_arc((XPos -sqrt(3)*SpineLength, YPos - SpineLength), CapRadius, -60, 120, False)

    # Spine Fillets
    NE_Fillet = msp.add_arc((XPos + Scale*sqrt(3),   YPos + Scale), Scale*sqrt(3) - CapRadius, -180, -120, True)
    SE_Fillet = msp.add_arc((XPos + Scale*sqrt(3)/2, YPos - Scale*3/2), Scale*sqrt(3)/2 - CapRadius, 60, -180, True)
    SW_Fillet = msp.add_arc((XPos - Scale*sqrt(3)/2, YPos - Scale*3/2), Scale*sqrt(3)/2 - CapRadius, 0, 120, True)
    NW_Fillet = msp.add_arc((XPos - Scale*sqrt(3), YPos + Scale), Scale*sqrt(3) - CapRadius, -60, 0, True)

    # Spine Lines
    msp.add_line(N_Cap.start_point, NE_Fillet.start_point)
    msp.add_line(NE_Fillet.end_point,SE_Cap.end_point)
    msp.add_line(SE_Cap.start_point, SE_Fillet.start_point)
    msp.add_line(SE_Fillet.end_point, S_Cap.end_point)
    msp.add_line(S_Cap.start_point, SW_Fillet.start_point)
    msp.add_line(SW_Fillet.end_point, SW_Cap.end_point)
    msp.add_line(SW_Cap.start_point, NW_Fillet.start_point)
    msp.add_line(NW_Fillet.end_point, N_Cap.end_point)

def _DrawPolySpine(doc, XPos, YPos, Scale):

    msp = doc.modelspace()

    SpineLength = Scale * Params["NoLithotagRings"]
    CapRadius = Scale * Params["FillFactor"] * (sqrt(3) - 1)

    Spine = msp.add_lwpolyline([])
    _AppendPolyArc(Spine, XPos, YPos + 2*SpineLength, CapRadius, 180, 0) # North Cap
    _AppendPolyArc(Spine, XPos + Scale*sqrt(3),   YPos + Scale, Scale*sqrt(3) - CapRadius, -180, -120) # NE Fillet
    _AppendPolyArc(Spine, XPos + sqrt(3)*SpineLength, YPos -SpineLength, CapRadius, 60, -120) # SE Cap
    _AppendPolyArc(Spine, XPos + Scale*sqrt(3)/2, YPos - Scale*3/2, Scale*sqrt(3)/2 - CapRadius, 60, 180) # SE Fillet
    _AppendPolyArc(Spine, XPos, YPos - 2*SpineLength, CapRadius, 0, -180) # S Cap
    _AppendPolyArc(Spine, XPos - Scale*sqrt(3)/2, YPos - Scale*3/2, Scale*sqrt(3)/2 - CapRadius, 0, 120) # SW Fillet
    _AppendPolyArc(Spine, XPos -sqrt(3)*SpineLength, YPos - SpineLength, CapRadius, 300, 120) # SW Cap
    _AppendPolyArc(Spine, XPos - Scale*sqrt(3), YPos + Scale, Scale*sqrt(3) - CapRadius, -60, 0) # NW Fillet
    Spine.closed = True

def _GetCoordinateLocs(strXY, XPos, YPos, Scale):

    if isinstance(strXY, str) == False:
        raise NameError("Expecting string")

    if strXY == "X":
        direction = -1
    elif strXY == "Y":
        direction = 1
    else:
        raise NameError("Expecting X or Y")

    arrX = [0]*9
    arrY = [0]*9
    idx = -1

    for idxCol in range(1, Params["NoLithotagRings"] + 1):
        for idxRow in range(1, Params["NoLithotagRings"] + 1):
            idx = idx + 1
            arrX[idx] = XPos + idxCol*cos(pi/6)*direction*2*Scale
            arrY[idx] = YPos + (-idxCol*sin(pi/6)*2 + 2*(4 - idxRow))*Scale

    return arrX, arrY

def _GetChecksumLocs(strXY, XPos, YPos, Scale):

    if isinstance(strXY, str) == False:
        raise NameError("Expecting string")

    if strXY == "X":
        direction = -1
    elif strXY == "Y":
        direction = 1
    else:
        raise NameError("Expecting X or Y")

    arrX = [0]*3
    arrY = [0]*3
    idx = -1
    idxRow = 1
    idxCol = 1

    for idxBit in range(1, round(Params["NoLithotagRings"]*(Params["NoLithotagRings"] - 1)/2) + 1):
        idx = idx + 1
        arrX[idx] = XPos + idxCol*cos(pi/6)*direction*2*Scale
        arrY[idx] = YPos + (-idxCol*sin(pi/6)*2 - 2*idxRow)*Scale
        if idxCol + idxRow > Params["NoLithotagRings"] - 1:
            idxCol = 1
            idxRow = idxRow + 1
        else:
            idxCol = idxCol + 1

    return arrX, arrY

def _GetXCoordinateLocs(XPos, YPos, Scale):
    return _GetCoordinateLocs("X", XPos, YPos, Scale)

def _GetYCoordinateLocs(XPos, YPos, Scale):
    return _GetCoordinateLocs("Y", XPos, YPos, Scale)

def _GetXChecksumLocs(XPos, YPos, Scale):
    return _GetChecksumLocs("X", XPos, YPos, Scale)

def _GetYChecksumLocs(XPos, YPos, Scale):
    return _GetChecksumLocs("Y", XPos, YPos, Scale)

def _EncodeCheckSum(intCoordinate):

    if isinstance(intCoordinate, int) == False:
        raise NameError("Coordinate must be integer")
    if intCoordinate < 0:
        raise NameError("Coordinates must be positive")

    divisor = pow(2, Params["NoCheckBits"] + 1) - 1;
    divisor = divisor << Params["NoMessageBits"] - Params["NoCheckBits"] - 1
    divisor = divisor << Params["NoCheckBits"]
    remainder = intCoordinate << Params["NoCheckBits"]

    for k in range (1, Params["NoMessageBits"] + 1):
        if (remainder >> Params["NoMessageBits"] + Params["NoCheckBits"] - 1) & 1:
            remainder = remainder ^ divisor;
        remainder = remainder << 1
    intCheckSum = remainder >> Params["NoMessageBits"]

    return intCheckSum

def _DrawNumber(doc, intNumber, Scale, arrX, arrY):

    if len(arrX) != len(arrY):
        raise NameError("Expect length of arrX to be equal to length of arrY")

    for idxBit in range(0, len(arrX)):
        if not ((intNumber >> idxBit) & 1):
            _DrawCircle(doc, arrX[idxBit], arrY[idxBit], Scale*Params["FillFactor"])

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

def _DrawXVal(doc, XPos, YPos, Scale, XVal):
    [x_pos, y_pos] = _GetXCoordinateLocs(XPos, YPos, Scale)
    _DrawNumber(doc, XVal, Scale, x_pos, y_pos)

def _DrawYVal(doc, XPos, YPos, Scale, YVal):
    [x_pos, y_pos] = _GetYCoordinateLocs(XPos, YPos, Scale)
    _DrawNumber(doc, YVal, Scale, x_pos, y_pos)

def _DrawXCheck(doc, XPos, YPos, Scale, XVal):
    XCheck = _EncodeCheckSum(XVal)
    [x_pos, y_pos] = _GetXChecksumLocs(XPos, YPos, Scale)
    _DrawNumber(doc, XCheck, Scale, x_pos, y_pos)

def _DrawYCheck(doc, XPos, YPos, Scale, YVal):
    YCheck = _EncodeCheckSum(YVal)
    [x_pos, y_pos] = _GetYChecksumLocs(XPos, YPos, Scale)
    _DrawNumber(doc, YCheck, Scale, x_pos, y_pos)

def _AppendPolyArc(polyline, XCentre, YCentre, Radius, Angle1, Angle2):

    dAngle = (Angle2 - Angle1)/(Params["NoPolyArcPoints"] - 1)
    for i in range(0, Params["NoPolyArcPoints"]):
        angle = (Angle1 + i*dAngle)/180*pi
        X = XCentre + Radius*cos(angle)
        Y = YCentre + Radius*sin(angle)
        polyline.append_points([(X, Y)])


def TagValuesToBin(XVal: int, YVal: int, XCheck: int, YCheck: int) -> np.ndarray:

    NoBits = Params["NoLithotagRings"] ** 2
    NoCheckBits = Params["NoCheckBits"]
    result = np.zeros(2 * NoBits + 2 * NoCheckBits, dtype=int)

    for i in range(NoBits):
        result[i] = (XVal >> i) & 1
    for i in range(NoBits):
        result[NoBits + i] = (YVal >> i) & 1
    for i in range(NoCheckBits):
        result[2*NoBits + i] = (XCheck >> i) & 1
    for i in range(NoCheckBits):
        result[2*NoBits + NoCheckBits + i] = (YCheck >> i) & 1

    return result

def BinToTagValues(arrBin: np.ndarray) -> tuple:

    NoBits = Params["NoLithotagRings"] ** 2
    NoCheckBits = Params["NoCheckBits"]

    XVal   = int(sum(arrBin[i] << i for i in range(NoBits)))
    YVal   = int(sum(arrBin[NoBits + i] << i for i in range(NoBits)))
    XCheck = int(sum(arrBin[2*NoBits + i] << i for i in range(NoCheckBits)))
    YCheck = int(sum(arrBin[2*NoBits + NoCheckBits + i] << i for i in range(NoCheckBits)))

    return XVal, YVal, XCheck, YCheck

def CreateLithotag(XVal: int, YVal: int, Width: int) -> dict:

    doc = ezdxf.new(dxfversion="R2010")
    doc.layers.add("Lithotags")
    _DrawLithotag(doc, 0.0, 0.0, 1.0, XVal, YVal)
    img = dxf_to_ndarray(doc, Width)

    return {
        'img':    img,
        'XVal':   XVal,
        'YVal':   YVal,
        'XCheck': _EncodeCheckSum(XVal),
        'YCheck': _EncodeCheckSum(YVal),
        'Width':  Width
    }

class LithotagIterator:

    def __iter__(self):
        return self

    def __next__(self) -> dict:
        size = random.randint(_SIZE_MIN, _SIZE_MAX)
        xval = random.randint(0, 100)
        yval = random.randint(0, 100)

        result = CreateLithotag(xval, yval, size)

        coeffs = [0.0,
                  random.uniform(-_TIP_TILT_MAX, _TIP_TILT_MAX),
                  random.uniform(-_TIP_TILT_MAX, _TIP_TILT_MAX),
                  random.uniform(-_DEFOCUS_MAX,  _DEFOCUS_MAX)] + \
                 [random.uniform(-_ZERNIKE_MAX, _ZERNIKE_MAX)
                  for _ in range(_NUM_ZERNIKES - 3)]
        result['coeffs'] = coeffs

        # TODO:
        # Make sure this all works
        # Add some kind of offset?
        # Multiply by random number instead of 255 to account for different illuminations
        result['img'] = result['img']
        result['img'] = result['img'] * random.uniform(_ILLUM_MIN, _ILLUM_MAX)
        result['img'] = result['img'].astype(np.float32)
        result['img'] = ApplyZernike(result['img'], *coeffs)
        result['img'] = np.random.poisson(result['img'])
        result['img'] = result['img'].astype(np.float32)
        result['img'] += np.random.normal(0.0, random.uniform(_READ_NOISE_MIN, _READ_NOISE_MAX), result['img'].shape)
        result['img'] += random.uniform(_BIAS_MIN, _BIAS_MAX)
        result['img'] = np.clip(result['img'], 0, 255)
        result['img'] = result['img'].astype(np.uint8)

        return result
