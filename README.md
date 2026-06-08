# CLIP ONNX Video Scene Searcher

경량화된 ONNX 가중치와 클라우드에 인덱싱된 이미지 주소를 활용하여, 실시간으로 영상 내 장면을 검색하는 시스템입니다.
Python 3.12.3에서 구동됩니다.

## 1. 로컬 환경 패키지 설치
1) git clone을 통해 전체 파일을 내려받습니다.
2) 프로젝트 폴더 내 터미널에서 아래 명령어를 실행하여 필수 라이브러리를 일괄 설치합니다.
pip install -r requirements.txt

## 2. 구글 드라이브에서 모든 파일 다운로드
https://drive.google.com/drive/folders/10MxrgZf02qI4Z1Td3XvOhDXJWOREVJKM?usp=sharing
해당 구글 드라이브에서 전체 파일을 다운로드받고, app.py 및 utils.py와 같은 디렉터리 경로에 붙여넣습니다.

## 3. 최종 파일 구조(참고용)
<img width="464" height="268" alt="파일 구조" src="https://github.com/user-attachments/assets/6cda10ca-ec52-41f5-92bd-bb3122a2e691" />

## 4. venv 가상환경에서 app.py 실행
