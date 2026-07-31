
# OpenCV Project 01 - Color Tracking(2026.07 ~ Present)
Python과 OpenCV를 활용하여 객체를 인식하고,
객체의 중심 좌표와 화면 내 위치를 계산하는 프로젝트입니다.

향후 드론 자율비행 및 객체 추적 시스템 구현을 위한
기초 영상처리 기술을 학습하는 것을 목표로 제작하였다.

## Projects
## Project Flow

Camera
↓

HSV Conversion
↓

Color Detection
↓

Contour Detection
↓

Bounding Box
↓

Center Point Calculation
↓

3×3 Grid
↓

Position Detection

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
LEFT TOP
CENTER TOP
RIGHT TOP

LEFT CENTER
CENTER
RIGHT CENTER

LEFT BOTTOM
CENTER BOTTOM
RIGHT BOTTOM


사용 기술:

- Python
- OpenCV
- HSV Color Detection
- Contour Detection


### 3 Development Environment

- Python
- OpenCV
- Visual Studio Code


### 4 Future Improvements

- 객체와 화면 중심 사이의 거리 계산
- 물체 추적 기능 추가
- 드론 이동 명령과 연동
- 실시간 자율비행 시스템 적용


 ### 5 어려웠던 점:

- 객체 중심 좌표 계산

처음에는 boundingRect()로 얻은 (x, y)가 객체의 중심 좌표인 줄 알았다. 공부하면서 (x, y)는 객체의 왼쪽 위 좌표이고, 중심 좌표는 x + w // 2, y + h // 2로 계산해야 한다는 것을 이해했다.

- 화면 좌표계 이해

수학 좌표와 OpenCV 좌표가 달라 처음에는 위치를 판단하는 과정에서 혼란이 있었다. OpenCV에서는 좌측 상단이 원점(0, 0)이며, x축은 오른쪽으로 증가하고 y축은 아래쪽으로 증가한다는 점이 지금까지 배워왔던 수학과 달라서 헷갈렸고 이후 좌표계를 이해한 뒤 위치 판단 조건을 올바르게 작성할 수 있었다

- 화면을 3×3으로 분할하는 조건 작성

if문으로 각 영역의 조건을 작성하는 과정에서 어떤 기준으로 나눠야 하는지 많이 헷갈렸다. 또한 객체의 중심 좌표가 화면에서 왼쪽으로 이동하면 x값이 작아지고, 오른쪽으로 이동하면 x값이 커진다는 좌표 개념이 위에 문제의 이유로 완전히 이해되지 않아 조건문을 작성하는 데 어려움을 겪었다. 이후 width // 3, (width * 2) // 3, height // 3, (height * 2) // 3를 이용해 화면을 3등분하는 방법을 이해하면서 원하는 위치를 정확하게 판단할 수 있었다

- 조건문의 위치

아직도 코드를 작성하다 보면 변수와 조건문을 어디에 작성해야 하는지 헷갈릴 때가 많다. 또한 위에서 만든 변수가 어떤 목적으로 만들어졌는지 기억이 나지 않아 같은 내용을 다시 찾아보는 경우도 있었다. 코드를 여러 번 수정하고 실행해 보면서 변수의 역할과 조건문의 실행 순서를 조금씩 이해하게 되었다.

- 해결 방법 (Solutions)

* `boundingRect()`와 중심 좌표 계산 방법을 다시 학습하였다.
* OpenCV 좌표계를 직접 그림으로 정리하여 x축과 y축의 증가 방향을 이해하였다.
* 화면을 일정한 비율로 나누는 방법을 적용하여 3×3 Grid를 구현하였다.
* 코드를 여러 번 수정하고 실행하면서 변수의 역할과 조건문의 실행 순서를 이해하였다.


