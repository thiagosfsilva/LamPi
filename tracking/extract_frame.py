import cv2
import numpy as np
 
# Set the video source
cap = cv2.VideoCapture('MP1_trimmed.mp4')
 
# Check if camera opened successfully
if (cap.isOpened()== False): 
  print("Error opening video stream or file")
 
# Read video once and save the frame 
ret, frame = cap.read()
if ret == True:
    cv2.imwrite('capture.jpg', frame) 
 
# When everything done, release the video capture object
cap.release()
 
# Closes all the frames
cv2.destroyAllWindows()