import cv2
import time

def play_video(file_path):
    cap = cv2.VideoCapture(file_path)
    if not cap.isOpened():
        print("Error: Could not open video file")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        cv2.imshow("Video Player", frame)
        if cv2.waitKey(30) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def start_app():
    on_video_path = "media/immersionon.mp4"
    off_video_path = "media/immersionoff.mp4"

    play_video(on_video_path)
    time.sleep(7)
    play_video(off_video_path)
    time.sleep(7)

if __name__ == "__main__":
    start_app()
