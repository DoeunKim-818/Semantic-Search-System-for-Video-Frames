# CLIP Video Scene Searcher 프로젝트

경량화된 ONNX 가중치와 클라우드에 인덱싱된 이미지 주소를 활용하여, 실시간으로 영상 내 장면을 검색하는 시스템입니다. 자연어 검색어와 영상 프레임 간의 시맨틱 매칭 정확도를 높이기 위해, CLIP 비전 인코더를 대상으로 LoRA기법을 도입하여 3차까지 파인튜닝을 수행했습니다. 13만 장의 대용량 이미지는 구글 클라우드에 격리하고 주소만 JSON 인덱스로 관리하여, 로컬 저장 공간 부담을 줄였습니다.

### 기술 스택 (Tech Stacks)
- AI Core: Python, OpenAI CLIP, PyTorch, LoRA Fine-Tuning
- Optimization & Inference: ONNX Runtime, Hugging Face Transformers (CLIP Tokenizer)
- Data Pipeline: Google Drive API v3 (Recursive Queue Search), JSON Indexing DataBase
- Frontend & Server: Streamlit, NumPy, Pillow

---
# 데이터 파이프라인

전체 파이프라인은 크게 **1) 오프라인 전처리 및 인덱싱 단계**와 **2) 온라인 실시간 AI 추론 단계**의 2-Track 구조로 흐릅니다. 대용량 이미지 데이터를 로컬에 담지 않고 구현하기 위해 고안한 아키텍처입니다.

## 1. 수집 및 특징 추출
- 원시 데이터: 수많은 원본 비디오들로부터 초당 프레임 단위로 자른 133,488개의 이미지 파일들입니다.
- 파인튜닝: 수집된 프레임 데이터를 고도화하기 위해 CLIP을 LoRA 기법으로 1차, 2차, 최종 3차까지 파인튜닝시켰습니다.
- 특징 추출: 파인튜닝된 AI 모델을 통해 이미지들의 고유한 시각적 의미를 담은 특징 벡터를 모두 추출해냈습니다.

## 2. 클라우드 이중화 및 주소 치환
- 자원 격리 배치: 이미지 파일들은 구글 드라이브 스토리지에 업로드하여 클라우드에 격리시켰습니다.
- 자동화 주소 변환: 파이썬의 구글 드라이브 API를 연동한 재귀적 탐색 스크립트를 구축했습니다. 이 스크립트가 트리 구조의 하위 폴더들을 잡아 이미지의 고유 ID를 확보합니다.
- 인덱스 DB 구축: 로컬 상대 경로로 적혀 있던 기존 JSON 데이터베이스들을 구글 드라이브 스트리밍 주소로 치환한 뒤, 대용량 병합 스크립트를 가동하여 json 파일 인덱스를 완성했습니다.

## 3. 웹 앱 추론 및 서빙
- 모델 경량화: 텍스트 인코더 모델을 ONNX Runtime 구조로 변환하여 배포 용량을 경량화했습니다.
- 메모리 캐싱 최적화: 파일 입출력 병목이 생기는 걸 막기 위해, Streamlit 캐싱 기능을 적용해 최초 1회만 로딩했습니다.
- 실시간 유사도 매칭: 사용자가 자연어로 상황을 검색하면, 실시간으로 텍스트 벡터를 뽑아내고, 이미지 벡터들과 코사인 유사도 연산을 수행합니다.
- 이미지 스트리밍: 최종 매칭된 결과물은 이미지를 로컬에서 로드하지 않고, 웹 브라우저가 구글 클라우드 서버에서 실시간 스트리밍 호출하여 렌더링합니다.
---

# 의존성 설치 및 실행 방법
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


