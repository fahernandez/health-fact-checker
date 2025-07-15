import os
import json
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import List, Optional, TypedDict, AsyncGenerator, Any
from dotenv import load_dotenv

# Import Annotated from typing_extensions for compatibility
from typing_extensions import Annotated

# Import LangGraph components
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import ToolNode
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_community.tools.google_scholar import GoogleScholarQueryRun
from langchain_community.utilities.google_scholar import (
    GoogleScholarAPIWrapper
)
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_community.tools.arxiv.tool import ArxivQueryRun
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Load environment variables
load_dotenv()

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Pydantic models
class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    response: str
    sources: Optional[List[str]] = []


# Initialize the LangGraph agent
def initialize_agent() -> Any:
    """Initialize the fact-checking agent with all tools"""
    
    # Check for required environment variables
    required_vars = ["OPENAI_API_KEY", "SERP_API_KEY", "TAVILY_API_KEY"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        raise ValueError(
            f"Missing required environment variables: {missing_vars}"
        )
    
    # Model definition
    model = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    
    # Tool definitions
    google_scholar_tool = GoogleScholarQueryRun(
        api_wrapper=GoogleScholarAPIWrapper()
    )
    tavily_tool = TavilySearchResults(max_results=10)
    arxiv_tool = ArxivQueryRun()
    
    # Compose tool belt
    tool_belt = [
        tavily_tool,
        arxiv_tool,
        google_scholar_tool
    ]
    
    # Bind tools to model
    model = model.bind_tools(tool_belt)
    
    # Agent state definition
    class AgentState(TypedDict):
        messages: Annotated[list, add_messages]
    
    # Model call node
    def call_model(state: AgentState) -> dict:
        messages = state["messages"]
        response = model.invoke(messages, config={"recursion_limit": 10})
        return {"messages": [response]}
    
    # Tool node
    tool_node = ToolNode(tool_belt)
    
    def is_grounded(state: AgentState) -> str:
        last_message = state["messages"][-1]
        
        if last_message.tool_calls:
            return "action"
        
        initial_query = state["messages"][0]
        final_response = state["messages"][-1]
        
        if len(state["messages"]) > 10:
            return "END"
        
        prompt_template = """\
        Given an initial query and a final response, determine if the \
response is scientifically grounded or not.
         
        Please indicate scientific groundedness with a 'Y' and \
ungroundedness as an 'N'.

        Initial Query:
        {initial_query}

        Final Response:
        {final_response}"""
        
        groundedness_prompt_template = PromptTemplate.from_template(
            prompt_template
        )
        groundedness_check_model = ChatOpenAI(model="gpt-4o-mini")
        groundedness_chain = (
            groundedness_prompt_template | 
            groundedness_check_model | 
            StrOutputParser()
        )
        groundedness_response = groundedness_chain.invoke({
            "initial_query": initial_query.content, 
            "final_response": final_response.content
        })
        
        if "Y" in groundedness_response:
            return "end"
        
        return "continue"
    
    # Graph definition
    uncompiled_graph = StateGraph(AgentState)
    uncompiled_graph.set_entry_point("agent")
    uncompiled_graph.add_node("agent", call_model)
    uncompiled_graph.add_node("action", tool_node)
    uncompiled_graph.add_conditional_edges(
        "agent", is_grounded, {
            "continue": "agent",
            "action": "action",
            "end": END
        }
    )
    uncompiled_graph.add_edge("action", "agent")
    
    return uncompiled_graph.compile()


# Global agent instance
agent = None


@app.on_event("startup")
async def startup_event() -> None:
    """Initialize the agent on startup"""
    global agent
    try:
        agent = initialize_agent()
        print("Agent initialized successfully")
    except Exception as e:
        print(f"Failed to initialize agent: {e}")
        # In production, you might want to fail startup here


@app.get("/")
async def root() -> dict:
    return {"message": "Health Fact Checker API"}


@app.get("/health")
async def health_check() -> dict:
    return {"status": "healthy"}


@app.post("/api/chat")
async def chat(request: ChatRequest) -> ChatResponse:
    """Handle chat requests for fact-checking"""
    if not agent:
        raise HTTPException(status_code=500, detail="Agent not initialized")
    
    try:
        # Prepare system message for health product fact-checking
        system_message = SystemMessage(content="""You are a cautious, \
evidence-driven health-product analyst assisting a user who is highly \
skeptical of advertising claims. 

Your role is to:
1. Analyze nutritional and health product claims with scientific rigor
2. Search for peer-reviewed research and credible sources
3. Provide balanced, evidence-based assessments
4. Clearly distinguish between proven benefits and marketing claims
5. Highlight any potential risks or side effects
6. Recommend consulting healthcare professionals for personalized advice

Always cite your sources and be transparent about the limitations of \
available evidence.""")
        
        human_message = HumanMessage(content=request.message)
        
        inputs = {
            "messages": [system_message, human_message]
        }
        
        # Stream the response
        final_response = ""
        sources = []
        
        async for chunk in agent.astream(inputs, stream_mode="updates"):
            for node, values in chunk.items():
                if "messages" in values:
                    for message in values["messages"]:
                        if hasattr(message, 'content') and message.content:
                            final_response = message.content
                        # Extract sources if available
                        if (hasattr(message, 'tool_calls') and 
                                message.tool_calls):
                            for tool_call in message.tool_calls:
                                tool_names = [
                                    'tavily_search', 
                                    'google_scholar', 
                                    'arxiv'
                                ]
                                if tool_call.get('name') in tool_names:
                                    sources.append(
                                        tool_call.get('name', 'Unknown source')
                                    )
        
        return ChatResponse(
            response=final_response, 
            sources=list(set(sources))
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error processing request: {str(e)}"
        )


@app.post("/api/chat/stream")
async def chat_stream(request: ChatRequest) -> StreamingResponse:
    """Handle streaming chat requests"""
    if not agent:
        raise HTTPException(status_code=500, detail="Agent not initialized")
    
    async def generate() -> AsyncGenerator[str, None]:
        try:
            system_message = SystemMessage(content="""You are a cautious, \
evidence-driven health-product analyst assisting a user who is highly \
skeptical of advertising claims. 

Your role is to:
1. Analyze nutritional and health product claims with scientific rigor
2. Search for peer-reviewed research and credible sources
3. Provide balanced, evidence-based assessments
4. Clearly distinguish between proven benefits and marketing claims
5. Highlight any potential risks or side effects
6. Recommend consulting healthcare professionals for personalized advice

Always cite your sources and be transparent about the limitations of \
available evidence.""")
            
            human_message = HumanMessage(content=request.message)
            
            inputs = {
                "messages": [system_message, human_message]
            }
            
            async for chunk in agent.astream(inputs, stream_mode="updates"):
                for node, values in chunk.items():
                    if "messages" in values:
                        for message in values["messages"]:
                            if hasattr(message, 'content') and message.content:
                                data = {
                                    'type': 'message', 
                                    'content': message.content, 
                                    'node': node
                                }
                                yield f"data: {json.dumps(data)}\n\n"
                            
            yield f"data: {json.dumps({'type': 'done'})}\n\n"
            
        except Exception as e:
            error_data = {'type': 'error', 'message': str(e)}
            yield f"data: {json.dumps(error_data)}\n\n"
    
    return StreamingResponse(generate(), media_type="text/plain")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 