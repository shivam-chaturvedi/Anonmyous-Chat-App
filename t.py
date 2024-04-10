import cv2
import os

# Function to load images from a directory and encode faces
def load_images_from_folder(folder):
    face_encodings = []
    face_names = []
    for filename in os.listdir(folder):
        img_path = os.path.join(folder, filename)
        img = cv2.imread(img_path)
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        face_encodings.append(gray_img)
        face_names.append(os.path.splitext(filename)[0])
    return face_encodings, face_names

# Load known images and encode them
known_face_encodings, known_face_names = load_images_from_folder("known_faces")

# Initialize LBPH face recognizer
face_recognizer = cv2.face.LBPHFaceRecognizer_create()

# Train the face recognizer with known face encodings
face_recognizer.train(known_face_encodings, np.array(range(len(known_face_names))))

# Initialize webcam
video_capture = cv2.VideoCapture(0)

while True:
    # Capture frame-by-frame
    ret, frame = video_capture.read()

    # Convert frame to grayscale for face detection
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the frame
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # Loop through each face found in the frame
    for (x, y, w, h) in faces:
        # Crop face region from the frame
        face_img = gray_frame[y:y+h, x:x+w]

        # Recognize the face using LBPH recognizer
        label, confidence = face_recognizer.predict(face_img)

        # If the confidence is less than 100, consider it a match
        if confidence < 100:
            name = known_face_names[label]
        else:
            name = "Unknown"

        # Display the name of the person recognized
        print(name)

        # Draw a rectangle around the face
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.putText(frame, name, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)

    # Display the resulting image
    cv2.imshow('Video', frame)

    # Break the loop when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release webcam and close windows
video_capture.release()
cv2.destroyAllWindows()
