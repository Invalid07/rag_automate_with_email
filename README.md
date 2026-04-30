# RAG Automate with Email

A knowledge-based RAG (Retrieval-Augmented Generation) system that reads your folder structure, provides intelligent solutions, and offers email integration for seamless communication.

## 🎯 Overview

This project implements a Retrieval-Augmented Generation (RAG) system that:
- Reads and indexes documents from your local folder
- Provides intelligent answers based on your knowledge base
- Generates multiple solution options
- Sends results via email automatically

## 🚀 Features

- **Knowledge Base Indexing**: Automatically reads and processes documents from your folder
- **RAG-powered Answers**: Leverages LLMs to provide accurate, context-aware solutions
- **Multiple Options**: Generates multiple solution alternatives for user queries
- **Email Integration**: Send results and recommendations directly to email addresses
- **Easy Configuration**: Simple setup with intuitive configuration options

## 📋 Requirements

- Python 3.8+
- Dependencies listed in `requirements.txt`

## 🛠️ Installation

1. Clone the repository:
```bash
git clone https://github.com/Invalid07/rag_automate_with_email.git
cd rag_automate_with_email
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure your settings:
   - Set up your knowledge base folder path
   - Configure email credentials (SMTP settings)
   - Set LLM API keys if needed

## 📖 Usage

```python
# Example usage
from rag_automate import RAGAutomation

# Initialize the system
rag = RAGAutomation(knowledge_base_path="./documents")

# Query the knowledge base
results = rag.query("Your question here")

# Get multiple options
options = rag.get_multiple_options("Your question here")

# Send results via email
rag.send_email_results(email="user@example.com", results=results)
```

## 🔧 Configuration

Create a `.env` file in the project root with:
```
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
EMAIL_ADDRESS=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
LLM_API_KEY=your_api_key
```

## 📁 Project Structure

```
rag_automate_with_email/
├── .gitignore                
├── .env.example               
├── README.md
├── requirements.txt
├── email_config.py
├── gmail_tool.py
├── main.py
├── main1.py
├── prompt.py
├── credentials.json.example   
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is open source and available under the MIT License.

## 📧 Contact & Support

For questions or support, please open an issue on GitHub or contact the maintainer.

---

**Built with ❤️ by Invalid07**
