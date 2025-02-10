import json
import asyncio
import imaplib
import smtplib
import email
import time
from email.header import decode_header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
from aineta.openai_service import analyze_with_openai
from aineta.utils import get_message_content, save_to_conversation_history

async def check_and_respond_to_emails(mailbox):
    try:
        mail = imaplib.IMAP4_SSL(mailbox["IMAP_SERVER"], mailbox["IMAP_PORT"])
        mail.login(mailbox["EMAIL_ACCOUNT"], mailbox["EMAIL_PASSWORD"])
        mail.select('inbox')
        
        status, messages = mail.search(None, 'UNSEEN')
        
        for msg_id in messages[0].split():
            status, msg_data = mail.fetch(msg_id, '(RFC822)')
            email_msg = email.message_from_bytes(msg_data[0][1])
            
            from_email = email_msg['from']
            if '<' in from_email:
                from_email = from_email.split('<')[1].strip('>')
            mail_prompt = mailbox["EMAIL_ACCOUNT"]
            received_msg = {
                "subject": email_msg["Subject"],
                "content": get_message_content(email_msg)
            }
            
            save_to_conversation_history(mail_prompt, from_email, received_msg, "received")
            
            response = analyze_with_openai(received_msg["content"], mail_prompt)
            sent_msg = {
                "subject": f"Re: {received_msg['subject']}",
                "content": response
            }
            
            save_to_conversation_history(mail_prompt, from_email, sent_msg, "sent")
            send_email_response(mailbox, from_email, sent_msg["subject"], response)
            
        mail.logout()
        
    except Exception as e:
        print(f"Error checking emails for {mailbox['EMAIL_ACCOUNT']}: {e}")

def send_email_response(mailbox, to_email, subject, response_message):
    try:
        msg = MIMEMultipart()
        msg['From'] = mailbox["EMAIL_ACCOUNT"]
        msg['To'] = to_email
        msg['Subject'] = f"Re: {subject}"

        msg.attach(MIMEText(response_message, 'plain', 'utf-8'))

        with smtplib.SMTP(mailbox["SMTP_SERVER"], mailbox["SMTP_PORT"]) as server:
            server.starttls()
            server.login(mailbox["EMAIL_ACCOUNT"], mailbox["EMAIL_PASSWORD"])
            server.send_message(msg)

        print(f"Response sent to {to_email} from {mailbox['EMAIL_ACCOUNT']}")

    except Exception as e:
        print(f"Error sending email from {mailbox['EMAIL_ACCOUNT']}: {e}")

async def periodic_email_check(mailboxes):
    while True:
        tasks = [check_and_respond_to_emails(mailbox) for mailbox in mailboxes]
        await asyncio.gather(*tasks)
        await asyncio.sleep(10)  # Check every 10 seconds

def get_conversations():
    conversations = {}
    try:
        for mailbox in MAILBOXES:
            mail = imaplib.IMAP4_SSL(mailbox["IMAP_SERVER"], mailbox["IMAP_PORT"])
            mail.login(mailbox["EMAIL_ACCOUNT"], mailbox["EMAIL_PASSWORD"])
            mail.select("inbox")

            status, messages = mail.search(None, "ALL")

            for msg_id in messages[0].split():
                status, msg_data = mail.fetch(msg_id, "(RFC822)")
                for response_part in msg_data:
                    if isinstance(response_part, tuple):
                        msg = email.message_from_bytes(response_part[1])
                        from_email = msg["From"]
                        subject = msg["Subject"]
                        body = get_message_content(msg)

                        if from_email not in conversations:
                            conversations[from_email] = []

                        conversations[from_email].append({
                            "subject": subject,
                            "received": body,
                            "sent": "Response placeholder"
                        })

            mail.logout()
        return conversations

    except Exception as e:
        print("Error:", e)
        return {}
