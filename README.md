# expt10

app.py to use the Gemini API. The UI, caching and session state are unchanged.
Updated procedure
pip install streamlit google-genai
Get a free key from Google AI Studio (aistudio.google.com).
export GEMINI_API_KEY=your_key, or paste it in the sidebar.
streamlit run app.py
What changed in the code
Import: from google import genai and from google.genai import types.
Client: genai.Client(api_key=...), still wrapped in @st.cache_resource.
Call: client.models.generate_content(model, contents, config).
Settings: temperature, max tokens and the system prompt now go through types.GenerateContentConfig.
Output: the text comes from response.text.
The model is set by MODEL_NAME = "gemini-2.5-flash" at the top of the file. If your key doesn't accept that name, change it to another Gemini model available in your AI Studio account.
In your Aim and Tools sections, replace "LLM API" with "Google Gemini API (google-genai SDK)".
