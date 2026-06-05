import streamlit as st
import csv

# 1. 페이지 기본 설정 및 예쁜 타이틀 ✨
st.set_page_config(page_title="배드민턴 랭킹 마스터 🏸", page_icon="🏸", layout="centered")
st.title("🏸 배드민턴 남자 단식 세계 랭킹 탐색기")
st.write("전 세계 배드민턴 선수들을 1위부터 순서대로 알아보고, 진짜 '실물 사진'도 확인하자구! 😎")

# 2. 데이터 불러오기 함수 (전체 선수 리스트 1위부터 칼정렬)
@st.cache_data(ttl=1)  # 캐시 엉킴 방지
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
                
                # 유령 공백 제거하고 진짜 숫자만 추출
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
                
        # 👑 선수들을 랭킹 숫자 크기대로 오름차순 정렬 (1위부터 차례대로!)
        all_players.sort(key=lambda x: x["ranking"])
            
    except FileNotFoundError:
        st.error("🚨 `men_single.csv` 파일을 찾을 수 없어! 파일 위치를 다시 확인해줘.")
        return []
    except Exception as e:
        st.warning(f"⚠️ 데이터를 읽는 중에 오류가 있었어: {e}")
    
    return all_players

player_list = load_world_ranking_data()

# 3. 화면 UI 구성 ✨
if player_list:
    st.divider()
    
    st.subheader("🏅 세계 랭킹 순으로 골라봐!")
    
    selected_player = st.selectbox(
        "👤 능력을 분석할 선수를 선택해줘! (위에서부터 차례대로 1위야! 📈)",
        options=player_list,
        format_func=lambda p: f"[{p['ranking']}위] {p['name']} ({p['country']})"
    )
    
    # 4. 선수 정보 및 사진 레이아웃 구성 📸
    if selected_player:
        player = selected_player
        
        # 화면을 좌우 2분할로 나누어 왼쪽엔 '진짜 사진', 오른쪽엔 프로필 배치!
        img_col, info_col = st.columns([1, 1.2])
        
        with img_col:
            p_name = player['name'].lower()
            
            # ⭐ [대대적인 실물 사진 매칭 패치!] ⭐
            # 랜덤 모델 사진을 싹 다 내버리고 실제 선수의 대회/프로필 고유 주소를 박아넣음!
            if "axelsen" in p_name: 
                # 🥇 세계 최강 덴마크 '빅토르 악셀센'의 진짜 경기 실물 사진!
                photo_url = "https://images.olympics.com/images/image/private/t_16-9_760/f_auto/primary/p8099aswipon2f6p7ehi"
            elif "ginting" in p_name: 
                # 🇮🇩 인도네시아 최고의 스타 '앤서니 시니수카 긴팅'의 진짜 얼굴!
                photo_url = "https://images.
