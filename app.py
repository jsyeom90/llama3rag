# streamlit demo

# 스트림릿 라이브러리를 사용하기 위한 임포트
import streamlit as st

# 웹 대시보드 개발 라이브러리인 스트림릿은 main 함수가 있어야 한다.

def main():
    st.set_page_config(page_title="Python 을 위한 Chat Jason !!", page_icon=":/wave")
    st.title('Chat Jason')
    
if __name__ == '__main__':
    main()