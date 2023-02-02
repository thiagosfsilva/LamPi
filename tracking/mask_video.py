import cv2 as cv
import numpy as np
import glob

# Set mask as first channel of the mask image
mask = cv.imread('mask.jpg',0)

file_list = glob.glob('*.mp4')

for file in file_list:

  # New file name
  out_name = file[:-4] + "_mask_str.mp4"

  # Set the video source
  cap = cv.VideoCapture(file)
  fps = int(cap.get(cv.CAP_PROP_FPS))
  frame_width = int(cap.get(3))
  frame_height = int(cap.get(4))
  out = cv.VideoWriter(out_name,cv.VideoWriter_fourcc(*'MP4V'), fps, (frame_width,frame_height))

  # Check if video opened successfully
  if (cap.isOpened()== False): 
    print("Error opening video stream or file")
  else:
    # Read video once and save the frame 
    while(True):
      ret, frame = cap.read()
      if ret == True:
        #cv.imshow('OriginalImage',frame)
        #cv.waitKey(0)
        b,g,r = cv.split(frame)
        scaled_b = cv.equalizeHist(b)
        scaled_g = cv.equalizeHist(g)
        scaled_r = cv.equalizeHist(r)
        img = cv.merge((scaled_b,scaled_g,scaled_r))
        img = cv.convertScaleAbs(img,alpha=0.8,beta=80)
        #cv.imshow('ScaledImage',img)
        #cv.waitKey(0)
        masked_frame = cv.bitwise_and(img,img, mask=mask) 
        #cv.imwrite('masked_frame.jpg', masked_frame) 
        out.write(masked_frame)
        # Press Q on keyboard to stop recording
        if cv.waitKey(0) & 0xFF == ord('q'):
          break
      # Break the loop
      else:
        break 

    # When everything done, release the video capture and video write objects
    cap.release()
    out.release()
    
    # Closes all the frames
    cv.destroyAllWindows()