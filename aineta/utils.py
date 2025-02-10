import json
import chardet
import re
from datetime import datetime
from email.header import decode_header

def load_mailboxes(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

def decode_content(content, charset=None):
    if not content:
        return ""
        
    encodings = [
        charset,
        'utf-8',
        'latin1',
        'iso-8859-1',
        'cp1252',
        None
    ]
    
    for encoding in encodings:
        try:
            if encoding is None:
                detected = chardet.detect(content)
                if detected['encoding']:
                    return content.decode(detected['encoding'])
            elif encoding:
                return content.decode(encoding)
        except Exception as e:
            continue
            
    return "Unable to decode message content"

def clean_email_content(content):
    content = re.sub(r'<script.*?>.*?</script>', '', content, flags=re.IGNORECASE)
    content = re.sub(r'<.*?>', '', content)
    content = content.split("\r\n\r\n", 1)[0]
    return content

def get_message_content(msg):
    try:
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    content = part.get_payload(decode=True)
                    charset = part.get_content_charset()
                    return clean_email_content(decode_content(content, charset))
        else:
            content = msg.get_payload(decode=True)
            charset = msg.get_content_charset()
            return clean_email_content(decode_content(content, charset))
    except Exception as e:
        print(f"Error getting message content: {e}")
        return ""

def decode_email_subject(subject):
    if not subject:
        return ""
        
    try:
        decoded_parts = decode_header(subject)
        decoded_subject = ""
        
        for part, charset in decoded_parts:
            if isinstance(part, bytes):
                if charset:
                    decoded_subject += part.decode(charset)
                else:
                    for encoding in ['utf-8', 'latin1', 'iso-8859-2']:
                        try:
                            decoded_subject += part.decode(encoding)
                            break
                        except:
                            continue
            else:
                decoded_subject += str(part)
                
        decoded_subject = re.sub(r'\r\n\s*', ' ', decoded_subject)
        decoded_subject = re.sub(r'\s+', ' ', decoded_subject)
        
        return decoded_subject.strip()
        
    except Exception as e:
        print(f"Error decoding subject: {e}")
        return subject

def save_to_conversation_history(mail_prompt, email_to, message, msg_type):
    filepath = 'conversation_history.json'
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {}
    except json.JSONDecodeError:
        data = {}

    if mail_prompt not in data:
        data[mail_prompt] = {}
    
    if email_to not in data[mail_prompt]:
        data[mail_prompt][email_to] = {
            "received": [],
            "sent": []
        }
    
    clean_subject = decode_email_subject(message.get("subject", ""))
    
    data[mail_prompt][email_to][msg_type].append({
        "timestamp": timestamp,
        "subject": clean_subject,
        "content": message.get("content", "")
    })

    

    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"The error while saving to the conversation history: {e}")

def clean_message_content(content):
    if not content:
        return ""
    content = re.sub(r'http\S+', '', content)
    content = re.sub(r'(?i)(napisał:|wrote:)', '', content)
    content = re.sub(r'\s+', ' ', content)
    return content.strip()

