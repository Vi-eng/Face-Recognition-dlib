import cv2
import numpy as np
from flask_sqlalchemy import SQLAlchemy
import urllib

def database(app):
    # Configure the SQLAlchemy connection string
    params = urllib.parse.quote_plus('DRIVER={ODBC Driver 17 for SQL Server};SERVER=DESKTOP-BJNEMLC;DATABASE=Flask_FaRec;Trusted_Connection=yes;')
    app.config['SQLALCHEMY_DATABASE_URI'] = "mssql+pyodbc:///?odbc_connect=%s" % params
    #app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://<username>:<password>@<dsn>'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db = SQLAlchemy(app)
    return db


# Load YOLOv3 files
net = cv2.dnn.readNet('yolot/yolov3-tiny.weights', 'yolot/yolov3-tiny.cfg')
with open('yolot/coco.names', 'r') as f:
    classes = f.read().strip().split('\n')

def detect_objects(frame):
    height, width, _ = frame.shape
    blob = cv2.dnn.blobFromImage(frame, 1/255, (416, 416), (0, 0, 0), swapRB=True, crop=False)
    net.setInput(blob)
    output_layers_names = net.getUnconnectedOutLayersNames()
    layer_outputs = net.forward(output_layers_names)

    boxes = []
    confidences = []
    class_ids = []

    for output in layer_outputs:
        for detection in output:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5:
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)
                x = int(center_x - w/2)
                y = int(center_y - h/2)

                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

    for i in range(len(boxes)):
        if i in indexes:
            x, y, w, h = boxes[i]
            label = classes[class_ids[i]]
            confidence = confidences[i]
            color = (0, 255, 0)  # Green color for bounding boxes
            cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
            cv2.putText(frame, f'{label} {confidence:.2f}', (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    return frame

def generate_frames():
    url = "https://192.168.48.143:8080/shot.jpg"
    cap = cv2.VideoCapture(0)
    while True:
        success, frame = cap.read()
        if not success:
            break
        else:
            frame = detect_objects(frame)
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
