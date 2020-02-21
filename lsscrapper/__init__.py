import os
import cv2
from tqdm import tqdm
from extract_regions import extract_ls_region_candidates

preprocessing_image_path = '../example.png'
video_path = '../example.mp4'

img = cv2.imread(preprocessing_image_path)
candidates = extract_ls_region_candidates(img)

for x, y, w, h in candidates:
    cv2.imshow("frame", img[y:y+h,x:x+w])
    
    print("Read signer region from image: %s\n\n Press ESC to continue..." % preprocessing_image_path)
    if cv2.waitKey(0) & 0xff == 27:
        cv2.destroyAllWindows()

# Use the region to create videos
video = cv2.VideoCapture(video_path)
if video.isOpened() == False:
    raise Exception("Couldn't open video :(")

# Find OpenCV version
(major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')

# Get FPS
if int(major_ver)  < 3 :
    fps = video.get(cv2.cv.CV_CAP_PROP_FPS)
else:
    fps = video.get(cv2.CAP_PROP_FPS)

# Get length
if int(major_ver)  < 3 :
    frame_count = int(video.get(cv2.cv.CAP_PROP_FRAME_COUNT))
else:
    frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

# Get output codec
if os.name == "nt":
    ext = "avi"
    fourcc = cv2.VideoWriter_fourcc(*"MJPG")
else:
    ext = "mkv"
    fourcc = cv2.VideoWriter_fourcc(*"XVID")

# Get a video for every possible sign language region
video_outputs = []
for i, candidate in enumerate(candidates):
    _, _, video_width, video_height = candidate
    video_outputs.append(cv2.VideoWriter("../newvideo_{0}.{1}".format(i, ext), 
                                         fourcc,
                                         fps,
                                         (video_width, video_height)
                                         )
                        )
with tqdm(total=frame_count, unit=" frames") as pbar:
    while video.isOpened():
        return_code, frame = video.read()
        pbar.update(1)
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
