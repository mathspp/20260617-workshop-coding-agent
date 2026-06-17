from anthropic import Anthropic

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