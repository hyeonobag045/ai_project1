import streamlit as st
import csv

# 1. 페이지 기본 설정 및 예쁜 타이틀 ✨
st.set_page_config(page_title="배드민턴 랭킹 마스터 🏸", page_icon="🏸", layout="centered")
st.title("🏸 배드민턴 남자 단식 세계 랭킹 탐색기")
st.write("세계적인 배드민턴 선수들의 정보를 한눈에 알아보자구! 😎")

# 2. 데이터 불러오기 함수
# ⭐ 중요: 캐시 이름(ttl이나 이름)을 살짝 틀어서 기존의 꼬인 캐시를 완전히 초기화함!
@st.cache_data(ttl=60)
def load_and_sort_badminton_data():
    players_by_country = {}
    
    try:
        with open("men_single.csv", mode="r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            
            for row in reader:
                clean_row = {k.strip(): v.strip() for k, v in row.items() if k is not None}
                
                country = clean_row.get("country", "Unknown").strip()
                ranking_raw = clean_row.get("ranking", "9999").strip()
                name = clean_row.get("player_name", clean_row.get("jorsey_name", "Unknown")).strip()
                tournaments_raw = clean_row.get("tournaments", "0").strip()
                points_raw = clean_row.get("points", "0").strip()
                
                if not country:
                    country = "Unknown"
                
                # 숫자만 깔끔하게 추출해서 '진짜 정수(int)'로 변환!
                ranking_clean = "".join(filter(str.isdigit(), ranking_raw))
                points_clean = "".join(filter(str.isdigit(), points_raw))
                tournaments_clean = "".join(filter(str.isdigit(), tournaments_raw))
                
                ranking = int(ranking_clean) if ranking_clean else 9999
                points = int(points_clean) if points_clean else 0
                tournaments = int(tournaments_clean) if tournaments_clean else 0
                
                if country not in players_by_country:
                    players_by_country[country] = []
                    
                players_by_country[country].append({
                    "ranking": ranking,
                    "name": name,
                    "tournaments": tournaments,
                    "points": points
                })
                
        # ⭐ 핵심 피드백 반영: 문자열이 아니라 '진짜 숫자 정수값' 기준으로 오름차순 정렬!!
        # 이렇게 하면 11위, 13위가 104위, 107위보다 무조건 먼저 앞으로 오게 돼!
        for country in players_by_country:
            players_by_country[country].sort(key=lambda x: x["ranking"])
            
    except FileNotFoundError:
        st.error("🚨 `men_single.csv` 파일을 찾을 수 없어! 파일 위치를 다시 확인해줘.")
        return {}
    except Exception as e:
        st.warning(f"⚠️ 데이터를 읽는 중에 이슈가 있었어! (에러 내용: {e})")
    
    return players_by_country

# 데이터 로드 실행!
data = load_and_sort_badminton_data()

# 3. 데이터가 정상적으로 있을 때만 화면 구성 🌍
if data:
    countries = sorted(list(data.keys()))
    selected_country = st.selectbox("👉 궁금한 나라를 선택해봐!", countries)
    
    st.divider() # 깔끔한 구분선
    
    # 4. 해당 나라의 선수 목록 보여주기 🏅
    st.subheader(f"🌍 {selected_country}의 전사들")
    country_players = data[selected_country]
    
    # 리스트 생성할 때 1위부터 순서대로 완벽하게 정렬되어 들어감! 📋
    player_options = [f"[{p['ranking']}위] {p['name']}" for p in country_players]
    
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
        col2.metric(label="총 랭킹 포인트 🔥", value=f"{player['points']:,}")
        col3.metric(label="대회 출전 횟수 🏸", value=f"{player['tournaments']} 회")
        
        st.write("") # 한 줄 띄우기
        
        st.markdown("#### 🧠 **AI가 분석한 이 선수의 스펙 능력치**")
        
        rank_num = player["ranking"]
            
        if rank_num == 1:
            st.success("👑 **[신계 영역]** 말해 뭐해? 현재 세계 배드민턴계를 씹어먹고 있는 절대 강자야! 적은 대회만 뛰고도 압도적인 포인트로 1위를 지키는 괴물 같은 효율성을 보여주고 있어. ㄷㄷ")
        elif rank_num <= 10:
            st.info("💎 **[월드클래스]** 전 세계 탑 10에 드는 초엘리트 선수! 코트 위에서 이 선수를 만나면 숨도 쉬기 힘들 걸? 대회마다 우승 후보로 꼽히는 엄청난 실력자야! 🚀")
        elif rank_num <= 50:
            st.warning("🔥 **[실력파 강자]** 상위 랭커들을 언제든지 꺾을 수 있는 강력한 다크호스! 끈질긴 수비력과 날카로운 공격력을 모두 갖춘 무서운 형이야. 💪")
        elif rank_num <= 200:
            st.write("🏃 **[라이징 스타 / 베테랑]** 세계적인 무대에서 맹활약하며 끊임없이 성장 중인 선수야. 경험이 풍부하거나 잠재력이 엄청나서 앞으로의 성장이 진짜 기대돼! 🌱")
        else:
            st.write("🎯 **[꿈을 향해 달리는 도전자]** 수많은 경쟁을 뚫고 세계 무대에 이름을 올린 멋진 전사야! 1점 1점을 위해 온 힘을 다해 뛰는 열정 가득한 선수지. 응원하자구! 🙌")
    else:
        st.warning("⚠️ 이 나라에는 등록된 선수가 없는 것 같아!")
else:
    st.info("💡 데이터를 불러오지 못했어. CSV 파일 위치를 꼭 확인해줘!")
