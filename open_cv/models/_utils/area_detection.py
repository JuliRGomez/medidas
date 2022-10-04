import cv2 
from scipy.spatial import distance as dist
def Detect(image,aruco_size):
    points_dict = {}
    constants_l=[]
    aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_7X7_50)
    aruco_params = cv2.aruco.DetectorParameters_create()
    (corners, ids, rejected) = cv2.aruco.detectMarkers(image, aruco_dict,parameters=aruco_params)
    if len (corners) > 0:
        ids =  ids.flatten()
        if len(ids)>=4:
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
                cX = int((topLeft[0] + bottomRight[0]) / 2.0)
                cY = int((topLeft[1] + bottomRight[1]) / 2.0)
                l1 = dist.euclidean((topLeft[0],topLeft[1]),(topRight[0],topRight[1]))
                l2 = dist.euclidean((topRight[0],topRight[1]),(bottomRight[0],bottomRight[1]))
                constants_l.append(aruco_size/((l1 +l2) / 2))            
                points_dict[str(markerID)] = {'centroid':(cX,cY)}

            constant_scale = sum (constants_l)/len(constants_l)
            points=[points_dict['1'].get('centroid'),points_dict['2'].get('centroid'),points_dict['3'].get('centroid'),points_dict['4'].get('centroid')]
            points_to_reduce = [points_dict['1'].get('centroid'),points_dict['4'].get('centroid')]
            return (image,points,constant_scale,points_to_reduce)
        else:
            return (image,[],0,[])
            # return [points_dict['1'].get('centroid'),points_dict['2'].get('centroid'),points_dict['3'].get('centroid'),points_dict['4'].get('centroid')] 
    else:
        return (image,[],0,[])
