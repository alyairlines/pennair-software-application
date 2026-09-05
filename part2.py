import cv2
from part1 import detect_shapes

INPUT = "dynamic.mp4"
OUTPUT = "part2_output.mp4"

# open video as stream of frames
cap = cv2.VideoCapture(INPUT)

fps = cap.get(cv2.CAP_PROP_FPS)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# setup output video writer
fourcc = cv2.VideoWriter_fourcc(*"mp4v")
out = cv2.VideoWriter(OUTPUT, fourcc, fps, (width, height))

frame_count = 0
while True:
    ok, frame = cap.read() # grab next frame
    if not ok: # video ends
        break

    annotated, mask, results = detect_shapes(frame, min_area=2000)

    out.write(annotated) # append processed frame to output video
    frame_count += 1

cap.release()
out.release()
print(f"done - {frame_count} frames processed, saved {OUTPUT}")