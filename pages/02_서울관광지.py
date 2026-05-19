import streamlit as st
import folium
from streamlit_folium import st_folium

# 페이지 설정
st.set_page_config(
    page_title="외국인이 좋아하는 서울 관광지 TOP 10",
    page_icon="🗼",
    layout="wide"
)

# 제목 및 설명
st.title("🇰🇷 외국인 관광객이 사랑하는 서울 명소 TOP 10")
st.markdown("""
스트림릿과 폴리움(Folium)을 활용하여 외국인 관광객들에게 가장 인기 있는 서울의 주요 관광지 10곳을 지도에 표시했습니다. 
마커를 클릭하면 해당 명소의 이름을 확인할 수 있습니다.
""")

# 서울 주요 관광지 TOP 10 데이터 (명칭, 위도, 경도)
seoul_tourist_spots = [
    {"name": "1. 경복궁 (Gyeongbokgung Palace)", "lat": 37.5796, "lon": 126.9770},
    {"name": "2. N서울타워 (N Seoul Tower)", "lat": 37.5512, "lon": 126.9882},
    {"name": "3. 명동 쇼핑거리 (Myeongdong Shopping Street)", "lat": 37.5635, "lon": 126.9846},
    {"name": "4. 북촌한옥마을 (Bukchon Hanok Village)", "lat": 37.5829, "lon": 126.9835},
    {"name": "5. 인사동길 (Insadong-gil)", "lat": 37.5744, "lon": 126.9848},
    {"name": "6. 홍대거리 (Hongdae Street)", "lat": 37.5567, "lon": 126.9235},
    {"name": "7. 동대문디자인플라자 (DDP)", "lat": 37.5665, "lon": 127.0092},
    {"name": "8. 롯데월드타워 (Lotte World Tower)", "lat": 37.5126, "lon": 127.1025},
    {"name": "9. 이태원 관광특구 (Itaewon)", "lat": 37.5345, "lon": 126.9942},
    {"name": "10. 광장시장 (Gwangjang Market)", "lat": 37.5701, "lon": 127.0010}
]

# 화면 레이아웃 분할 (좌측: 리스트, 우측: 지도)
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("📍 명소 리스트")
    for spot in seoul_tourist_spots:
        st.write(spot["name"])

with col2:
    st.subheader("🗺️ 서울 지도 확인")
    
    # 지도 중심점 설정 (서울 중심부)
    m = folium.Map(location=[37.555, 126.985], zoom_start=12)
    
    # 마커 추가
    for spot in seoul_tourist_spots:
        folium.Marker(
            location=[spot["lat"], spot["lon"]],
            popup=spot["name"],
            tooltip=spot["name"],
            icon=folium.Icon(color="red", icon="info-sign")
        ).add_to(m)
    
    # 스트림릿 웹페이지에 지도 렌더링
    st_folium(m, width="100%", height=500, returned_objects=[])
