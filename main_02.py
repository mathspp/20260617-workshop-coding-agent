"""
Add the command `/exit` to stop the agent.
Add a slash command `/rewind IDX` that “rewinds” the context
by keeping only the messages `context[:idx]`.
You may want to reprint the chat to update it.
Prepend each message (yours or the agent's) with the index.
"""

from anthropic import Anthropic

client = Anthropic()

context = []

while True:
    user_message = input(" >>> ").strip()

    context.append(
        {
            "role": "user",
            "content": user_message,
        }
    )

    response = client.messages.create(
        max_tokens=1024,
        messages=context,
        model="claude-haiku-4-5",
    )

    for block in response.content:
        if block.type == "text":
            print(block.text)
            context.append(
                {
                    "role": "assistant",
                    "content": block.text,
                }
            )
        else:
            raise RuntimeError(f"Can't handle block type {block.type}.")