import streamlit as st
import onnxruntime as ort
from transformers import AutoTokenizer
import numpy as np
import json
import os

@st.cache_resource
def load_onnx_tokenizer():
    """
    CLIP 표준 토크나이저를 로드합니다.
    """
    return AutoTokenizer.from_pretrained("openai/clip-vit-base-patch32")

@st.cache_resource
def load_onnx_text_model(model_dir):
    """
    변환 완료된 텍스트 인코더 ONNX 세션을 로드합니다.
    """
    text_onnx_path = os.path.join(model_dir, "clip_text_model.onnx")
    if not os.path.exists(text_onnx_path):
        raise FileNotFoundError(f"clip_text_model.onnx 파일을 찾을 수 없습니다. 변환 스크립트를 먼저 실행하십시오.")
    
    session = ort.InferenceSession(text_onnx_path, providers=['CPUExecutionProvider'])
    return session


def search_video_frames(query_text, onnx_session, tokenizer, top_k=2):
    """
    ONNX Runtime을 사용하여 텍스트 쿼리를 인코딩하고, 
    JSON DB 내부의 이미지 특징 벡터들과 실시간 코사인 유사도를 연산합니다.
    """
    json_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "video_web_train.json")
    
    if not os.path.exists(json_path):
        print(f"오류: {json_path} 파일이 존재하지 않습니다.")
        return []
        
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            data_list = json.load(f) 
            
        if not data_list or not isinstance(data_list, list):
            print("오류: JSON 파일이 비어있거나 올바른 리스트 형식이 아닙니다.")
            return []
            
        # ONNX 텍스트 인코더가 요구하는 입력 형태로 변환 (77 토큰 제한)
        inputs = tokenizer([query_text], padding="max_length", max_length=77, truncation=True)
        
        input_ids = np.array(inputs["input_ids"], dtype=np.int64)
        attention_mask = np.array(inputs["attention_mask"], dtype=np.int64)
        
        # ONNX 모델 추론 진행
        onnx_outputs = onnx_session.run(
            ['text_embeddings'],
            {
                'input_ids': input_ids, 
                'attention_mask': attention_mask
            }
        )
        text_features = onnx_outputs[0]
        
        # 코사인 유사도 연산을 위한 L2 정규화
        text_features = text_features / np.linalg.norm(text_features, axis=-1, keepdims=True)
        
        search_pool = []
        
        # JSON 인덱스 풀을 순회하며 코사인 유사도 연산 수행
        for item in data_list:
            if "features" not in item:
                continue
                
            saved_feature = np.array(item["features"], dtype=np.float32)
            saved_feature = saved_feature / np.linalg.norm(saved_feature, axis=-1, keepdims=True)
            
            similarity = float(np.dot(text_features, saved_feature.T)[0])
            
            # 타임스탬프 파싱 (분:초 구조를 초 단위 데이터로 변환)
            time_str = item.get("timestamp", "00:00")
            time_parts = time_str.split(":")
            if len(time_parts) == 2:
                minutes, seconds = map(int, time_parts)
                total_seconds = float(minutes * 60 + seconds)
            else:
                total_seconds = 0.0
                
            search_pool.append({
                "video_name": item.get("video_id", "unknown.mp4"),
                # 구글 API 스크립트가 치환 완료한 uc?export=download 주소를 frame_name 키에 매핑합니다.
                "frame_name": item.get("image_path", ""), 
                "timestamp": total_seconds,
                "similarity": similarity
            })
            
        # 유사도 점수 기준 내림차순 정렬
        search_pool.sort(key=lambda x: x["similarity"], reverse=True)
        return search_pool[:top_k]

    except Exception as e:
        print(f"search_video_frames 내부 연산 중 예외 발생: {e}")
        return []