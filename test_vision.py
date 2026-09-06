import ollama

response = ollama.chat(
    model="qwen3.5:4b",
    messages=[
        {
            "role": "user",
            "content": "Describe this image.",
            "images": [
                "output/scenes/scene_001/frame_01.jpg"
            ]
        }
    ]
)

print(response["message"]["content"])


