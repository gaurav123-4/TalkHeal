import googletrans
from googletrans import Translator
import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime
from core.utils import get_current_time, get_ai_response, save_conversations
import requests

# Inject JS to get user's local time zone
def set_user_time_in_session():
    if "user_time_offset" not in st.session_state:
        components.html("""
            <script>
            const offset = new Date().getTimezoneOffset(); 
            const time = new Date().toLocaleString();      
            const data = {offset: offset, time: time};
            window.parent.postMessage({type: 'USER_TIME', data: data}, '*');
            </script>
        """, height=0)

        st.markdown("""
        <script>
        window.addEventListener("message", (event) => {
            if (event.data.type === "USER_TIME") {
                const payload = JSON.stringify(event.data.data);
                fetch("/", {
                    method: "POST",
                    headers: {"Content-Type": "application/json"},
                    body: payload
                }).then(() => location.reload());
            }
        });
        </script>
        """, unsafe_allow_html=True)

set_user_time_in_session()

# Display chat messages
def render_chat_interface():
    # 🌐 Language selector in sidebar
    st.sidebar.title("🌐 Language Settings")
    language_map = googletrans.LANGUAGES
    lang_name_to_code = {v.title(): k for k, v in language_map.items()}
    selected_lang_name = st.sidebar.selectbox("Choose your language", sorted(lang_name_to_code.keys()), index=0)
    selected_lang_code = lang_name_to_code[selected_lang_name]
    st.session_state['selected_lang_code'] = selected_lang_code

    if st.session_state.active_conversation >= 0:
        active_convo = st.session_state.conversations[st.session_state.active_conversation]

        if not active_convo["messages"]:
            st.markdown(f"""
            <div class="welcome-message">
                <strong>Hello! I'm TalkHeal, your mental health companion 🤗</strong><br>
                How are you feeling today? You can write below or start a new topic.
                <div class="message-time">{get_current_time()}</div>
            </div>
            """, unsafe_allow_html=True)

        for msg in active_convo["messages"]:
            css_class = "user-message" if msg["sender"] == "user" else "bot-message"
    timestamp = msg.get("timestamp")
    if timestamp:
        message_time = time.strftime('%I:%M %p', time.localtime(timestamp))
    else:
        message_time = ""

    st.markdown(f"""
    <div class="{css_class}">
        {msg["message"]}
        <div class="message-time">{message_time}</div>
    </div>
    """, unsafe_allow_html=True)


# Handle chat input and generate AI response
def handle_chat_input(model, system_prompt):
    if "pre_filled_chat_input" not in st.session_state:
        st.session_state.pre_filled_chat_input = ""
    initial_value = st.session_state.pre_filled_chat_input

    translator = Translator()
    target_lang = st.session_state.get("selected_lang_code", "en")

    st.session_state.pre_filled_chat_input = ""

    with st.form(key="chat_form", clear_on_submit=True):
        col1, col2 = st.columns([5, 1])
        with col1:
            user_input = st.text_input(
                "Share your thoughts...",
                key="message_input",
                label_visibility="collapsed",
                placeholder="Type your message here...",
                value=initial_value
            )
        with col2:
            send_pressed = st.form_submit_button("Send", use_container_width=True)

    if (send_pressed or st.session_state.get("send_chat_message", False)) and user_input.strip():
        translated_input = translator.translate(user_input, dest="en").text

        if 'send_chat_message' in st.session_state:
            st.session_state.send_chat_message = False

        if st.session_state.active_conversation >= 0:
            current_time = get_current_time()
            active_convo = st.session_state.conversations[st.session_state.active_conversation]

            active_convo["messages"].append({
                "sender": "user",
                "message": user_input.strip(),
                "time": current_time
            })

            if len(active_convo["messages"]) == 1:
                title = user_input[:30] + "..." if len(user_input) > 30 else user_input
                active_convo["title"] = title

            save_conversations(st.session_state.conversations)

            def format_memory(convo_history, max_turns=10):
                context = ""
                for msg in convo_history[-max_turns*2:]:
                    sender = "User" if msg["sender"] == "user" else "Bot"
                    context += f"{sender}: {msg['message']}\n"
                return context

            
                with st.spinner("TalkHeal is thinking..."):
                    memory = format_memory(active_convo["messages"])
                    prompt = f"{system_prompt}\n\n{memory}\nUser: {translated_input}\nBot:"
            try:
                    response = type('obj', (object,), {
                    'status_code': 200,
                    'json': lambda: {"response": "I understand. Can you tell me more?"}
                        })
                    ai_response = response.json().get("response") or "Sorry, I didn’t understand that."

                    if target_lang != "en":
                        try:
                            translated_obj = translator.translate(ai_response, dest=target_lang)
                            ai_response = translated_obj.text
                        except Exception:
                            st.warning("⚠️ Translation failed. Showing English response.")

                    active_convo["messages"].append({
                        "sender": "bot",
                        "message": ai_response,
                        "time": get_current_time()
                    })

            except requests.RequestException:
                st.error("Network connection issue. Please check your internet connection.")
                active_convo["messages"].append({
                    "sender": "bot",
                    "message": "I'm having trouble connecting to my services. Please check your internet connection and try again.",
                    "time": get_current_time()
                })

            except Exception:
                st.error("An unexpected error occurred. Please try again.")
                active_convo["messages"].append({
                    "sender": "bot",
                    "message": "I'm having trouble responding right now. Please try again in a moment.",
                    "time": get_current_time()
                })

            save_conversations(st.session_state.conversations)
            st.rerun()
