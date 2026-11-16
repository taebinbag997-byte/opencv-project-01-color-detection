import cv2

# test.mp4 영상 불러오기
cap = cv2.VideoCapture(0)

# 영상을 보여줄 창 설정
cv2.namedWindow("Camera", cv2.WINDOW_NORMAL)

def drone_move(command):

    if command == "RIGHT":
        print("드론 오른쪽 이동")

    elif command == "LEFT":
        print("드론 왼쪽 이동")

    elif command == "UP":
        print("드론 위쪽 이동")

    elif command == "DOWN":
        print("드론 아래쪽 이동")

    elif command == "RIGHT + FORWARD":
        print("드론 오른쪽 + 전진")

    elif command == "LEFT + FORWARD":
        print("드론 왼쪽 + 전진")

    elif command == "RIGHT + BACKWARD":
        print("드론 오른쪽 + 후진")

    elif command == "LEFT + BACKWARD":
        print("드론 왼쪽 + 후진")

    elif command == "RIGHT UP":
        print("드론 오른쪽 위 이동")

    elif command == "RIGHT DOWN":
        print("드론 오른쪽 아래 이동")

    elif command == "LEFT UP":
        print("드론 왼쪽 위 이동")

    elif command == "LEFT DOWN":
        print("드론 왼쪽 아래 이동")

    elif command == "UP + FORWARD":
        print("드론 위쪽 + 전진")

    elif command == "DOWN + FORWARD":
        print("드론 아래쪽 + 전진")

    elif command == "UP + BACKWARD":
        print("드론 위쪽 + 후진")

    elif command == "DOWN + BACKWARD":
        print("드론 아래쪽 + 후진")

    elif command == "RIGHT UP + FORWARD":
        print("드론 오른쪽 위 + 전진")

    elif command == "RIGHT DOWN + FORWARD":
        print("드론 오른쪽 아래 + 전진")

    elif command == "LEFT UP + FORWARD":
        print("드론 왼쪽 위 + 전진")

    elif command == "LEFT DOWN + FORWARD":
        print("드론 왼쪽 아래 + 전진")

    elif command == "RIGHT UP + BACKWARD":
        print("드론 오른쪽 위 + 후진")

    elif command == "RIGHT DOWN + BACKWARD":
        print("드론 오른쪽 아래 + 후진")

    elif command == "LEFT UP + BACKWARD":
        print("드론 왼쪽 위 + 후진")

    elif command == "LEFT DOWN + BACKWARD":
        print("드론 왼쪽 아래 + 후진")

    elif command == "FORWARD":
        print("드론 전진")

    elif command == "BACKWARD":
        print("드론 후진")

    elif command == "CENTER":
        print("드론 위치 유지")

    elif command == "STOP":
        print("드론 정지")

previous_final_command = None
previous_distance_direction = None
smooth_center_x = None
smooth_center_y = None


while True:

    # 매 프레임마다 거리 상태 초기화
    distance_direction = "GOOD"
    
    # 영상에서 한 프레임 읽기
    ret, frame = cap.read()

    # 카메라에서 영상을 읽지 못하면 반복문 종료
    if not ret:
        print("카메라 영상을 읽을 수 없습니다.")
        break

    # 현재 영상의 높이와 너비 확인
    # frame의 크기를 알아야 화면을 3×3으로 나눌 수 있음
    height, width, _ = frame.shape

    # 화면의 정중앙 좌표
    # 객체가 이 위치에 가까워지는지를 판단하기 위해 사용
    screen_center_x = width // 2
    screen_center_y = height // 2

    # 화면을 3등분하기 위한 기준선
    left_line_x = width // 3
    right_line_x = (width * 2) // 3

    top_line_y = height // 3
    bottom_line_y = (height * 2) // 3

    # 화면을 3×3으로 나누는 선 그리기
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

    # BGR로 되어 있는 영상을 HSV로 변환
    # 색상을 기준으로 물체를 찾기 위해 사용
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # 빨간색을 찾기 위한 HSV 범위
    lower_red = (0, 150, 90)
    upper_red = (10, 255, 255)

    # HSV 영상에서 빨간색 영역만 남김
    mask = cv2.inRange(hsv, lower_red, upper_red)

    # 빨간색 영역의 외곽선 찾기
    red_contours, _ = cv2.findContours(
        mask,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    move_direction = "STOP"

    # 빨간색 객체가 발견되었는지 확인
    if red_contours:

        # 여러 빨간색 영역 중 가장 큰 영역 선택
        cnt = max(red_contours, key=cv2.contourArea)

        # 선택한 객체의 사각형 정보
        x, y, w, h = cv2.boundingRect(cnt)

        # 너무 작은 영역은 실제 객체가 아니라고 판단
        if w * h > 3000:

            # 객체의 중심 좌표 계산
            red_center_x = x + w // 2
            red_center_y = y + h // 2

            # 중앙점 스무딩
            # 이전 중심 좌표와 현재 중심 좌표를 섞어 객체 중심의 갑작스러운 흔들림을 줄임
            if smooth_center_x is None:
                smooth_center_x = red_center_x
                smooth_center_y = red_center_y
            else:
                alpha = 0.3
                smooth_center_x = int(alpha * red_center_x + (1 - alpha) * smooth_center_x)
                smooth_center_y = int(alpha * red_center_y + (1 - alpha) * smooth_center_y)

            # 화면 중심과 보정된 객체 중심의 차이
            # 객체가 화면 중심보다 왼쪽에 있으면 양수, 오른쪽에 있으면 음수가 됨
            # Y축은 화면 좌표 특성상 객체가 위쪽에 있으면 양수, 아래쪽에 있으면 음수가 됨
            error_x = screen_center_x - smooth_center_x
            error_y = screen_center_y - smooth_center_y

            #카메라 앞에서 물체를 멀리/가까이 움직여보면서 값이 어떻게 변하는지 확인하기 위한 임시 기준값 
            red_size = w * h

            if red_size < 5000:
                distance_direction = "FAR"
            elif red_size > 15000:
                distance_direction = "NEAR"
            else:
                distance_direction = "GOOD"

            if distance_direction != previous_distance_direction:
                print("DISTANCE:", distance_direction)
                previous_distance_direction = distance_direction
     
                
            cv2.putText(
                frame,
                f"DISTANCE: {distance_direction}",
                (20, 60),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (255, 255, 255),
                2
                )

            # 이동 방향 판단
            if error_x > 50 and error_y > 50:
                move_direction = "LEFT UP"

            elif error_x < -50 and error_y > 50:
                move_direction = "RIGHT UP"

            elif error_x > 50 and error_y < -50:
                move_direction = "LEFT DOWN"

            elif error_x < -50 and error_y < -50:
                move_direction = "RIGHT DOWN"

            elif error_x > 82:
                move_direction = "LEFT"

            elif error_x < -83:
                move_direction = "RIGHT"

            elif error_y > 50:
                move_direction = "UP"

            elif error_y < -50:
                move_direction = "DOWN"

            else:
                move_direction = "CENTER"


            # 화면에 X 오차 표시
            cv2.putText(
                frame,
                "ERROR X : " + str(error_x),
                (20,150),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0,255,0),
                2
            )

            # 화면에 Y 오차 표시
            cv2.putText(
                frame,
                "ERROR Y : " + str(error_y),
                (20,190),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0,255,0),
                2
            )

            # 객체 중심 표시
            cv2.circle(
                frame,
                (smooth_center_x, smooth_center_y),
                5,
                (0,255,0),
                -1
            )

            # 스무딩된 객체 중심 좌표를 기준으로 화면의 좌우 영역 구분
            if smooth_center_x < left_line_x:
                x_position = "X : LEFT"
            elif smooth_center_x < right_line_x:
                x_position = "X : CENTER"
            else:
                x_position = "X : RIGHT"

            cv2.putText(
                frame,
                x_position,
                (20,90),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0,255,0),
                2
            )

            # 스무딩된 객체 중심 좌표를 기준으로 화면의 상하 영역 구분
            if smooth_center_y < top_line_y:
                y_position = "Y : UP"
            elif smooth_center_y < bottom_line_y:
                y_position = "Y : CENTER"
            else:
                y_position = "Y : BOTTOM"

            cv2.putText(
                frame,
                y_position,
                (20,120),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0,255,0),
                2
            )
        else:
            # 검출된 영역이 너무 작으면 이전 중앙점 초기화
            smooth_center_x = None
            smooth_center_y = None

    else:
        # 빨간색 객체가 검출되지 않으면 이전 중앙점 초기화
        smooth_center_x = None
        smooth_center_y = None        
    # 최종 명령 결정
    final_command = "STOP"

    # 빨간색 객체가 정상적으로 검출되었을 때만 이동 명령 결정
    if move_direction != "STOP":

        if distance_direction == "FAR":

            if move_direction == "CENTER":
                final_command = "FORWARD"

            else:
                final_command = move_direction + " + FORWARD"

        elif distance_direction == "NEAR":

            if move_direction == "CENTER":
                final_command = "BACKWARD"

            else:
                final_command = move_direction + " + BACKWARD"

        else:
            final_command = move_direction

    # 최종 명령이 바뀌었을 때만 출력 및 함수 실행
    if final_command != previous_final_command:
        print("FINAL COMMAND:", final_command)
        drone_move(final_command)
        previous_final_command = final_command

    # 현재 이동 방향을 화면에 표시
    cv2.putText(
        frame,
        move_direction,
        (20,210),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (0,255,0),
        2
    )

    # 빨간색 픽셀 개수 계산
    red_pixels = cv2.countNonZero(mask)

    # 빨간색 영역이 충분히 많으면 RED 표시
    if red_pixels > 5000:
        cv2.putText(
            frame,
            "RED",
            (20,30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0,0,255),
            2
        )

    # 최종적으로 처리된 영상을 화면에 표시
    cv2.imshow("Camera", frame)

    # 빨간색 Mask도 별도의 창으로 표시
    cv2.imshow("Red Mask", mask)

    # ESC 키를 누르면 반복문 종료
    if cv2.waitKey(1) == 27:
        break

# 영상 사용 종료
cap.release()

# OpenCV 창 닫기
cv2.destroyAllWindows()
