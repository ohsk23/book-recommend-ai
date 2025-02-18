import streamlit as st
import json
from book_classifier import classify_book
from sheets_manager import SheetsManager

# 페이지 설정
st.set_page_config(
    page_title="📚 책 추천 AI",
    page_icon="📚",
    layout="wide"
)

# 제목과 설명
st.title("📚 책 추천 AI")
st.write("책 제목을 입력하면, 적절한 레벨로 분류하고 추천해드립니다!")

# 사이드바에 설명 추가
with st.sidebar:
    st.header("📖 고전 레벨 분류 기준")
    st.write("""
    - **고전 레벨 3**: 학문의 창시자급
    - **고전 레벨 2**: 역사의 한 획을 그은 독창적인 저서
    - **고전 레벨 1**: 현대적이지만 검증된 저서
    - **교양서**: 사회적 영향력과 파급력을 고려한 대중 교양서
    """)

# 메인 입력 폼
book_name = st.text_input("책 제목을 입력하세요:")

if book_name:
    with st.spinner('AI가 분석 중입니다...'):
        try:
            # AI 분석 결과 가져오기
            result = classify_book(book_name)
            result_dict = json.loads(result)
            
            # 결과 표시
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("📊 분류 결과")
                st.write(f"**입력하신 책**: {result_dict['book']}")
                st.write(f"**저자**: {result_dict['author']}")
                st.write(f"**분류 레벨**: {result_dict['level']}")
                st.write("**추천 이유**:", result_dict['explanation'])
            
            with col2:
                st.subheader("📚 추천 도서")
                for idx, book in enumerate(result_dict['recommendations'], 1):
                    st.write(f"{idx}. {book}")
            
            # Google Sheets에 저장
            sheets_manager = SheetsManager()
            sheets_manager.save_recommendation(result)
            
            st.success("분석 결과가 저장되었습니다! 👍")
            
        except Exception as e:
            st.error(f"오류가 발생했습니다: {str(e)}") 