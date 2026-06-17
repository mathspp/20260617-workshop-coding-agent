from anthropic import Anthropic

TOOL_INSTRUCTIONS = (
    "If you need to read the contents of a "
    + "file, reply with the exact string "
    + "'tool_call: read('path/to/file')' "
    + "and I'll send you the contents of the file back."
)

client = Anthropic()

context = []

while True:
    user_message = input(" >>> ").strip()

    if user_message.startswith("/"):
        if user_message.startswith(("/quit", "/exit")):
            break
        elif user_message.startswith("/rewind"):
            ...
        else:
            raise RuntimeError(f"Unknown command {user_message}.")
        continue

    context.append(
        {
            "role": "user",
            "content": user_message,
        }
    )

    response = client.messages.create(
        max_tokens=1024,
        messages=context + [
            {
                "role": "user",
                "content": TOOL_INSTRUCTIONS,
            }
        ],
        model="claude-haiku-4-5",
    )

    print(response.content)
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