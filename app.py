import html
import json
import time
import requests
import streamlit as st

st.set_page_config(page_title="ScamShield", page_icon="🛡️")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;700&family=Space+Mono:wght@400;700&display=swap');

:root {
  --bg: #0b0b0b;
  --panel: #131313;
  --ink: #f5f5f0;
  --lime: #c6ff00;
  --pink: #ff2e63;
  --yellow: #ffd600;
  --red: #ff4d4d;
  --green: #39ff88;
  --mono: 'Space Mono', Consolas, 'Courier New', monospace;
  --sans: 'Space Grotesk', 'Segoe UI', Arial, sans-serif;
}

/* ---------- Background: dark with a faint grid ---------- */
.stApp {
  background-color: var(--bg);
  background-image:
    linear-gradient(rgba(245,245,240,0.05) 1px, transparent 1px),
    linear-gradient(90deg, rgba(245,245,240,0.05) 1px, transparent 1px);
  background-size: 40px 40px;
  font-family: var(--sans);
  color: var(--ink);
}
[data-testid="stHeader"] {background: transparent;}

/* ---------- Main block: thick border + hard shadow ---------- */
.block-container {
  max-width: 740px;
  margin-top: 2rem;
  padding: 2.4rem 2.2rem 2rem 2.2rem;
  background: var(--panel);
  border: 4px solid var(--ink);
  border-radius: 0;
  box-shadow: 12px 12px 0 var(--lime);
}

/* ---------- Title ---------- */
h1 {
  font-family: var(--sans);
  font-size: 3.8rem !important;
  font-weight: 700;
  line-height: 0.95 !important;
  text-transform: uppercase;
  letter-spacing: -2px;
  color: var(--ink);
  text-shadow: 5px 5px 0 var(--pink);
  padding-bottom: 0.4rem;
}
.sticker {
  display: inline-block;
  background: var(--yellow);
  color: #000;
  font-family: var(--mono);
  font-weight: 700;
  font-size: 0.8rem;
  letter-spacing: 1px;
  padding: 4px 10px;
  border: 3px solid #000;
  transform: rotate(-2deg);
  box-shadow: 4px 4px 0 var(--ink);
  margin: 4px 0 18px 4px;
}
.intro {
  font-family: var(--mono);
  font-size: 0.95rem;
  border-left: 6px solid var(--lime);
  padding-left: 12px;
  margin-bottom: 1.4rem;
}

/* ---------- Labels ---------- */
[data-testid="stWidgetLabel"] p {
  font-family: var(--mono);
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 1px;
  font-size: 0.85rem;
  color: var(--lime);
}

/* ---------- Inputs ---------- */
div[data-baseweb="textarea"],
div[data-baseweb="input"],
div[data-baseweb="select"] > div {
  background: #000 !important;
  border: 3px solid var(--ink) !important;
  border-radius: 0 !important;
  box-shadow: 5px 5px 0 var(--ink);
}
div[data-baseweb="textarea"]:focus-within,
div[data-baseweb="input"]:focus-within,
div[data-baseweb="select"] > div:focus-within {
  border-color: var(--lime) !important;
  box-shadow: 5px 5px 0 var(--lime);
}
div[data-baseweb="textarea"] textarea,
div[data-baseweb="input"] input {
  background: transparent !important;
  color: var(--ink) !important;
  font-family: var(--mono);
}

/* ---------- Button ---------- */
.stButton > button {
  background: var(--lime);
  border: 3px solid var(--ink);
  border-radius: 0;
  padding: 0.7rem 1.8rem;
  box-shadow: 6px 6px 0 var(--pink);
  transition: transform 0.08s ease, box-shadow 0.08s ease;
}
.stButton > button p {
  color: #000 !important;
  font-family: var(--sans);
  font-weight: 700;
  font-size: 1.05rem;
  text-transform: uppercase;
  letter-spacing: 1px;
}
.stButton > button:hover {
  background: var(--lime);
  border-color: var(--ink);
  transform: translate(-3px, -3px);
  box-shadow: 9px 9px 0 var(--pink);
}
.stButton > button:active {
  transform: translate(4px, 4px);
  box-shadow: 2px 2px 0 var(--pink);
}

/* ---------- Verdict card ---------- */
.card {
  border: 4px solid var(--ink);
  border-radius: 0;
  padding: 20px 22px;
  margin: 24px 0 18px 0;
  color: #000;
  box-shadow: 9px 9px 0 var(--ink);
}
.card .tag {
  display: inline-block;
  background: #000;
  color: var(--ink);
  font-family: var(--mono);
  font-weight: 700;
  font-size: 0.85rem;
  letter-spacing: 2px;
  padding: 4px 10px;
}
.card h3 {
  font-family: var(--sans);
  font-size: 1.7rem;
  font-weight: 700;
  line-height: 1.15;
  margin: 12px 0 10px 0;
  color: #000;
}
.card p {
  margin: 0;
  font-size: 1.02rem;
  line-height: 1.6;
  color: #000;
  font-weight: 500;
}
.high   {background: var(--red);}
.medium {background: var(--yellow);}
.low    {background: var(--green);}

/* ---------- Steps ---------- */
.steps-title {
  font-family: var(--mono);
  font-weight: 700;
  letter-spacing: 1px;
  color: var(--lime);
  margin: 6px 0 8px 0;
}
.step {
  display: flex;
  gap: 12px;
  align-items: flex-start;
  background: #000;
  border: 3px solid var(--ink);
  padding: 10px 14px;
  margin: 8px 0;
  font-size: 1rem;
  line-height: 1.5;
}
.step span {
  background: var(--lime);
  color: #000;
  font-family: var(--mono);
  font-weight: 700;
  padding: 0 9px;
  min-width: 28px;
  text-align: center;
}

/* ---------- Expander, alerts, caption ---------- */
[data-testid="stExpander"] details {
  background: #000;
  border: 3px solid var(--ink);
  border-radius: 0;
}
[data-testid="stExpander"] summary p {
  font-family: var(--mono);
  font-weight: 700;
  text-transform: uppercase;
}
[data-testid="stAlert"] {
  border: 3px solid var(--ink);
  border-radius: 0;
  box-shadow: 5px 5px 0 var(--ink);
}
[data-testid="stCaptionContainer"] {
  font-family: var(--mono);
  color: #9a9a95;
  border-top: 3px dashed #444;
  padding-top: 12px;
  margin-top: 18px;
}
</style>
""", unsafe_allow_html=True)

st.title("ScamShield")
st.markdown('<div class="sticker">AI SCAM DETECTOR</div>', unsafe_allow_html=True)
st.markdown('<div class="intro">Got a message that feels off? Paste it below. '
            'I will tell you if it looks like a scam, in plain words.</div>',
            unsafe_allow_html=True)

# ---------- API key (secrets file first, text box as backup) ----------
api_key = ""
try:
    api_key = st.secrets.get("GEMINI_API_KEY", "")
except Exception:
    pass
if not api_key:
    api_key = st.text_input("Paste your Gemini API key here", type="password")

language = st.selectbox("Explain in", ["English", "Telugu", "Hindi"])
message = st.text_area("Paste the suspicious message here", height=150)


# ---------- Quick checks ----------
def quick_checks(text):
    t = text.lower()
    notes, score = [], 0

    if "http" in t or "www." in t:
        notes.append("It contains a link.")
        score += 1
    if any(s in t for s in ["bit.ly", "tinyurl", "cutt.ly", "rb.gy", "t.co/"]):
        notes.append("The link is shortened, so you can't see where it really goes.")
        score += 2
    if any(x in t for x in [".xyz", ".top", ".click", ".buzz", ".site"]):
        notes.append("The website ends in an address often used by scammers.")
        score += 2

    pressure = [w for w in ["urgent", "immediately", "blocked", "suspended",
                            "kyc", "verify now", "last chance", "within 24 hours"]
                if w in t]
    if pressure:
        notes.append("It tries to rush you (" + ", ".join(pressure) + ").")
        score += 2

    private = [w for w in ["otp", "password", "pin", "cvv", "aadhaar", "card number"]
               if w in t]
    if private:
        notes.append("It mentions private details (" + ", ".join(private) + ").")
        score += 3

    if any(w in t for w in ["you have won", "you just won", "you won", "congratulations",
                            "lottery", "prize", "free gift", "claim your", "cash reward"]):
        notes.append("It promises a prize or free money.")
        score += 2

    # Real bank messages usually warn you NOT to share things
    if any(w in t for w in ["do not share", "don't share", "never share"]):
        score -= 3

    return notes, max(score, 0)


# ---------- Gemini call ----------
def ask_gemini(key, text, notes, lang):
    prompt = f"""You help ordinary people, including parents and grandparents,
decide whether a message is a scam. Talk like a calm, friendly person, not a robot.
Use short, simple sentences. Never say "as an AI". Never tell the user to click anything.
If the message looks genuine, say so honestly. Do not claim to be 100% sure.

Message:
\"\"\"{text}\"\"\"

Warning signs spotted by a simple checker: {notes if notes else "none"}

Reply ONLY with JSON in exactly this shape:
{{"risk": "Low" or "Medium" or "High",
  "headline": "one short sentence verdict",
  "why": "2-3 simple sentences explaining why",
  "steps": ["step 1", "step 2", "step 3"]}}

Keep the keys and the risk value in English. Write headline, why and steps in {lang}."""

    # Fastest first. If one is slow or busy, the next one is tried.
    MODELS = ["gemini-3.5-flash-lite", "gemini-3.7-flash", "gemini-3.8-flash"]

    headers = {"x-goog-api-key": key.strip(), "Content-Type": "application/json"}
    body = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": 0.3,
            "maxOutputTokens": 2048,
            "responseMimeType": "application/json",
        },
    }

    data = None
    last_problem = None
    for model in MODELS:
        url = ("https://generativelanguage.googleapis.com/v1beta/models/"
               + model + ":generateContent")
        r = None
        for attempt in range(2):
            try:
                r = requests.post(url, headers=headers, json=body, timeout=25)
            except (requests.exceptions.Timeout, requests.exceptions.ConnectionError):
                last_problem = "slow"
                r = None
                break
            last_problem = r.status_code
            if r.status_code in (500, 503):
                time.sleep(2)
                continue
            break
        if r is None or r.status_code in (404, 429, 500, 503):
            continue
        r.raise_for_status()
        data = r.json()
        break

    if data is None:
        if last_problem == "slow":
            raise ValueError("Google is replying very slowly, or your internet "
                             "is slow. Try again, or switch to a phone hotspot.")
        if last_problem in (429, 500, 503):
            raise ValueError("Gemini is very busy right now. Wait a minute "
                             "and press the button again.")
        raise ValueError("None of the model names worked. Check the current "
                         "Flash model name in Google AI Studio.")

    candidates = data.get("candidates")
    if not candidates:
        raise ValueError("Gemini gave no answer. Details: "
                         + str(data.get("promptFeedback", "unknown")))
    parts = candidates[0].get("content", {}).get("parts", [])
    raw = "".join(p.get("text", "") for p in parts).strip()
    if not raw:
        raise ValueError("Gemini sent an empty reply (reason: "
                         + str(candidates[0].get("finishReason", "unknown")) + ").")
    raw = raw.replace("```json", "").replace("```", "").strip()
    return json.loads(raw)


def esc(x):
    return html.escape(str(x))


# ---------- Button ----------
if st.button("Check this message"):
    if not message.strip():
        st.warning("Paste a message first.")
    elif not api_key.strip():
        st.warning("Paste your API key first.")
    else:
        notes, score = quick_checks(message)
        try:
            with st.spinner("Reading the message..."):
                result = ask_gemini(api_key, message, notes, language)

            risk = str(result.get("risk", "Medium")).strip().lower()
            if risk not in ("low", "medium", "high"):
                risk = "medium"
            label = {"low": "LOOKS SAFE", "medium": "BE CAREFUL",
                     "high": "LIKELY A SCAM"}[risk]

            st.markdown(
                f"""<div class="card {risk}">
                <span class="tag">{label}</span>
                <h3>{esc(result.get("headline", ""))}</h3>
                <p>{esc(result.get("why", ""))}</p></div>""",
                unsafe_allow_html=True)

            steps = result.get("steps", [])
            if steps:
                steps_html = "".join(
                    f'<div class="step"><span>{i}</span><div>{esc(s)}</div></div>'
                    for i, s in enumerate(steps, 1))
                st.markdown('<div class="steps-title">WHAT TO DO NOW</div>'
                            + steps_html, unsafe_allow_html=True)

        except requests.HTTPError as e:
            code = e.response.status_code
            if code in (400, 403):
                st.error("Gemini rejected the API key. Create a fresh key and paste it again.")
            else:
                st.error(f"Gemini error {code}.")
        except Exception as e:
            st.error("Something went wrong: " + str(e))

        with st.expander("What the quick checker noticed"):
            if notes:
                for n in notes:
                    st.write("-", n)
            else:
                st.write("Nothing obvious. The AI still read the whole message.")

st.caption("ScamShield gives guidance, not a guarantee. If you're unsure, "
           "call your bank using the number on your card.")