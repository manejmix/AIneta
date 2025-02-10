# aineta - AI Email Response Automation System


## Polski

### Przegląd
aineta to zautomatyzowany system przetwarzania e-maili, który wykorzystuje AI do analizy i odpowiadania na przychodzące wiadomości. System okresowo sprawdza skonfigurowane konta e-mail, generuje odpowiedzi kontekstowe za pomocą OpenAI API i utrzymuje historię konwersacji.

### Kluczowe funkcje
- 🕵️ Automatyczne sprawdzanie e-maili za pomocą IMAP
- 🤖 Generowanie odpowiedzi AI z wykorzystaniem GPT-4
- 📨 Automatyczne odpowiedzi na e-maile za pomocą SMTP
- 📊 Śledzenie historii konwersacji
- ⚙️ Obsługa wielu skrzynek pocztowych

### Instalacja
1. Sklonuj repozytorium
```bash
git clone https://github.com/yourusername/aineta.git
cd aineta
```
2. Zainstaluj zależności
```bash
pip install -r requirements.txt
```
3. Skonfiguruj zmienne środowiskowe (.env file):
```ini
OPENAI_API_KEY=your_openai_api_key
OPENAI_API_URL=https://api.openai.com/v1/chat/completions
```
4. Skonfiguruj skrzynki pocztowe w `mailboxes.json`:
```json
[
  {
    "EMAIL_ACCOUNT": "your.email@example.com",
    "EMAIL_PASSWORD": "app-specific-password",
    "IMAP_SERVER": "imap.example.com",
    "IMAP_PORT": 993,
    "SMTP_SERVER": "smtp.example.com",
    "SMTP_PORT": 587,
    "PROMPT": "Jesteś pomocnym asystentem AI odpowiadającym na e-maile klientów..."
  }
]
```

### Użytkowanie
Uruchom serwis:
```bash
uvicorn main:app --reload
```
Rozpocznij przetwarzanie e-maili:
```bash
curl http://localhost:8000/start-email-check
```


### Struktura projektu
```
aineta/
├── email_service.py    # Logika przetwarzania e-maili
├── openai_service.py   # Integracja z API OpenAI
└── utils.py            # Funkcje pomocnicze

main.py                 # Serwer FastAPI
mailboxes.json          # Konfiguracja kont e-mail
requirements.txt        # Zależności Pythona
```

### Współtworzenie
Zachęcamy do zgłaszania pull requestów i otwierania issue, aby omówić proponowane zmiany.

### Licencja
Licencja MIT



## English

### Overview
aineta is an automated email processing system that uses AI to analyze and respond to incoming emails. The system periodically checks configured email accounts, generates context-aware responses using OpenAI's API, and maintains a conversation history.

### Key Features
- 🕵️ Automated email checking via IMAP
- 🤖 AI-powered response generation using GPT-4
- 📨 Automatic email responses via SMTP
- 📊 Conversation history tracking
- 
- ⚙️ Multiple mailbox configuration support

### Installation
1. Clone the repository
```bash
git clone https://github.com/yourusername/aineta.git
cd aineta
```
2. Install dependencies
```bash
pip install -r requirements.txt
```
3. Configure environment variables (.env file):
```ini
OPENAI_API_KEY=your_openai_api_key
OPENAI_API_URL=https://api.openai.com/v1/chat/completions
```
4. Configure mailboxes in `mailboxes.json`:
```json
[
  {
    "EMAIL_ACCOUNT": "your.email@example.com",
    "EMAIL_PASSWORD": "app-specific-password",
    "IMAP_SERVER": "imap.example.com",
    "IMAP_PORT": 993,
    "SMTP_SERVER": "smtp.example.com",
    "SMTP_PORT": 587,
    "PROMPT": "You are a helpful AI assistant responding to customer emails..."
  }
]
```

### Usage
Start the service:
```bash
uvicorn main:app --reload
```
Start email processing:
```bash
curl http://localhost:8000/start-email-check
```



### Project Structure
```
aineta/
├── email_service.py    # Email processing core logic
├── openai_service.py   # OpenAI API integration
└── utils.py            # Helper functions

main.py                 # FastAPI web server
mailboxes.json          # Email account configurations
requirements.txt        # Python dependencies
```

### Contributing
Contributions are welcome! Please open an issue first to discuss proposed changes.

### License
MIT License

---



