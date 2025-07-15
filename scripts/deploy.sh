#!/bin/bash

# Deployment script for Health Fact Checker

echo "🚀 Deploying Health Fact Checker to Vercel..."

# Check if vercel CLI is installed
if ! command -v vercel &> /dev/null; then
    echo "📦 Installing Vercel CLI..."
    npm install -g vercel
fi

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  Warning: .env file not found. Make sure to configure environment variables in Vercel dashboard."
fi

# Build and deploy
echo "🔨 Building and deploying..."
vercel --prod

echo "✅ Deployment complete!"
echo "📝 Don't forget to configure environment variables in your Vercel dashboard:"
echo "   - OPENAI_API_KEY"
echo "   - SERP_API_KEY"
echo "   - TAVILY_API_KEY" 