import cv2
from ultralytics import YOLO

# Load the YOLO11 model
model = YOLO("/root/yolov11/runs/SICISP_merged_200/weights/best.pt")

# Open the video file
video_path = "/root/yolov11/datasets/data/videos/2022302131103.mp4"
cap = cv2.VideoCapture(video_path)

# Get video properties for output video writer
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = int(cap.get(cv2.CAP_PROP_FPS))

# Define the codec and create VideoWriter object
output_video_path = "/root/yolov11/runs/Tracking_output_1.mp4"
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec for .mp4
out = cv2.VideoWriter(output_video_path, fourcc, fps, (frame_width, frame_height))

# Loop through the video frames
while cap.isOpened():
    success, frame = cap.read()

    if success:
        # Run YOLO11 tracking on the frame, persisting tracks between frames
        results = model.track(frame, persist=True)

        # Visualize the results on the frame
        annotated_frame = results[0].plot()

        # 获取当前帧中检测到的目标数量
        current_count = len(results[0])
        
        # 在图像左上角绘制目标数量文本
        text = f"Objects: {current_count}"
        position = (20, 50)  # 坐标位置（x, y）
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 1.5
        color = (0, 255, 0)  # 绿色字体
        thickness = 2
        cv2.putText(annotated_frame, text, position, font, font_scale, color, thickness, cv2.LINE_AA)

        # Write the annotated frame to the output video
        out.write(annotated_frame)

        # Display the annotated frame (optional)
        # cv2.imshow("YOLO11 Tracking", annotated_frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    else:
        break

# Release the video capture and writer objects, and close all windows
cap.release()
out.release()
cv2.destroyAllWindows()