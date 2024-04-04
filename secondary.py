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


import os

from langchain.agents import AgentType, initialize_agent, load_tools
from langchain_openai import OpenAI
import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain.agents import AgentType, create_openai_tools_agent, load_tools
from dotenv import load_dotenv

load_dotenv

template = """
    You are a very knowledgeable, nerdy assistant and you answer questions.  Answer the following questions considering the history of the conversation.

 
    """

llm = ChatOpenAI(model_name="gpt-3.5-turbo")
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant"),
        MessagesPlaceholder("chat_history", optional=True),
        ("human", "{input}"),
        MessagesPlaceholder("agent_scratchpad"),
    ]
)
tools = load_tools(["openweathermap-api"], llm)

agent_chain = create_openai_tools_agent(llm, tools, prompt)

agent_chain.run("What's the Weather in New York?")
