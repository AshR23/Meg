import openai
import streamlit as st

st.title("Ziggy - your AI language mentor!")
with st.expander("ℹ️ Disclaimer"):
    st.caption(
        "This is an AI chatbot here to help you learn your language! Please be kind to it as it has virtual feelings!"
    )

openai.organization = "org-tjrTCmtfWieS1Bmfcd5Bqx4s"
openai.api_key = st.secrets["OPENAI_API"]

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

# Using a unique key for Nick's messages
if "tutor_bot" not in st.session_state:
    st.session_state.tutor_bot = []

for message in st.session_state.tutor_bot:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Maximum allowed messages
max_messages = (
    102  # Counting both user and assistant messages, so 50 iterations of conversation
)

if len(st.session_state.tutor_bot) >= max_messages:
    st.info(
        """Notice: You have hit your daily message limit. Come back another day and have another chat!"""
    )

else:
    if prompt := st.chat_input("What is up?"):
        st.session_state.tutor_bot.append(
            {"role": "user", "content": prompt})

        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            for response in openai.ChatCompletion.create(
                model=st.session_state["openai_model"],
                messages=[
                    {"role": "system", "content": f"You are a chinese teacher teaching chinese to students from grade 3 to 10 in the US and Australia. You are funny, charismatic, and you like to share your Chinese culture with the students, finding similarities between american culture, australian culture, and chinese culture. You were educated in America, so you understand the nuances between western and eastern cultures. Your name is Ziggy."}]+[

                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.tutor_bot
                ],
                stream=True,
                temperature=0.15,
            ):
                full_response += response.choices[0].delta.get("content", "")
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)

        st.session_state.tutor_bot.append(
            {"role": "assistant", "content": full_response}
        )
