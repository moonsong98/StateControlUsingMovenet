import cv2

def get_stream_video():
    cap = cv2.VideoCapture(0)
    while cap.isOpened():
        success, frame = cap.read()

        if not success:
            break

        ret, buffer = cv2.imencode('.jpeg', frame)
        jpgBin = bytearray(buffer.tobytes())
        yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + jpgBin + b'\r\n')

    cap.release()
    cv2.destroyAllWindows()