import pandas as pd
from datetime import datetime, timedelta
import random
import time
import google.generativeai as genai

# Gemini API 키 설정
# TODO: YOUR_GEMINI_API_KEY 부분을 본인의 실제 Gemini API 키로 교체하세요.
# https://aistudio.google.com/app/apikey 에서 API 키를 발급받을 수 있습니다.
genai.configure(api_key="AIzaSyDyA0YZNHk6O01O1i03cnJl-8zMJDuX5uY")

model = genai.GenerativeModel('gemini-2.0-flash')

# 리뷰 생성 프롬프트 함수
def generate_review_with_gemini_flash(product_name, review_type):
    """
    Gemini 2.0 Flash 모델을 호출하여 특정 제품에 대한 한국어 고객 리뷰 텍스트를 생성합니다.
    """
    prompt_base = f"Google Merchandise Store에서 판매하는 '{product_name}'에 대한 한국어 고객 리뷰를 작성해 줘. 리뷰는 최소 80자 이상 250자 이하로 작성하고, 고객이 실제로 사용하고 느낀 것처럼 생생하고 자연스럽게 써 줘. 반말로 쓰지 말고 정중한 어투로 작성해 줘. 리뷰에는 상품명 '{product_name}'을 한 번 이상 포함시켜 줘."

    if review_type == "positive":
        prompt = prompt_base + " 리뷰는 매우 긍정적인 내용이어야 해. 어떤 점이 가장 만족스러웠고 좋았는지 구체적인 사용 경험을 바탕으로 자세히 설명해 줘. 예를 들어 디자인, 기능, 품질, 배송, 사용 편의성 등을 언급해 줘."
    elif review_type == "negative":
        prompt = prompt_base + " 리뷰는 솔직하고 비판적인 부정적인 내용이어야 해. 어떤 점이 아쉬웠거나 불편했고, 개선이 필요하다고 생각하는지 구체적인 불만 사항과 이유를 적어 줘. 예를 들어 성능 문제, 품질 불량, 배송 지연, 고객 서비스 문제 등을 언급해 줘. 하지만 너무 공격적이지 않고, 건설적인 비판으로 작성해 줘."
    else: # mixed
        prompt = prompt_base + " 리뷰는 긍정적인 부분과 아쉬운 부분이 섞여 있는 현실적인 내용이어야 해. 장점과 단점을 모두 포함하여 균형 잡힌 시각으로 작성해 줘."

    try:
        response = model.generate_content(prompt)
        if not response.text:
            return ""
        return response.text.strip()
    except Exception as e:
        print(f"API 호출 오류 발생 ({product_name}, {review_type}): {e}. 재시도 또는 건너뛰기...")
        return ""

# 가상 고객 리뷰 데이터 생성 함수
def generate_customer_reviews_gemini(num_records):
    """
    Gemini 2.0 Flash를 사용하여 지정된 수의 가상 고객 리뷰 데이터를 생성합니다.
    """
    data = []
    # 리뷰 발생 기간 설정 (현재 날짜 기준)
    # !! 리뷰 데이터의 시작 날짜를 변경하려면 이 부분을 수정하세요 (예: datetime(2024, 1, 1, 0, 0, 0)) !!
    start_date = datetime(2024, 11, 1, 9, 0, 0)
    # !! 리뷰 데이터의 종료 날짜를 변경하려면 이 부분을 수정하세요 (예: datetime(2025, 12, 31, 23, 59, 59)) !!
    end_date = datetime(2025, 6, 30, 23, 59, 59)

    # 대중적인 Google Merchandise Shop 제품 10가지
    popular_product_types = [
        "Google 로고 티셔츠",
        "Google 머그컵",
        "크롬캐스트",
        "네스트 허브",
        "Pixel 폰 케이스",
        "Google 후드티",
        "Google 백팩",
        "Google 에코백",
        "Google 스테인리스 물병",
        "Google 스마트 스피커"
    ]

    # 소셜 미디어 소스 목록
    social_media_sources = ["Twitter", "Instagram", "Facebook", "X", "YouTube", "Threads", "블로그", "네이버카페"]
    # 가상 고객 위치 ID 목록
    locations = [5001, 5002, 5003, 5004, 5005, 5006, 5007, 5008, 5009, 5010] # 10개 임의 지역 ID

    generated_review_texts = set() # 생성된 리뷰 텍스트의 중복을 확인하기 위한 집합

    for i in range(1, num_records + 1):
        customer_review_id = i
        customer_id = 1000 + i
        location_id = random.choice(locations)

        # 시작 날짜와 종료 날짜 사이에서 임의의 시간 생성
        total_seconds = int((end_date - start_date).total_seconds())
        random_seconds = random.randint(0, total_seconds)
        review_datetime = (start_date + timedelta(seconds=random_seconds)).strftime("%Y-%m-%d %H:%M:%S")

        review_text = ""
        attempts = 0
        product_name = random.choice(popular_product_types)
        # 리뷰 유형을 긍정, 부정, 혼합으로 무작위 선택 (비율 조정)
        review_type = random.choices(["positive", "negative", "mixed"], weights=[0.65, 0.2, 0.15], k=1)[0] # 긍정 비중을 높임

        # 고유하고 유효한 리뷰 텍스트가 생성될 때까지 최대 15번 시도
        while (not review_text or review_text in generated_review_texts) and attempts < 15:
            review_text = generate_review_with_gemini_flash(product_name, review_type)
            attempts += 1
            time.sleep(1.0) # Flash 모델은 더 빠르므로 지연 시간을 1초로 조정

        # 15번 시도 후에도 유효한 리뷰가 생성되지 않았다면 해당 레코드를 건너뜁니다.
        if not review_text or review_text in generated_review_texts:
            print(f"경고: {customer_id} 고객의 리뷰를 여러 번 시도했지만 고유하고 유효하게 생성할 수 없었습니다. 이 레코드는 건너뜁니다.")
            continue # 이 레코드를 건너뛰고 다음 레코드로 이동

        generated_review_texts.add(review_text) # 생성된 리뷰 텍스트 집합에 추가

        social_media_source = random.choice(social_media_sources)
        social_media_handle = f"@{social_media_source.replace(' ', '').replace('네이버', 'Naver').replace('블로그', 'Blog')}User_{customer_id}_{random.randint(100,999)}" # 더 다양하고 자연스러운 소셜 미디어 핸들 생성

        data.append({
            "customer_review_id": customer_review_id,
            "customer_id": customer_id,
            "location_id": location_id,
            "review_datetime": review_datetime,
            "review_text": review_text,
            "social_media_source": social_media_source,
            "social_media_handle": social_media_handle
        })

    # 실제로 생성된 레코드 수가 요청된 num_records보다 적을 수 있음을 알립니다.
    if len(data) < num_records:
        print(f"참고: 요청된 {num_records}개 중 {len(data)}개의 고유하고 유효한 리뷰만 생성되었습니다. 일부 API 호출 오류나 중복으로 인해 건너뛴 레코드가 있을 수 있습니다.")

    return pd.DataFrame(data)

# 50개 데이터 생성 시작 메시지
print("50개의 고객 리뷰를 Gemini 2.0 Flash를 통해 생성 중입니다. 이 과정은 API 호출 및 응답 대기로 인해 시간이 다소 소요될 수 있습니다. 잠시만 기다려 주세요...")
df_gemini_generated = generate_customer_reviews_gemini(50) # 50개 리뷰 생성
print("리뷰 생성이 완료되었습니다!")

# CSV 파일로 저장
csv_file_path_gemini_generated = "customer_reviews_50_gemini_flash_v2.csv"
# 한글 깨짐 방지를 위해 'utf-8-sig' 인코딩 사용
df_gemini_generated.to_csv(csv_file_path_gemini_generated, index=False, encoding='utf-8-sig')

print(f"'{csv_file_path_gemini_generated}' 파일이 생성되었습니다. 이 파일을 다운로드하여 사용하시면 됩니다.")