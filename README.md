**Intelligent-Intake-and-Expert-Matching-System**
AI-powered wellness intake and expert matching assistant prototype with conversational assessment, classification, PDF summary generation, and session booking demo. 
**AI Wellness Intake & Expert Matching Assistant — Prototype**

This repository contains a working prototype of an AI-powered wellness intake and expert matching assistant built for a B2B mental well-being platform use case (Product Manager assignment scenario).

The prototype demonstrates how AI can improve first-session match quality, reduce drop-off, and increase utilization by combining conversational intake, structured classification, expert recommendation, PDF summary generation, and session booking inside a single chat flow.

**Overview**

Users often struggle to choose the right counseling expert or support format. This AI assistant conducts a short conversational intake, understands the user’s concern, classifies severity and context, recommends the best-fit expert type, and converts intent into session booking — while generating a structured intake summary for expert preparation.

**Flow:**

User → AI intake chat → need classification → expert recommendation → PDF intake summary → session booking

## Features

- Conversational AI intake (LLM-powered)
- Adaptive question flow
- Issue and severity classification
- Expert and counseling format recommendation
- Structured intake summary output
- PDF intake report download
- AI-assisted booking flow with slot selection
- Streamlit chat interface
- Groq LLM API integration

  
## Tech Stack

- Python
- Streamlit
- Groq LLM API
- python-dotenv
- ReportLab (PDF generation)

## Project Structure


## Setup Instructions

Follow these steps to run the prototype locally.


### Step 1 — Clone Repository

```bash
git clone <your-repo-url>
cd <repo-folder>
```
**Step 2- Create Virtual environment**

```
python -m venv venv

```
for windows: 
```
venv\Scripts\activate
```
mac/linux
```
source venv/bin/activate

```
### Step 3 - Install Dependencies
```
pip install -r requirements.txt
```
### Step 4- Get Groq API Key (Free)
```
Go to https://console.groq.com/
Create a free account
Generate an API key
```
****Step 5 — Create Environment File**
```
Create a file named .env in the project root folder and add:
GROQ_API_KEY=your_groq_api_key_here
```
Example:
```
GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxx
```
****Step 6 — Run the Application**
```
streamlit run chatbot.py



