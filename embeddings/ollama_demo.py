import ollama

response = ollama.chat(
    model="qwen3:8b-q4_K_M",
    messages=[
        {
            "role": "user",
            "content": "Explain what an API is in simple terms."
        }
    ]
)

print(response)