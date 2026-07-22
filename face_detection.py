import cv2
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5
    )
    face_count = len(faces)
    for (x,y,w,h) in faces:
        cv2.rectangle(
            frame,
            (x, y),
            (x+w+20, y+h+20),
            (0,255,0),
            2
        )
    if face_count >= 3:
        cv2.putText(
        frame,
        "Group",
        (50, 70),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 0, 255),
        2
        )
    cv2.putText(
    frame,
    "Faces : " + str(face_count),
    (10, 30),
    cv2.FONT_HERSHEY_SIMPLEX,
    1,
    (0, 255, 0),
    2
    )

    cv2.imshow("Face Detection",frame)
    
    if cv2.waitKey(1) == 27:
        break
cap.release()
cv2.destroyAllWindows()