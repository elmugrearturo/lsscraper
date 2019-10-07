import cv2
import numpy as np

def extract_ls_region_candidates(img, 
                                 haar_scale_factor=1.1, 
                                 haar_min_neighbors=4,
                                 canny_min_value=50,
                                 canny_max_value=150,
                                 canny_aperture_size=3,
                                 structuring_kernel_length=7,
                                 structuring_kernel_opening_size=3,
                                 morph_open_iterations=3,
                                 alpha_addition=0.5):

    face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
            )
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    
    faces = face_cascade.detectMultiScale(gray, 
                                          haar_scale_factor,
                                          haar_min_neighbors)
    face_centers = []
    for (x, y, w, h) in faces:
        #cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
        face_centers.append((x + w/2, y + h/2))

    edges = cv2.Canny(gray, 
                      canny_min_value, 
                      canny_max_value, 
                      apertureSize = canny_aperture_size)

    # Straight line detection
    vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, 
                                                (1, 
                                                 structuring_kernel_length
                                                 ))
    horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, 
                                                  (structuring_kernel_length, 
                                                   1))
    opening_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, 
                                               (structuring_kernel_opening_size, 
                                                structuring_kernel_opening_size))
    # vertical lines
    vertical_edges_img = cv2.erode(edges, 
                                   vertical_kernel, 
                                   iterations=morph_open_iterations)
    vertical_edges_img = cv2.dilate(vertical_edges_img, 
                                    vertical_kernel, 
                                    iterations=morph_open_iterations)
    
    # Morphological operation to detect horizontal lines from an image
    horizontal_edges_img = cv2.erode(edges, 
                                     horizontal_kernel, 
                                     iterations=morph_open_iterations)
    horizontal_edges_img = cv2.dilate(horizontal_edges_img, 
                                      horizontal_kernel, 
                                      iterations=morph_open_iterations)

    alpha2_addition = 1.0 - alpha_addition
    straight_edges_img = cv2.addWeighted(vertical_edges_img, 
                                         alpha_addition, 
                                         horizontal_edges_img, 
                                         alpha2_addition, 0.0)
    
    # Invert image for contours
    straight_edges_img = cv2.erode(~straight_edges_img, 
                                   (structuring_kernel_opening_size, 
                                    structuring_kernel_opening_size), 
                                   iterations=2)
    (thresh, straight_edges_img) = cv2.threshold(
                                        ~straight_edges_img, 
                                        128, 255, 
                                        cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    # Obtaining contours
    selected_contours = []
    (contours, _) = cv2.findContours(straight_edges_img, 
                                     cv2.RETR_EXTERNAL, 
                                     cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        # approximate contour
        perimeter = cv2.arcLength(contour, True)
        approximation = cv2.approxPolyDP(contour, 0.02 * perimeter, True)
    
        # approximation has four points, so it is a box
        if len(approximation) == 4:
            # select contours with a face
            for face_center in face_centers:
                rect_from_polygon = cv2.boundingRect(approximation)
                x, y, w, h = rect_from_polygon
                if x < face_center[0] < x+w:
                    if y < face_center[1] < y+h:
                        selected_contours.append(cv2.boundingRect(approximation))

    return selected_contours
