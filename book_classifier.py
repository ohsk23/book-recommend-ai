import os
from openai import OpenAI
import streamlit as st

client = OpenAI(api_key=st.secrets["openai"]["api_key"])

def classify_book(user_input: str) -> dict:
    prompt = f"""당신은 독서 큐레이터이자 학문적 분류 전문가입니다.
    사용자가 제시한 책 "{user_input}"을 고전 레벨별로 분류하고, 적절한 책을 추가 추천하세요.

### **📌 분류 기준**
✅ **고전 레벨 3 (학문의 창시자급, 패러다임을 만든 책)**
- 특정 학문의 기반을 만든 필수 원전이거나, 학문의 패러다임을 처음으로 제시한 책.
- 기존 학문을 완전히 새롭게 창시했거나, 기존 질서를 뒤엎은 혁신적인 책.
- **대표 예시:**
  - **철학/정치:** 아리스토텔레스 《니코마코스 윤리학》, 플라톤 《국가》
  - **역사:** 헤로도토스 《역사》
  - **경제학:** 아담 스미스 《국부론》, 마르크스 《자본론》
  - **과학:** 다윈 《종의 기원》, 프로이트 《꿈의 해석》
  - **기타:** 니체 《차라투스트라는 이렇게 말했다》

✅ **고전 레벨 2 (역사의 한 획을 그은 독창적인 저서)**
- 학문의 정점은 아니지만, 기존 패러다임을 확장하거나 새로운 이론을 제시한 책.
- 학문적으로 검증되었으며, 현대 학계에서도 중요한 논의 대상.
- **대표 예시:**
  - **정치/사회:** 한나 아렌트 《예루살렘의 아이히만》, 《악의 평범성》
  - **과학/물리학:** 하이젠베르크 《부분과 전체》
  - **역사/문명:** 제러드 다이아몬드 《총, 균, 쇠》 (학문적으로 논란이 있지만, 데이터 기반 연구가 포함되어 있음)

✅ **고전 레벨 1 (현대적이지만 검증된 저서)**
- 현대 학문에서 중요한 저서로, 학문적으로 신뢰할 수 있으며 논리적 검증이 이루어진 책.
- 실험적 연구와 데이터를 기반으로 하며, 학계에서도 일정 수준 검증된 내용 포함.
- **대표 예시:**
  - **인지과학/심리학:** 대니얼 카너먼 《생각에 관한 생각》, 마이클 토마셀로 《생각의 기원》
  - **도덕심리학:** 조너선 하이트 《바른 마음》
  - **진화생물학:** 리처드 도킨스 《이기적 유전자》

✅ **사회적 영향력과 파급력을 고려한 대중 교양서 (읽어볼 가치가 있는 책)**
- 학문적 엄밀함은 부족할 수 있지만, 사회적으로 큰 논의와 영향을 미친 책.
- 논란이 있거나 학계에서 절대적 검증을 받지는 않았으나, 지적 탐구에 유익한 책.
- **대표 예시:**
  - **역사/문명:** 유발 하라리 《사피엔스》, 《호모 데우스》
  - **리스크/경제:** 나심 탈레브 《블랙 스완》, 《안티프래질》
  - **경영/실용서:** 레이 달리오 《원칙》

  고전 레벨이나 추천할만한 대중 교양서에 해당하지 않는 경우에는 반드시 해당없음으로 분류해야 합니다.
  사회적 영향력과 파급력을 고려할 때 위 목록에 해당하는 도서들과 견줄 만하지 않다면 추천해서는 안 됩니다.
  추천이 목적이므로 별로인 도서를 추천하는 것은 최악의 선택입니다.
  고전은 아니나 향후 고전의 반열에 오를 수 있을 정도의 도서만 분류합니다.
  - 《미움받을 용기》, 《물은 답을 알고 있다》 처럼 사실이 아닌 내용을 사실인 것처럼 포장하는 도서
  - 《지적 대화를 위한 넓고 얕은 지식》, 《미라클 모닝》 이런 가벼운 내용은 해당없음으로 분류합니다. 
  - 모든 문학은 답변 대상이 아니므로 해당없음으로 분류합니다.
  - 책이 실제로 존재하는 책인지도 꼭 확인하세요.
  - 대중 교양서 중에 다른 대중 교양서를 많이 참조하는 책들은 가능하면 제외합니다. 고전을 많이 참조한 책이 좋은 책입니다.
  - 책 추천은 해당 분야의 비슷한 레벨의 다른 책들을 추천합니다. 제시된 예시에 한정하지 말고 가장 대표성이 뛰어난 책들을 추천하세요.

    다음 JSON 형식으로 응답해주세요:
    {{
        "book": "입력된 책 제목",
        "author": "입력된 책 저자",
        "level": "분류된 레벨",
        "recommendations": ["추천 책1", "추천 책2", "추천 책3"],
        "explanation": "분류 및 추천 이유"
    }}
    """

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "당신은 책 추천 전문가입니다."},
            {"role": "user", "content": prompt}
        ],
        response_format={"type": "json_object"}
    )

    return response.choices[0].message.content