import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


st.set_page_config(page_title="Angry Fergy Bot", page_icon="\U0001F916")
st.title("Angry Fergy Bot")


# get response


def get_response(query, chat_history):
    template = """
    You are a very angry assistant, but you still answer questions.  Answer the following questions considering the history of the conversation.

    Chat history: {chat_history}

    User question: {user_question}
    """
    prompt = ChatPromptTemplate.from_template(template)
    llm = ChatOpenAI()
    chain = prompt | llm | StrOutputParser()
    return chain.stream({"chat_history": chat_history, "user_question": query})


# conversation
for message in st.session_state.chat_history:
    if isinstance(message, HumanMessage):
        with st.chat_message("Human"):
            st.markdown(message.content)
    else:
        with st.chat_message("AI"):
            st.markdown(message.content)


# user input
user_query = st.chat_input("Your message")
if user_query is not None and user_query != "":
    st.session_state.chat_history.append(HumanMessage(user_query))

with st.chat_message("Human"):
    st.markdown(user_query)

with st.chat_message("AI"):
    ai_response = st.write_stream(
        get_response(user_query, st.session_state.chat_history)
    )


st.session_state.chat_history.append(AIMessage(ai_response))
# client = OpenAI()

# completion = client.chat.completions.create(
#     model="gpt-3.5-turbo",
#     messages=[
#         {
#             "role": "system",
#             "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair.",
#         },
#         {
#             "role": "user",
#             "content": "Compose a poem that explains the concept of recursion in programming.",
#         },
#     ],
# )

# print(completion.choices[0].message)
