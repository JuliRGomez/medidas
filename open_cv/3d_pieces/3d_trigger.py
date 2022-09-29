from dis import dis
import numpy as np
import cv2
from scipy.spatial import distance as dist
import imutils
import mediapipe as mp
import time

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands 
capture = cv2.VideoCapture(1)#doidcam 3
arucoDict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_7X7_50)
arucoParams = cv2.aruco.DetectorParameters_create()
shot_measure = []
distance_scale = 0
with mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.7) as hands:
    while (capture.isOpened()):
        ret, frame = capture.read()
        image = imutils.resize(frame,width=780)
        height, width, _ = image.shape
        (corners, ids, rejected) = cv2.aruco.detectMarkers(image, arucoDict,parameters=arucoParams)
        
        image_shot = cv2.flip(image, 1)                
        image_rgb =cv2.cvtColor(image_shot, cv2.COLOR_BGR2RGB)
        shot_data = {'1':{'distance':0},'2':{'distance':0}}
        results = hands.process(image_rgb)

        if results.multi_hand_landmarks is not None:
            index = 0 
            for hand_landmarks in results.multi_hand_landmarks:
                index += 1
                thumb_cx = int(hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x*width)
                thumb_cy = int(hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y*height)
                index_pip_cx = int(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP].x*width)
                index_pip_cy = int(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP].y*height)
                distance = int(dist.euclidean((thumb_cx,thumb_cy),(index_pip_cx,index_pip_cy)))
                shot_data[str(index)] = {'distance':distance}

        if len (corners) > 0:
            constants = []
            ids =  ids.flatten()
            centroids={'1':{},'2':{}}
            for (markerCorner,markerID) in zip(corners,ids):
                corners = markerCorner.reshape((4, 2))
                (topLeft, topRight, bottomRight, bottomLeft) = corners
                topRight = (int(topRight[0]), int(topRight[1]))
                bottomRight = (int(bottomRight[0]), int(bottomRight[1]))
                bottomLeft = (int(bottomLeft[0]), int(bottomLeft[1]))
                topLeft = (int(topLeft[0]), int(topLeft[1]))
                cv2.line(image, topLeft, topRight, (0, 255, 0), 2)
                cv2.line(image, topRight, bottomRight, (0, 255, 0), 2)
                cv2.line(image, bottomRight, bottomLeft, (0, 255, 0), 2)
                cv2.line(image, bottomLeft, topLeft, (0, 255, 0), 2)
                l1 = dist.euclidean((topLeft[0],topLeft[1]),(topRight[0],topRight[1]))
                l2 = dist.euclidean((topRight[0],topRight[1]),(bottomRight[0],bottomRight[1]))
                constante_l1=2.58/l1
                constante_l2=2.58/l2
                constants.append(constante_l1)
                constants.append(constante_l2)
                cX = int((topLeft[0] + bottomRight[0]) / 2.0)
                cY = int((topLeft[1] + bottomRight[1]) / 2.0)
                centroids[str(markerID)] = {'id':markerID,'cx':cX,'cy':cY}
                cv2.circle(image, (cX, cY), 4, (0, 0, 255), -1)
                cv2.putText(image, str(markerID),(topLeft[0], topLeft[1] - 15), cv2.FONT_HERSHEY_SIMPLEX,0.5, (0, 255, 0), 2)

            if len(constants)>=4:
                constant_sum = sum(constants)
                constant_average = constant_sum / 4
                cv2.line(image, (centroids.get('1').get('cx'),centroids.get('1').get('cy')), (centroids.get('2').get('cx'),centroids.get('2').get('cy')),
                                (0, 0, 255), 2)#amarilla
                distance = dist.euclidean((centroids.get('1').get('cx'), centroids.get('1').get('cy')), (centroids.get('2').get('cx'), centroids.get('2').get('cy')))
                distance_scale = distance*constant_average
                cv2.putText(image, "{:.1f} cm".format(distance_scale),
                                    (int( centroids.get('1').get('cx')+ 100), centroids.get('1').get('cy')-15), cv2.FONT_HERSHEY_SIMPLEX,
                                    1.5, (255,0, 0), 2)
                
                if shot_data.get('1').get('distance')>0 and shot_data.get('2').get('distance')>0 :
                    if shot_data.get('1').get('distance')<45 and shot_data.get('2').get('distance')<45 :
                        cv2.putText(image, "{}".format("Disparo!"),
                                                        (int( width/2), int(height/2)), cv2.FONT_HERSHEY_SIMPLEX,
                                                        1, (255,0, 0), 2)
                        shot_measure.append(distance_scale)
                        if len(shot_measure)>=5:
                            frames_sum = sum(shot_measure)
                            shot_average = frames_sum/5
                            print('--------Promedio de muestra--------')
                            print(shot_average)
                            print('-----------------------------------')
                            time.sleep(2.5)
                            shot_measure.clear()

        cv2.imshow("contornos", image)
        if (cv2.waitKey(1) == ord('s')):
            break

capture.release()
cv2.destroyAllWindows()