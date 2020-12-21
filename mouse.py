import numpy as np
import cv2
import math
from scipy import ndimage
import pytesseract


IMAGE_FILE_LOCATION = input()
input_img = cv2.imread(IMAGE_FILE_LOCATION)

def orientation_correction(img, save_image = False):
    # GrayScale Conversion for the Canny Algorithm  
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
    # Canny Algorithm for edge detection was developed by John F. Canny not Kennedy!! :)
    img_edges = cv2.Canny(img_gray, 100, 100, apertureSize=3)
    # Using Houghlines to detect lines
    lines = cv2.HoughLinesP(img_edges, 1, math.pi / 180.0, 100, minLineLength=100, maxLineGap=5)
    
    # Finding angle of lines in polar coordinates
    angles = []
    for x1, y1, x2, y2 in lines[0]:
        angle = math.degrees(math.atan2(y2 - y1, x2 - x1))
        angles.append(angle)
    
    # Getting the median angle
    median_angle = np.median(angles)
    
    # Rotating the image with this median angle
    img_rotated = ndimage.rotate(img, median_angle)
    
    if save_image:
        cv2.imwrite('orientation_corrected.jpg', img_rotated)
    return img_rotated

img_rotated = orientation_correction(input_img)

coordinates = [] 
  
def shape_selection(event, x, y, flags, param): 
    global coordinates 
  
    if event == cv2.EVENT_LBUTTONDOWN: 
        coordinates = [(x, y)] 
  
    elif event == cv2.EVENT_LBUTTONUP: 
        coordinates.append((x, y)) 
  
        cv2.rectangle(image, coordinates[0], coordinates[1], (0,0,255), 2) 
        cv2.imshow("image", image) 
  
  
image = img_rotated
image_copy = image.copy()
cv2.namedWindow("image") 
cv2.setMouseCallback("image", shape_selection) 
  
  
while True: 
    cv2.imshow("image", image) 
    key = cv2.waitKey(1) & 0xFF
  
    if key==13: # If 'enter' is pressed, apply OCR
        break
    
    if key == ord("c"): # Clear the selection when 'c' is pressed 
        image = image_copy.copy() 
  
if len(coordinates) == 2: 
    image_roi = image_copy[coordinates[0][1]:coordinates[1][1], 
                               coordinates[0][0]:coordinates[1][0]] 
    cv2.imshow("Selected Region of Interest - Press any key to proceed", image_roi) 
    cv2.waitKey(0) 
  
cv2.destroyAllWindows()  

text = pytesseract.image_to_string(image_roi)
print("The text in the selected region is as follows:")
print(text)
