# 🤖 Simple RAG Chat

A beautiful React-based chat interface for your RAG (Retrieval-Augmented Generation) system powered by ChromaDB, Gemini embeddings, and FastAPI.

## ✨ Features

- **Beautiful Chat UI**: Modern, responsive React interface with chat history
- **RAG Integration**: Uses ChromaDB for vector storage and Gemini for embeddings
- **Real-time Chat**: Ask questions and get AI-powered answers from your documents
- **Document Indexing**: Automatically processes `.txt` files from `my_data/` folder
- **Error Handling**: Graceful error handling and loading states
- **Mobile Responsive**: Works great on desktop and mobile devices

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- Node.js 18+ (for React development)
- A Gemini API key

### 1. Setup Environment

```bash
# Clone or navigate to the project directory
cd "simple rag"

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install Python dependencies
pip install -r requirements.txt

# Set up your Gemini API key
echo "GEMINI_API_KEY=your_actual_api_key_here" > .env
```

### 2. Add Your Documents

Place your `.txt` files in the `my_data/` folder. The system will automatically index them.

### 3. Start the Application

**Option A: Use the startup script (recommended)**
```bash
./start.sh
```

**Option B: Manual startup**

Terminal 1 (Backend):
```bash
source .venv/bin/activate
uvicorn api:app --host 127.0.0.1 --port 8000
```

Terminal 2 (Frontend):
```bash
cd ui
npm install
npm run dev -- --host 127.0.0.1 --port 5173
```

### 4. Open the App

Visit [http://127.0.0.1:5173](http://127.0.0.1:5173) in your browser.

## 📁 Project Structure

```
simple rag/
├── api.py                 # FastAPI server with /ask endpoint
├── rag_core.py           # Core RAG logic and ChromaDB integration
├── rag.py                # CLI interface (original script)
├── requirements.txt      # Python dependencies
├── start.sh              # Startup script for both servers
├── .env                  # Environment variables (create this)
├── my_data/              # Your documents go here
│   ├── doc.txt
│   └── mamun.txt
└── ui/                   # React frontend
    ├── src/
    │   ├── App.jsx       # Main chat component
    │   ├── App.css       # Beautiful styling
    │   └── index.css     # Base styles
    └── package.json
```

## 🔧 API Endpoints

- `POST /ask` - Ask a question and get an AI-generated answer
  ```json
  {
    "question": "Tell me about Samrat",
    "top_k": 5
  }
  ```
- `GET /docs` - Interactive API documentation

## 🎨 UI Features

- **Chat History**: See all your previous questions and answers
- **Loading States**: Visual feedback while processing
- **Error Handling**: Clear error messages if something goes wrong
- **Responsive Design**: Works on all screen sizes
- **Clear History**: Reset the conversation anytime

## 🛠️ Development

### Backend Development
```bash
source .venv/bin/activate
uvicorn api:app --host 127.0.0.1 --port 8000 --reload
```

### Frontend Development
```bash
cd ui
npm run dev
```

### Adding New Documents
Just add `.txt` files to the `my_data/` folder and restart the backend. The system will automatically re-index if the collection is empty.

## 🔍 How It Works

1. **Document Processing**: Text files are chunked and embedded using Gemini's text-embedding-004 model
2. **Vector Storage**: Embeddings are stored in ChromaDB for fast similarity search
3. **Query Processing**: User questions are embedded and matched against stored chunks
4. **Answer Generation**: Relevant context is sent to Gemini 1.5 Flash for answer generation
5. **Response Display**: Answers are displayed in the beautiful chat interface

## 🐛 Troubleshooting

### Node.js Version Issues
If you get Node.js version errors, the project uses Vite 4.5.3 which is compatible with Node 18+.

### API Connection Issues
Make sure both servers are running:
- Backend: http://127.0.0.1:8000
- Frontend: http://127.0.0.1:5173

### Missing Dependencies
```bash
# Backend
pip install -r requirements.txt

# Frontend
cd ui && npm install
```

## 📝 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Feel free to submit issues and enhancement requests!
