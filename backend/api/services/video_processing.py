import os
import cv2
import numpy as np

def detect_tiktok_watermark(video_path: str) -> bool:
    cap = cv2.VideoCapture(video_path)

    success, frame = cap.read()
    cap.release()

    if not success or frame is None:
        return False

    height, width, _ = frame.shape

    top_left = frame[0:int(height * 0.2), 0:int(width * 0.2)]
    bottom_right = frame[int(height * 0.8):height, int(width * 0.8):width]

    def is_bright(image_part):
        gray = cv2.cvtColor(image_part, cv2.COLOR_BGR2GRAY)
        mean_brightness = np.mean(gray)
        return mean_brightness > 180

    if is_bright(top_left) or is_bright(bottom_right):
        return True

    return False


def remove_watermark(input_path: str, output_path: str) -> None:
    cap = cv2.VideoCapture(input_path)

    if not cap.isOpened():
        raise ValueError(f"Cannot open video file: {input_path}")

    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    if width == 0 or height == 0:
        cap.release()
        raise ValueError("Invalid video dimensions.")

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    while True:
        success, frame = cap.read()
        if not success or frame is None:
            break

        top_left = frame[0:int(height * 0.2), 0:int(width * 0.2)]
        bottom_right = frame[int(height * 0.8):height, int(width * 0.8):width]

        top_left_blur = cv2.GaussianBlur(top_left, (23, 23), 30)
        bottom_right_blur = cv2.GaussianBlur(bottom_right, (23, 23), 30)

        frame[0:int(height * 0.2), 0:int(width * 0.2)] = top_left_blur
        frame[int(height * 0.8):height, int(width * 0.8):width] = bottom_right_blur

        out.write(frame)

    cap.release()
    out.release()