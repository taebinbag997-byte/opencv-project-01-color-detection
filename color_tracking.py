import cv2

# test.mp4 영상 불러오기
cap = cv2.VideoCapture(0)

# 영상을 보여줄 창 설정
cv2.namedWindow("Camera", cv2.WINDOW_NORMAL)

while True:

    # 영상에서 한 프레임 읽기
    ret, frame = cap.read()

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

    # 빨간색과 파란색을 찾기 위한 HSV 범위
    lower_red = (0, 150, 90)
    upper_red = (10, 255, 255)

    lower_blue = (100, 150, 0)
    upper_blue = (140, 255, 255)

    # HSV 영상에서 빨간색 영역만 남김
    mask = cv2.inRange(hsv, lower_red, upper_red)

    # HSV 영상에서 파란색 영역만 남김
    mask2 = cv2.inRange(hsv, lower_blue, upper_blue)

    # 빨간색 영역의 외곽선 찾기
    red_contours, _ = cv2.findContours(
        mask,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    # 파란색 영역의 외곽선 찾기
    blue_contours, _ = cv2.findContours(
        mask2,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    # 빨간색 객체가 발견되었는지 확인
    if red_contours:

        # 여러 빨간색 영역 중 가장 큰 영역 선택
        cnt = max(red_contours, key=cv2.contourArea)

        # 선택한 객체의 사각형 정보
        # x, y = 왼쪽 위 좌표
        # w, h = 사각형의 너비와 높이
        x, y, w, h = cv2.boundingRect(cnt)

        # 너무 작은 영역은 실제 객체가 아니라고 판단
        if w * h > 3000:

            # 객체의 중심 좌표 계산
            # x, y는 왼쪽 위이므로 너비와 높이의 절반을 더함
            red_center_x = x + w // 2
            red_center_y = y + h // 2

            # 화면 중심과 객체 중심의 X 방향 차이
            error_x = screen_center_x - red_center_x

            # 화면 중심과 객체 중심의 Y 방향 차이
            error_y = screen_center_y - red_center_y

            # X 오차를 이용해서 객체가 어느 방향에 있는지 판단
            if error_x > 10:
                print("LEFT")

            elif error_x < -10:
                print("RIGHT")

            else:
                print("CENTER")

            # Y 오차를 이용해서 객체가 어느 방향에 있는지 판단
            if error_y > 10:
                print("UP")

            elif error_y < -10:
                print("DOWN")

            else:
                print("Y CENTER")

            # 화면에 X 오차 표시
            # str()을 사용하는 이유:
            # "ERROR X : "는 문자이고 error_x는 숫자이기 때문에
            # 숫자를 문자로 바꿔서 하나의 문자열로 만들기 위해 사용
            cv2.putText(
                frame,
                "ERROR X : " + str(error_x),
                (50,350),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0,255,0),
                2
            )

            # 화면에 Y 오차 표시
            cv2.putText(
                frame,
                "ERROR Y : " + str(error_y),
                (50,400),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0,255,0),
                2
            )

            # 객체의 중심 위치에 초록색 점 표시
            cv2.circle(
                frame,
                (red_center_x, red_center_y),
                5,
                (0,255,0),
                -1
            )

            # --------------------------------
            # 3×3 Grid에서 객체의 X 위치 판단
            # --------------------------------

            if red_center_x < left_line_x:
                cv2.putText(
                    frame,
                    "X : LEFT",
                    (50,150),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0,255,0),
                    2
                )

            elif left_line_x < red_center_x < right_line_x:
                cv2.putText(
                    frame,
                    "X : CENTER",
                    (50,150),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0,255,0),
                    2
                )

            else:
                cv2.putText(
                    frame,
                    "X : RIGHT",
                    (50,150),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0,255,0),
                    2
                )

            # --------------------------------
            # 3×3 Grid에서 객체의 Y 위치 판단
            # --------------------------------

            if red_center_y < top_line_y:
                cv2.putText(
                    frame,
                    "Y : UP",
                    (50,250),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0,255,0),
                    2
                )

            elif top_line_y < red_center_y < bottom_line_y:
                cv2.putText(
                    frame,
                    "Y : CENTER",
                    (50,250),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0,255,0),
                    2
                )

            else:
                cv2.putText(
                    frame,
                    "Y : BOTTOM",
                    (50,250),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0,255,0),
                    2
                )

    # 파란색 객체들도 찾아서 중심점 표시
    for cnt in blue_contours:

        # 파란색 객체의 사각형 정보
        x, y, w, h = cv2.boundingRect(cnt)

        # 너무 작은 파란색 영역은 제외
        if w * h > 1000:

            # 파란색 객체 중심 좌표
            blue_center_x = x + w // 2
            blue_center_y = y + h // 2

            # 파란색 객체 중심에 초록색 점 표시
            cv2.circle(
                frame,
                (blue_center_x, blue_center_y),
                5,
                (0,255,0),
                -1
            )

    # 빨간색 픽셀 개수 계산
    red_pixels = cv2.countNonZero(mask)

    # 파란색 픽셀 개수 계산
    blue_pixels = cv2.countNonZero(mask2)

    # 빨간색 영역이 충분히 많으면 RED 표시
    if red_pixels > 5000:
        cv2.putText(
            frame,
            "RED",
            (50,50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0,0,255),
            2
        )

    # 파란색 영역이 충분히 많으면 BLUE 표시
    if blue_pixels > 5000:
        cv2.putText(
            frame,
            "BLUE",
            (50,90),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (255,0,0),
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
