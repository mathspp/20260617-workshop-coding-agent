"""
Handle the tool call and provide the result in the way
that's expected by the Claude API, as described in
https://platform.claude.com/docs/en/agents-and-tools/tool-use/handle-tool-calls.
"""

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
    {
        "name": "read",
        "description": "Read the contents of the given file.",
        "input_schema": {  # JSON schema
            "type": "object",
            "properties": {  # Dictionary with info on all arguments.
                "filepath": {
                    "type": "string",  # integer, boolean, ...
                    "description": "The relative or absolute path to the file to read.",
                },
            },
            "required": ["filepath"],
        },
    }
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
        else:
            raise RuntimeError(f"Can't handle block type {block.type}.")