'use client'

import { useState, useRef, useEffect } from 'react'
import { Send, Loader2, User, Bot, AlertCircle } from 'lucide-react'
import axios from 'axios'
import ReactMarkdown from 'react-markdown'

interface Message {
  id: string
  content: string
  role: 'user' | 'assistant' | 'loading'
  sources?: string[]
  timestamp: Date
}

export default function ChatInterface() {
  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!input.trim() || isLoading) return

    const userMessage: Message = {
      id: Date.now().toString(),
      content: input,
      role: 'user',
      timestamp: new Date(),
    }

    setMessages(prev => [...prev, userMessage])
    setInput('')
    setIsLoading(true)
    setError(null)

    try {
      const response = await axios.post('/api/chat', {
        message: input,
      })

      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        content: response.data.response,
        role: 'assistant',
        sources: response.data.sources,
        timestamp: new Date(),
      }

      setMessages(prev => [...prev, assistantMessage])
    } catch (err) {
      console.error('Error:', err)
      setError('Failed to get response. Please try again.')
      
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        content: 'Sorry, I encountered an error while processing your request. Please try again.',
        role: 'assistant',
        timestamp: new Date(),
      }
      
      setMessages(prev => [...prev, errorMessage])
    } finally {
      setIsLoading(false)
    }
  }

  const exampleQuestions = [
    "Is turmeric effective for reducing inflammation?",
    "What are the benefits of omega-3 supplements?",
    "Are probiotics good for digestive health?",
    "Does green tea extract help with weight loss?",
  ]

  const handleExampleClick = (question: string) => {
    setInput(question)
  }

  return (
    <div className="bg-white rounded-lg shadow-lg overflow-hidden">
      {/* Messages Area */}
      <div className="h-96 overflow-y-auto p-4 space-y-4">
        {messages.length === 0 ? (
          <div className="text-center py-8">
            <Bot className="h-12 w-12 text-gray-400 mx-auto mb-4" />
            <p className="text-gray-600 mb-6">
              Ask me about any health product or nutritional claim you'd like me to fact-check.
            </p>
            
            <div className="space-y-2">
              <p className="text-sm text-gray-500 mb-3">Try these example questions:</p>
              {exampleQuestions.map((question, index) => (
                <button
                  key={index}
                  onClick={() => handleExampleClick(question)}
                  className="block w-full text-left p-3 text-sm text-blue-600 hover:bg-blue-50 rounded-lg border border-blue-200 transition-colors"
                >
                  {question}
                </button>
              ))}
            </div>
          </div>
        ) : (
          messages.map((message) => (
            <div key={message.id} className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}>
              <div className={`max-w-3xl ${message.role === 'user' ? 'user-message' : 'assistant-message'} chat-message`}>
                <div className="flex items-start space-x-3">
                  <div className="flex-shrink-0">
                    {message.role === 'user' ? (
                      <User className="h-6 w-6 text-blue-600" />
                    ) : (
                      <Bot className="h-6 w-6 text-gray-600" />
                    )}
                  </div>
                  
                  <div className="flex-1">
                    <div className="prose prose-sm max-w-none">
                      <ReactMarkdown>{message.content}</ReactMarkdown>
                    </div>
                    
                    {message.sources && message.sources.length > 0 && (
                      <div className="mt-2 p-2 bg-gray-100 rounded text-xs">
                        <strong>Sources used:</strong> {message.sources.join(', ')}
                      </div>
                    )}
                    
                    <div className="text-xs text-gray-500 mt-1">
                      {message.timestamp.toLocaleTimeString()}
                    </div>
                  </div>
                </div>
              </div>
            </div>
          ))
        )}
        
        {isLoading && (
          <div className="flex justify-start">
            <div className="loading-message chat-message max-w-3xl">
              <div className="flex items-center space-x-3">
                <Bot className="h-6 w-6 text-yellow-600" />
                <div className="flex items-center space-x-2">
                  <Loader2 className="h-4 w-4 animate-spin text-yellow-600" />
                  <span className="text-yellow-800">Researching and fact-checking...</span>
                </div>
              </div>
            </div>
          </div>
        )}
        
        {error && (
          <div className="bg-red-50 border border-red-200 rounded-lg p-4">
            <div className="flex items-center space-x-2">
              <AlertCircle className="h-5 w-5 text-red-600" />
              <span className="text-red-800">{error}</span>
            </div>
          </div>
        )}
        
        <div ref={messagesEndRef} />
      </div>

      {/* Input Area */}
      <div className="border-t border-gray-200 p-4">
        <form onSubmit={handleSubmit} className="flex space-x-4">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask about a health product or nutritional claim..."
            className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            disabled={isLoading}
          />
          <button
            type="submit"
            disabled={isLoading || !input.trim()}
            className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center space-x-2"
          >
            {isLoading ? (
              <Loader2 className="h-4 w-4 animate-spin" />
            ) : (
              <Send className="h-4 w-4" />
            )}
            <span>Send</span>
          </button>
        </form>
      </div>
    </div>
  )
} 