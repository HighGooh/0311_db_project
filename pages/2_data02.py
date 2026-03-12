from db import findAll
import streamlit as st
import pandas as pd

st.set_page_config(
  page_title="4팀",
  page_icon="💗",
  layout="wide",
)

st.title("DB 프로젝트")

def getList_airport(txt):
    
    sql = f'''
    SELECT `공항` from `db_to_air`.`실운행_공항_목록` WHERE `공항` LIKE '{txt}%'
    '''
    return findAll(sql)

def getList_airline(data):
    
    sql = f'''
    SELECT `항공사명`,`항공사코드` from `db_to_air`.`공항별_항공사_목록` WHERE `공항`='{data}'
    '''
    return findAll(sql)

         
def airline_card(name, code, city):
    # 단순한 CSS 스타일 적용
    st.markdown(f"""
        <div style="
            border: 1px solid #ddd;
            border-radius: 10px;
            padding: 15px;
            margin-bottom: 10px;
            background-color: #f9f9f9;">
            <h4 style="margin:0; color: #1f77b4;">✈️ {name}</h4>
            <p style="margin:5px 0 0 0; color: #666;"><b>Code:</b> {code} | <b>City:</b> {city}</p>
        </div>
    """, unsafe_allow_html=True)


user_name = st.text_input("검색하실 공항명의 첫 글자를 적어주세요(a-z)", placeholder="a", max_chars=1)

if user_name:
  options = []
  for data in getList_airport(user_name):
    options.append(data["공항"])

  if options:
    selection = st.pills("공항 선택", options, selection_mode="single")
    if selection:
      st.markdown(f"현재 **{selection}** 공항에 해당하는 데이터만 필터링 중입니다.")
      airlineList = getList_airline(selection)
      if airlineList :
        st.subheader("항공사 목록 (카드형)")
        cols = st.columns(2)  # 2열로 배치
        airline = [data['항공사명'] for data in airlineList]
        code = [data['항공사코드'] for data in airlineList]
        for i, name in enumerate(airline):
            with cols[i % 2]:
                airline_card(name, code[i], selection)
