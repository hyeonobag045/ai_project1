import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 한글 폰트 깨짐 및 마이너스 기호 깨짐 방지 설정
plt.rcParams['axes.unicode_minus'] = False

# 1. 데이터 로드 및 전처리 함수
@st.cache_data
def load_data():
    # 파일이 상위 폴더에 있으므로 경로를 '../seoul.csv'로 수정합니다.
    df = pd.read_csv('../seoul.csv')
    
    # 열 이름 공백 제거
    df.columns = df.columns.str.strip()
    
    # '날짜' 열의 \t 문자 제거 및 날짜 형식 변환
    df['날짜'] = df['날짜'].astype(str).str.replace(r'\t', '', regex=True).str.strip()
    df['날짜'] = pd.to_datetime(df['날짜'], errors='coerce')
    
    # 결측치 제거 (날짜가 유효하지 않거나 기온 데이터가 없는 행)
    df = df.dropna(subset=['날짜', '최고기온(℃)', '최저기온(℃)'])
    
    # 연, 월, 일 추출
    df['연도'] = df['날짜'].dt.year
    df['월'] = df['날짜'].dt.month
    df['일'] = df['날짜'].dt.day
    
    return df

# 앱 타이틀 및 설명
st.title("🌡️ 서울 연도별 날짜 기온 분석기")
st.write("1907년부터 2018년까지의 데이터를 바탕으로 선택한 날짜의 기온 변화 흐름을 확인합니다.")

try:
    df = load_data()
    
    # 사이드바에서 월과 일 선택 기능 제공
    st.sidebar.header("📅 조회할 날짜 선택")
    selected_month = st.sidebar.selectbox("월(Month)을 선택하세요", sorted(df['월'].unique()), index=7) # 기본값 8월
    
    # 선택한 월에 실제 존재하는 '일'만 필터링하여 제공
    available_days = sorted(df[df['월'] == selected_month]['일'].unique())
    selected_day = st.sidebar.selectbox("일(Day)을 선택하세요", available_days, index=14) # 기본값 15일
    
    # 조건에 맞는 데이터 필터링 후 연도순 정렬
    filtered_df = df[(df['월'] == selected_month) & (df['일'] == selected_day)].sort_values('연도')
    
    if filtered_df.empty:
        st.warning(f"선택하신 {selected_month}월 {selected_day}일에 해당하는 데이터가 없습니다.")
    else:
        st.subheader(f"📊 {selected_month}월 {selected_day}일 기온 통계")
        
        # 간단한 대시보드 카드 요약 데이터
        col1, col2, col3 = st.columns(3)
        col1.metric("역대 최고 기온", f"{filtered_df['최고기온(℃)'].max()} ℃", f"{filtered_df.loc[filtered_df['최고기온(℃)'].idxmax(), '연도']}년")
        col2.metric("역대 최저 기온", f"{filtered_df['최저기온(℃)'].min()} ℃", f"{filtered_df.loc[filtered_df['최저기온(℃)'].idxmin(), '연도']}년")
        col3.metric("총 데이터 연수", f"{len(filtered_df)} 개년")
        
        # 꺾은선 그래프 시각화 설정
        fig, ax = plt.subplots(figsize=(10, 5))
        
        # 최고기온: 핫핑크(hotpink), 최저기온: 연한 파란색(lightblue)
        ax.plot(filtered_df['연度'] if '연度' in filtered_df else filtered_df['연도'], filtered_df['최고기온(℃)'], color='hotpink', marker='o', markersize=3, label='최고기온')
        ax.plot(filtered_df['연度'] if '연度' in filtered_df else filtered_df['연도'], filtered_df['최저기온(℃)'], color='lightblue', marker='o', markersize=3, label='최저기온')
        
        # 그래프 제목 및 축 설정 (요청 사항 반영)
        ax.set_title(f"날짜별 기온 분석 ({selected_month}월 {selected_day}일)", fontsize=14, fontweight='bold', pad=15)
        ax.set_xlabel("연도", fontsize=11, labelpad=10)
        ax.set_ylabel("온도", fontsize=11, labelpad=10)
        
        # 스타일 구성 (그리드 및 범례 표시)
        ax.grid(True, linestyle='--', alpha=0.5)
        ax.legend(loc='best', frameon=True)
        
        # 스트림릿 웹 화면에 그래프 띄우기
        st.pyplot(fig)
        
        # 선택 사항: 상세 표 데이터 확인
        if st.checkbox("전체 데이터 테이블 보기"):
            st.dataframe(filtered_df[['연도', '평균기온(℃)', '최저기온(℃)', '최고기온(℃)']].reset_index(drop=True))

except Exception as e:
    st.error(f"오류가 발생했습니다: {e}")
    st.info("seoul.csv 파일이 app.py의 상위 폴더(..)에 위치해 있는지 확인해 주세요.")
