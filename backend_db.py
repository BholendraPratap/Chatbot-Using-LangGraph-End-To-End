from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage,HumanMessage
from langchain_groq import ChatGroq
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph.message import add_messages
from dotenv import load_dotenv
import sqlite3


load_dotenv()

llm = ChatGroq(model="gemma2-9b-it")

class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

def chat_node(state: ChatState):
    messages = state['messages']
    response = llm.invoke(messages)
    return {"messages": [response]}

# Checkpointer
conn = sqlite3.connect(database="chatbot.db", check_same_thread=False)
checkpointer = SqliteSaver(conn=conn)

graph = StateGraph(ChatState)
graph.add_node("chat_node", chat_node)
graph.add_edge(START, "chat_node")
graph.add_edge("chat_node", END)

# Compile the graph
chatbot = graph.compile(checkpointer=checkpointer)

# Retrieve all chat threads
def retrieve_all_threads():
    all_threads = set()
    # Retrieve all thread IDs from the checkpointer
    for checkpoint in checkpointer.list(None):
        all_threads.add(checkpoint.config['configurable']['thread_id'])

    return list(all_threads)

# #testing
# config={'configurable':{'thread_id':'thread-1'}}

# result = chatbot.invoke({"messages": [HumanMessage(content="what is my name?")]}, config=config)

# print(result)