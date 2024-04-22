import numpy as np
import cvlib as cv

def face_detect(frame):
    face, confidence = cv.detect_face(frame)
    result = None
    if confidence and confidence[0] > 0.9:
        print('프레임 받음')
        for idx, f in enumerate(face):
            result = frame[f[1]:f[3], f[0]:f[2], :]
    return result
