import cv2
import numpy as np
from part1 import detect_shapes

# camera and circle parameters as given
fx = 2564.3186869
fy = 2569.70273111
REAL_RADIUS_IN = 10.0

def estimate_circle_3d(contour, cx_img, cy_img):
    """ Estimate the 3D position of a circle given its contour and image center. """
    
    (u, v), pixel_radius = cv2.minEnclosingCircle(contour) # tightest circle around contour
    Z = (fx * REAL_RADIUS_IN) / pixel_radius # depth from apparent size

    # principal point assumed as image center
    X = (u - cx_img) * Z /fx # horizontal position from image center
    Y = (v - cy_img) * Z / fy # vertical position from image center
    return X, Y, Z

def is_circle(contour): 
    """ True if the contour roughly fills its enclosing circle."""
    area = cv2.contourArea(contour)
    (_, _), r = cv2.minEnclosingCircle(contour)
    circle_area = np.pi * r * r
    return circle_area > 0 and area / circle_area > 0.8

# in case this gets imported
if __name__ == "__main__":
    img = cv2.imread("static.png")
    h, w = img.shape[:2]
    cx_img, cy_img = w / 2, h / 2

    output, mask, results = detect_shapes(img)

    for contour, cx, cy, area in results:
        if is_circle(contour):
            X, Y, Z = estimate_circle_3d(contour, cx_img, cy_img) # loop every detected shape, keep only the circular one, and find depth
            label = f"Z={Z:.1f}in"
            cv2.putText(output, label, (cx - 40, cy - 20), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            print(f"circle centre px=({cx},{cy}) -> X={X:.1f}in, Y={Y:.1f}in, Z={Z:.1f}in")

    cv2.imwrite("part4_output.png", output)
    print("saved part4_output.png")


