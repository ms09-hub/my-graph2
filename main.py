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

genre_counts = data["genre"].value_counts().reset_index()
genre_counts.columns = ["장르", "영화 수"]

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

top_movie = data.loc[data["total_audi"].idxmax()]
top_movie_name = top_movie["movieNm"]
top_movie_audi = top_movie["total_audi"]

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

st.subheader("💡 이 그래프로 알 수 있는 것")
st.info(
    "개봉일 스크린수가 많을수록 대체로 높은 총 관객수를 기록하는 양의 상관관계를 보이지만, 스크린수가 적어도 관객 흥행에 성공하거나 반대로 초기 스크린수 대비 상행 기대에 못 미친 아웃라이어 영화도 확인할 수 있습니다."
)

st.divider()

# ----------------------------------------------------
# 5. 주요 장르별 총 관객수 분포 (상자 그림)
# ----------------------------------------------------
st.header("5. 주요 장르별 총 관객수 분포 비교")

genre_counts_series = data["genre"].value_counts()
major_genres = genre_counts_series[genre_counts_series >= 10].index
filtered_data = data[data["genre"].isin(major_genres)]

fig5 = px.box(
    filtered_data,
    x="genre",
    y="total_audi",
    color="genre",
    hover_name="movieNm",
    points="outliers",
    title="영화 10편 이상 주요 장르별 총 관객수 상자 그림",
    labels={"genre": "장르", "total_audi": "총 관객수"},
)

fig5.update_traces(
    hovertemplate="<b>%{hovertext}</b><br>총 관객수: %{y:,.0f}명<extra></extra>"
)

st.plotly_chart(fig5, use_container_width=True)

st.subheader("💡 이 그래프로 알 수 있는 것")
st.info(
    "주요 장르별 관객수의 중앙값과 사분위 범위를 통해 장르별 전반적인 흥행 규모를 파악할 수 있으며, "
    "상자 밖으로 크게 벗어난 점(이상치)을 통해 해당 장르 내에서 이례적인 대경신을 기록한 영화를 쉽게 구분할 수 있습니다."
)

st.divider()

# ----------------------------------------------------
# 6. 개봉일 스크린수·총 관객수·첫 주 관객수 관계 (버블 차트)
# ----------------------------------------------------
st.header("6. 스크린수, 총 관객수, 첫 주 관객수의 다차원 관계")

fig6 = px.scatter(
    data,
    x="first_scrn",
    y="total_audi",
    size="first_week_audi",
    color="genre",
    hover_name="movieNm",
    size_max=50,
    title="개봉일 스크린수 vs 총 관객수 (버블 크기: 개봉 첫 주 관객수)",
    labels={
        "first_scrn": "개봉일 스크린수",
        "total_audi": "총 관객수",
        "first_week_audi": "개봉 첫 주 관객수",
        "genre": "장르",
    },
)

fig6.update_traces(
    hovertemplate="<b>%{hovertext}</b><br>개봉일 스크린수: %{x:,.0f}개<br>총 관객수: %{y:,.0f}명<br>개봉 첫 주 관객수: %{marker.size:,.0f}명<extra></extra>"
)

st.plotly_chart(fig6, use_container_width=True)

st.subheader("💡 이 그래프로 알 수 있는 것")
st.info(
    "버블의 크기(첫 주 관객수)를 통해 초반 흥행 기세가 최종 관객수 및 초기 스크린 확보와 얼마나 밀접한 관계를 가지는지 한 번에 다차원적으로 비교할 수 있습니다."
)

st.divider()
