import cv2
from extract_regions import extract_ls_region_candidates


img = cv2.imread('../example.png')
candidates = extract_ls_region_candidates(img)

for x, y, w, h in candidates:
    cv2.imshow("frame", img[y:y+h,x:x+w])

    if cv2.waitKey(0) & 0xff == 27:
        cv2.destroyAllWindows()
