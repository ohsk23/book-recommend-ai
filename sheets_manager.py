import os
import gspread
import json
from dotenv import load_dotenv
import streamlit as st
from datetime import datetime

load_dotenv()

class SheetsManager:
    def __init__(self):
        # Streamlit Cloud 환경의 secrets에서 인증 정보 가져오기
        gcp_credentials = {
            "type": st.secrets["gcp_service_account"]["type"],
            "project_id": st.secrets["gcp_service_account"]["project_id"],
            "private_key_id": st.secrets["gcp_service_account"]["private_key_id"],
            "private_key": st.secrets["gcp_service_account"]["private_key"],
            "client_email": st.secrets["gcp_service_account"]["client_email"],
            "client_id": st.secrets["gcp_service_account"]["client_id"],
            "auth_uri": st.secrets["gcp_service_account"]["auth_uri"],
            "token_uri": st.secrets["gcp_service_account"]["token_uri"],
            "auth_provider_x509_cert_url": st.secrets["gcp_service_account"]["auth_provider_x509_cert_url"],
            "client_x509_cert_url": st.secrets["gcp_service_account"]["client_x509_cert_url"],
            "universe_domain": st.secrets["gcp_service_account"]["universe_domain"]
        }

        gc = gspread.service_account_from_dict(gcp_credentials)
        self.sheet = gc.open(st.secrets["google_sheets"]["sheets_name"]).sheet1
        
        # 스프레드시트 헤더 초기화
        if not self.sheet.get_all_values():
            self.sheet.append_row([
                "책 제목",
                "저자",
                "분류 레벨",
                "추천 도서",
                "분류 및 추천 이유",
                "추천 일시"
            ])

    def save_recommendation(self, data: str):
        """추천 결과를 스프레드시트에 저장"""
        book_data = json.loads(data)
        self.sheet.append_row([
            book_data["book"],
            book_data["author"],
            book_data["level"],
            ", ".join(book_data["recommendations"]),
            book_data["explanation"],
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ]) 