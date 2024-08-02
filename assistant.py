from openai import OpenAI  
from dotenv import load_dotenv
import json, os

load_dotenv()

client = OpenAI()

class Assistant:
    @staticmethod
    def create(file_path: str):
        file = client.files.create(
            file=open(file_path, "rb"),
            purpose='assistants'
        )
        assistant = client.beta.assistants.create(
                name="OpenAI Assistant",
                instructions= """you are a helpfull assistant""",
                tools=[{"type": "code_interpreter"}],
                model="gpt-3.5-turbo",
                tool_resources={
                    "code_interpreter": {
                    "file_ids": [file.id]
                    }
                }
            )
        # if os.path.exists(file_path):
        #     os.remove(file_path)
        return assistant
    
    @staticmethod
    def createThreadId():
        thread = client.beta.threads.create()
        return thread.id
    
    @staticmethod
    def ask(assistant_id, thread_id, prompt):
        client.beta.threads.messages.create(
                thread_id=thread_id,
                role="user",
                content=prompt
            )
        run = client.beta.threads.runs.create(
                thread_id=thread_id,
                assistant_id=assistant_id,
            )
        while run.status != "completed":
            run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run.id)
            messages = client.beta.threads.messages.list(thread_id=thread_id)
            reply = messages.data[0].content
        for response in reply:
            return response.text.value