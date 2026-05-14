import numpy as np
import cv2
from colour_detecter import detect_orange

kf = cv2.KalmanFilter(4,2)
kf.transitionMatrix = np.array([[1,0,0.033,0],[0,1,0,0.033],[0,0,1,0],[0,0,0,1]], np.float32)
kf.measurementMatrix = np.array([[1,0,0,0],[0,1,0,0]],np.float32)
kf.processNoiseCov = np.eye(4, dtype=np.float32)*0.03
kf.measurementNoiseCov = np.eye(2, dtype=np.float32)*0.05
kf.errorCovPost = np.eye(4, dtype=np.float32)*100
kf.statePost = np.array([0,0,0,0],np.float32).reshape(4, 1)

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    frame,x_pos,y_pos,contour_area = detect_orange(frame)
    if contour_area > 4000:
        print("TOOCLOSE")
        
        cv2.imshow('Alert', frame)
        cv2.waitKey(4)
        break
    if x_pos:
        prediction = kf.predict()
        measurement = np.array([[x_pos], [y_pos]], np.float32)
        kf.correct(measurement)
        new_state = kf.statePost
        tracked_x = int(new_state[0][0])
        tracked_y = int(new_state[1][0])
        cv2.circle(frame, (tracked_x, tracked_y), 10, (0, 255, 0), -1)
    cv2.imshow('Orange Detection', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()