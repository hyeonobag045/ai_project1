import streamlit as st
import csv

# 1. 페이지 기본 설정 및 예쁜 타이틀 ✨
st.set_page_config(page_title="여자 배드민턴 랭킹 마스터 🏸", page_icon="🏸", layout="centered")
st.title("🏸 배드민턴 여자 단식 세계 랭킹 탐색기")
st.write("전 세계 여자 배드민턴 선수들을 1위부터 순서대로 알아보자구! 😎")

# 2. 데이터 불러오기 함수 (전체 선수 리스트 1위부터 칼정렬)
@st.cache_data(ttl=1)  # 캐시 엉킴을 방지하는 무적의 1초 설정 🛠️
def load_women_ranking_data():
    all_players = []
    
    try:
        # ⭐ 여자 단식 파일명(women_single.csv) 반영!
        with open("women_single.csv", mode="r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            
            for row in reader:
                # 데이터 앞뒤 공백 지워주기
                clean_row = {k.strip(): v.strip() for k, v in row.items() if k is not None}
                
                country = clean_row.get("country", "Unknown").strip()
                ranking_raw = clean_row.get("ranking", "9999").strip()
                name = clean_row.get("player_name", clean_row.get("jorsey_name", "Unknown")).strip()
                tournaments_raw = clean_row.get("tournaments", "0").strip()
                points_raw = clean_row.get("points", "0").strip()
                
                # 특수문자나 유령 공백 제거하고 '진짜 숫자'만 남기기
                ranking_clean = "".join([c for c in ranking_raw if c.isdigit()])
                points_clean = "".join([c for c in points_raw if c.isdigit()])
                tournaments_clean = "".join([c for c in tournaments_raw if c.isdigit()])
                
                ranking = int(ranking_clean) if ranking_clean else 9999
                points = int(points_clean) if points_clean else 0
                tournaments = int(tournaments_clean) if tournaments_clean else 0
                
                all_players.append({
                    "ranking": ranking,
                    "name": name,
                    "country": country,
                    "tournaments": tournaments,
                    "points": points
                })
                
        # 👑 [핵심] 전 세계 선수들을 진짜 '랭킹 숫자 크기'대로 오름차순 정렬!!
        all_players.sort(key=lambda x: x["ranking"])
            
    except FileNotFoundError:
        st.error("🚨 `women_single.csv` 파일을 찾을 수 없어! 파일 위치와 이름을 다시 확인해줘.")
        return []
    except Exception as e:
        st.warning(f"⚠️ 데이터를 읽는 중에 오류가 있었어: {e}")
    
    return all_players

# 데이터 로딩 시작!
player_list = load_women_ranking_data()

# 3. 화면 UI 구성 ✨
if player_list:
    st.divider() # 깔끔한 구분선
    
    st.subheader("🏅 세계 랭킹 순으로 골라봐!")
    
    # 💥 정렬이 완벽하게 끝난 전체 선수 목록을 셀렉트박스에 바로 집어넣기!
    # format_func 덕분에 화면에는 깔끔하게 보이고, 정렬 순서(1위~끝순위)는 절대 깨지지 않아!
    selected_player = st.selectbox(
        "👤 능력을 분석할 선수를 선택해줘! (위에서부터 차례대로 1위야! 📈)",
        options=player_list,
        format_func=lambda p: f"[{p['ranking']}위] {p['name']} ({p['country']})"
    )
    
    # 4. 선수 정보 및 역량 분석 (이모지 뿜뿜! 🔥)
    if selected_player:
        player = selected_player
        
        st.markdown(f"### ⚡ **{player['name']}** 선수의 시크릿 프로필")
        st.markdown(f"**🌍 소속 국가:** {player['country']}")
        
        # 메트릭 대시보드로 간지나게 보여주기
        col1, col2, col3 = st.columns(3)
        col1.metric(label="현재 세계 랭킹 🥇", value=f"{player['ranking']} 위")
        col2.metric(label="총 랭킹 포인트 🔥", value=f"{player['points']:,}")
        col3.metric(label="대회 출전 횟수 🏸", value=f"{player['tournaments']} 회")
        
        st.write("")
        st.markdown("#### 🧠 **AI가 분석한 이 선수의 스펙 능력치**")
        
        rank_num = player["ranking"]
            
        if rank_num == 1:
            st.success("👑 **[신계 영역]** 말해 뭐해? 현재 세계 여자 배드민턴계를 완전히 정복한 절대 지존이야! 압도적인 경기 운영력과 스피드로 1위를 지키는 전설적인 선수지. 대단해! ㄷㄷ")
        elif rank_num <= 10:
            st.info("💎 **[월드클래스]** 전 세계 탑 10에 드는 초엘리트 클래스! 기술과 체력 모두 정점에 도달한 상태야. 매 대회마다 강력한 우승 후보로 거론되는 탑티어 실력자지! 🚀")
        elif rank_num <= 50:
            st.warning("🔥 **[실력파 강자]** 언제든 탑 10을 위협할 수 있는 엄청난 파괴력을 가진 다크호스! 날카로운 스트로크와 끈질긴 랠리 능력이 일품인 선수야. 💪")
        elif rank_num <= 200:
            st.write("🏃 **[라이징 스타 / 베테랑]** 전 세계를 무대로 엄청난 잠재력을 뽐내며 치열하게 성장 중인 선수야. 앞으로 순위가 어디까지 떡상할지 진짜 기대되는걸? 🌱")
        else:
            st.write("🎯 **[꿈을 향해 달리는 도전자]** 바늘구멍 같은 세계 무대 경쟁을 뚫고 당당히 이름을 올린 멋진 여전사야! 매 경기 땀방울을 흘리며 열정적으로 뛰는 이 선수를 응원해! 🙌")
else:
    st.info("💡 데이터를 불러오지 못했어. `women_single.csv` 파일이 정상적인 위치에 업로드 되었는지 확인해줘!")
