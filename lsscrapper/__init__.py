import os
import cv2
from extract_regions import extract_ls_region_candidates

img = cv2.imread('../example.png')
candidates = extract_ls_region_candidates(img)

for x, y, w, h in candidates:
    cv2.imshow("frame", img[y:y+h,x:x+w])

    if cv2.waitKey(0) & 0xff == 27:
        cv2.destroyAllWindows()

# Use the region to create videos
video = cv2.VideoCapture("../example.mp4")
if video.isOpened() == False:
    raise Exception("Couldn't open video :(")

# Get FPS
# Find OpenCV version
(major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')

if int(major_ver)  < 3 :
    fps = video.get(cv2.cv.CV_CAP_PROP_FPS)
else :
    fps = video.get(cv2.CAP_PROP_FPS)

# Get output codec
if os.name == "nt":
    ext = "avi"
    fourcc = cv2.VideoWriter_fourcc(*"MJPG")
else:
    ext = "mkv"
    fourcc = cv2.VideoWriter_fourcc(*"XVID")

video_outputs = []
for i, candidate in enumerate(candidates):
    _, _, video_width, video_height = candidate
    video_outputs.append(cv2.VideoWriter("../newvideo_{0}.{1}".format(i, ext), 
                                         fourcc,
                                         fps,
                                         (video_width, video_height)
                                         )
                        )
while video.isOpened():
    return_code, frame = video.read()
    if return_code == True:
        for i, candidate in enumerate(candidates):
            x, y, w, h = candidate
            video_outputs[i].write(frame[y:y+h,x:x+w])
    else:
        break

# Close streams
video.release()
for i in range(len(candidates)):
    video_outputs[i].release()
