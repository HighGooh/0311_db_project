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
    sql = "select * from db_to_air.`data07` order by `회복비행비율` desc"
    data = findAll(sql)
    if data:
        df = pd.DataFrame(data)
        return df
    else:
        return None
    
df = get_data()

airline = ['전체']

for i in df['항공사명']:
    airline.append(i.strip())

selected = st.selectbox(label="항공사를 선택하세요", 
	options=airline,
	index=None,
	placeholder="수집 대상을 선택하세요.")

if df is not None:
  if selected == '전체':
    st.bar_chart(data=df, x="항공사명", y="회복비행비율")
    st.dataframe(df, use_container_width=True, hide_index=True)
  else:
      sql = f"select * from db_to_air.`data07` where `항공사명` = '{selected}'"
      data = findOne(sql)
      if data:
          recovery = int(data['회복비행횟수'])
          deley = int(data['총지연횟수'])
          unrecovery = deley - recovery
          pie_df = pd.DataFrame({
            "구분": ["회복 성공", "회복 실패"],
            "횟수": [recovery, unrecovery]
          })
          fig = px.pie(pie_df, values='횟수', names='구분', 
                     title=f"{selected} 회복 비행 비율",
                     color_discrete_sequence=['#FF5252',"#C4E9F8"])
          st.plotly_chart(fig, use_container_width=True)
          