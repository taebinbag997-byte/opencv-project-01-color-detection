import cv2
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_red = (0, 120, 70)
    upper_red = (10,255, 255)
    lower_blue = (100, 150, 0)
    upper_blue= (140,255, 255)
    mask = cv2.inRange(hsv, lower_red, upper_red)
    mask2 = cv2.inRange(hsv, lower_blue, upper_blue)
    red_contours, _ = cv2.findContours(
        mask,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )
    blue_contours, _ = cv2.findContours(
        mask2,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )
    for cnt in red_contours:
        x, y, w, h = cv2.boundingRect(cnt)

        if w * h > 1000:
            cv2.rectangle(
                frame,
                (x, y),
                (x + w, y + h),
                (0, 0, 255),
                2
            )
    for cnt in blue_contours:
        x, y, w, h = cv2.boundingRect(cnt)

        if w * h > 1000:
            cv2.rectangle(
                frame,
                (x, y),
                (x + w, y + h),
                (255, 0, 0),
                2
            )
    red_pixels = cv2.countNonZero(mask)
    blue_pixels = cv2.countNonZero(mask2)
    if red_pixels >5000:
        cv2.putText(frame,"RED",(50,70),cv2.FONT_HERSHEY_SIMPLEX
                    ,1,(0,0,255),2)
    if blue_pixels >5000:
        cv2.putText(frame,"BLUE",(80,100),cv2.FONT_HERSHEY_SIMPLEX
                    ,1,(255,0,0),2)
    cv2.imshow("Camera", frame)
    cv2.imshow("Red Mask", mask)

    if cv2.waitKey(1) == 27:
        break
cap.release()
cv2.destroyAllWindows()