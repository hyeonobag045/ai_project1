import streamlit as st
import csv

# 1. 페이지 기본 설정 및 예쁜 타이틀 ✨
st.set_page_config(page_title="배드민턴 랭킹 마스터 🏸", page_icon="🏸", layout="centered")
st.title("🏸 배드민턴 남자 단식 세계 랭킹 탐색기")
st.write("세계적인 배드민턴 선수들의 정보를 한눈에 알아보자구! 😎")

# 2. 데이터 불러오기 함수 (인코딩 패치 + 자동 순위 정렬! 📈)
@st.cache_data
def load_data():
    players_by_country = {}
    
    try:
        # 'utf-8-sig'로 유령 글자 제거 🛡️
        with open("men_single.csv", mode="r", encoding="utf-8-sig") as f:
            sample = f.read(2048)
            f.seek(0)
            dialect = csv.Sniffer().sniff(sample) if sample else None
            
            if dialect:
                reader = csv.DictReader(f, dialect=dialect)
            else:
                reader = csv.DictReader(f)
                
            for row in reader:
                clean_row = {k.strip(): v.strip() for k, v in row.items() if k is not None}
                
                country = clean_row.get("country", "Unknown")
                ranking = clean_row.get("ranking", "0")
                name = clean_row.get("player_name", clean_row.get("jorsey_name", "Unknown"))
                tournaments = clean_row.get("tournaments", "0")
                points = clean_row.get("points", "0")
                
                if country not in players_by_country:
                    players_by_country[country] = []
                    
                players_by_country[country].append({
                    "ranking": ranking,
                    "name": name,
                    "tournaments": tournaments,
                    "points": points
                })
                
        # ⭐ 핵심 피드백 반영: 각 나라별 선수들을 랭킹 숫자가 작은 순(1위부터)으로 정렬하기!
        for country in players_by_country:
            players_by_country[country].sort(key=lambda x: int(x["ranking"]) if x["ranking"].isdigit() else 9999)
            
    except FileNotFoundError:
        st.error("🚨 `men_single.csv` 파일을 찾을 수 없어! 대소문자나 파일 위치를 다시 확인해줘.")
        return {}
    except Exception as e:
        st.error(f"🚨 오 마이 갓! 데이터를 읽다가 다른 에러가 났어: {e}")
        return {}
    
    return players_by_country

data = load_data()

if data:
    # 3. 나라 선택 셀렉트박스 🌍
    countries = sorted(list(data.keys()))
    selected_country = st.selectbox("👉 궁금한 나라를 선택해봐!", countries)
    
    st.divider() # 깔끔한 구분선
    
    # 4. 해당 나라의 선수 목록 보여주기 🏅
    st.subheader(f"🌍 {selected_country}의 전사들")
    country_players = data[selected_country]
    
    # 이제 1위부터 순서대로 깔끔하게 리스트가 만들어져! 👍
    player_options
