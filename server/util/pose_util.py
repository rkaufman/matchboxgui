'''
Determine pose: pitch, roll, yaw

This is based on open source code:
    https://github.com/jerryhouuu/Face-Yaw-Roll-Pitch-from-Pose-Estimation-using-OpenCV

Additional information on calculations here:
    https://www.learnopencv.com/head-pose-estimation-using-opencv-and-dlib/

Also, note the CNN implementation:
    https://github.com/mpatacchiola/deepgaze/tree/2.0/deepgaze

Landmark detection yields 68 landmarks. Pass only select landmarks for pose.
'''
import cv2

import dlib
import numpy as np
import math
import util.mlconstants as mlconstants
import distro


def get_pose(image_size, nose, chin, eye_lcorner, eye_rcorner, mouth_l, mouth_r):
    platform = ''
    (dist, _, _) = distro.linux_distribution()
    if "Mendel" in dist:
        platform = 'coral'

    #2D image points. If you change the image, you need to change vector
    image_points = np.array([   (nose),                     # Nose tip
                                (chin),                     # Chin
                                (eye_lcorner),              # Lt eye lt corner
                                (eye_rcorner),              # Rt eye rt corner
                                (mouth_l),                  # Left Mouth corner
                                (mouth_r)                   # Right mouth corner
                            ], dtype="double")

    # 3D model points. This would need to be adjusted for use with eye centers.
    model_points = np.array([   (0.0, 0.0, 0.0),            # Nose tip
                                (0.0, -330.0, -65.0),       # Chin
                                (-225.0, 170.0, -135.0),    # Lt eye lt corner
                                (225.0, 170.0, -135.0),     # Rt eye rt corner
                                (-150.0, -150.0, -125.0),   # Left Mouth corner
                                (150.0, -150.0, -125.0)     # Right mouth corner
                            ])

    # Camera internals
    focal_length = image_size[1]
    print("focal_length", focal_length)
    center = (image_size[1]/2, image_size[0]/2)
    camera_matrix = np.array(   [[focal_length, 0, center[0]],
                                [0, focal_length, center[1]],
                                [0, 0, 1]], dtype = "double"
                             )

    # print("Camera Matrix :\n {0}".format(camera_matrix))
    dist_coeffs = np.zeros((4,1)) # Assuming no lens distortion
    if platform == 'coral':
        flags = cv2.SOLVEPNP_ITERATIVE
    else:
        flags = cv2.cv2.SOLVEPNP_ITERATIVE

    (success, rotation_vector, translation_vector) = cv2.solvePnP(model_points, image_points, camera_matrix, dist_coeffs, flags=flags)
    # print("Rotation Vector:\n {0}".format(rotation_vector))
    # print("Translation Vector:\n {0}".format(translation_vector))

    rvec_matrix = cv2.Rodrigues(rotation_vector)[0]
    proj_matrix = np.hstack((rvec_matrix, translation_vector))
    eulerAngles = cv2.decomposeProjectionMatrix(proj_matrix)[6]

    pitch, yaw, roll = [math.radians(_) for _ in eulerAngles]

    # TODO - compare these values with ground truth
    pitch = -math.degrees(math.asin(math.sin(pitch))) #JA: had to minus this one
    roll = -math.degrees(math.asin(math.sin(roll)))
    yaw = -math.degrees(math.asin(math.sin(yaw))) #JA: had to minus this one


    # Project a 3D point (0, 0, 1000.0) onto the image plane.
    # We use this to draw a line pointing out from the nose
    (nose_end_point2D, jacobian) = cv2.projectPoints(np.array([(0.0, 0.0, 1000.0)]), rotation_vector, translation_vector, camera_matrix, dist_coeffs)
    p1 = ( int(image_points[0][0]), int(image_points[0][1]))
    p2 = ( int(nose_end_point2D[0][0][0]), int(nose_end_point2D[0][0][1]))

    return(p1, p2, pitch, yaw, roll)


# Eye cordinates include corners, but not center. So calculate eye centers.
def get_centroid(arr):
    '''
    Pass and array of ponts. Example:
        [[319 750]
         [340 734]
         [352 749]
         [332 764]]
    Returns center point: (x, y)
    '''
    length = len(arr)
    sum_x = np.sum(arr[:, 0])
    sum_y = np.sum(arr[:, 1])
    return sum_x/length, sum_y/length


# Draw points on image for debugging
def draw_landmarks(image, x1, y1, x2, y2):
    '''
    Draw landmarks on image, x1, y1, x2, y2 is the bounding box of face.
    '''
    drect = dlib.rectangle(x1, y1, x2, y2)
    predictor = dlib.shape_predictor(mlconstants.DLIB_LANDMARK_MODEL)
    landmarks = predictor(image, drect)
    for i in range (68):
        # Maybe only display a subset of points
        if True:
        # if i in [37, 38, 40, 41, 43, 44, 46, 47, 30, 48, 54, 8]: # this would draw just the points we want
            x = landmarks.part(i).x
            y = landmarks.part(i).y
            # Dots
            #cv2.circle(img, (x, y), radius = 5, color = (255, 255, 0), thickness = -1)
            # Text with point ID. This helps determine which point IDs of the 68 represent
            #    the points we care about: chin, nose, eyes, etc.
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(image, str(i), (x, y), font, 0.4, (0, 255, 0), 1, cv2.LINE_AA)

    return image


# Draw all points provided for debugging
def draw_points(image, points):
    """
    Draw all lansmarks.
    """
    for point in points:
        img = cv2.circle(img, point, radius = 5, color = (255, 255, 255), thickness = -1)
    return image


# Draw just the points relevant for the pose model.
# This includes eye centers an corners.
# Some models/calculations use eye centers vs corners
def draw_model_points(image, nose, chin, eye_lcenter, eye_rcenter, mouth_l, mouth_r, eye_lcorner, eye_rcorner):
    """
    Draw just the landmarks used for the pose determination model. Include both eye center and eye corner.
    """
    image = cv2.circle(image, nose, radius = 5, color = (255, 255, 255), thickness = -1)
    image = cv2.circle(image, chin, radius = 5, color = (255, 255, 255), thickness = -1)
    image = cv2.circle(image, eye_lcenter, radius = 5, color = (0, 0, 255), thickness = -1)
    image = cv2.circle(image, eye_rcenter, radius = 5, color = (255, 0, 0), thickness = -1)
    image = cv2.circle(image, mouth_l, radius = 15, color = (0, 0, 255), thickness = -1)
    image = cv2.circle(image, mouth_r, radius = 15, color = (255, 0, 0), thickness = -1)
    image = cv2.circle(image, eye_lcorner, radius = 15, color = (0, 0, 255), thickness = -1)
    image = cv2.circle(image, eye_rcorner, radius = 15, color = (255, 0, 0), thickness = -1)
    return image
