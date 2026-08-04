import cv2
cap = cv2.VideoCapture(0)
cv2.namedWindow("Camera", cv2.WINDOW_NORMAL)

while True:
    ret, frame = cap.read()
    height, width, _ = frame.shape
    screen_center_x = width // 2
    screen_center_y = height // 2
    left_line_x = width // 3
    right_line_x = (width*2) // 3 
    top_line_y = height // 3
    bottom_line_y = (height*2) // 3
    cv2.line(
    frame,
    (left_line_x, 0),
    (left_line_x, height),
    (0,255,0),
    2
    )
    cv2.line(
    frame,
    (0, top_line_y),
    (width, top_line_y),
    (0,255,0),
    2
    )
    cv2.line(
    frame,
    (right_line_x, 0),
    (right_line_x, height),
    (0,255,0),
    2
    )
    cv2.line(
    frame,
    (0, bottom_line_y),
    (width, bottom_line_y),
    (0,255,0),
    2
    )
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_red = (0, 150, 90)
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
    if red_contours:
        cnt = max(red_contours, key=cv2.contourArea)

        x, y, w, h = cv2.boundingRect(cnt)
    

        if w * h > 3000:
            red_center_x = x + w//2
            red_center_y = y + h//2
            error_x = screen_center_x - red_center_x
            error_y = screen_center_y - red_center_y
            cv2.circle(
                frame,
                (red_center_x, red_center_y),
                5,
                (0,255,0),
                -1
            )
           
            if red_center_x < left_line_x:
                cv2.putText(frame, "X : LEFT", 
                    (50,150),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0,255,0),
                    2)

            elif left_line_x < red_center_x < right_line_x:
                cv2.putText(frame, "X : CENTER", 
                    (50,150),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0,255,0),
                    2)
            else:
                cv2.putText(frame, "X : RIGHT", 
                    (50,150),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0,255,0),
                    2)
            if red_center_y < top_line_y:
                cv2.putText(frame, "Y : UP", 
                (50,250),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0,255,0),
                2)
            
            elif top_line_y < red_center_y < bottom_line_y:
                cv2.putText(frame, "Y : CENTER", 
                (50,250),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0,255,0),
                2)
            else:
                cv2.putText(frame, "Y : BOTTOM", 
                (50,250),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0,255,0),
                2)

    
    for cnt in blue_contours:
        x, y, w, h = cv2.boundingRect(cnt)
        

        if w * h > 1000:
            blue_center_x = x + w//2
            blue_center_y = y + h//2
            cv2.circle(
                frame,
                (blue_center_x,blue_center_y),
                5,
                (0, 255, 0),
                -1
            )
            # if blue_center_x < screen_center_x:
            #     cv2.putText(frame, "LEFT", 
            #     (50,150),
            #     cv2.FONT_HERSHEY_SIMPLEX,
            #     1,
            #     (0,255,0),
            #     2)
            
            # elif blue_center_x > screen_center_x:
            #     cv2.putText(frame, "RIGHT", 
            #     (40,180),
            #     cv2.FONT_HERSHEY_SIMPLEX,
            #     1,
            #     (0,255,0),
            #     2)
    red_pixels = cv2.countNonZero(mask)
    blue_pixels = cv2.countNonZero(mask2)
    if red_pixels >5000:
        cv2.putText(frame,"RED",(50,50),cv2.FONT_HERSHEY_SIMPLEX
                    ,1,(0,0,255),2)
    if blue_pixels >5000:
        cv2.putText(frame,"BLUE",(50,90),cv2.FONT_HERSHEY_SIMPLEX
                    ,1,(255,0,0),2)
    
    cv2.imshow("Camera", frame)
    cv2.imshow("Red Mask", mask)

    if cv2.waitKey(1) == 27:
        break
cap.release()
cv2.destroyAllWindows()
