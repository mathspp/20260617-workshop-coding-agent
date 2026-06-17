from anthropic import Anthropic

# --- TOOLS

TOOLS = []

def read(filepath):
    from pathlib import Path

    path = Path(filepath)
    if not path.exists() or not path.is_file():
        return "Can't read from there."
    
    return path.read_text()

TOOLS.append(
    "name": "read",
    "description": "Read the contents of the given file.",
    "input_schema": {  # JSON schema
        "type": "object",
        "properties": {  # Dictionary with info on all arguments.
            "filepath": {
                "type": "string",  # integer, boolean, ...
            }
        }
    },
)

# ---

client = Anthropic()

context = []

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
        tools=TOOLS,
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