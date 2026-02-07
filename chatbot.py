import streamlit as st
import os
from groq import Groq
from dotenv import load_dotenv
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO

# -------------------------
# ENV + CLIENT
# -------------------------
load_dotenv(override=True)
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# -------------------------
# PAGE CONFIG
# -------------------------
st.set_page_config(page_title="AI Wellness Intake Assistant")

st.title("AI Wellness Intake Assistant")
st.write("I will help match you with the right counseling expert in ~2 minutes.")

# -------------------------
# STATE
# -------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "final_classification" not in st.session_state:
    st.session_state.final_classification = None

if "booking_started" not in st.session_state:
    st.session_state.booking_started = False

# -------------------------
# SYSTEM PROMPT
# -------------------------
SYSTEM_PROMPT = """
You are a mental wellness intake assistant.

Rules:
- Ask one question at a time
- Keep questions short
- Be supportive and neutral
- Collect: issue, severity, duration, context, preference

After enough info, output structured classification.

Return EXACTLY in this format:

ISSUE_CLUSTER:
SEVERITY: (low/medium/high)
CONTEXT: (work/personal/both)
PREFERRED_STYLE:
RECOMMENDED_EXPERT:
RECOMMENDED_FORMAT:
URGENCY_LEVEL:
SUMMARY:

Do not output this until enough info is collected.
"""

# -------------------------
# LLM CALL
# -------------------------
def call_llm(messages):
    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=messages,
        temperature=0.3,
    )
    return completion.choices[0].message.content

# -------------------------
# PDF BUILDER
# -------------------------
def create_pdf(text):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)

    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, 770, "Wellness Intake Summary")

    c.setFont("Helvetica", 11)

    y = 740
    for line in text.split("\n"):
        if y < 60:
            c.showPage()
            c.setFont("Helvetica", 11)
            y = 750
        c.drawString(50, y, line)
        y -= 18

    c.save()
    buffer.seek(0)
    return buffer

# -------------------------
# DEMO SLOT DATA
# -------------------------
SLOTS = [
    "Tomorrow — 10:00 AM",
    "Tomorrow — 2:30 PM",
    "Friday — 11:00 AM",
    "Friday — 4:00 PM"
]

# -------------------------
# DISPLAY CHAT HISTORY
# -------------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# -------------------------
# FIRST MESSAGE
# -------------------------
if not st.session_state.messages:
    first = "Hi — what brings you here today?"
    st.session_state.messages.append({"role": "assistant", "content": first})
    with st.chat_message("assistant"):
        st.markdown(first)

# -------------------------
# CHAT INPUT
# -------------------------
if prompt := st.chat_input("Type your answer..."):

    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    llm_messages = [{"role": "system", "content": SYSTEM_PROMPT}] + st.session_state.messages

    reply = call_llm(llm_messages)

    st.session_state.messages.append({"role": "assistant", "content": reply})

    with st.chat_message("assistant"):
        st.markdown(reply)

    # -------------------------
    # DETECT FINAL CLASSIFICATION
    # -------------------------
    if "ISSUE_CLUSTER:" in reply:
        st.session_state.final_classification = reply

# -------------------------
# POST-CLASSIFICATION FEATURES
# -------------------------
if st.session_state.final_classification:

    st.divider()
    st.subheader("Assessment Complete")

    # ---- PDF DOWNLOAD ----
    pdf_buffer = create_pdf(st.session_state.final_classification)

    st.download_button(
        label="Download Intake Summary PDF",
        data=pdf_buffer,
        file_name="wellness_intake_summary.pdf",
        mime="application/pdf"
    )

    # ---- BOOKING AGENT ----
    st.subheader("AI Booking Assistant")

    if not st.session_state.booking_started:
        if st.button("Book Session with Recommended Expert"):
            st.session_state.booking_started = True

    if st.session_state.booking_started:
        slot = st.selectbox("Choose available slot", SLOTS)

        if st.button("Confirm Booking"):
            st.success(f"Session booked for {slot}")
            st.info("A confirmation summary has been generated for the expert.")

