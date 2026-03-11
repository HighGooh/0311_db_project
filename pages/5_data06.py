import streamlit as st
from db import findAll, findOne
import pandas as pd
import plotly.express as px

st.set_page_config(
  page_title="4팀",
  page_icon="💗",
  layout="wide",
)

    
st.title("항공사별 회복비행비율")

def get_data():
    sql = "select * from db_to_air.`항공사별_회복비행비율` order by `회복비행비율` desc"
    data = findAll(sql)
    if data:
        df = pd.DataFrame(data)
        df['회복비행비율'] = pd.to_numeric(df['회복비행비율'], errors='coerce')
        df['항공사명'] = df['항공사명'].str.strip()
        return df
    else:
        return None
    
df = get_data()

airline = ['전체',...]

selected = st.selectbox(label="항공사를 선택하세요", 
	options=airline,
	index=None,
	placeholder="수집 대상을 선택하세요.")

for i in df['항공사명']:
  airline.append(i)

if df is not None:
  st.button("수집하기")
  if selected == '전체':
        st.bar_chart(data=df, x="항공사명", y="회복비행비율")
        st.dataframe(df, use_container_width=True, hide_index=True)
  else:
      sql = f"select * from db_to_air.`항공사별_회복비행비율` where `항공사명` = '{selected}'"
      data = findOne(sql)
      if data:
          recovery = int(data['회복비행횟수'])