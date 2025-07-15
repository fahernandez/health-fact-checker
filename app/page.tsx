'use client'

import { useState } from 'react'
import ChatInterface from './components/ChatInterface'
import Header from './components/Header'

export default function Home() {
  return (
    <div className="container mx-auto px-4 py-8 max-w-4xl">
      <Header />
      <ChatInterface />
    </div>
  )
} 