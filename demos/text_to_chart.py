from langchain.pydantic_v1 import BaseModel
from langchain.tools import BaseTool
from typing import Type
from eezo.interface.message import Message
from eezo import Eezo
from groq import Groq

import dotenv

dotenv.load_dotenv()

AGENT_ID = "ea508f14-8aaf-4a14-a8f4-3efacf23832b"

# Add EEZO_API_KEY to your .env file
e = Eezo(logger=True)
g = Groq()


eezo_ui_api = e.get_ui_component_api_as_string()


class GenerateUIArgsSchema(BaseModel):
    query: str


class GenerateUI(BaseTool):
    name: str = "Generate UI"
    description: str = "Generate UI components based on the given data and user prompt."
    args_schema: Type[BaseModel] = GenerateUIArgsSchema
    message: Message | None
    thread: str | None

    def __init__(
        self, message: Message | None = None, thread: str = "No history privided."
    ):
        super().__init__()
        self.message = message
        self.thread = thread

    def _run(self, **kwargs):
        system_prompt = f"""
You are a world class python coder, a expert from Stanford. You have been asked to summarize a section for a research to answer one specific question by generating UI components and their content. You have a set of Python UI components at your disposal:

Components:
{eezo_ui_api}

The data you need to decide which UI components to generate and to fill with content:
{self.thread}

User prompt for the summary: 
{self.message}

Instructions:
- Only use the components provided above.
- You can use every component multiple times.
- Use images when a url is provided.
- Use youtube videos when a video_id is provided.
- Use self.message to add new components. self.message is provided for you.
- Last line of the script should be 'self.message.notify()' to display the UI.
- Always include urls like [name](url) for references.
- Don't add the code itself or other code explanations as a part of the UI.
- Use markup to format the text component with bullet points and **bold** text.
- Be concise and quote as much numbers and facts as possible. 
- Don't just copy the data. Answer the research question.
- Use charts only when you have to put multiple datapoints in relationship.
- It is important to include sources and references after each sentence or paragraph using Markup, like [1](https://www.example.com) in the text and in the list at the end of the summary with: **1:** [link name](https://www.example.com).
- Only check the last message in the chat history for context.

Now, complete the code below to generate the UI:
```python
self.message.add("text", text="Answer:")

# Add your UI components here
"""

        completion = g.chat.completions.create(
            model="llama3-70b-8192",
            temperature=0.7,
            messages=[
                {"role": "system", "content": system_prompt},
                {
                    "role": "user",
                    "content": "Generate a UI to summarize the given data.",
                },
            ],
        )
        result = completion.choices[0].message.content
        ui_str = result.split("```python\n")[1].split("\n```")[0]

        try:
            exec(ui_str)
        except Exception as e:
            self.message.add("text", text="An error occurred while executing the code:")
            self.message.add("text", text=f"Error: {e}")
            self.message.notify()


@e.on(AGENT_ID)
def text_to_chart(context, **kwargs):
    m: Message = context.new_message()
    m.add("text", text="Generate UI...")
    m.notify()

    thread = context.get_thread(to_string=True)

    gen_ui = GenerateUI(m, thread)
    gen_ui.invoke(input={"query": kwargs["query"]})

    m.notify()


e.connect()
