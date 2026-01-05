import asyncio

from langgraph_sdk import get_client
from langchain_core.messages import HumanMessage
from langchain_core.messages import convert_to_messages
from pathlib import Path


def save_report(path: str, content: str, encoding="utf-8"):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding=encoding)


async def main(topic: str, max_analysts: int, auto_approve: bool) -> None:
    url_for_client_deployment = "http://localhost:2024"
    client = get_client(url=url_for_client_deployment)
    assistant_id = 'research_assistant'
    thread = await client.threads.create()

    async for chunk in client.runs.stream(
        thread["thread_id"],
        assistant_id,
        input={
        "topic": topic,
        "max_analysts": max_analysts
        },
        stream_mode="values"
    ):
        if chunk.event == 'values' and chunk.data.get('analysts'):
            for analyst in chunk.data["analysts"]:
                print(f"Name: {analyst["name"]}")
                print(f"Affiliation: {analyst["affiliation"]}")
                print(f"Role: {analyst["role"]}")
                print(f"Description: {analyst["description"]}")
                print("-" * 50)  

    if auto_approve: 
        print("Skipping approval!!!")
        human_feedback = "approve"
    else:
        human_feedback = input("Get feedback (type 'approve' to continue): ")

    await client.threads.update_state(thread["thread_id"], {"human_analyst_feedback": human_feedback}, as_node="human_feedback")
    
    async for chunk in client.runs.stream(
        thread["thread_id"],
        assistant_id,
        input=None,
        stream_mode="updates"
    ):
        if chunk.event != "updates": continue
        print("--Node--")
        node_name = next(iter(chunk.data.keys()))
        print(node_name)

    final_state = await client.threads.get_state(thread["thread_id"])
    report = final_state["values"]["final_report"]
    
    from uuid import uuid4
    filename = f"{uuid4()}.md"
    save_report(f"reports/{filename}", report)
   
if __name__ == "__main__":
    topic = input("Topic: ")
    #topic = "The benefits of relocation to Spain for Belarussion citizens with valid Lithuania Blue Card"
    max_analysts = input("Max Analysts: ")
    #max_analysts = 3

    print('='*80)
    asyncio.run(main(topic, max_analysts, auto_approve = True))