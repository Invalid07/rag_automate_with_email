# 📚 RAG App with grokApi + Gmail

A Retrieval-Augmented Generation (RAG) app that lets you ask questions about any `.txt` file using OpenAI, and optionally email the answer via Gmail.

---

## 📁 Project Structure

```
rag_project/
├── main1.py            # Main app
├── gmail_tool.py      # Gmail OAuth2 helper
├── requirements.txt   # Dependencies
├── .env.example       # Rename to .env and fill in your keys
├── .gitignore         # Keeps secrets out of Git
└── README.md          # This file
```

---

## ⚙️ Setup

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Set up your `.env` file
```bash
cp .env.example .env
```
Then edit `.env` and add your real keys.

### 3. Set up Gmail OAuth2
- Go to [Google Cloud Console](https://console.cloud.google.com)
- Create a project → Enable **Gmail API**
- Create **OAuth 2.0 credentials** (Desktop App)
- Download `credentials.json` and place it in this folder
- OAuth2 it not working properly so i move only with smpt

### 4. Run the app
```bash
python main.py
```

---

## 🔄 How It Works

1. 📂 **Pick a `.txt` file** via file dialog
2. 📄 **Splits** the file into chunks
3. 🔢 **Embeds** chunks using OpenAI `text-embedding-3-small`
4. 🗃️ **Stores** vectors in ChromaDB
5. 💬 **Ask a question** — GPT-4o-mini answers using your file
6. 📧 **Optionally email** the answer via Gmail

---

## 🔐 Security Notes

- **Never share your `.env` file or API keys**
- `token.json` and `credentials.json` are also secrets — keep them local
- All secret files are listed in `.gitignore`
