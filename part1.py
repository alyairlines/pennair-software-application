import cv2
import numpy as np

def detect_shapes(img, texture_thresh=14, win=9, min_area=1000):
    """ Find smooth shapes on a textured background. """
    # convert to grayscale to account for brightness variation
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY).astype(np.float32)

    mean = cv2.blur(gray, (win, win))
    mean_sq = cv2.blur(gray*gray, (win, win))
    variance = mean_sq - mean*mean  # variance of the neighboring area's brightness
    stddev = np.sqrt(np.maximum(variance, 0)) # low value when the area is smooth

    # the shapes are smooth so the std dev will be low -> white
    mask = np.where(stddev < texture_thresh, 255, 0).astype(np.uint8)

    kernel = np.ones((5,5), np.uint8)
    # remove noise from shapes
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    # outline and mark the center of the shapes
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    output = img.copy()
    results = []
    for c in contours:
        area = cv2.contourArea(c)
        if area < min_area: # filter out small contours
            continue
        cv2.drawContours(output, [c], -1, (0, 0, 0), 2)

        # find center via moments (centroid)
        M = cv2.moments(c)
        cx = int(M["m10"] / M["m00"])
        cy = int(M["m01"] / M["m00"])

        cv2.circle(output, (cx, cy), 5, (0, 0, 255), -1) # red dot at the center

        results.append((c, cx, cy, area))   # keep for later parts (e.g. depth)

    return output, mask, results

# this next section of the code (to make the image etc.) is purely for the function above
# so if another script imports this file, it won't run the code below
if __name__ == "__main__":
    img = cv2.imread("static.png")
    output, mask, results = detect_shapes(img)
    cv2.imwrite("mask.png", mask)
    cv2.imwrite("part1_output.png", output)
    print(f"done - {len(results)} shapes")
    for c, cx, cy, area in results:
        print(f"center ({cx}, {cy}), area {int(area)}")