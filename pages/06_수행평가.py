import streamlit as st
import csv

# 1. 페이지 기본 설정 및 타이틀
st.set_page_config(page_title="배드민턴 랭킹 마스터", page_icon="🏸", layout="centered")
st.title("🏸 배드민턴 남자 단식 세계 랭킹 탐색기")
st.write("전 세계 배드민턴 선수들을 1위부터 순서대로 알아보고 실물 사진도 확인하자구! 😎")

# 2. 데이터 불러오기 함수
@st.cache_data(ttl=1)
def load_world_ranking_data():
    all_players = []
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
        all_players.sort(key=lambda x: x["ranking"])
    except FileNotFoundError:
        st.error("🚨 `men_single.csv` 파일을 찾을 수 없어! 파일 위치를 다시 확인해줘.")
        return []
    except Exception as e:
        st.warning(f"⚠️ 데이터를 읽는 중에 오류가 있었어: {e}")
    return all_players

player_list = load_world_ranking_data()

# 3. 화면 UI 구성
if player_list:
    st.divider()
    st.subheader("🏅 세계 랭킹 순으로 골라봐!")
    
    selected_player = st.selectbox(
        "👤 능력을 분석할 선수를 선택해줘!",
        options=player_list,
        format_func=lambda p: f"[{p['ranking']}위] {p['name']} ({p['country']})"
    )
    
    # 4. 선수 정보 및 사진 레이아웃
    if selected_player:
        player = selected_player
        img_col, info_col = st.columns([1, 1.2])
        
        with img_col:
            p_name = player['name'].lower()
            
            # 선수별 실제 공식 프로필 및 매치 사진 링크 매칭
            if "axelsen" in p_name:
                photo_url = "https://images.olympics.com/images/image/private/t_16-9_760/f_auto/primary/p8099aswipon2f6p7ehi"
            elif "ginting" in p_name:
                photo_url = "https://images.bwfbadminton.com/players/headshot/75336.png"
            elif "jonatan" in p_name or "christie" in p_name:
                photo_url = "https://images.bwfbadminton.com/players/headshot/81816.png"
            elif "kodai" in p_name or "naraoka" in p_name:
                photo_url = "https://images.bwfbadminton.com/players/headshot/83274.png"
            elif "shifeng" in p_name or "li shi feng" in p_name:
                photo_url = "https://images.bwfbadminton.com/players/headshot/93855.png"
            elif "kunlavut" in p_name or "vitidsarn" in p_name:
                photo_url = "https://images.bwfbadminton.com/players/headshot/94174.png"
            elif "lee zi" in p_name or "zi jia" in p_name:
                photo_url = "https://images.bwfbadminton.com/players/headshot/73434.png"
            else:
                photo_url = "https://images.unsplash.com/photo-1613918108466-292b78a8ef95?w=500"
            
            st.image(photo_url, caption=f"{player['name']} 선수 프로필", use_container_width=True)

        with info_col:
            st.markdown(f"### ⚡ **{player['name']}** 선수의 시크릿 프로필")
            st.markdown(f"**🌍 소속 국가:** {player['country']}")
            
            col1, col2 = st.columns(2)
            col1.metric(label="현재 세계 랭킹 🥇", value=f"{player['ranking']} 위")
            col2.metric(label="대회 출전 횟수 🏸", value=f"{player['tournaments']} 회")
            st.metric(label="총 랭킹 포인트 🔥", value=f"{player['points']:,} 점")
            
            st.write("")
            st.markdown("#### 🧠 **AI가 분석한 이 선수의 스펙 능력치**")
            
            rank_num = player["ranking"]
            if rank_num == 1:
                st.success("👑 **[신계 영역]** 말해 뭐해? 현재 세계 배드민턴계를 완전히 씹어먹고 있는 절대 강자야! 적은 대회만 뛰고도 압도적인 포인트로 1위를 지키는 괴물 같은 효율성을 보여주고 있어. ㄷㄷ")
            elif rank_num <= 10:
                st.info("💎 **[월드클래스]** 전 세계 탑 10에 드는 초엘리트 선수! 코트 위에서 이 선수를 만나면 숨도 쉬기 힘들 걸? 대회마다 우승 후보로 꼽히는 엄청난 실력자야! 🚀")
            elif rank_num <= 50:
                st.warning("🔥 **[실력파 강자]** 상위 랭커들을 언제든지 꺾을 수 있는 강력한 다크호스! 끈질긴 수비력과 날카로운 공격력을 모두 갖춘 무서운 형이야. 💪")
            elif rank_num <= 200:
                st.write("🏃 **[라이징 스타 / 베테랑]** 세계적인 무대에서 맹활약하며 끊임없이 성장 중인 선수야. 경험이 풍부하거나 잠재력이 엄청나서 앞으로의 성장이 진짜 기대돼! 🌱")
            else:
                st.write("🎯 **[꿈을 향해 달리는 도전자]** 수많은 경쟁을 뚫고 세계 무대에 이름을 올린 멋진 전사야! 1점 1점을 위해 온 힘을 다해 뛰는 열정 가득한 선수지. 응원하자구! 🙌")
else:
    st.info("💡 데이터를 불러오지 못했어. `men_single.csv` 파일 위치를 확인해줘!")
