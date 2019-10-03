import cv2
import numpy as np

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
img = cv2.imread('../example.png')
corner_img = img.copy()
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

faces = face_cascade.detectMultiScale(gray, 1.1, 4)
face_centers = []
for (x, y, w, h) in faces:
    #cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
    face_centers.append((x + w/2, y + h/2))

edges = cv2.Canny(gray,50,150,apertureSize = 3)

# Defining a kernel length
# kernel_length = np.array(img).shape[1]//40
kernel_length = 7

# A vertical kernel of (1 X kernel_length), which will detect all the vertical lines from the image.
vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, kernel_length))
# A horizontal kernel of (kernel_length X 1), which will help to detect all the horizontal line from the image.
hori_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_length, 1))
# A kernel of (3 X 3) ones.
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))

# Morphological operation to detect vertical lines from an image
img_temp1 = cv2.erode(edges, vertical_kernel, iterations=3)
vertical_lines_img = cv2.dilate(img_temp1, vertical_kernel, iterations=3)

# Morphological operation to detect horizontal lines from an image
img_temp2 = cv2.erode(edges, hori_kernel, iterations=3)
horizontal_lines_img = cv2.dilate(img_temp2, hori_kernel, iterations=3)

# Weighting parameters, this will decide the quantity of an image to be added to make a new image.
alpha = 0.5
beta = 1.0 - alpha
# This function helps to add two image with specific weight parameter to get a third image as summation of two image.
img_final_bin = cv2.addWeighted(vertical_lines_img, alpha, horizontal_lines_img, beta, 0.0)
img_final_bin = cv2.erode(~img_final_bin, kernel, iterations=2)
(thresh, img_final_bin) = cv2.threshold(~img_final_bin, 128,255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

selected_contours = []
(cnts, _) = cv2.findContours(img_final_bin, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
# loop over the contours
for c in cnts:
    # approximate the contour
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.02 * peri, True)

    # if the approximated contour has four points, it is a box
    if len(approx) == 4:
        for face_center in face_centers:
            if cv2.pointPolygonTest(c, face_center, False) > 0:
                #cv2.drawContours(img, [approx], -1, (0, 255, 0), 4)
                selected_contours.append(cv2.boundingRect(approx))

#corners = cv2.cornerHarris(np.float32(gray),2,3,0.04)
#corners = cv2.dilate(corners,None)
## Threshold for an optimal value, it may vary depending on the image.
#corner_img[corners>0.01*corners.max()]=[0,0,255]

#minLineLength = 100
#maxLineGap = 10
#lines = cv2.HoughLinesP(edges,1,np.pi/180,100,minLineLength,maxLineGap)
#for x1,y1,x2,y2 in lines[0]:
#    cv2.line(img,(x1,y1),(x2,y2),(0,255,0),2)

for x,y,w,h in selected_contours:
    cv2.imshow("frame", img[y:y+h,x:x+w])

#cv2.imshow("result", img)
#cv2.imshow("result corners", corner_img)
#cv2.imshow("gray", gray)
#cv2.imshow("edges", edges)
#cv2.imshow("MV", vertical_lines_img)
#cv2.imshow("MH", horizontal_lines_img)
#cv2.imshow("Added", img_final_bin)
cv2.imwrite('../faces.jpg',img)

if cv2.waitKey(0) & 0xff == 27:
    cv2.destroyAllWindows()
