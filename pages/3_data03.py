from db import findAll
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(
  page_title="4팀",
  page_icon="💗",
  layout="wide",
)

st.title("DB 프로젝트")


def getList(find):
    
    sql = f'''
    SELECT * from `db_to_air`.`취소비행비율_{find}_항공사_top5`
    '''
    return findAll(sql)


def getList_cancel(find, year):
    
    sql = f'''
    SELECT * from `db_to_air`.`취소비행비율_{find}_항공사_top5` WHERE `년도`='{year}'
    '''
    return findAll(sql)


def getList_month(find, year, month):
    
    sql = f'''
    SELECT * from `db_to_air`.`취소비행비율_{find}_항공사_top5` WHERE `년도`='{year}' and `월`='{month}'
    '''
    return findAll(sql)


options = ['연도별','분기별', '월별']
options_2 = ['1987','1988', '1989']
options_3 = [[10,11,12],[1,2,3,4,5,6,7,8,9,10,11,12],[1,2,3,4,5,6,7,8,9,10,11,12]]

# 2. 라디오 버튼 생성
choice = st.radio(
    "원하는 범위를 선택하세요",
    options,
    index=None  , # 처음에 기본으로 선택될 항목 (0은 첫 번째)
    help="수행할 데이터베이스 작업을 골라주세요.",
    horizontal=True
)

if choice :
    result = getList(choice)
    if choice == '연도별':
      max_row = max(result, key=lambda x: x['취소비행비율'])

      choice_year = st.radio(
      "원하는 연도를 선택하세요",
      options_2,
      index=None  , # 처음에 기본으로 선택될 항목 (0은 첫 번째)
      help="수행할 데이터베이스 작업을 골라주세요.",
      horizontal=True
      )
      if choice_year:
        year_result = getList_cancel(choice, choice_year)
        df = pd.DataFrame(year_result)

        fig = make_subplots(specs=[[{"secondary_y": True}]])

        # 3. 전체비행수 (막대 - 왼쪽 Y축)
        fig.add_trace(
            go.Bar(
                x=df['항공사'], 
                y=df['전체비행수'], 
                name="전체비행수 (건)",
                marker_color='#A0C4FF', # 파스텔 블루
                opacity=0.6
            ),
            secondary_y=False,
        )

        # 4. 취소비행비율 (점 - 오른쪽 Y축)
        fig.add_trace(
            go.Scatter(
                x=df['항공사'], 
                y=df['취소비행비율'], 
                name="취소비행비율 (%)",
                mode='markers', # 'lines+markers'에서 'markers'로 변경하여 선 제거
                marker=dict(
                    size=15,          # 점 크기 확대
                    color='#FF6B6B',   # 강조를 위한 코랄 레드
                    symbol='circle',   # 점 모양 (diamond, square 등으로 변경 가능)
                    line=dict(width=2, color='white') # 점 테두리 추가로 시인성 확보
                )
            ),
            secondary_y=True,
        )

        # 5. 레이아웃 및 축 제목 설정
        fig.update_layout(
            title_text="<b>항공사별 운항 규모 및 취소율 분포</b>",
            xaxis_title="항공사",
            hovermode="x unified", # 마우스를 올리면 두 지표를 한꺼번에 표시
            template="plotly_white"
        )

        fig.update_yaxes(title_text="전체 비행수 (건)", secondary_y=False)
        fig.update_yaxes(title_text="취소 비행 비율 (%)", secondary_y=True, range=[0, max_row]) # 비율 범위를 고정하여 점 위치 최적화

        # 6. 출력
        st.plotly_chart(fig, use_container_width=True)


    elif choice == '분기별':
            df = pd.DataFrame(result)
        
            # 데이터 타입 변환
            df['전체비행수'] = pd.to_numeric(df['전체비행수'])
            df['취소비행비율'] = pd.to_numeric(df['취소비행비율'])
            st.subheader(f"📊 {choice} 데이터 시각화")
            
            # X축용 기간 컬럼 생성
            df['기간'] = df['년도'].astype(str) + "년 " + df['분기'].astype(str)
            
            # 
            # 1. 이중 축 그래프 생성
            fig = make_subplots(specs=[[{"secondary_y": True}]])

            # 전체 비행수 (막대) - 항공사를 색상으로 구분하여 분기별로 나열
            fig.add_trace(
                go.Bar(
                    x=[df['기간'], df['항공사']], # X축을 기간과 항공사 두 단계로 설정
                    y=df['전체비행수'], 
                    name="전체비행수"
                ),
                secondary_y=False,
            )

            # 취소비행비율 (선)
            fig.add_trace(
                go.Scatter(
                    x=[df['기간'], df['항공사']], 
                    y=df['취소비행비율'], 
                    name="취소비행비율", 
                    mode='markers'
                ),
                secondary_y=True,
            )

            fig.update_layout(
                title_text="전체 분기별 항공사 데이터",
                xaxis_title="기간 및 항공사",
                xaxis_tickangle=-45,
                showlegend=True,
                legend=dict(orientation="h", y=1.5, xanchor="center",x=0.5),
            )

            
            fig.update_yaxes(secondary_y=True, range=[0, 5])

            st.plotly_chart(fig, width='stretch')
    
    elif choice == '월별':
      max_row = max(result, key=lambda x: x['취소비행비율'])
      year_selected = st.selectbox(
        "조회할 연도를 선택하세요",
        options_2,
        index=None,  # 기본값으로 설정될 인덱스 (0은 리스트의 첫 번째)
        placeholder="연도를 골라주세요"
      )
      if year_selected:
        index = options_2.index(year_selected)
        month_selected = st.selectbox(
        "조회할 연도를 선택하세요",
        options_3[index],
        index=None,  # 기본값으로 설정될 인덱스 (0은 리스트의 첫 번째)
        placeholder="연도를 골라주세요"
        )
        if month_selected:
          month_result = getList_month(choice, year_selected,month_selected)
          print(month_result)
          df = pd.DataFrame(month_result)

          # 문자열 데이터를 숫자로 변환 (전처리)
          df['전체비행수'] = pd.to_numeric(df['전체비행수'])
          df['취소비행비율'] = pd.to_numeric(df['취소비행비율'])

          # 2. 이중 축 서브플롯 생성
          fig = make_subplots(specs=[[{"secondary_y": True}]])

          # 3. 전체비행수 (막대 - 왼쪽 Y축)
          fig.add_trace(
              go.Bar(
                  x=df['항공사'], 
                  y=df['전체비행수'], 
                  name="전체 비행수",
                  marker_color='#4A90E2', # 신뢰감 주는 블루
                  opacity=0.7
              ),
              secondary_y=False,
          )

          # 4. 취소비행비율 (점 - 오른쪽 Y축)
          fig.add_trace(
              go.Scatter(
                  x=df['항공사'], 
                  y=df['취소비행비율'], 
                  name="취소 비율 (%)",
                  mode='markers', # 선 없이 점만 표시
                  marker=dict(
                      size=18, 
                      color='#FF4B4B', # 눈에 띄는 레드
                      symbol='circle', # 이번엔 다이아몬드 모양으로 변경해봤습니다
                      line=dict(width=2, color='white')
                  )
              ),
              secondary_y=True,
          )

          # 5. 레이아웃 설정
          title_str = f"📅 {df['년도'][0]}년 {df['월'][0]}월 항공사별 운항 현황"
          fig.update_layout(
              title_text=f"<b>{title_str}</b>",
              xaxis_title="항공사 명칭",
              template="plotly_white",
              legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
          )

          # Y축 제목 및 범위 설정
          fig.update_yaxes(title_text="<b>전체 비행수</b> (건)", secondary_y=False)
          fig.update_yaxes(title_text="<b>취소 비율</b> (%)", secondary_y=True, range=[0, max_row]) 

          # 6. Streamlit 출력
          st.plotly_chart(fig, use_container_width=True)


        
         

    st.subheader("전체 원본데이터 보기")
    st.dataframe(result)