from anthropic import Anthropic

client = Anthropic()

response = client.messages.create(
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": "Tell me a joke.",
        }
    ],
    model="claude-haiku-4-5",
)
print(response.content)