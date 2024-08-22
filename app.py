# streamlit demo

# 스트림릿 라이브러리를 사용하기 위한 임포트
import streamlit as st




# 웹 대시보드 개발 라이브러리인 스트림릿은 main 함수가 있어야 한다.

def main():
    st.set_page_config(page_title="Python 을 위한 Chat Jason !!", page_icon=":/wave")
    st.title('Chat Jason')

    # 메세지를 누적해서 쌓기위해 새로고침을 막음 
    if "messages" not in st.session_state:
        st.session_state["messages"] = []


    def print_messages():
        # 이전 대화기록을 출력해주는 코드
        if "messages" in st.session_state and len(st.session_state["messages"])>0:

            for role, message in st.session_state["messages"]:
                st.chat_message(role).write(message)

    print_messages()

    if user_input := st.chat_input("메세지를 입력해주세요."):
        st.chat_message("user").write(f'{user_input}')
        st.session_state["messages"].append(("user", user_input))


        with st.chat_message("assistant"):
            msg= f"당신이 입력한 내용: {user_input}"
            st.write(msg)
            st.session_state["messages"].append((("assistant", msg)))

if __name__ == '__main__':
    main()


