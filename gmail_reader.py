import os
import base64
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

def get_gmail_service():
    print("🔑 Setting up Gmail connection...")
    SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
    creds = None
    token_path = 'token.json'
    
    if os.path.exists(token_path):
        print("✅ Found existing token.json")
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)
    
    if not creds or not creds.valid:
        print("🔄 Getting new access...")
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        with open(token_path, 'w') as token:
            token.write(creds.to_json())
        print("✅ Token saved!")
    
    service = build('gmail', 'v1', credentials=creds)
    print("✅ Successfully connected to Gmail!")
    return service


def get_recent_emails(max_results=5):
    print(f"📬 Fetching your last {max_results} emails...")
    service = get_gmail_service()
    
    results = service.users().messages().list(userId='me', maxResults=max_results).execute()
    messages = results.get('messages', [])
    print(f"Found {len(messages)} messages in inbox.")
    
    emails = []
    
    for i, msg in enumerate(messages, 1):
        print(f"   Reading email {i} of {len(messages)}...")
        try:
            msg_data = service.users().messages().get(userId='me', id=msg['id'], format='full').execute()
            
            headers = msg_data['payload']['headers']
            subject = next((h['value'] for h in headers if h['name'].lower() == 'subject'), 'No Subject')
            sender = next((h['value'] for h in headers if h['name'].lower() == 'from'), 'Unknown')
            
            # Simplified & safer body extraction
            body = "No readable body"
            try:
                payload = msg_data['payload']
                if 'parts' in payload:
                    for part in payload['parts']:
                        if part['mimeType'] == 'text/plain':
                            data = part['body'].get('data', '')
                            if data:
                                body = base64.urlsafe_b64decode(data).decode('utf-8')
                                break
                else:
                    data = payload['body'].get('data', '')
                    if data:
                        body = base64.urlsafe_b64decode(data).decode('utf-8')
            except:
                pass
            
            emails.append({
                'from': sender,
                'subject': subject,
                'body': body[:600]
            })
            print(f"   ✅ Email {i} processed successfully")
            
        except Exception as e:
            print(f"   ❌ Error reading email {i}: {e}")
            emails.append({
                'from': sender if 'sender' in locals() else 'Unknown',
                'subject': subject if 'subject' in locals() else 'Error',
                'body': 'Could not read this email'
            })
    
    return emails


# Main Test
if __name__ == "__main__":
    print("🚀 Starting Gmail Reader...\n")
    emails = get_recent_emails(max_results=5)
    
    print(f"\n✅ Successfully fetched {len(emails)} emails!\n")
    for i, email in enumerate(emails, 1):
        print(f"Email {i}:")
        print(f"FROM    : {email['from']}")
        print(f"SUBJECT : {email['subject']}")
        print(f"BODY    : {email['body'][:150]}...\n")
        print("-" * 70)