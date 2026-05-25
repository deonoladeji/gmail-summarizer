from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Your email inbox — a list of dictionaries
emails = [
    {
        "sender": "Mascot",
        "subject": "The $4m Deal",
        "body": "Dear Oladeji, following up on our $4m deal. Budget finalized at $2.7m. Need your approval by Friday. Please confirm Monday 10am meeting."
    },
    {
        "sender": "Bank Manager",
        "subject": "Account Alert",
        "body": "Dear Oladeji, your account has been credited with 500,000 Naira from Zenith Traders. Your new balance is 1,250,000 Naira. Transaction ID: ZB2024091."
    },
    {
        "sender": "Landlord",
        "subject": "Rent Reminder",
        "body": "Dear Oladeji, this is a reminder that your rent of 800,000 Naira is due on the 1st of next month. Kindly ensure payment is made on time to avoid penalties."
    }
]

def summarize_email(email):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are an assistant that summarizes emails in 1 clear sentence. Be direct and include any key numbers or dates."
                },
                {
                    "role": "user", 
                    "content": "Summarize this email: " + email["body"]
                }
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"[Error summarizing this email: {str(e)}]"

# Loop through every email and summarize automatically
from datetime import datetime

today = datetime.now().strftime("%A, %B %d %Y")

print("\n")
print("=" * 60)
print(f"   YOUR MORNING EMAIL BRIEFING — {today}")
print("=" * 60)

for i, email in enumerate(emails):
    print(f"\n  📧 Email {i+1} of {len(emails)}")
    print(f"  FROM    : {email['sender']}")
    print(f"  SUBJECT : {email['subject']}")
    print(f"  SUMMARY : {summarize_email(email)}")
    print("  " + "-" * 56)

print("\n✅ Briefing complete. Have a productive day, Oladeji!\n")


# Save briefing to a file
filename = f"briefing_{datetime.now().strftime('%Y-%m-%d')}.txt"

with open(filename, "w") as f:
    f.write(f"MORNING EMAIL BRIEFING — {today}\n")
    f.write("=" * 60 + "\n\n")
    for i, email in enumerate(emails):
        f.write(f"Email {i+1}: FROM {email['sender']}\n")
        f.write(f"SUBJECT: {email['subject']}\n")
        f.write(f"SUMMARY: {summarize_email(email)}\n")
        f.write("-" * 56 + "\n\n")

print(f"📁 Briefing saved to: {filename}")