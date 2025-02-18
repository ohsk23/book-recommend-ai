import os
from openai import OpenAI
import streamlit as st

client = OpenAI(api_key=st.secrets["openai"]["api_key"])

def classify_book(user_input: str) -> dict:
    prompt = f"""당신은 책 추천 전문가입니다.

    사용자가 제시한 책 "{user_input}"을 고전 레벨별로 분류하고, 적절한 책을 추가 추천하세요.

    분류 기준:
    - 고전 레벨 3 (학문의 창시자급)
    - 고전 레벨 2 (역사의 한 획을 그은 독창적인 저서)
    - 고전 레벨 1 (현대적이지만 검증된 저서)
    - 사회적 영향력과 파급력을 고려한 대중 교양서

    다음 JSON 형식으로 응답해주세요:
    {{
        "book": "입력된 책 제목",
        "level": "분류된 레벨",
        "recommendations": ["추천 책1", "추천 책2", "추천 책3"],
        "explanation": "분류 및 추천 이유"
    }}
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "당신은 책 추천 전문가입니다."},
            {"role": "user", "content": prompt}
        ],
        response_format={"type": "json_object"}
    )

    return response.choices[0].message.content