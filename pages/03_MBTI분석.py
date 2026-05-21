import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# 페이지 레이아웃 설정
st.set_page_config(
    page_title="Global MBTI Dashboard",
    page_icon="📊",
    layout="wide"
)

# 데이터 로드
@st.cache_data
def load_data():
    df = pd.read_csv('countriesMBTI_16types.csv')
    return df

try:
    df = load_data()
except Exception as e:
    st.error(f"데이터 파일을 찾을 수 없습니다: {e}")
    st.stop()

st.title("🌐 글로벌 MBTI 데이터 분석 대시보드")
st.markdown("국가별 MBTI 분포를 확인하거나, 특정 MBTI가 가장 많은 국가 순위를 확인해 보세요.")

# 탭 구성 (1번: 국가별 조회 / 2번: MBTI별 상위 국가 조회)
tab1, tab2 = st.tabs(["🗺️ 국가별 MBTI 분포", "🏆 MBTI별 국가 순위 (Top 10)"])

mbti_types = df.columns[1:] # 16개 MBTI 유형 컬럼

# ----------------------------------------------------
# Tab 1: 국가별 MBTI 분포 (기존 기능)
# ----------------------------------------------------
with tab1:
    st.subheader("국가별 성격 유형 분포")
    countries = sorted(df['Country'].unique())
    default_country_idx = countries.index("South Korea") if "South Korea" in countries else 0
    selected_country = st.selectbox("조회할 국가를 선택하세요:", countries, index=default_country_idx, key="tab1_country")
    
    country_data = df[df['Country'] == selected_country].iloc[0]
    country_mbti_df = pd.DataFrame({
        'MBTI': mbti_types,
        'Percentage': country_data[mbti_types].values * 100
    }).sort_values(by='Percentage', ascending=False).reset_index(drop=True)
    
    # 색상 적용 (1등 레드, 나머지 블루 그라데이션)
    c1 = ['#FF4B4B'] + [f'rgba(28, 131, 225, {1.0 - (i/len(country_mbti_df))*0.6})' for i in range(1, len(country_mbti_df))]
    
    fig1 = go.Figure(go.Bar(
        x=country_mbti_df['MBTI'],
        y=country_mbti_df['Percentage'],
        marker_color=c1,
        text=country_mbti_df['Percentage'].round(2).astype(str) + '%',
        textposition='outside',
        hovertemplate='<b>MBTI</b>: %{x}<br><b>비율</b>: %{y:.2f}%<extra></extra>'
    ))
    fig1.update_layout(
        title=f"📊 {selected_country}의 MBTI 유형별 분포 (높은 순)",
        xaxis_title="MBTI 유형", yaxis_title="비율 (%)",
        yaxis=dict(ticksuffix="%", range=[0, country_mbti_df['Percentage'].max() * 1.15]),
        plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)'
    )
    fig1.update_yaxes(showgrid=True, gridwidth=1, gridcolor='rgba(200, 200, 200, 0.2)')
    st.plotly_chart(fig1, use_container_width=True)


# ----------------------------------------------------
# Tab 2: MBTI별 국가 순위 (신규 요청 기능)
# ----------------------------------------------------
with tab2:
    st.subheader("특정 MBTI 비율이 가장 높은 국가 Top 10")
    selected_mbti = st.selectbox("조회할 MBTI 유형을 선택하세요:", mbti_types, index=0, key="tab2_mbti")
    
    # 선택된 MBTI 성향이 높은 상위 10개국 추출
    top10_df = df[['Country', selected_mbti]].copy()
    top10_df[selected_mbti] = top10_df[selected_mbti] * 100 # 소수를 백분율(%)로 변환
    top10_df = top10_df.sort_values(by=selected_mbti, ascending=False).head(10).reset_index(drop=True)
    
    # 🎨 색상 규칙: 1등은 빨간색, 2~10등은 점차 옅어지는 파란색 그라데이션
    c2 = []
    for i in range(10):
        if i == 0:
            c2.append('#FF4B4B') # 1등 레드
        else:
            alpha = 1.0 - (i / 10) * 0.6 # 순위가 내려갈수록 불투명도를 낮춤 (1.0 -> 0.46)
            c2.append(f'rgba(28, 131, 225, {alpha})')
            
    fig2 = go.Figure(go.Bar(
        x=top10_df['Country'],
        y=top10_df[selected_mbti],
        marker_color=c2,
        text=top10_df[selected_mbti].round(2).astype(str) + '%',
        textposition='outside',
        hovertemplate='<b>국가</b>: %{x}<br><b>비율</b>: %{y:.2f}%<extra></extra>'
    ))
    fig2.update_layout(
        title=f"🏆 전 세계 {selected_mbti} 비율이 가장 높은 상위 10개국",
        xaxis_title="국가", yaxis_title="비율 (%)",
        yaxis=dict(ticksuffix="%", range=[0, top10_df[selected_mbti].max() * 1.15]),
        plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)'
    )
    fig2.update_yaxes(showgrid=True, gridwidth=1, gridcolor='rgba(200, 200, 200, 0.2)')
    st.plotly_chart(fig2, use_container_width=True)
