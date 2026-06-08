# CLIP ONNX Video Scene Searcher

경량화된 ONNX 가중치와 클라우드에 인덱싱된 이미지 주소를 활용하여, 실시간으로 영상 내 장면을 검색하는 시스템입니다.

데이터 파이프라인

---

## 1. 로컬 환경 패키지 설치
1) Python 3.12.3에서 구동됩니다.
2) git clone을 통해 전체 파일을 내려받습니다.
3) 프로젝트 폴더 내 터미널에서 아래 명령어를 실행하여 필수 라이브러리를 일괄 설치합니다.
pip install -r requirements.txt

## 2. 구글 드라이브에서 모든 파일 다운로드
https://drive.google.com/drive/folders/10MxrgZf02qI4Z1Td3XvOhDXJWOREVJKM?usp=sharing
해당 구글 드라이브에서 전체 파일을 다운로드받고, app.py 및 utils.py와 같은 디렉터리 경로에 붙여넣습니다.

## 3. 최종 파일 구조(참고용)
<img width="464" height="268" alt="파일 구조" src="https://github.com/user-attachments/assets/6cda10ca-ec52-41f5-92bd-bb3122a2e691" />

## 4. venv 가상환경에서 app.py 실행

## 5. 실행화면
1) 처음 실행시켰을 때의 화면
<img width="1919" height="906" alt="실행화면 1" src="https://github.com/user-attachments/assets/93fa0c96-b319-470a-9582-50f7517f67f1" />
2) 텍스트 쿼리를 주고 모델 추론을 실행시켰을 때의 화면
<img width="1919" height="903" alt="실행화면 2" src="https://github.com/user-attachments/assets/f35d02c8-6600-41c2-a356-e83593cfe0d8" />
3) 결과
<img width="1919" height="905" alt="실행화면 3" src="https://github.com/user-attachments/assets/4ef23b23-8951-4f99-a8b0-2318c4153700" />
<img width="1919" height="908" alt="실행화면 4" src="https://github.com/user-attachments/assets/11dd171c-2681-4fc4-87cd-ad68e69bffd2" />

---
# 팀원별 역할 분담
큰 틀로 봤을 때 모델 담당은 최수아이고, 시스템 담당은 김도은입니다. 다만 물리적으로 아예 역할 분담을 나눈 것이 아닌 어려운 점이 있다면 적극 소통하고 존중하여 화학적으로도 역할을 분담했습니다. 해당 역할 분담은 단순히 기여도가 더 높은 쪽을 작성하였고, 모든 분야에서 서로 협력하였습니다.
-20230964 김도은: 기획, 이미지 데이터 수집, RoLA 파인튜닝 1차, UI 설계, Web app 통합 및 시스템 안정화
-20240904 최수아: 기획, 동영상 데이터 수집, RoLA 파인튜닝 2-3차 및 파인튜닝 총괄, 실험 설계 및 성능평가


