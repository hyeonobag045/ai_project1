import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression
import numpy as np
import os

# 데이터 로드 및 전처리 함수
@st.cache_data
def load_data():
    # 현재 파일(pages/...)의 위치를 기준으로 상위 폴더의 seoul.csv 절대 경로 계산
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    csv_path = os.path.join(parent_dir, 'seoul.csv')
    
    # 한글 인코딩(cp949)으로 데이터 읽기
    df = pd.read_csv(csv_path, encoding='cp949')
    
    # 열 이름 공백 제거
    df.columns = df.columns.str.strip()
    
    # '날짜' 열의 \t 문자 제거 및 날짜 형식 변환
    df['날짜'] = df['날짜'].astype(str).str.replace(r'\t', '', regex=True).str.strip()
    df['날짜'] = pd.to_datetime(df['날짜'], errors='coerce')
    
    # 결측치 제거
    df = df.dropna(subset=['날짜', '최고기온(℃)', '최저기온(℃)'])
    
    # 연, 월, 일 추출
    df['연도'] = df['날짜'].dt.year
    df['월'] = df['날짜'].dt.month
    df['일'] = df['날짜'].dt.day
    
    return df

# 앱 타이틀 및 설명
st.title("🌡️ 서울 연도별 날짜 기온 분석 및 예측기")
st.write("1907년부터 2018년까지의 데이터를 바탕으로 선택한 날짜의 기온 변화 흐름을 확인하고, 미래의 기온을 예측합니다.")

try:
    df = load_data()
    max_year_in_data = int(df['연도'].max())  # 데이터의 마지막 연도 (2018)
    
    # 사이드바 설정
    st.sidebar.header("📅 조회 및 예측 설정")
    
    # 월/일 선택
    selected_month = st.sidebar.selectbox("월(Month)을 선택하세요", sorted(df['월'].unique()), index=7) # 기본값 8월
    available_days = sorted(df[df['월'] == selected_month]['일'].unique())
    selected_day = st.sidebar.selectbox("일(Day)을 선택하세요", available_days, index=14) # 기본값 15일
    
    # 미래 예측 연도 선택 (2019년부터 2050년까지)
    predict_year = st.sidebar.slider(
        f"예측할 미래 연도를 선택하세요 ({max_year_in_data}년 이후)", 
        min_value=max_year_in_data + 1, 
        max_value=2050, 
        value=2030
    )
    
    # 조건에 맞는 과거 데이터 필터링 후 연도순 정렬
    filtered_df = df[(df['월'] == selected_month) & (df['일'] == selected_day)].sort_values('연도')
    
    if filtered_df.empty:
        st.warning(f"선택하신 {selected_month}월 {selected_day}일에 해당하는 데이터가 없습니다.")
    else:
        st.subheader(f"📊 {selected_month}월 {selected_day}일 기온 통계 및 미래 예측")
        
        # --- [머신러닝 기반 기온 예측 로직] ---
        X = filtered_df[['연도']].values
        y_max = filtered_df['최고기온(℃)'].values
        y_min = filtered_df['최저기온(℃)'].values
        
        # 최고기온 예측 모델 학습 및 예측
        model_max = LinearRegression()
        model_max.fit(X, y_max)
        pred_max = model_max.predict(np.array([[predict_year]]))[0]
        
        # 최저기온 예측 모델 학습 및 예측
        model_min = LinearRegression()
        model_min.fit(X, y_min)
        pred_min = model_min.predict(np.array([[predict_year]]))[0]
        
        # --- 대시보드 요약 카드 정보 출력 ---
        col1, col2, col3 = st.columns(3)
        col1.metric(f"{predict_year}년 최고기온 예측", f"{pred_max:.1f} ℃", "추세선 기준")
        col2.metric(f"{predict_year}년 최저기온 예측", f"{pred_min:.1f} ℃", "추세선 기준")
        col3.metric("과거 데이터 수", f"{len(filtered_df)} 개년")
        
        # --- [Plotly를 이용한 상호작용형 그래프 시각화] ---
        fig = go.Figure()
        
        # 1. 과거 최고기온 데이터 꺾은선 (핫핑크)
        fig.add_trace(go.Scatter(
            x=filtered_df['연도'],
            y=filtered_df['최고기온(℃)'],
            mode='lines+markers',
            name='최고기온 (과거)',
            line=dict(color='hotpink', width=2),
            marker=dict(size=4),
            hovertemplate='<b>%{x}년 최고기온</b><br>기온: %{y}℃<extra></extra>'
        ))
        
        # 2. 과거 최저기온 데이터 꺾은선 (연한 파란색)
        fig.add_trace(go.Scatter(
            x=filtered_df['연도'],
            y=filtered_df['최저기온(℃)'],
            mode='lines+markers',
            name='최저기온 (과거)',
            line=dict(color='lightblue', width=2),
            marker=dict(size=4),
            hovertemplate='<b>%{x}년 최저기온</b><br>기온: %{y}℃<extra></extra>'
        ))
        
        # 3. 미래 최고기온 예측 점 (진한 핑크)
        fig.add_trace(go.Scatter(
            x=[predict_year],
            y=[pred_max],
            mode='markers',
            name=f'{predict_year}년 최고 예측',
            marker=dict(color='deeppink', size=10, symbol='diamond'),
            hovertemplate=f'<b>{predict_year}년 최고기온 예측</b><br>기온: {pred_max:.1f}℃<extra></extra>'
        ))
        
        # 4. 미래 최저기온 예측 점 (진한 하늘색)
        fig.add_trace(go.Scatter(
            x=[predict_year],
            y=[pred_min],
            mode='markers',
            name=f'{predict_year}년 최저 예측',
            marker=dict(color='dodgerblue', size=10, symbol='diamond'),
            hovertemplate=f'<b>{predict_year}년 최저기온 예측</b><br>기온: {pred_min:.1f}℃<extra></extra>'
        ))
        
        # 그래프 레이아웃 설정
        fig.update_layout(
            title=dict(
                text=f"날짜별 기온 분석 및 {predict_year}년 예측 ({selected_month}월 {selected_day}일)",
                x=0.5,
                xanchor='center',
                font=dict(size=16, weight='bold')
            ),
            xaxis_title="연도",
            yaxis_title="온도",
            hovermode="x unified",  # 마우스 올렸을 때 툴팁 통합 표시
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            margin=dict(l=40, r=40, t=80, b=40),
            plot_bgcolor='white'
        )
        
        # 축 그리드 설정
        fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='LightGrey')
        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='LightGrey')
        
        # 스트림릿 웹 화면에 Plotly 그래프 출력
        st.plotly_chart(fig, use_container_width=True)
        
        # 참고 텍스트 제공
        st.info(f"💡 **참고 (과거 기록):** 이 날짜의 역대 최고 기온은 {filtered_df['최고기온(℃)'].max()}℃({filtered_df.loc[filtered_df['최고기온(℃)'].idxmax(), '연도']}년) 이었으며, "
                f"역대 최저 기온은 {filtered_df['최저기온(℃)'].min()}℃({filtered_df.loc[filtered_df['최저기온(℃)'].idxmin(), '연도']}년) 이었습니다.")

        # 선택 사항: 상세 표 데이터 확인
        if st.checkbox("전체 데이터 테이블 보기"):
            st.dataframe(filtered_df[['연도', '평균기온(℃)', '최저기온(℃)', '최고기온(℃)']].reset_index(drop=True))

except Exception as e:
    st.error(f"오류가 발생했습니다: {e}")
    st.info("seoul.csv 파일의 위치와 파일 인코딩(cp949)을 확인해 주세요.")
