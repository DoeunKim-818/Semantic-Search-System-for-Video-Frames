import streamlit as st
from PIL import Image
import os
from utils import load_onnx_tokenizer, load_onnx_text_model, search_video_frames

st.set_page_config(page_title="CLIP Video Scene Searcher", layout="wide")
st.title("CLIP 동영상 내 프레임 검색 시스템")
st.write("텍스트-비디오 인덱싱 매칭을 수행합니다.")

st.divider()

st.sidebar.header("파라미터 설정(결과 개수)")
top_k = st.sidebar.slider("출력할 결과 개수 선택", min_value=1, max_value=3, value=2, step=1)

# 경로 설정
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ONNX_MODELS_DIR = BASE_DIR  
VIDEO_DIR = os.path.join(BASE_DIR, "video_frames")

st.subheader("1. 텍스트 쿼리 입력")
text_query = st.text_input("검색하고 싶은 풍경이나 상황의 묘사를 입력하세요.", placeholder="예: a man driving a car with a steering")

st.divider()
st.subheader("2. CLIP 검출 결과")

if text_query:
    if st.button("검출 시작", type="primary"):
        with st.spinner("ONNX Runtime 엔진이 프레임을 분석 중입니다."):
            try:
                tokenizer = load_onnx_tokenizer()
                onnx_session = load_onnx_text_model(ONNX_MODELS_DIR)
                
                search_results = search_video_frames(text_query, onnx_session, tokenizer, top_k=top_k)
                
                if not search_results:
                    st.warning("일치하는 검색 결과가 없거나 JSON 파일 로드에 실패했습니다.")
                
                for rank, result in enumerate(search_results):
                    st.markdown(f"### {rank + 1} 순위 매칭 결과 (유사도: {result['similarity']:.4f})")
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write("해당 시점의 동영상")
                        local_video_path = os.path.join(VIDEO_DIR, result['video_name'])
                        
                        if os.path.exists(local_video_path):
                            st.video(local_video_path, start_time=int(result['timestamp']))
                        else:
                            st.warning(f"로컬 디렉토리에 {result['video_name']} 파일이 존재하지 않아 외부 샘플 영상으로 대체 재생합니다.")
                            st.video("https://vjs.zencdn.net/v/oceans.mp4", start_time=int(result['timestamp']))
                            
                    with col2:
                        st.write("그때의 이미지 (Key Frame)")
                        
                        # utils.py에서 전달해준 구글 드라이브 다운로드 URL 주소 수신
                        web_image_url = result.get('frame_name')
                        
                        if web_image_url and web_image_url.startswith("http"):
                            # 엑스박스로 그냥 넘어가는 현상을 방지하기 위해 HTML 구조를 우회하여 에러 처리를 검증합니다.
                            try:
                                st.image(web_image_url, caption=f"추출 시점: {int(result['timestamp'])}초", use_container_width=True)
                            except Exception as img_err:
                                st.error(f"이미지 렌더링 도중 예외 발생: {img_err}")
                        else:
                            st.error("유효하지 않거나 비어있는 이미지 주소 형식입니다.")
                            st.code(f"수신된 주소 데이터: {web_image_url}")
                            
                    st.divider()
                    
                st.success("ONNX 추론 및 매칭 출력이 완료되었습니다.")
            except Exception as e:
                st.error(f"검색 연산 도중 오류가 발생했습니다: {e}")