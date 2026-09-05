import cv2
from part1 import detect_shapes

INPUT = "dynamic-hard.mp4"
OUTPUT = "part3_output.mp4"

cap = cv2.VideoCapture(INPUT)
fps = cap.get(cv2.CAP_PROP_FPS)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

fourcc = cv2.VideoWriter_fourcc(*"mp4v")
out = cv2.VideoWriter(OUTPUT, fourcc, fps, (width, height))

frame_count = 0
while True:
    ok, frame = cap.read() 
    if not ok: 
        break

    annotated, mask, results = detect_shapes(
        frame, 
        texture_thresh=10, # stricter
        win=18, # bigger window for steadier estimate on static
        min_area=3000) # bigger area for the background noise

    out.write(annotated) 
    frame_count += 1

cap.release()
out.release()
print(f"done - {frame_count} frames processed, saved {OUTPUT}")