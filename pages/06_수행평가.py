import streamlit as st
import csv

# 1. 페이지 기본 설정 및 예쁜 타이틀 ✨
st.set_page_config(page_title="배드민턴 랭킹 마스터 🏸", page_icon="🏸", layout="centered")
st.title("🏸 배드민턴 남자 단식 세계 랭킹 탐색기")
st.write("세계적인 배드민턴 선수들의 정보를 한눈에 알아보자구! 😎")

# 2. 데이터 불러오기 함수
@st.cache_data(ttl=1) # 캐시가 절대 방해하지 못하게 초기화 세팅!
def load_clean_badminton_data():
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
                
                # 숫자 외에 다른 공백문자 싹 다 박멸하기!
                ranking_clean = "".join([c for c in ranking_raw if c.isdigit()])
                points_clean = "".join([c for c in points_raw if c.isdigit()])
                tournaments_clean = "".join([c for c in tournaments_raw if c.isdigit()])
                
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
                
    except FileNotFoundError:
        st.error("🚨 `men_single.csv` 파일을 찾을 수 없어!")
        return {}
    except Exception as e:
        st.warning(f"⚠️ 데이터 읽기 오류: {e}")
    
    return players_by_country

data = load_clean_badminton_data()

# 3. 화면 UI 구성
if data:
    countries = sorted(list(data.keys()))
    selected_country = st.selectbox("👉 궁금한 나라를 선택해봐!", countries)
    
    st.divider()
    
    st.subheader(f"🌍 {selected_country}의 전사들")
    
    # 💥 [해결의 열쇠] 선택된 나라의 선수 목록을 가져온 뒤, '진짜 정수 숫자' 크기 기준으로 오름차순 정렬!
    country_players = data[selected_country]
    country_players.sort(key=lambda x: x["ranking"])
    
    # ⭐ [절대 정렬이 깨지지 않는 치트키] ⭐
    # 스트림릿 셀렉트박스에 '텍스트 글자' 대신 '완벽히 정렬된 딕셔너리 리스트'를 그대로 꽂아버려!
    # format_func를 이용하면 화면에 보여줄 때만 글자로 변환하므로, 파이썬 정렬 순서가 1밀리초도 안 깨져!
    selected_player = st.selectbox(
        "👤 능력을 분석할 선수를 골라봐!",
        options=country_players,
        format_func=lambda p: f"[{p['ranking']}위] {p['name']}"
    )
    
    # 4. 선수 정보 및 역량 분석 (이모지 폭탄! 💥)
    if selected_player:
        player = selected_player
        
        st.markdown(f"### ⚡ **{player['name']}** 선수의 시크릿 프로필")
        
        col1, col2, col3 = st.columns(3)
        col1.metric(label="현재 세계 랭킹 🥇", value=f"{player['ranking']} 위")
        col2.metric(label="총 랭킹 포인트 🔥", value=f"{player['points']:,}")
        col3.metric(label="대회 출전 횟수 🏸", value=f"{player['tournaments']} 회")
        
        st.write("")
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
