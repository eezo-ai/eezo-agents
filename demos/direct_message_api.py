from eezo import Eezo

import dotenv
import time

dotenv.load_dotenv()

EEZO_ID = "57e01563-a8e4-4cf8-b74c-c211c6d205b5"
THREAD_ID = "4471cef7-14fa-4b96-ba27-a1b867c96f01"

# Add EEZO_API_KEY to your .env file
e = Eezo()

# Send a message to the Chat UI
m = e.new_message(eezo_id=EEZO_ID, thread_id=THREAD_ID, context="test")

m.add("text", text="Hello, world!")
m.notify()

time.sleep(3)

# Update the message in Chat UI
m = e.update_message(m.id)
m.add("text", text="Hello, world! Updated!")
m.notify()

time.sleep(3)

# Update the message in Chat UI
m = e.update_message(m.id)
m.add("text", text="Hello, world! Updated!")
m.notify()

time.sleep(3)

m.add(
    "chart",
    chart_type="donut",
    data=[10, 20, 30],
    xaxis=["a", "b", "c"],
    name="Example chart",
    chart_title="Example chart",
)
m.notify()

time.sleep(3)

# Delete the message from Chat UI
e.delete_message(m.id)
