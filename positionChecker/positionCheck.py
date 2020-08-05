import cv2
import dlib
import numpy as np
from imutils import face_utils
import sys
import base64

### CONVERTING IMAGE FROM BASE64
import io
import cv2
import base64 
import numpy as np
from PIL import Image

#testing

class PositionChecker(object):
    global s
    global i

    def __init__(self):
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor("./positionChecker/face_landmarks.dat")
        K = [6.5308391993466671e+002, 0.0, 3.1950000000000000e+002,
            0.0, 6.5308391993466671e+002, 2.3950000000000000e+002,
            0.0, 0.0, 1.0]
        D = [7.0834633684407095e-002, 6.9140193737175351e-002, 0.0, 0.0, -1.3073460323689292e+000]
        self.cam_matrix = np.array(K).reshape(3, 3).astype(np.float32)
        self.dist_coeffs = np.array(D).reshape(5, 1).astype(np.float32)

        self.object_pts = np.float32([[6.825897, 6.760612, 4.402142],
                                [1.330353, 7.122144, 6.903745],
                                [-1.330353, 7.122144, 6.903745],
                                [-6.825897, 6.760612, 4.402142],
                                [5.311432, 5.485328, 3.987654],
                                [1.789930, 5.393625, 4.413414],
                                [-1.789930, 5.393625, 4.413414],
                                [-5.311432, 5.485328, 3.987654],
                                [2.005628, 1.409845, 6.165652],
                                [-2.005628, 1.409845, 6.165652],
                                [2.774015, -2.080775, 5.048531],
                                [-2.774015, -2.080775, 5.048531],
                                [0.000000, -3.116408, 6.097667],
                                [0.000000, -7.415691, 4.070434]])

        self.reprojectsrc = np.float32([[10.0, 10.0, 10.0],
                                [10.0, 10.0, -10.0],
                                [10.0, -10.0, -10.0],
                                [10.0, -10.0, 10.0],
                                [-10.0, 10.0, 10.0],
                                [-10.0, 10.0, -10.0],
                                [-10.0, -10.0, -10.0],
                                [-10.0, -10.0, 10.0]])

        self.line_pairs = [[0, 1], [1, 2], [2, 3], [3, 0],
                    [4, 5], [5, 6], [6, 7], [7, 4],
                    [0, 4], [1, 5], [2, 6], [3, 7]]
        

        print('created!')

    
    # I need to know solvePnP.

    def get_head_pose(self, shape):

        image_pts = np.float32([shape[17], shape[21], shape[22], shape[26], shape[36],
                                shape[39], shape[42], shape[45], shape[31], shape[35],
                                shape[48], shape[54], shape[57], shape[8]])

        _, rotation_vec, translation_vec = cv2.solvePnP(self.object_pts, image_pts, self.cam_matrix, self.dist_coeffs)

        reprojectdst, _ = cv2.projectPoints(self.reprojectsrc, rotation_vec, translation_vec, self.cam_matrix,
                                            self.dist_coeffs)

        reprojectdst = tuple(map(tuple, reprojectdst.reshape(8, 2)))

        # calc euler angle
        rotation_mat, _ = cv2.Rodrigues(rotation_vec)
        pose_mat = cv2.hconcat((rotation_mat, translation_vec))
        _, _, _, _, _, _, euler_angle = cv2.decomposeProjectionMatrix(pose_mat)
        #"""yaw = euler_angle[1], roll = euler_angle[2], pitch = euler_angle[0]"""

        
        s=''
        i=0
        pit = [0,0,0,0,0,0,0]

        j=i%7
        i+=1;

        #print(i)
        pit[j]=euler_angle[0]
        avg=0
        
        
        if(j==0):  
            for k in range(7):
                avg+=pit[k]
            if(avg/7>2 and avg/7<=17):
                s= "Humped Back Sitting."
                
            elif(avg/7<-2 and avg/7>=-17):
                s = 'Inclined Sitting Position.'
            
            elif(avg/7>17):
                s = 'You are looking down.'
                
            elif(avg/7<-17):
                s = 'You are overly inclined.'
            
            else:
                s = "You are approximatly sitting straight."
        print(s)

        return [reprojectdst, euler_angle, s]
    
   

    def check_position(self, image):
        # return

        ### LOADS IN TEMPORARY PHOTO SAMPLE ####
        #img = cv2.imread(cv2.samples.findFile("temp_photo.jpg"))
        #if img is None:
        #    sys.exit("Could not read the image.")
       
        #print(image)

        #image = Image.open('image.jpg')

        ## this opens up image popup #######
        #image.show()

        frame = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

        #print(image) 
        
        # cv2.imshow('image', frame)
        # cv2.waitKey(0)
        face_rects = self.detector(frame, 0)
        print(face_rects)
                
        if (len(face_rects)==0):
            print("I can't see you")
                    #if( s=='You are looking down.' or s== 'Humped Back Sitting.'):
                    #    print("extremely down.")
                    #elif(s=='Inclined Sitting Position.' or s=='You are overly inclined.'):
                    #    print("You are overly inclined.")
                    #print("WHEN FACE_RECT == 0: " + s)

        response = "no image detected"                
        if len(face_rects) > 0:
            print("greater than 0")
            shape = self.predictor(frame, face_rects[0])
            shape = face_utils.shape_to_np(shape)
            """if 'shape' is locals():
                print('we got it')"""
                    
            poseArray = self.get_head_pose(shape)
            response = poseArray[2]

        #cv2.imshow("Display window", img)
        #k = cv2.waitKey(0)
        
        return response
                

    
        
    def checkPosition(self, image):
        print('thanks for the image!')
        results = {}
        results['posture'] = "straight"
        return results