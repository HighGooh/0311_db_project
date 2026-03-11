import streamlit as st
import pandas as pd
import plotly.express as px
from db import findAll

st.set_page_config(
  page_title="4팀",
  page_icon="💗",
  layout="wide",
)

def get_data():
    try:
       data = findAll("SELECT * FROM db_to_air.`data01`")
       if data:
           return data
    except Exception as e:
      st.error(f"DB 에러: {e}")
      return None

st.title("01. 지연이 많았던 항공사")

# DB 데이터 불러오기
data = get_data()

if data:
    df = pd.DataFrame(data)
    # 인덱스를 1부터 시작하도록 변경
    df.index = range(1, len(df) + 1)

    # 문자열 타입 => 숫자로 변환
    df['도착지연횟수'] = pd.to_numeric(df['도착지연횟수'])

    st.subheader("✈️ 항공사별 지연 건수 (1987.10 ~ 1989.12)")

    # 보기 옵션 선택창
    view_option = st.radio("", ["Top 5", "전체 보기"], horizontal=True)

    # 선택에 따른 데이터 필터링
    if view_option == "Top 5":
        selected_df = df.head(5)
    else:
        selected_df = df

    # bar 차트
    fig_bar = px.bar(
        selected_df, 
        x="항공사", 
        y="도착지연횟수", 
        text_auto='.3s', # 막대 위에 수치 표시
        )
    fig_bar.update_layout(
        xaxis=dict(title=None),
        margin=dict(l=40, r=20, t=20, b=20)
    )
    st.plotly_chart(fig_bar, width='stretch')

    # 데이터 보기
    with st.expander("원본 데이터 상세보기"):
        st.dataframe(df)
else:
    st.info("표시할 데이터가 없습니다.")