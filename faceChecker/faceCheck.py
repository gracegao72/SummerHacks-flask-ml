import cv2
import subprocess
import numpy
from hand_face_detectors import CVLibDetector
from hand_face_detectors import TSDetector
from hand_face_detectors import addObjs
from hand_face_detectors import objects_intersect

# test


class FaceChecker(object):
    def __init__(self):
        print('created!')

        self.FaceDetector = CVLibDetector()
        self.HandsDetector = TSDetector()

    def checkPosition(self, image):
        #print('thanks for the image!')
        results = {}

        #image.show()

        rgb = cv2.cvtColor(numpy.array(image), cv2.COLOR_BGR2RGB)
        #cv2.imshow("anything", rgb)
        #app.pycv2.waitKey(0)

        hands = self.HandsDetector.detect(rgb)
        face = self.FaceDetector.detect(rgb)

        # add detected face and hands to frampe
        #detect_img = addObjs(rgb, hands)
        #detect_img = addObjs(detect_img, face, color=(0, 255, 0))

        # display frame with added objects
        #cv2.imshow('frame', cv2.cvtColor(detect_img, cv2.COLOR_RGB2BGR))

        print(face, hands)

        if objects_intersect(face, hands):
            results['hand_detection'] = True
            #subprocess.call(["afplay", "beepaudio.wav"])
        else:
            results['hand_detection'] = False
        
        print(results)
    
        return results