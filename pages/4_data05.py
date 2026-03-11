import streamlit as st
from db import findAll
import pandas as pd

st.set_page_config(
  page_title="4팀",
  page_icon="💗",
  layout="wide",
)

st.title("항공사별 초과비행시간 평균값")

def get_data():
    sql = "select * from db_to_air.`항공사별_초과비행시간` order by `평균초과비행시간` desc"
    data = findAll(sql)
    if data:
        df = pd.DataFrame(data)
        return df
    else:
        return None
    
if st.button("차트그리기"):
    st.bar_chart(data= get_data(), x="항공사명", y="평균초과비행시간")
    st.dataframe(get_data(), use_container_width=True, hide_index=True)
    