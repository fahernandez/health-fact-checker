# Health Fact Checker 🔬✨

An AI-powered web application for fact-checking nutritional claims and health product information using NextJS frontend and FastAPI backend, deployed on Vercel.

*Because the internet is full of "trust me bro" health advice, and science deserves better!*

## Features 🚀

- **AI-Powered Fact Checking**: Uses LangGraph with multiple research tools (like having a PhD researcher as your personal fact-checker!)
- **Scientific Research**: Integrates Google Scholar, ArXiv, and Tavily search (we dig deep into the real science)
- **Modern UI**: Clean, responsive chat interface built with NextJS and TailwindCSS (pretty AND functional)
- **Real-time Chat**: Interactive chatbot experience with streaming responses (no more waiting around!)
- **Source Attribution**: Shows research sources used for each response (receipts included!)
- **Vercel Deployment**: Optimized for easy deployment and scaling (one-click magic)

## Tech Stack 🛠️

### Frontend
- **NextJS 14** - React framework with TypeScript
- **TailwindCSS** - Utility-first CSS framework
- **Shadcn/UI** - Modern component library
- **React** - Interactive user interface

### Backend
- **FastAPI** - High-performance Python web framework
- **LangGraph** - AI agent orchestration
- **LangChain** - LLM integration and tooling
- **OpenAI GPT-4** - Large language model
- **Multiple Search APIs** - Google Scholar, ArXiv, Tavily

### Development Tools
- **uv** - Ultra-fast Python package manager
- **TypeScript** - Type-safe JavaScript
- **Black** - Python code formatter
- **isort** - Python import sorter
- **MyPy** - Static type checking

## Prerequisites 📋

Before diving into this health fact-checking adventure, you'll need:

1. **Node.js** (v18 or higher) - The JavaScript runtime that powers our frontend
2. **Python** (v3.11.11) - Specific version required for our AI-powered backend
3. **uv** - The blazingly fast Python package manager ([Get it here](https://docs.astral.sh/uv/))
4. **API Keys** (the secret sauce):
   - OpenAI API Key ([Get here](https://platform.openai.com/api-keys))
   - SERP API Key ([Get here](https://serpapi.com/))
   - Tavily API Key ([Get here](https://tavily.com/))

## Project Structure 📁

```
health-fact-checker/
├── api/                    # FastAPI backend
│   ├── main.py            # FastAPI application entry point
│   └── test_agent.py      # Agent testing utilities
├── app/                   # NextJS frontend
│   ├── components/        # React components
│   │   ├── ChatInterface.tsx
│   │   └── Header.tsx
│   ├── globals.css        # Global styles
│   ├── layout.tsx         # App layout
│   └── page.tsx           # Main page
├── scripts/               # Development and deployment scripts
│   ├── dev.sh            # Development server script
│   └── deploy.sh         # Deployment script
├── pyproject.toml         # Python project configuration
├── package.json           # Node.js dependencies
├── requirements.txt       # Python dependencies (fallback)
├── uv.lock               # uv lock file
└── vercel.json           # Vercel deployment configuration
```

## Local Development Setup 🏗️

### 1. Clone and Install Dependencies

```bash
# Clone the repository (let's get this party started!)
git clone https://github.com/yourusername/health-fact-checker.git
cd health-fact-checker

# Install Node.js dependencies (frontend magic)
npm install

# Install Python dependencies with uv (lightning fast! ⚡)
uv sync
```

> **Pro tip**: If you don't have `uv` installed yet, grab it with:
> ```bash
> curl -LsSf https://astral.sh/uv/install.sh | sh
> ```

### 2. Environment Variables

Create a `.env` file in the root directory (your secret API keys live here):

```env
OPENAI_API_KEY=sk-your-openai-api-key-here
SERP_API_KEY=your-serp-api-key-here
TAVILY_API_KEY=your-tavily-api-key-here
```

### 3. Run Development Servers

**Option A - Easy Mode (use our handy script):**
```bash
chmod +x scripts/dev.sh
./scripts/dev.sh
```

**Option B - Manual Mode (for the control freaks):**

*Terminal 1 - Frontend (NextJS):*
```bash
npm run dev
```

*Terminal 2 - Backend (FastAPI):*
```bash
cd api
uv run python main.py
```

The application will be available at:
- Frontend: http://localhost:3000 (your shiny UI)
- Backend API: http://localhost:8000 (the brainy backend)

## Development Tools 🔧

### Code Quality
The project includes pre-configured development tools:

```bash
# Format Python code
uv run black api/

# Sort Python imports
uv run isort api/

# Type checking
uv run mypy api/

# Run tests
uv run pytest
```

### Dependencies
- **Core dependencies**: FastAPI, LangChain, LangGraph, OpenAI
- **Development dependencies**: pytest, black, isort, mypy
- **Search integrations**: google-search-results, tavily-python, arxiv

## Deployment to Vercel 🚀

### 1. Install Vercel CLI

```bash
npm install -g vercel
```

### 2. Deploy (the moment of truth!)

**Easy Mode:**
```bash
chmod +x scripts/deploy.sh
./scripts/deploy.sh
```

**Manual Mode:**
```bash
# Login to Vercel
vercel login

# Deploy the application (fingers crossed!)
vercel --prod
```

### 3. Configure Environment Variables

In your Vercel dashboard, add the following environment variables (don't forget these or nothing will work!):

- `OPENAI_API_KEY`: Your OpenAI API key
- `SERP_API_KEY`: Your SERP API key  
- `TAVILY_API_KEY`: Your Tavily API key

### 4. Custom Domain (Optional but cool)

You can configure a custom domain in your Vercel dashboard under the project settings. Make it something snappy like `fact-check-my-vitamins.com`!

## API Endpoints

### Health Check
- `GET /health` - Check if the API is running

### Chat
- `POST /api/chat` - Send a message for fact-checking
- `POST /api/chat/stream` - Stream responses for real-time chat

## Example Usage

Ask questions like:
- "Is turmeric effective for reducing inflammation?"
- "What are the benefits of omega-3 supplements?"
- "Are probiotics good for digestive health?"
- "Does green tea extract help with weight loss?"

## Architecture

The application uses a sophisticated fact-checking pipeline:

1. **User Query**: User submits a health-related question
2. **Research Phase**: AI agent searches multiple sources:
   - Google Scholar for peer-reviewed research
   - ArXiv for scientific papers
   - Tavily for web search results
3. **Analysis**: AI analyzes findings for scientific groundedness
4. **Response**: Provides evidence-based assessment with source citations

## Security & Privacy

- All API keys are secured through environment variables
- CORS is configured for secure cross-origin requests
- No personal health data is stored
- All interactions are processed in real-time

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes
4. Run the code quality tools: `uv run black api/ && uv run isort api/`
5. Run tests: `uv run pytest`
6. Commit your changes: `git commit -m 'Add amazing feature'`
7. Push to the branch: `git push origin feature/amazing-feature`
8. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

This tool provides educational information only and should not replace professional medical advice. Always consult with healthcare professionals before making health-related decisions.

## Support

For issues and questions, please create an issue in the GitHub repository.

---

*Built with ❤️ by the Health Fact Checker Team*