import requests
import csv
import os

# ✅ 사용자 REST API 키 적용
api_key = "2828b3f825cd2176c9fa58716bbdfd0d"

# 📌 검색할 제주 지역 (서쪽, 중간, 동쪽)
search_areas = [
    {'x': 126.1628, 'y': 33.3946, 'area_name': 'West Jeju'},
    {'x': 126.570667, 'y': 33.450701, 'area_name': 'Middle Jeju'},
    {'x': 126.9748, 'y': 33.5097, 'area_name': 'East Jeju'}
]

# 요청 헤더 설정
headers = {
    "Authorization": f"KakaoAK {api_key}"
}

# CSV 파일 경로
csv_file = "jeju_restaurant.csv"

# ✅ 중복 방지를 위한 장소 ID 저장
unique_place_ids = set()

# 기존 파일이 있는지 확인
file_exists = os.path.isfile(csv_file)

# CSV 파일 열기 (추가 모드)
with open(csv_file, mode="a", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)

    # 헤더 작성 (파일이 없을 때만)
    if not file_exists:
        writer.writerow(["Place Name", "Longitude", "Latitude", "Phone", "Address"])

    # 각 지역별로 검색 수행
    for area in search_areas:
        print(f"🔍 Searching in {area['area_name']}...")

        page = 1  # 페이지 초기화

        while True:
            # API 요청 파라미터 설정
            params = {
                "query": "음식점",  # "음식점" (식당) 검색
                "x": area["x"],
                "y": area["y"],
                "radius": 20000,  # 20km 반경 내 검색
                "page": page,
                "size": 15  # 한 페이지당 15개 결과
            }

            try:
                # API 호출
                response = requests.get(
                    "https://dapi.kakao.com/v2/local/search/keyword.json",
                    headers=headers,
                    params=params
                )
                response.raise_for_status()  # 오류 발생 시 예외 처리
            except requests.exceptions.RequestException as e:
                print(f"❌ API 요청 실패: {e}")
                break

            # API 응답 데이터 처리
            data = response.json()
            documents = data.get("documents", [])

            if not documents:
                break  # 더 이상 결과 없음 → 검색 종료

            for document in documents:
                place_name = document.get("place_name")
                place_id = document.get("id")
                longitude = document.get("x")
                latitude = document.get("y")
                phone = document.get("phone", "N/A")
                address = document.get("road_address_name", document.get("address_name", "N/A"))

                # 중복 장소 필터링
                if place_id in unique_place_ids:
                    continue
                unique_place_ids.add(place_id)

                # CSV 파일에 저장
                writer.writerow([place_name, longitude, latitude, phone, address])

            page += 1  # 다음 페이지 요청

print("✅ 데이터 수집 완료! 결과가 jeju_restaurants.csv 파일에 저장되었습니다.")
