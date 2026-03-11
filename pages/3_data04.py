from db import findAll
import streamlit as st
import pandas as pd

st.set_page_config(
  page_title="4팀",
  page_icon="💗",
  layout="wide",
)

st.title("DB 프로젝트")


def getList_airport(find):
    
    sql = f'''
    SELECT * from `db_to_air`.`취소비행비율_{find}_항공사_top5`
    '''
    return findAll(sql)


options = ['분기별', '연도별', '월별']

# 2. 라디오 버튼 생성
choice = st.radio(
    "원하는 작업을 선택하세요",
    options,
    index=None  , # 처음에 기본으로 선택될 항목 (0은 첫 번째)
    help="수행할 데이터베이스 작업을 골라주세요.",
    horizontal=True
)

if choice :
    result = getList_airport(choice)
    print(result)
    st.dataframe(result)