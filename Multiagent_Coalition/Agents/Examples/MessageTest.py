from mango import Agent, create_container
import asyncio

class PVAgent(Agent):
    def __init__(self, container):
        super().__init__(container)
        print(f"Hello I am a PV agent! My id is {self.aid}.")

    def handle_message(self, content, meta):
        print(f"Received message with content: {content} and meta {meta}.")



async def main():

    PV_CONTAINER_ADDRESS = ("localhost", 5555)
    # defaults to tcp connection
    pv_container = await create_container(addr=PV_CONTAINER_ADDRESS)

    pv_agent_0 = PVAgent(pv_container)
    pv_agent_1 = PVAgent(pv_container)

    await pv_container.send_message(
        "Hello, this is a simple message.",
        receiver_addr=PV_CONTAINER_ADDRESS,
        receiver_id="agent0",
    )

    await asyncio.sleep(1)

    await pv_agent_0.shutdown()
    await pv_agent_1.shutdown()
    await pv_container.shutdown()


if __name__ == "__main__":
    asyncio.run(main())
