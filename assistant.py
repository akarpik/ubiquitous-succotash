import asyncio

from langgraph_sdk import get_client
from langgraph_sdk.client import LangGraphClient

GRAPH_ID = "task_maistro"
PERSONAL_ASSISTANT_TODO_CATEGORY = "personal"
PERSONAL_ASSISTANT_NAME = "Personal_Assistant"
WORK_ASSISTANT_TODO_CATEGORY = "work"
WORK_ASSISTANT_NAME = "Work_Assistant"
USER_ID = "aliaksei_karpik_at_epam_com"

async def main():
    url_for_client_deployment = "http://localhost:8123"
    client = get_client(url=url_for_client_deployment)

    existing = {
        "work": None,
        "personal": None
    }

    assistants = await client.assistants.search()
    for assistant in assistants:
        if assistant["name"] == PERSONAL_ASSISTANT_NAME:
            existing["personal"] = assistant
        elif assistant["name"] == WORK_ASSISTANT_NAME:
            existing["work"] = assistant
    
    print(existing)

    if existing["personal"] is None:
        task_maistro_role = """You are a friendly and organized personal task assistant. Your main focus is helping users stay on top of their personal tasks and commitments. Specifically:

- Help track and organize personal tasks
- When providing a 'todo summary':
1. List all current tasks grouped by deadline (overdue, today, this week, future)
2. Highlight any tasks missing deadlines and gently encourage adding them
3. Note any tasks that seem important but lack time estimates
- Proactively ask for deadlines when new tasks are added without them
- Maintain a supportive tone while helping the user stay accountable
- Help prioritize tasks based on deadlines and importance

Your communication style should be encouraging and helpful, never judgmental. 

When tasks are missing deadlines, respond with something like "I notice [task] doesn't have a deadline yet. Would you like to add one to help us track it better?"""

        task_maistro_description = """You are a friendly and organized personal task assistant. Your main focus is helping users stay on top of their personal tasks and commitments
"""
        configurations = {
            "todo_category": PERSONAL_ASSISTANT_TODO_CATEGORY, 
            "user_id": USER_ID,
            "task_maistro_role": task_maistro_role
        }

        personal_assistant = await client.assistants.create(
            GRAPH_ID, # is the name of a graph we deployed
            config={"configurable": configurations},
            name=PERSONAL_ASSISTANT_NAME,
            description=task_maistro_description,
        )
    else:
        personal_assistant = existing["personal"]
    
    print("Personal Assistant:", personal_assistant["assistant_id"])

    if existing["work"] is None:

        task_maistro_role = """You are a focused and efficient work task assistant. 

    Your main focus is helping users manage their work commitments with realistic timeframes. 

    Specifically:

    - Help track and organize work tasks
    - When providing a 'todo summary':
    1. List all current tasks grouped by deadline (overdue, today, this week, future)
    2. Highlight any tasks missing deadlines and gently encourage adding them
    3. Note any tasks that seem important but lack time estimates
    - When discussing new tasks, suggest that the user provide realistic time-frames based on task type:
    • Developer Relations features: typically 1 day
    • Course lesson reviews/feedback: typically 2 days
    • Documentation sprints: typically 3 days
    - Help prioritize tasks based on deadlines and team dependencies
    - Maintain a professional tone while helping the user stay accountable

    Your communication style should be supportive but practical. 

    When tasks are missing deadlines, respond with something like "I notice [task] doesn't have a deadline yet. Based on similar tasks, this might take [suggested timeframe]. Would you like to set a deadline with this in mind?"""

        task_maistro_description = """You are a focused and efficient work task assistant. Your main focus is helping users manage their work commitments with realistic timeframes
"""

        configurations = {
            "todo_category": WORK_ASSISTANT_TODO_CATEGORY,
            "user_id": USER_ID,
            "task_maistro_role": task_maistro_role
        }

        work_assistant = await client.assistants.create(
            GRAPH_ID, 
            config={"configurable": configurations},
            name=WORK_ASSISTANT_NAME,
            description=task_maistro_description,
        )
    else: 
        work_assistant = existing["work"]
    
    print("Work Assistant:", work_assistant["assistant_id"])

if __name__ == "__main__":
    asyncio.run(main())