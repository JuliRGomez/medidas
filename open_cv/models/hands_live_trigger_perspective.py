
import numpy as np  
import cv2
from scipy.spatial import distance as dist
import imutils
import mediapipe as mp
import time
from _utils import area_detection,area_trace

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands 
capture = cv2.VideoCapture(0)#doidcam 3
distance = 0
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
        (arucos,points,constant,points_to_reduce) = area_detection.Detect(image)

        if len(points)>0:
            new_height = points_to_reduce.get('4')[1]
            new_width = points_to_reduce.get('4')[0]-points_to_reduce.get('1')[0]

            dst =  area_trace.Align(image,points,width,height)
            image = cv2.flip(dst, 1)                
            image_rgb =cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            centroids = {'Left':{'cx':0,'cy':0},'Right':{'cx':0,'cy':0}}
            shot_data = {'Left':{'distance':0},'Right':{'distance':0}}
            hands_label = {'0':'','1':''}

            results = hands.process(image_rgb)
            try:
                hands_label[str(results.multi_handedness[0].classification[0].index)] = results.multi_handedness[0].classification[0].label
            except:
                pass
            try:
                hands_label[str(results.multi_handedness[1].classification[0].index)] = results.multi_handedness[1].classification[0].label
            except:
                pass
            if results.multi_hand_landmarks is not None:
                index = 0 
                for hand_landmarks in results.multi_hand_landmarks:
                    x1 = int(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x*width)
                    y1 = int(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y*height)
                    
                    thumb_cx = int(hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x*width)
                    thumb_cy = int(hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y*height)
                    index_pip_cx = int(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP].x*width)
                    index_pip_cy = int(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP].y*height)
                    distance_shot = int(dist.euclidean((thumb_cx,thumb_cy),(index_pip_cx,index_pip_cy)))
                    shot_data[hands_label.get(str(index))] = {'distance':distance_shot}

                    centroids[hands_label.get(str(index))] = {'cx':x1,'cy':y1}
                    cv2.circle(dst,(x1,y1),3,(255,0,0),3)
                    index += 1
        
                if centroids.get('Left').get('cx')>0 and centroids.get('Right').get('cx')>0:
                    
                    cv2.line(dst, (centroids.get('Left').get('cx'),centroids.get('Left').get('cy')), (centroids.get('Right').get('cx'),centroids.get('Right').get('cy')),
                                    (0, 0, 255), 2)#amarilla
                    distance = dist.euclidean((centroids.get('Left').get('cx'), centroids.get('Left').get('cy')), (centroids.get('Right').get('cx'), centroids.get('Right').get('cy')))
                    distance_scale = distance*constant
                    cv2.putText(dst, "{:.1f} cm".format(distance_scale),
                                                (int( centroids.get('Left').get('cx')+ 100), centroids.get('Left').get('cy')-15), cv2.FONT_HERSHEY_SIMPLEX,
                                                1, (255,0, 0), 2)

                    if shot_data.get('Left').get('distance')>0 and shot_data.get('Right').get('distance')>0 :
                        if shot_data.get('Left').get('distance')<45 and shot_data.get('Right').get('distance')<45 :
                            cv2.putText(dst, "{}".format("Disparo!"),
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

            cv2.imshow('salida',dst)
        cv2.imshow('Original',arucos)    
        if cv2.waitKey(1) & 0xFF == 27:
            break

capture.release()
cv2.destroyAllWindows()