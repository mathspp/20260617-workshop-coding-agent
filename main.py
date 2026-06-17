from anthropic import Anthropic

client = Anthropic()

while True:
    user_message = input(" >>> ").strip()

    response = client.messages.create(
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": user_message,
            }
        ],
        model="claude-haiku-4-5",
    )
    print(response.content)