# streamlit demo

# 스트림릿 라이브러리를 사용하기 위한 임포트
import streamlit as st
from utils import print_messages, StreamHandler
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.messages import ChatMessage


# ChatGPT 로드
#from langchain_openai import ChatOpenAI
from langchain_community.chat_models import ChatOpenAI


# Ollama 로드
#from langchain_community.llms import ollama
from langchain_community.chat_models import ChatOllama



from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser

import os

#API KEY 세팅
#os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
           
           
st.set_page_config(page_title="Python 을 위한 Chat Jason !!", page_icon=":/wave")
st.title('Chat Jason')

# 메세지를 누적해서 쌓기위해 새로고침을 막음 
if "messages" not in st.session_state:
    st.session_state["messages"] = []


# 채팅 대화기록을 저장하는 store 세션 상태 변수
if "store" not in st.session_state:
    st.session_state["store"] = dict()

# 사이드바 생성해서 세션 id 넣어주기
with st.sidebar:
    session_id = st.text_input("Session ID", value="abc123")
    clear_btn = st.button("대화기록 초기화")
    if clear_btn:
        st.session_state["messages"] = []
        st.experimental_rerun()


# 이전 대화기록을 출력해주는 코드
print_messages()



# 세션 ID를 기반으로 세션 기록을 가져오는 함수
def get_session_history(session_ids: str) -> BaseChatMessageHistory:
    if session_ids not in st.session_state["store"]: #세션 ID 가 store 에 없는 경우
        #새로운 ChatMessageHistory 객체를 생성하여 store에 저장
        st.session_state["store"][session_ids] = ChatMessageHistory()
    
    return st.session_state["store"][session_ids]





if user_input := st.chat_input("메세지를 입력해주세요."):
    
    # 사용자가 입력한 내용
    st.chat_message("user").write(f'{user_input}')
    st.session_state["messages"].append(ChatMessage(role="user", content=user_input))


  

    # AI의 답변
    with st.chat_message("assistant"):
        stream_handler = StreamHandler(st.empty())

        # LLM 을 사용하여 AI의 답변을 생성
        # 1. 모델 생성
        #llm = ChatOpenAI(streaming=True, callbacks=[stream_handler])
        llm = ChatOllama(model = "llama3:latest", streaming=True, callbacks=[stream_handler])


        # 2. 프롬프트 생성
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "질문에 짧고 간결하게 답변해 주세요."
                ),
                # 대화 기록용 변수로 사용, history 가 MessageHistory 의 key가 됨
                MessagesPlaceholder(variable_name="history"),
                ("human", "{question}"), #사용자의 질문을 입력

            ]
        )

        chain = prompt | llm

        chain_with_memory = RunnableWithMessageHistory( # RunnableWithMessageHistory 객체 생성
            chain, #실행할 Runnable 객체
            get_session_history, # 세션 기록을 가져오는 함수
            input_messages_key="question", # 사용자 질문의 키
            history_messages_key="history", # 기록 메세지의 키 

        )


        response = chain_with_memory.invoke(

            {"question":  user_input},

            #세션ID 설정
            config = {"configurable": {"session_id": session_id }},

        )

        st.session_state["messages"].append(ChatMessage(role="assistant", content=response.content))



