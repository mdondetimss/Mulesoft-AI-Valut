import os
import streamlit as st
import requests
import json
from dotenv import load_dotenv

load_dotenv()

MULE_API_URL = os.getenv("MULE_API_URL")
TEMPLATE_FILE = "Jira_Issue.json"
def load_payload_template():
    with open(TEMPLATE_FILE, "r") as f:
        return f.read()


def build_payload(template_str, variables):
    payload_str = template_str
    for key, value in variables.items():
        payload_str = payload_str.replace(f"{{{{{key}}}}}", value)
    return json.loads(payload_str)


st.set_page_config(page_title="Jira AI Analyzer", layout="centered")
st.title("Jira AI Analyzer")

# UI Inputs (dynamic values)
issue_id = st.text_input("Issue ID")
description = st.text_input("Description")
summary = st.text_area("Summary")

if st.button("Analyze with AI"):
    try:
        template = load_payload_template()

        variables = {
            "issue_id": issue_id,
            "description": description,
            "summary": summary
        }

        payload = build_payload(template, variables)

        # st.subheader("Payload Sent to Mule")
        # st.json(payload)

        response = requests.post(MULE_API_URL, json=payload, timeout=10)

        if response.status_code != 200:
            st.error(f"Mule Error: {response.status_code}")
            st.text(response.text)
            st.stop
        
        raw_body = response.text.lower().strip()

        if raw_body == "synched":
            st.warning("This issue was already processed. AI flow was skipped.")
            # st.subheader("Synced Payload")
            # st.json(payload)
            st.stop()

        if response.status_code == 200:
            data = response.json()

            ai_summary = (
                data["fields"]["customfield_10038"]
                ["content"][0]["content"][0]["text"]
            )

            ai_sentiment = data["fields"]["customfield_10039"]

            st.subheader("AI Summary")
            st.write(ai_summary)

            st.subheader("AI Sentiment")
            st.write(ai_sentiment)

        else:
            st.error(f"Mule API Error: {response.status_code}")
            st.text(response.text)

    except Exception as e:
        st.error(f"Error: {e}")