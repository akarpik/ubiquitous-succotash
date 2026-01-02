import asyncio

from langgraph_sdk import get_client
from langchain_core.messages import HumanMessage
from langchain_core.messages import convert_to_messages


async def main(assistant_id: str) -> None:
    url_for_client_deployment = "http://localhost:8123"
    client = get_client(url=url_for_client_deployment)
    thread = await client.threads.create()
        

    while True:
        query = input("Human:")
        if query == "q":
            break
        
        async for chunk in client.runs.stream(
            thread["thread_id"], 
            assistant_id,
            input={"messages": [HumanMessage(content=query)]},
            stream_mode=["updates"]):
            if chunk.event == 'updates':
                state = chunk.data
                convert_to_messages(state['task_mAIstro']['messages'])[-1].pretty_print()


if __name__ == "__main__":
    work_assistant_id = "e3290f9c-e857-4c23-9559-2b9d9cf6e7a8"
    asyncio.run(main(work_assistant_id))