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
        messages=[
            {
                "role": "user",
                "content": user_message,
            }
        ],
        model="claude-haiku-4-5",
    )
    print(response.content)