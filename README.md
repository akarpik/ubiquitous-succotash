# Project Overview

## Tools and Libraries
- **Langgraph**: Stateful workflow management system for building AI agents
- **Pydantic**: Data validation and settings management using BaseModel
- **Trustcall**: Tool call extraction and memory management system
- **LangChain**: Integration with LLMs (ChatOllama)
- **Langgraph MemorySaver**: Persistent state management
- **InMemoryStore**: In-memory storage for temporary data
- **Datetime**: Date/time handling
- **TypedDict**: Type annotations for dictionaries
- **BaseModel**: Data validation for profiles and tasks

## Databases
- **InMemoryStore**: Used for temporary state storage (no persistent storage)
- **Langgraph Store**: Manages memory across different categories (profile, todo, instructions)

## Deployment Tools
- **Git**: Version control system (recent push shown in terminal)
- **Python Virtual Environment**: .venv directory for dependency isolation
- **Langgraph Execution**: Agent runs via Python script execution
- **Terminal Integration**: Debug console for running Python scripts

## Key Features
- Memory management across user profiles, tasks, and instructions
- Tool call extraction for updating memories
- Stateful workflow with conditional routing
- In-memory storage for temporary data
- Integration with LLMs for natural language processing

## Architecture
The agent uses a state graph with:
1. Message processing node
2. Memory update nodes (profile, todo, instructions)
3. Conditional routing based on tool calls
4. Persistent state storage

This implementation provides a foundation for building conversational AI agents with memory management capabilities.

# Setup

## 1. Environment Setup

### Initialize Virtual Environment
```bash
uv venv
source .venv/bin/activate
```

### Configure Environment Variables
1. Create a `.env` file from the sample:
```bash
cp studio/sample-.env studio/.env
```

## 2. Docker Configuration

### Navigate to Deployment Directory
```bash
cd deployment
```

### Configure Docker
1. Create docker-compose.yml from sample:
```bash
cp sample-docker-compose.yml docker-compose.yml
```
2. Build Docker image:
```bash
langgraph build -t my-image
```
3. Start Docker containers:
```bash
docker compose up
```

## 3. Create Assistants
```bash
python assistant.py
```

## 4. Verification
- Use LangSmith to view the graph and assistants
- Add MCP server and select created assistants as tools
- Inspect with MCP inspector:
```bash
npx @modelcontextprotocol/inspector --transport http --server-url http://localhost:8123/mcp/
```