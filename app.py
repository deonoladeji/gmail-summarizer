import streamlit as st
from datetime import date
from gmail_reader import get_recent_emails
import openai
from dotenv import load_dotenv
import os

load_dotenv()
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.set_page_config(page_title="Gmail Summarizer", page_icon="📧")
st.title("📧 Gmail Email Summarizer")
st.markdown("---")

num_emails = st.slider("How many emails do you want to fetch?", min_value=3, max_value=15, value=5)

if st.button("🔍 Fetch & Summarize My Emails"):
    with st.spinner("Connecting to Gmail and reading your emails..."):
        emails = get_recent_emails(max_results=num_emails)

    if not emails:
        st.error("No emails found. Check your Gmail connection.")
    else:
        st.success(f"✅ Successfully fetched {len(emails)} emails!")
        st.markdown("---")

        briefing_lines = []
        briefing_lines.append(f"YOUR MORNING EMAIL BRIEFING — {date.today().strftime('%A, %B %d %Y')}")
        briefing_lines.append("=" * 60)

        for i, email in enumerate(emails, 1):
            with st.expander(f"📩 Email {i} — {email['subject']} (from {email['from']})"):
                st.markdown(f"**From:** {email['from']}")
                st.markdown(f"**Subject:** {email['subject']}")
                st.markdown(f"**Body Preview:**")
                st.text(email['body'][:300])

                with st.spinner("Generating AI summary..."):
                    response = client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[
                            {"role": "system", "content": "Summarize this email in one clear sentence."},
                            {"role": "user", "content": email['body']}
                        ]
                    )
                    summary = response.choices[0].message.content

                st.info(f"🤖 AI Summary: {summary}")

                briefing_lines.append(f"\nEmail {i} of {len(emails)}")
                briefing_lines.append(f"FROM    : {email['from']}")
                briefing_lines.append(f"SUBJECT : {email['subject']}")
                briefing_lines.append(f"SUMMARY : {summary}")
                briefing_lines.append("-" * 60)

        filename = f"briefing_{date.today()}.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write("\n".join(briefing_lines))

        st.markdown("---")
        st.success(f"💾 Briefing saved to {filename}")