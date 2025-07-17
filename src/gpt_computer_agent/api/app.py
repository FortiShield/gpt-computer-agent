""
FastAPI web interface for the GPT Computer Agent.
"""
from fastapi import FastAPI, HTTPException, Depends, Request, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
import uvicorn
import json
import asyncio
from pathlib import Path
import uuid
from datetime import datetime

from ..core.agent import GPTChatAgent, AgentConfig
from ..core.tools import ToolRegistry, tool
from ..utils.storage import storage, Conversation, Message
from ..config.settings import settings
from ..config.logging import setup_logging, get_logger
from ..core.security import get_current_active_user, oauth2_scheme
from ..db.session import init_db
from .routers import auth, users

# Configure logging
logger = setup_logging()

app = FastAPI(
    title="GPT Computer Agent API",
    description="Web interface for the GPT Computer Agent",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url=f"{settings.API_PREFIX}/openapi.json"
)

# CORS middleware
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Initialize database
@app.on_event("startup")
async def startup_event():
    try:
        init_db()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Error initializing database: {e}")
        raise

# Mount static files
static_dir = Path(__file__).parent / "static"
static_dir.mkdir(exist_ok=True)
app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Templates
templates = Jinja2Templates(directory=str(Path(__file__).parent / "templates"))

# Include routers
app.include_router(
    auth.router,
    prefix=f"{settings.API_PREFIX}/auth",
    tags=["Authentication"]
)

app.include_router(
    users.router,
    prefix=f"{settings.API_PREFIX}/users",
    tags=["Users"],
    dependencies=[Depends(get_current_active_user)]
)

# Agent instance
agent_config = AgentConfig(
    name="Web Agent",
    description="A web-based agent with conversation history",
    llm_provider=settings.LLM_PROVIDER,
    temperature=0.7,
    verbose=True
)

# Initialize the agent
agent = GPTChatAgent(agent_config)

# Register tools here
@tool
def search_web(query: str, max_results: int = 3) -> List[Dict[str, str]]:
    """Search the web for information."""
    # This is a placeholder - implement actual web search
    return [
        {
            "title": f"Result {i+1} for '{query}'",
            "url": f"https://example.com/result/{i+1}",
            "snippet": f"This is a sample result for '{query}'."
        }
        for i in range(min(max_results, 3))
    ]

agent.tool_registry.register(search_web)

# API Models
class MessageRequest(BaseModel):
    content: str
    conversation_id: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)

class MessageResponse(BaseModel):
    id: str
    role: str
    content: str
    timestamp: str
    metadata: Dict[str, Any] = {}

class ConversationResponse(BaseModel):
    id: str
    title: str
    created_at: str
    updated_at: str
    messages: List[MessageResponse] = []

# API Routes
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """Serve the main web interface."""
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/api/conversations", response_model=List[Dict[str, Any]])
async def list_conversations(limit: int = 10, offset: int = 0):
    """List all conversations."""
    return storage.list_conversations(limit=limit, offset=offset)

@app.post("/api/conversations", response_model=Dict[str, str])
async def create_conversation(title: str = "New Conversation"):
    """Create a new conversation."""
    conv_id = storage.create_conversation(title=title)
    return {"conversation_id": conv_id}

@app.get("/api/conversations/{conversation_id}", response_model=ConversationResponse)
async def get_conversation(conversation_id: str):
    """Get a conversation by ID."""
    conv = storage.get_conversation(conversation_id)
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    return {
        "id": conv.id,
        "title": conv.title,
        "created_at": conv.created_at.isoformat(),
        "updated_at": conv.updated_at.isoformat(),
        "messages": [
            {
                "id": str(i),
                "role": msg.role,
                "content": msg.content,
                "timestamp": msg.timestamp.isoformat(),
                "metadata": msg.metadata
            }
            for i, msg in enumerate(conv.messages)
        ]
    }

@app.delete("/api/conversations/{conversation_id}")
async def delete_conversation(conversation_id: str):
    """Delete a conversation."""
    storage.delete_conversation(conversation_id)
    return {"status": "success"}

@app.post("/api/messages", response_model=MessageResponse)
async def create_message(message: MessageRequest):
    """Send a message to the agent."""
    # Create conversation if not exists
    if not message.conversation_id:
        message.conversation_id = storage.create_conversation()
    
    # Add user message to storage
    storage.add_message(
        conversation_id=message.conversation_id,
        role="user",
        content=message.content,
        metadata=message.metadata
    )
    
    # Get conversation history
    conv = storage.get_conversation(message.conversation_id)
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    # Format messages for the agent
    messages = [
        {"role": msg.role, "content": msg.content}
        for msg in conv.messages
    ]
    
    # Get agent response
    try:
        response = await agent.run(messages)
        
        # Add agent response to storage
        storage.add_message(
            conversation_id=message.conversation_id,
            role="agent",
            content=response.content,
            metadata=response.metadata if hasattr(response, 'metadata') else {}
        )
        
        # Update conversation title if it's the first message
        if len(conv.messages) == 1:
            # Generate a title based on the first message
            title = message.content[:50] + (message.content[50:] and '...')
            storage._save_conversation(Conversation(
                **{
                    **conv.dict(),
                    "title": title,
                    "updated_at": datetime.utcnow()
                }
            ))
        
        return {
            "id": str(len(conv.messages) + 1),
            "role": "agent",
            "content": response.content,
            "timestamp": datetime.utcnow().isoformat(),
            "metadata": response.metadata if hasattr(response, 'metadata') else {}
        }
    
    except Exception as e:
        logger.error(f"Error in agent response: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# WebSocket endpoint for real-time communication
@app.websocket("/ws/{conversation_id}")
async def websocket_endpoint(websocket: WebSocket, conversation_id: str):
    """WebSocket endpoint for real-time chat."""
    await websocket.accept()
    
    try:
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            message = json.loads(data)
            
            # Add user message to storage
            storage.add_message(
                conversation_id=conversation_id,
                role="user",
                content=message["content"],
                metadata=message.get("metadata", {})
            )
            
            # Get conversation history
            conv = storage.get_conversation(conversation_id)
            if not conv:
                await websocket.send_text(json.dumps({
                    "error": "Conversation not found"
                }))
                continue
            
            # Stream agent response
            response_text = ""
            async for chunk in agent.stream_response(conv.messages):
                if chunk:
                    response_text += chunk
                    await websocket.send_text(json.dumps({
                        "type": "chunk",
                        "content": chunk
                    }))
            
            # Add final response to storage
            storage.add_message(
                conversation_id=conversation_id,
                role="agent",
                content=response_text,
                metadata={}
            )
            
            await websocket.send_text(json.dumps({
                "type": "complete"
            }))
    
    except WebSocketDisconnect:
        logger.info("WebSocket disconnected")
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        await websocket.close()

def run_server(host: str = "0.0.0.0", port: int = 8000, reload: bool = False):
    """Run the FastAPI server."""
    uvicorn.run(
        "gpt_computer_agent.api.app:app",
        host=host,
        port=port,
        reload=reload,
        log_level="info"
    )

if __name__ == "__main__":
    run_server()
