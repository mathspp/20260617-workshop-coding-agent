from anthropic import Anthropic

# --- TOOLS

TOOLS = []

def read(filepath):
    from pathlib import Path

    path = Path(filepath)
    if not path.exists() or not path.is_file():
        return True, ""
    
    return False, path.read_text()

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

import subprocess

def bash(command):
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=30  # Add timeout to prevent hanging
        )

        # Combine stdout and stderr
        output = result.stdout
        if result.stderr:
            output += result.stderr

        # Return (is_error, result)
        is_error = result.returncode != 0
        return is_error, output
    except subprocess.TimeoutExpired:
        return True, "Command timed out after 30 seconds"
    except Exception as e:
        return True, f"Error executing command: {str(e)}"

TOOLS.append(
    {
        "name": "bash",
        "description": "Execute arbitrary bash commands and return the output.",
        "input_schema": {
            "type": "object",
            "properties": {
                "command": {
                    "type": "string",
                    "description": "The bash command to execute.",
                },
            },
            "required": ["command"],
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

    print("-" * 20)
    for block in response.content:
        print(block)
    print("-" * 20)
    
    tool_call_blocks = []
    content_dictionaries = []
    for block in response.content:
        if block.type == "text":
            print(block.text)
            content_dictionaries.append(
                {
                    "type": "text",
                    "text": block.text,
                }
            )
        elif block.type == "tool_use":
            tool_call_blocks.append(block)
            content_dictionaries.append(block.to_dict())
        else:
            raise RuntimeError(f"Can't handle block type {block.type}.")

    context.append(
        {
            "role": "assistant",
            "content": content_dictionaries,
        }
    )

    # --- Handle tool calls
    for block in tool_call_blocks:
        # Figure out which tool to call and get the result...
        tool_name = block.name
        if tool_name == "read":
            is_error, result = read(block.input["filepath"])
        elif tool_name == "bash":
            is_error, result = bash(block.input["command"])
        else:
            raise RuntimeError(f"Unknown tool {tool_name}.")

        context.append(
            {
                "role": "user",
                "content": [
                    {
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": result,
                        "is_error": is_error,
                    }
                ]
            }
        )

    need_user_input = response.stop_reason != "tool_use"