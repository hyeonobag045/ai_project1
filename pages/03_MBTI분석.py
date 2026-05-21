import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# 페이지 레이아웃 설정
st.set_page_config(
    page_title="Global MBTI Dashboard",
    page_icon="📊",
    layout="wide"
)

# 데이터 로드 (캐싱을 적용하여 속도 최적화)
@st.cache_data
def load_data():
    # 'countriesMBTI_16types.csv' 파일이 app.py와 같은 폴더에 있어야 합니다.
    df = pd.read_csv('countriesMBTI_16types.csv')
    return df

try:
    df = load_data()
except Exception as e:
    st.error(f"데이터 파일을 찾을 수 없습니다: {e}")
    st.info("GitHub 저장소에 'countriesMBTI_16types.csv' 파일이 함께 업로드되었는지 확인해주세요.")
    st.stop()

# 대시보드 타이틀
st.title("🌐 국가별 MBTI 분포 대시보드")
st.markdown("전 세계 국가들의 MBTI 비율을 확인하고 인터랙티브한 그래프로 비교해 보세요.")

# 사이드바에서 국가 선택
st.sidebar.header("🗺️ 국가 선택")
countries = sorted(df['Country'].unique())

# 'South Korea'가 데이터에 있으면 기본값으로 지정, 없으면 첫 번째 국가 지정
default_idx = countries.index("South Korea") if "South Korea" in countries else 0
selected_country = st.sidebar.selectbox("조회할 국가를 선택하세요:", countries, index=default_idx)

# 선택한 국가의 데이터 추출 및 전처리
country_data = df[df['Country'] == selected_country].iloc[0]
mbti_types = df.columns[1:] # Country 컬럼을 제외한 16가지 MBTI 유형

# 데이터프레임 구조로 변환 후 백분율(%) 처리
mbti_df = pd.DataFrame({
    'MBTI': mbti_types,
    'Percentage': country_data[mbti_types].values * 100  # 소수점 비율을 % 단위로 변환
})

# 비율이 높은 순서대로 정렬 (1등을 찾기 위함)
mbti_df = mbti_df.sort_values(by='Percentage', ascending=False).reset_index(drop=True)

# 🎨 색상 지정 로직: 1등은 빨간색, 나머지는 순위 순으로 옅어지는 파란색 그라데이션
colors = []
num_items = len(mbti_df)

for i in range(num_items):
    if i == 0:
        colors.append('#FF4B4B')  # 1등: 스트림릿 시그니처 레드
    else:
        # 순위가 낮아질수록 rgba의 투명도(Alpha)를 낮춰 파란색 그라데이션 효과 적용
        alpha = 1.0 - (i / num_items) * 0.6  # 1.0에서 점진적으로 0.4까지 감소
        colors.append(f'rgba(28, 131, 225, {alpha})')

# 📊 Plotly 인터랙티브 막대그래프 생성
fig = go.Figure()

fig.add_trace(go.Bar(
    x=mbti_df['MBTI'],
    y=mbti_df['Percentage'],
    marker_color=colors,
    text=mbti_df['Percentage'].round(2).astype(str) + '%', # 막대 위에 수치 표시
    textposition='outside',
    hovertemplate='<b>MBTI</b>: %{x}<br><b>비율</b>: %{y:.2f}%<extra></extra>' # 마우스 오버 툴팁
))

# 깔끔하고 세련된 그래프 레이아웃 설정
fig.update_layout(
    title=f"📊 {selected_country}의 MBTI 유형별 분포 (높은 순)",
    xaxis_title="MBTI 유형",
    yaxis_title="비율 (%)",
    yaxis=dict(ticksuffix="%", range=[0, mbti_df['Percentage'].max() * 1.15]), # 상단 글자 안 잘리게 여유 공간 부여
    margin=dict(l=40, r=40, t=60, b=40),
    plot_bgcolor='rgba(0,0,0,0)', # 배경 투명
    paper_bgcolor='rgba(0,0,0,0)',
)

# 은은한 가로 격자선 추가
fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='rgba(200, 200, 200, 0.2)')
fig.update_xaxes(showgrid=False)

# 스트림릿 화면에 그래프 띄우기
st.plotly_chart(fig, use_container_width=True)

# 💡 하단에 요약 카드(Top 3) 추가 시각화
st.markdown("---")
st.subheader(f"💡 {selected_country}의 주요 특징 요약")

col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="🥇 1위 유형", value=mbti_df.loc[0, 'MBTI'], delta=f"{mbti_df.loc[0, 'Percentage']:.2f}%")
with col2:
    st.metric(label="🥈 2위 유형", value=mbti_df.loc[1, 'MBTI'], delta=f"{mbti_df.loc[1, 'Percentage']:.2f}%", delta_color="off")
with col3:
    st.metric(label="🥉 3위 유형", value=mbti_df.loc[2, 'MBTI'], delta=f"{mbti_df.loc[2, 'Percentage']:.2f}%", delta_color="off")
