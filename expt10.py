import os
import streamlit as st
from google import genai
from google.genai import types

# ---------- Page configuration ----------
st.set_page_config(page_title="AI Text Utility", page_icon="✍️", layout="wide")

MODEL_NAME = "gemini-2.5-flash"

# ---------- Cached resource: API client created once, reused across reruns ----------
@st.cache_resource
def get_client(api_key: str):
    return genai.Client(api_key=api_key)

    # ---------- Cached data: identical requests return instantly ----------
    @st.cache_data(show_spinner=False)
    def run_llm(api_key: str, task: str, text: str, temperature: float, max_tokens: int) -> str:
        client = get_client(api_key)
            response = client.models.generate_content(
                    model=MODEL_NAME,
                            contents=text,
                                    config=types.GenerateContentConfig(
                                                system_instruction=f"You are a text utility. Task: {task}. Return only the result in markdown.",
                                                            temperature=temperature,
                                                                        max_output_tokens=max_tokens,
                                                                                ),
                                                                                    )
                                                                                        return response.text

                                                                                        # ---------- Session state: persists across reruns ----------
                                                                                        if "history" not in st.session_state:
                                                                                            st.session_state.history = []

                                                                                            # ---------- Sidebar: configuration ----------
                                                                                            with st.sidebar:
                                                                                                st.header("⚙️ Configuration")
                                                                                                    api_key = st.text_input(
                                                                                                            "Gemini API Key", type="password", value=os.getenv("GEMINI_API_KEY", "")
                                                                                                                )
                                                                                                                    task = st.selectbox("Task", ["Summarise", "Rewrite formally", "Fix grammar", "Translate to Hindi"])
                                                                                                                        temperature = st.slider("Temperature", 0.0, 1.0, 0.3, 0.1)
                                                                                                                            max_tokens = st.slider("Max tokens", 100, 2000, 600, 100)

                                                                                                                            # ---------- Main area ----------
                                                                                                                            st.title("✍️ AI Text Utility")
                                                                                                                            st.caption("A Streamlit front end wrapped around the Gemini API.")

                                                                                                                            user_text = st.text_area("Enter your text", height=220, placeholder="Paste text here...")

                                                                                                                            if st.button("Run", type="primary"):
                                                                                                                                if not api_key:
                                                                                                                                        st.error("Please enter your Gemini API key in the sidebar.")
                                                                                                                                            elif not user_text.strip():
                                                                                                                                                    st.warning("Please enter some text.")
                                                                                                                                                        else:
                                                                                                                                                                with st.spinner("Processing..."):
                                                                                                                                                                            try:
                                                                                                                                                                                            result = run_llm(api_key, task, user_text, temperature, max_tokens)
                                                                                                                                                                                                            st.session_state.history.append((task, result))
                                                                                                                                                                                                                        except Exception as e:
                                                                                                                                                                                                                                        st.error(f"Request failed: {e}")

                                                                                                                                                                                                                                        # ---------- Output rendering ----------
                                                                                                                                                                                                                                        if st.session_state.history:
                                                                                                                                                                                                                                            st.subheader("Result")
                                                                                                                                                                                                                                                st.markdown(st.session_state.history[-1][1])
                                                                                                                                                                                                                                                    with st.expander("History"):
                                                                                                                                                                                                                                                            for t, r in reversed(st.session_state.history):
                                                                                                                                                                                                                                                                        st.markdown(f"**{t}**")
                                                                                                                                                                                                                                                                                    st.markdown(r)
                                                                                                                                                                                                                                                                                                st.divider()
                                                                                                                                                                                                                                                                                                