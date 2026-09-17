import pandas as pd
import plotly.express as px
import streamlit as st

# 페이지 설정
st.set_page_config(
    page_title="영화 데이터 그래프 도감 2 - 분포와 관계", layout="wide"
)

st.title("🎬 영화 데이터 그래프 도감 2 - 분포와 관계")
st.write(
    "박스오피스 상위권 영화 데이터를 바탕으로 영화 시장의 분포와 관계를 탐색합니다."
)

# 데이터 불러오기 및 전처리
DATA_URL = (
    "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_movies.csv"
)


@st.cache_data
def load_data():
    df = pd.read_csv(DATA_URL)
    # 장르 처리: 세로막대 기호(|)로 구분된 경우 첫 번째 장르만 추출
    df["genre"] = df["genre"].fillna("미상").astype(str).str.split("|").str[0]
    return df


data = load_data()

st.divider()

# ----------------------------------------------------
# 1. 장르별 영화 편수 (도넛 그래프)
# ----------------------------------------------------
st.header("1. 장르별 영화 편수 비율")

# 장르별 편수 집계
genre_counts = data["genre"].value_counts().reset_index()
genre_counts.columns = ["장르", "영화 수"]

# Plotly 도넛 차트 생성
fig1 = px.pie(
    genre_counts,
    values="영화 수",
    names="장르",
    hole=0.4,
    title="장르별 분포",
    hover_data=["영화 수"],
)

# 마우스오버 시 편수와 비율이 함께 표시되도록 설정
fig1.update_traces(
    textinfo="percent+label",
    hovertemplate="<b>장르: %{label}</b><br>편수: %{value}편<br>비율: %{percent}",
)

st.plotly_chart(fig1, use_container_width=True)

# 그래프 해석 안내 구역
st.subheader("💡 이 그래프로 알 수 있는 것")
st.info(
    "박스오피스 상위권에 가장 많이 진입한 주요 장르의 비중을 한눈에 파악할 수 있으며, 특정 장르의 쏠림 현상을 확인해 볼 수 있습니다."
)

st.divider()

# ----------------------------------------------------
# 2. 장르별 영화 총 관객수 분포 (트리맵)
# ----------------------------------------------------
st.header("2. 장르 및 영화별 총 관객수 분포")

# Plotly 트리맵 생성 (계층 구조: 장르 -> 영화명, 크기: 총 관객수)
fig2 = px.treemap(
    data,
    path=[px.Constant("전체"), "genre", "movieNm"],
    values="total_audi",
    color="genre",
    title="장르별 영화 관객수 트리맵",
)

# 마우스오버 시 영화명과 총 관객수가 깔끔하게 표시되도록 설정
fig2.update_traces(
    hovertemplate="<b>%{label}</b><br>총 관객수: %{value:,.0f}명<extra></extra>"
)

st.plotly_chart(fig2, use_container_width=True)

# 그래프 해석 안내 구역
st.subheader("💡 이 그래프로 알 수 있는 것")
st.info(
    "각 장르 내부에서 어느 영화가 관객수를 주로 견인했는지, 그리고 전체 관객수 관점에서 어떤 장르와 영화가 가장 큰 비중을 차지하는지 한눈에 비교할 수 있습니다."
)

st.divider()
