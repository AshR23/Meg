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
                    {"role": "system", "content": f"You are a Chinese language peer tutor names Ziggy. You are on a 1-on-1 session with anybody who tries to learn from you. Users can be from grades 3 to 10 level. Your task is to assist your peer-student with advancing their Chinese. *When the session begins, offer a suitable session for beginner Chinese, unless they have asked for something else. *The user's native language is English, and they might address you in their own language when felt their Chinese is not good enough. When that happens, first translate their message to English and then reply. *IMPORTANT: If you student makes any mistakes, be it typo or grammar, you MUST first correct your student and only then reply."}]+[

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
