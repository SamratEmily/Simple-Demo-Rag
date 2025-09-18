import { useState } from 'react'
import './App.css'

function App() {
  const [question, setQuestion] = useState('')
  const [answer, setAnswer] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [history, setHistory] = useState([])

  async function askApi(e) {
    e.preventDefault()
    setError('')
    setAnswer('')
    const q = question.trim()
    if (!q) return
    setLoading(true)
    
    // Add question to history
    const newEntry = { question: q, answer: '', loading: true, timestamp: new Date() }
    setHistory(prev => [...prev, newEntry])
    
    try {
      const res = await fetch('http://127.0.0.1:8000/ask', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question: q })
      })
      if (!res.ok) {
        throw new Error(`HTTP ${res.status}: ${res.statusText}`)
      }
      const data = await res.json()
      const finalAnswer = data.answer || 'No answer received'
      
      // Update the last entry with the answer
      setHistory(prev => prev.map((entry, index) => 
        index === prev.length - 1 
          ? { ...entry, answer: finalAnswer, loading: false }
          : entry
      ))
      setAnswer(finalAnswer)
    } catch (err) {
      const errorMsg = err.message || 'Request failed'
      setError(errorMsg)
      
      // Update the last entry with error
      setHistory(prev => prev.map((entry, index) => 
        index === prev.length - 1 
          ? { ...entry, answer: `Error: ${errorMsg}`, loading: false, error: true }
          : entry
      ))
    } finally {
      setLoading(false)
    }
  }

  const clearHistory = () => {
    setHistory([])
    setAnswer('')
    setError('')
  }

  return (
    <div className="app">
      <header className="header">
        <h1>🤖 Simple RAG Chat</h1>
        <p>Ask questions about your documents using AI-powered retrieval</p>
      </header>

      <div className="chat-container">
        <div className="chat-history">
          {history.length === 0 ? (
            <div className="empty-state">
              <p>👋 Welcome! Ask me anything about your documents.</p>
              <p>Try: "Tell me about Samrat" or "What do you know about Mamun?"</p>
            </div>
          ) : (
            history.map((entry, index) => (
              <div key={index} className="chat-entry">
                <div className="question">
                  <strong>You:</strong> {entry.question}
                </div>
                <div className={`answer ${entry.error ? 'error' : ''}`}>
                  <strong>Assistant:</strong> {
                    entry.loading ? (
                      <span className="loading">Thinking...</span>
                    ) : (
                      entry.answer
                    )
                  }
                </div>
              </div>
            ))
          )}
        </div>

        <form onSubmit={askApi} className="input-form">
          <div className="input-group">
            <input
              type="text"
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              placeholder="Ask a question about your documents..."
              disabled={loading}
              className="question-input"
            />
            <button 
              type="submit" 
              disabled={loading || !question.trim()} 
              className="ask-button"
            >
              {loading ? '⏳' : '🚀'}
            </button>
          </div>
        </form>

        {history.length > 0 && (
          <button onClick={clearHistory} className="clear-button">
            Clear History
          </button>
        )}
      </div>
    </div>
  )
}

export default App
