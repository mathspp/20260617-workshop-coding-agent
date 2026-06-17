from anthropic import Anthropic

TOOL_INSTRUCTIONS = (
    "If you need to read the contents of a "
    + "file, reply with the exact string "
    + "'tool_call: read('path/to/file')' and nothing else "
    + "and you'll get the contents of the file."
)

def read(filepath):
    from pathlib import Path

    path = Path(filepath)
    if not path.exists() or not path.is_file():
        return "Can't read from there."
    
    return path.read_text()

client = Anthropic()

context = [
    {
        "role": "user",
        "content": TOOL_INSTRUCTIONS,
    }
]

need_user_input = True

while True:
    if need_user_input:
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
        messages=context,
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

            if block.text.startswith("tool_call"):
                _, function_call = block.text.split(": ")
                if function_call.startswith("read"):
                    filepath = (
                        function_call
                        .removeprefix("read(")
                        .removesuffix(")")
                        .strip("'\"")
                    )
                    result = read(filepath)
                else:
                    raise RuntimeError(f"Unknown function call {function_call}.")

                context.append(
                    {
                        "role": "user",
                        "content": result,
                    }
                )

                need_user_input = False
            else:
                need_user_input = True

        else:
            raise RuntimeError(f"Can't handle block type {block.type}.")