import cv2
import numpy as np

x_pos = 0
y_pos= 0
head_area = 0

def keep_previous(old_x,old_y,old_area):
    global x_pos,y_pos,head_area
    x_pos,y_pos,head_area = old_x,old_y,old_area

def detect_orange(frame):

    # Apply CLAHE for lighting 
    lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    l = clahe.apply(l)
    frame = cv2.cvtColor(cv2.merge([l, a, b]), cv2.COLOR_LAB2BGR)
    
    # Apply bilateral filter
    frame = cv2.bilateralFilter(frame, 9, 75, 75)
    
    # Convert to HSV for Mask
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_orange = np.array([12, 109, 228])
    upper_orange = np.array([51, 255, 255])
    mask = cv2.inRange(hsv, lower_orange, upper_orange)
    
    # Morphological operations
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.dilate(mask, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7)), iterations=2)
    mask = cv2.GaussianBlur(mask, (7, 7), 0)
    
    # Show ball
    contours, ret = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 500:
            print(area)
            main_area = area
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 165, 255), 2)
            mid_x, mid_y = int((x+w/2)),int((y+h/2))
            keep_previous(mid_x,mid_y,main_area)
            
    
    return frame,x_pos,y_pos,head_area

if __name__ == "__main__":
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame = detect_orange(frame)
        cv2.imshow('Orange Detection', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()