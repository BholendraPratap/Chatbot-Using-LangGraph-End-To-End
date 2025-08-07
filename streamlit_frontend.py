import streamlit as st
from chatbot_backend import chatbot
from langchain_core.messages import HumanMessage

# st.session_state -> dict -> 
CONFIG = {'configurable': {'thread_id': 'thread-1'}}

if 'message_history' not in st.session_state:
    #here session state is used to store the conversation history which is a list of dictionaries and it will be not reset when the user refreshes the page
    st.session_state['message_history'] = []

# loading the conversation history
for message in st.session_state['message_history']:# this is a list of dictionaries
    # message is a dictionary with keys 'role' and 'content'
    with st.chat_message(message['role']):
        st.text(message['content'])

#{'role': 'user', 'content': 'Hi'}
#{'role': 'assistant', 'content': 'Hi=ello'}

user_input = st.chat_input('Type here')

if user_input:

    # first add the message to message_history
    st.session_state['message_history'].append({'role': 'user', 'content': user_input})
    with st.chat_message('user'):# this is a special function in streamlit to display the message in the chat format
        st.text(user_input)# this will display the user message in the chat format

    # invoke the chatbot with the user input
    # the chatbot expects a dictionary with key 'messages' which is a list of messages
    response = chatbot.invoke({'messages': [HumanMessage(content=user_input)]}, config=CONFIG)
    
    ai_message = response['messages'][-1].content
    # first add the message to message_history
    # then display the message in the chat format
    # response['messages'] is a list of messages and we are getting the last message which is the AI response
    st.session_state['message_history'].append({'role': 'assistant', 'content': ai_message})
    with st.chat_message('assistant'):
        st.text(ai_message)