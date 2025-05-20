import cv2
from ultralytics import YOLO

# Load the YOLO model
model = YOLO("/root/yolov11/runs/SICISP_merged_200/weights/best.pt")

# Open the video file
video_path = "/root/yolov11/datasets/data/videos/2022302131004.mp4"
cap = cv2.VideoCapture(video_path)

# Get video properties for output video writer
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = int(cap.get(cv2.CAP_PROP_FPS))

# Define the codec and create VideoWriter object
output_video_path = "/root/yolov11/runs/Tracking_output2_poly.mp4"
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec for .mp4
out = cv2.VideoWriter(output_video_path, fourcc, fps, (frame_width, frame_height))

# Dictionary to store track history: {track_id: [(x, y), ...]}
track_history = {}

# Maximum number of points to keep in history
MAX_HISTORY_LENGTH = 30

# Loop through the video frames
while cap.isOpened():
    # Read a frame from the video
    success, frame = cap.read()

    if success:
        # Run YOLO tracking on the frame, persisting tracks between frames
        results = model.track(frame, persist=True)

        # Visualize the results on the frame
        annotated_frame = results[0].plot()

        # Get current track IDs
        current_ids = []
        if results[0].boxes is not None and hasattr(results[0].boxes, 'id'):
            boxes = results[0].boxes.xywh.cpu()
            ids = results[0].boxes.id.int().cpu().tolist()
            current_ids = ids

            # Update track history
            for box, track_id in zip(boxes, ids):
                x_center, y_center, _, _ = box
                point = (int(x_center), int(y_center))

                if track_id not in track_history:
                    track_history[track_id] = []
                track_history[track_id].append(point)

                # Limit the length of history
                if len(track_history[track_id]) > MAX_HISTORY_LENGTH:
                    track_history[track_id].pop(0)

        # Remove track history for IDs not present in current frame
        for track_id in list(track_history.keys()):
            if track_id not in current_ids:
                del track_history[track_id]

        # Draw the trajectories
        for track_id, points in track_history.items():
            for i in range(1, len(points)):
                thickness = int(i / len(points) * 5) + 1  # Fade effect
                cv2.line(annotated_frame, points[i - 1], points[i], (0, 255, 0), thickness)

        # Write the annotated frame to the output video
        out.write(annotated_frame)

        # Display the annotated frame (optional)
        # cv2.imshow("YOLO11 Tracking", annotated_frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    else:
        # Break the loop if the end of the video is reached
        break

# Release the video capture and writer objects, and close all windows
cap.release()
out.release()
cv2.destroyAllWindows()