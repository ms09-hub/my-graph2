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
# 2. 장르 및 영화별 총 관객수 분포 (트리맵)
# ----------------------------------------------------
st.header("2. 장르 및 영화별 총 관객수 분포")

fig2 = px.treemap(
    data,
    path=[px.Constant("전체"), "genre", "movieNm"],
    values="total_audi",
    color="genre",
    title="장르별 영화 관객수 트리맵",
)

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

# ----------------------------------------------------
# 3. 총 관객수 분포 (히스토그램)
# ----------------------------------------------------
st.header("3. 영화별 총 관객수 분포")

fig3 = px.histogram(
    data,
    x="total_audi",
    nbins=20,
    title="총 관객수 분포 히스토그램",
    labels={"total_audi": "총 관객수", "count": "영화 수"},
)

fig3.update_traces(
    hovertemplate="<b>총 관객수 구간: %{x}</b><br>영화 수: %{y}편<extra></extra>"
)

st.plotly_chart(fig3, use_container_width=True)

# 최고 관객수 영화 정보 자동 추출
top_movie = data.loc[data["total_audi"].idxmax()]
top_movie_name = top_movie["movieNm"]
top_movie_audi = top_movie["total_audi"]

# 그래프 해석 안내 구역
st.subheader("💡 이 그래프로 알 수 있는 것")
st.info(
    f"대부분의 영화가 관객수 **200만 명 이하 하위 구간**에 밀집되어 있으며, 관객수가 커질수록 영화 수가 급격히 줄어드는 오른쪽 꼬리가 긴 분포 형태를 보입니다.\n\n"
    f"이 중 가장 많은 관객을 동원한 영화는 **'{top_movie_name}'**(총 관객수 {top_movie_audi:,.0f}명)입니다."
)

st.divider()

# ----------------------------------------------------
# 4. 개봉일 스크린수와 총 관객수의 관계 (산점도)
# ----------------------------------------------------
st.header("4. 개봉일 스크린수와 총 관객수의 관계")

fig4 = px.scatter(
    data,
    x="first_scrn",
    y="total_audi",
    color="genre",
    hover_name="movieNm",
    title="개봉일 스크린수 vs 총 관객수",
    labels={
        "first_scrn": "개봉일 스크린수",
        "total_audi": "총 관객수",
        "genre": "장르",
    },
)

fig4.update_traces(
    hovertemplate="<b>%{hovertext}</b><br>개봉일 스크린수: %{x:,.0f}개<br>총 관객수: %{y:,.0f}명<extra></extra>"
)

st.plotly_chart(fig4, use_container_width=True)

# 그래프 해석 안내 구역
st.subheader("💡 이 그래프로 알 수 있는 것")
st.info(
    "개봉일 스크린수가 많을수록 대체로 높은 총 관객수를 기록하는 양의 상관관계를 보이지만, 스크린수가 적어도 관객 흥행에 성공하거나 반대로 초기 스크린수 대비 상행 기대에 못 미친 아웃라이어 영화도 확인할 수 있습니다."
)

st.divider()
