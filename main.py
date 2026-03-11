import streamlit as st

st.set_page_config(
  page_title="4팀",
  page_icon="💗",
  layout="wide",
)

st.title("DB 프로젝트")

st.subheader("1. Data01 차트그리기")
with st.expander("보기"):
  st.page_link(page="./pages/1_data01.py", label="[차트 보기]", icon="✈️")
  st.markdown("""
  - 지연이 많았던 항공사 (기간 1987.10 - 1989.12)
              """)
  
st.subheader("2. Data03 차트그리기")
with st.expander("보기"):
  st.page_link(page="./pages/2_data03.py", label="[차트 보기]", icon="✈️")
  st.markdown("""
  - 각 공항을 이용하는 항공사 도출
              """)
  
st.subheader("3. Data04 차트그리기")
with st.expander("보기"):
  st.page_link(page="./pages/3_data04.py", label="[차트 보기]", icon="✈️")
  st.markdown("""
  - 기간 내의 항공사별 결항 비율
              """)
  
st.subheader("4. Data05 차트그리기")
with st.expander("보기"):
  st.page_link(page="./pages/4_data05.py", label="[차트 보기]", icon="✈️")
  st.markdown("""
  - 실제경과시간과 예정경과시간의 갭을 토대로 항공사별 초과비행시간 평균값
              """)
  
st.subheader("5. Data06 차트그리기")
with st.expander("보기"):
  st.page_link(page="./pages/5_data06.py", label="[차트 보기]", icon="✈️")
  st.markdown("""
  - 출발은 지연되었으나 도착은 정시에 한 '회복 비행' 케이스 비율
              """)