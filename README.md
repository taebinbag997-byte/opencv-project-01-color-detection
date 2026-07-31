
# OpenCV Project 01 - Color Tracking(2026.07 ~ Present)
Python과 OpenCV를 활용하여 객체를 인식하고,
객체의 중심 좌표와 화면 내 위치를 계산하는 프로젝트입니다.

향후 드론 자율비행 및 객체 추적 시스템 구현을 위한
기초 영상처리 기술을 학습하는 것을 목표로 제

## Projects

### 1. Face Detection

- Haar Cascade를 이용한 얼굴 인식
- 카메라 영상에서 얼굴 개수 검출
- 검출된 얼굴 개수 표시

사용 기술:
- Python
- OpenCV
- Haar Cascade


### 2. Color Detection & Position Detection

카메라 영상에서 특정 색상을 인식하고 객체의 위치를 판단하는 프로젝트입니다.

구현 기능:

- Red / Blue 색상 인식
- HSV 색 공간 변환
- Mask 생성
- Contour 검출
- 객체 중심 좌표 계산
- 화면 3×3 Grid 분할
- 객체 위치 판단

위치 판단 방식:
LEFT TOP CENTER TOP RIGHT TOP


사용 기술:

- Python
- OpenCV
- HSV Color Detection
- Contour Detection


###3 Development Environment

- Python
- OpenCV
- Visual Studio Code


###4 Future Improvements

- 객체와 화면 중심 사이의 거리 계산
- 물체 추적 기능 추가
- 드론 이동 명령과 연동
- 실시간 자율비행 시스템 적용


###4 어려웠던 점:

- 객체 중심 좌표 계산

처음에는 `boundingRect()`로 얻은 `(x, y)`가 객체의 중심 좌표라고 생각했다. 하지만 `(x, y)`는 객체의 왼쪽 위 좌표라는 것을 알게 되었고, 중심 좌표를 구하기 위해 `center_x = x + w // 2`, `center_y = y + h // 2` 공식을 적용하였다.

- 화면 좌표계 이해

수학 좌표계와 OpenCV 좌표계가 달라 처음에는 위치를 판단하는 과정에서 혼란이 있었다. OpenCV에서는 좌측 상단이 원점(0, 0)이며, x축은 오른쪽으로 증가하고 y축은 아래쪽으로 증가한다는 점을 이해한 뒤 위치 판단 조건을 올바르게 작성할 수 있었다.

- 화면을 3×3으로 분할하는 조건 작성

처음에는 화면 중앙과 객체의 오차(`error_x`, `error_y`)를 이용하여 LEFT, RIGHT, CENTER를 판단하였다. 이후 화면을 3×3 영역으로 나누기 위해 `width // 3`, `(width * 2) // 3`, `height // 3`, `(height * 2) // 3` 값을 이용하여 각 영역을 판단하도록 코드를 수정하였다.

- 조건문의 위치

처음에는 객체가 검출되지 않았을 때도 `center_x`를 사용하는 문제가 발생하였다. 이를 해결하기 위해 객체가 검출된 경우(`if w * h > 1000:`) 안에서 중심 좌표를 계산하고, 그 안에서 위치를 판단하도록 코드를 수정하였다.

- 해결 방법 (Solutions)

* `boundingRect()`와 중심 좌표 계산 방법을 다시 학습하였다.
* OpenCV 좌표계를 직접 그림으로 정리하여 x축과 y축의 증가 방향을 이해하였다.
* 화면을 일정한 비율로 나누는 방법을 적용하여 3×3 Grid를 구현하였다.
* 변수의 생성 위치와 조건문의 실행 순서를 수정하여 오류를 방지하였다.


