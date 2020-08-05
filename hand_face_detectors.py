import cv2
import numpy as np
import cvlib as cv
from hand_utils import object_detect_utils as hand_utils
from shapely.geometry import Polygon


class Detector:
    detector_params = {}
    detector = None

    def __init__(self):
        pass

    def set_detector_params(self, params):
        self.detector_params = params

    def detect(self):
        pass


class CVLibDetector(Detector):
    def __init__(self):
        self.detector = cv

    def detect(self, rgb_image):
        # returns an array of (top, right, bottom, left)
        objects, confidences = self.detector.detect_face(rgb_image)
        # change to an array of (x, y, w, h)
        return [(top, left, bottom - top, right - left) for (top, right, bottom, left) in objects]


class TSDetector(Detector):
    def __init__(self):
        self.detection_graph, self.sess = hand_utils.load_inference_graph()

    def detect(self, rgb_image):
        # returns (top [0], left [1], bottom [2], right [3])
        boxes, confidences = hand_utils.detect_objects(rgb_image, self.detection_graph, self.sess)

        im_height, im_width = rgb_image.shape[:2]

        detection_th = self.detector_params.get('detection_th', 0.1)
        objects = [(box[0] * im_height, box[3] * im_width, box[2] * im_height, box[1] * im_width) for box, score in
                   zip(boxes, confidences) if score >= detection_th]
        # change to an array of (x, y, w, h)
        return [(int(left), int(top), int(right - left), int(bottom - top)) for (top, right, bottom, left) in objects]


# add objects (hands and face) to frame
def addObjs(img1, objects, color=(255, 0, 0)):
    img = np.copy(img1)
    for (x, y, w, h) in objects:
        img = cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
    return img


# convert the object to a polygon
def obj_poly(obj):
    x, y, w, h = obj
    return Polygon([(x, y), (x + w, y), (x + w, y + h), (x, y + h)])

# convert to polygon and check if face and hands intersect
def objects_intersect(face, hands):
    if face and hands:
        facePoly = obj_poly(face[0])
        for hand in hands:
            handPoly = obj_poly(hand)
            if facePoly.intersects(handPoly):
                return True
    return False
