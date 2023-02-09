import cv2
import tensorflow as tf
import tensorflow_hub as hub
import numpy as np
from dotenv import load_dotenv
import os

load_dotenv()

def draw_keypoints(frame, keypoints, confidence_threshold):
    y, x, c = frame.shape
    shaped = np.squeeze(np.multiply(keypoints, [y,x,1]))
    
    for kp in shaped:
        ky, kx, kp_conf = kp
        if kp_conf > confidence_threshold:
            cv2.circle(frame, (int(kx), int(ky)), 6, (0,255,0), -1)

EDGES = {
    (0, 1): 'm',
    (0, 2): 'c',
    (1, 3): 'm',
    (2, 4): 'c',
    (0, 5): 'm',
    (0, 6): 'c',
    (5, 7): 'm',
    (7, 9): 'm',
    (6, 8): 'c',
    (8, 10): 'c',
    (5, 6): 'y',
    (5, 11): 'm',
    (6, 12): 'c',
    (11, 12): 'y',
    (11, 13): 'm',
    (13, 15): 'm',
    (12, 14): 'c',
    (14, 16): 'c'
}

def draw_connections(frame, keypoints, edges, confidence_threshold):
    y, x, c = frame.shape
    shaped = np.squeeze(np.multiply(keypoints, [y,x,1]))
    
    for edge, color in edges.items():
        p1, p2 = edge
        y1, x1, c1 = shaped[p1]
        y2, x2, c2 = shaped[p2]
        
        if (c1 > confidence_threshold) & (c2 > confidence_threshold):      
            cv2.line(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0,0,255), 2)

def draw_id(frame, keypoints, confidence_threshold, id):
    y, x, c = frame.shape
    shaped = np.squeeze(np.multiply(keypoints, [y,x,1]))
    
    for kp in shaped:
        ky, kx, kp_conf = kp
        if kp_conf > confidence_threshold:
            cv2.putText(frame, f'id: {id}', (int(kx), int(ky)), cv2.FONT_HERSHEY_PLAIN, 2, (0,255,0), 1)
            break

def draw_box(frame, coordinates, id):
    ymin, xmin, ymax, xmax, score = coordinates
    if(score > 0.3):   
        cv2.rectangle(frame, pt1= (int(xmin*640), int(ymax*480)), pt2 = (int(xmax*640), int(ymin*480)), color = (255, 0, 0), thickness = 3)

# Function to Loop through each person detected and render
def loop_through_people(frame, keypoints_with_scores, boxes_with_scores, edges, confidence_threshold):
    for id, person in enumerate(keypoints_with_scores):
        if boxes_with_scores[id][4] > 0.5:
            draw_connections(frame, person, edges, confidence_threshold)
            draw_keypoints(frame, person, confidence_threshold)
            draw_id(frame, person, confidence_threshold, id)
            draw_box(frame, boxes_with_scores[id], id)

def get_stream_video():
    # Load model
    model_directory = os.environ.get('MODEL_DIRECTORY')
    model = hub.load(model_directory)
    movenet = model.signatures['serving_default']

    cap = cv2.VideoCapture(0)
    while cap.isOpened():
        success, frame = cap.read()

        img = frame.copy()
        img = tf.image.resize_with_pad(tf.expand_dims(img, axis=0), 192, 256)
        input_img = tf.cast(img, dtype=tf.int32)

        # Detection section(y, x, condifence score)
        results = movenet(input_img)
        keypoints_with_scores = results['output_0'].numpy()[:,:,:51].reshape((6,17,3))
        boxes_with_scores = results['output_0'].numpy()[:,:,51:].reshape((6, 5))

        loop_through_people(frame, keypoints_with_scores, boxes_with_scores, EDGES, 0.3)

        ret, buffer = cv2.imencode('.jpeg', frame)
        jpgBin = bytearray(buffer.tobytes())
        yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + jpgBin + b'\r\n')

    cap.release()
    cv2.destroyAllWindows()