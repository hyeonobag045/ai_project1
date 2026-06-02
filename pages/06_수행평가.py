import streamlit as st
import csv

# 1. 페이지 기본 설정 및 예쁜 타이틀 ✨
st.set_page_config(page_title="배드민턴 랭킹 마스터 🏸", page_icon="🏸", layout="centered")
st.title("🏸 배드민턴 남자 단식 세계 랭킹 탐색기")
st.write("세계적인 배드민턴 선수들의 정보를 한눈에 알아보자구! 😎")

# 2. 데이터 불러오기 함수 (안전 제일 패치! 🛡️)
@st.cache_data
def load_data():
    players_by_country = {}
    
    try:
        with open("men_single.csv", mode="r", encoding="utf-8-sig") as f:
            # 안전하게 데이터를 한 줄씩 읽기 위한 내장 DictReader 사용
            reader = csv.DictReader(f)
            
            for row in reader:
                # key나 value에 공백이 있으면 싹 지워주기
                clean_row = {k.strip(): v.strip() for k, v in row.items() if k is not None}
                
                # 열 이름이 정확하지 않을 때를 대비한 꼼꼼한 예외 처리!
                country = clean_row.get("country", "Unknown").strip()
                ranking = clean_row.get("ranking", "9999").strip()
                name = clean_row.get("player_name", clean_row.get("jorsey_name", "Unknown")).strip()
                tournaments = clean_row.get("tournaments", "0").strip()
                points = clean_row.get("points", "0").strip()
                
                if not country:
                    country = "Unknown"
                    
                if country not in players_by_country:
                    players_by_country[country] = []
                    
                players_by_country[country].append({
                    "ranking": ranking,
                    "name": name,
                    "tournaments": tournaments,
                    "points": points
                })
                
        # 각 나라별 선수들을 랭킹 숫자가 작은 순(1위부터)으로 정렬하기!
        for country in players_by_country:
            players_by_country[country].sort(key=lambda x: int(x["ranking"]) if x["ranking"].isdigit() else 9999)
            
    except FileNotFoundError:
        st.error("🚨 `men_single.csv` 파일을 찾을 수 없어! 파일이 `app.py`와 같은 폴더(혹은 깃허브 저장소 루트)에 있는지 확인해줘.")
        return {}
    except Exception as e:
        # 에러가 나더라도 프로그램이 완전히 죽지 않도록 예외 처리
        st.warning(f"⚠️ 데이터를 읽는 중에 사소한 이슈가 있었어, 하지만 계속 진행해볼게! (에러 내용: {e})")
    
    return players_by_country

# 데이터 로드 실행!
data = load_data()

# 3. 데이터가 정상적으로 있을 때만 화면 구성 🌍
if data:
    countries = sorted(list(data.keys()))
    selected_country = st.selectbox("👉 궁금한 나라를 선택해봐!", countries)
    
    st.divider() # 깔끔한 구분선
    
    # 4. 해당 나라의 선수 목록 보여주기 🏅
    st.subheader(f"🌍 {selected_country}의 전사들")
    country_players = data[selected_country]
    
    # 1위부터 정렬된 리스트 안전하게 생성 📋
    player_options = [f"[{p['ranking']}위] {p['name']}" for p in country_players]
    
    # 변수가 생성된 후에만 셀렉트박스와 하위 레이아웃이 돌아가게 안전장치 작동!
    if player_options:
        selected_player_opt = st.selectbox("👤 능력을 분석할 선수를 골라봐!", player_options)
        
        # 선택된 선수 데이터 매칭하기
        selected_index = player_options.index(selected_player_opt)
        player = country_players[selected_index]
        
        # 5. 선수 정보 및 역량 분석 (이모지 폭탄! 💣✨)
        st.markdown(f"### ⚡ **{player['name']}** 선수의 시크릿 프로필")
        
        # 세련된 메트릭 레이아웃
        col1, col2, col3 = st.columns(3)
        col1.metric(label="현재 세계 랭킹 🥇", value=f"{player['ranking']} 위")
        
        try:
            pts = f"{int(player['points']):,}"
        except ValueError:
            pts = player['points']
            
        col2.metric(label="총 랭킹 포인트 🔥", value=pts)
