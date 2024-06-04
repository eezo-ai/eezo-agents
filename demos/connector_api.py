from eezo import Eezo

import dotenv

dotenv.load_dotenv()

AGENT_ID = "dc81c93d-663c-4d05-81a3-00c0e4c75238"

# Add EEZO_API_KEY to your .env file
e = Eezo()


def super_agent(c, choice):
    m = c.new_message()

    if choice == "image":
        image_url = "https://i0.wp.com/devopsmeme.com/wp-content/uploads/2023/11/img_5295-1.jpg?w=643&ssl=1"
        m.add("image", url=image_url)

    if choice == "video":
        m.add("youtube_video", video_id="tWP6z0hvw1M")

    if choice == "text":
        m.add("text", text="Hola, World!")

    if choice == "chart":
        m.add(
            "chart",
            chart_type="donut",
            data=[10, 20, 30],
            xaxis=["a", "b", "c"],
            name="Example chart",
            chart_title="Example chart",
        )
    m.notify()


@e.on(AGENT_ID)
def connector(c, **kwargs):
    super_agent(c, kwargs.get("choice", "image"))


e.connect()
