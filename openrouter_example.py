from openai import OpenAI

client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key="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",
)

completion = client.chat.completions.create(
  extra_headers={
    "HTTP-Referer": "http://localhost", # Optional. Site URL for rankings on openrouter.ai.
    "X-Title": "Test Script", # Optional. Site title for rankings on openrouter.ai.
  },
  extra_body={},
  model="meta-llama/llama-4-maverick:free",
  messages=[
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "What is in this image?"
        },
        {
          "type": "image_url",
          "image_url": {
            "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg"
          }
        }
      ]
    }
  ]
)
print(completion.choices[0].message.content) 