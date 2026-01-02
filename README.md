# ubiquitous-succotash

# Setup

## Setup env

### Init Virtual Env

uv venv
source .venv/bin/activate

### Create .env file and provide veriables

cp studio/sample-.env studio/.env

## Create docker container

### Get to directory

cd deployment

### Create docker-compose.yml file and provide configuration

cp sample-docker-compose.yml docker-compose.yml

### Build image

langgraph build -t my-image

### Compose container

docker compose up

## Create Personal and Work Assistants

python assistant.py


# Usage

Use LangSmith to view graph and assistants

You could add MCP server and select created assistants as Tools

Run for inspection
npx @modelcontextprotocol/inspector --transport http --server-url http://localhost:8123/mcp/