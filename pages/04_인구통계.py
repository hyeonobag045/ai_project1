import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# 페이지 기본 설정
st.set_page_config(page_title="서울시 인구통계 대시보드", layout="centered")

# [중요] 스트림릿 클라우드(리눅스 기반) 환경에서 한글 깨짐을 방지하기 위한 폰트 설정
@st.cache_data
def set_korean_font():
    # 서버 시스템 내에 설치되어 있는 폰트 중 대표적인 한글 폰트 목록 확인
    font_names = ['NanumGothic', 'NanumBarunGothic', 'Malgun Gothic', 'AppleGothic', 'Noto Sans CJK KR']
    available_fonts = [f.name for f in fm.fontManager.ttflist]
    
    selected_font = None
    for font in font_names:
        if any(font in f_name for f_name in available_fonts):
            selected_font = font
            break
            
    if selected_font:
        plt.rc('font', family=selected_font)
    else:
        plt.rc('font', family='sans-serif')
    
    # 마이너스 기호 깨짐 방지
    plt.rcParams['axes.unicode_minus'] = False

set_korean_font()

st.title("🏙️ 서울시 자치구별 인구통계")
st.markdown("`population.csv` 데이터를 기반으로 연령대별 인구수 추이를 확인합니다.")

# 데이터 로드 및 전처리 함수
@st.cache_data
def load_data():
    df = pd.read_csv("population.csv", encoding="utf-8")
    
    # 숫자 데이터 내 콤마(,) 제거 후 정수형(int) 변환
    for col in df.columns[1:]:
        df[col] = df[col].astype(str).str.replace(",", "").astype(int)
        
    # 행정구역 코드 부분을 제외한 순수 구 이름만 추출
    df['행정구역_정제'] = df['행정구역'].apply(lambda x: x.split("(")[0].strip())
    df['행정구역_정제'] = df['행정구역_정제'].replace("서울특별시", "서울특별시 전체")
    
    return df

try:
    df = load_data()
    
    # 행정구 선택 셀렉트박스
    region_list = df['행정구역_정제'].tolist()
    selected_region = st.selectbox("조회할 행정구를 선택하세요:", region_list)
    
    # 선택된 자치구의 데이터 필터링
    row_data = df[df['행정구역_정제'] == selected_region].iloc[0]
    
    # 그래프를 그리기 위한 데이터 변환 (가로축: 연령대, 세로축: 인구수)
    age_groups = df.columns[1:-1].tolist()
    populations = [row_data[age] for age in age_groups]
    
    plot_df = pd.DataFrame({
        '연령대': age_groups,
        '인구수': populations
    })
    
    # 꺾은선 그래프 시각화 설정
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # 배경색 요구사항: 연한 보라색 배경 적용
    ax.set_facecolor('#F0ECFC')       # 그래프 플롯 내부 연보라색
    fig.patch.set_facecolor('#F8F6FF') # 그래프 바깥 여백 연보라색
    
    # 그래프 선 요구사항: 빨간색 꺾은선 그래프
    ax.plot(plot_df['연령대'], plot_df['인구수'], marker='o', color='#FF0000', linewidth=2.5, markersize=6)
    
    # 그래프 제목 요구사항: "서울시의 인구통계"
    ax.set_title(f"서울시의 인구통계 - {selected_region}", fontsize=16, fontweight='bold', pad=15)
    ax.set_xlabel("연령대", fontsize=12, labelpad=10)
    ax.set_ylabel("인구수 (명)", fontsize=12, labelpad=10)
    
    # 가독성을 높이기 위한 설정들
    ax.grid(True, linestyle='--', alpha=0.4, color='#9E9E9E')
    import matplotlib.ticker as ticker
    ax.get_yaxis().set_major_formatter(ticker.FuncFormatter(lambda x, p: format(int(x), ',')))
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    # 스트림릿 웹페이지에 그래프 표출
    st.pyplot(fig)
    
    # 상세 수치 표 제공
    with st.expander("📊 상세 데이터 표 확인하기"):
        st.dataframe(plot_df.set_index('연령대').style.format("{:,}명"))

except FileNotFoundError:
    st.error("⚠️ `population.csv` 파일이 동일한 디렉토리에 존재하지 않습니다. 파일을 업로드해 주세요.")
except Exception as e:
    st.error(f"❌ 오류가 발생했습니다: {e}")
