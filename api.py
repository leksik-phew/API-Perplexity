from openai import OpenAI
class api():
  def __init__(api_key=None):
    if api_key == None: 
      with open("key.txt") as key_file:
        api_key = key_file.readline()
    self.API_KEY = api_key
    self.client = OpenAI(
        api_key=API_KEY,
        base_url="https://api.perplexity.ai"
    )
    
  def get(mes):
    message = [
        {
            "role": "system", "content": "Ты полезный ассистент, отвечай кратко и точно."
        },
        {
            "role": "user", "content": mes
        }
    ]

    response = client.chat.completions.create(
        model="sonar-pro", 
        messages=message,
        max_tokens=1024,
        temperature=0.1,
        stream=False
    )
    return (response.choices[0].message.content, 
            f"Использовано токенов: {response.usage.total_tokens}")

