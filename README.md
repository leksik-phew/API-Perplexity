# Temp
from openai import OpenAI

# Замените на ваш API-ключ из настроек Perplexity (Settings > API)
API_KEY = "pplx-your_api_key_here"

# Инициализация клиента
client = OpenAI(
    api_key=API_KEY,
    base_url="https://api.perplexity.ai"
)

# Пример запроса
messages = [
    {
        "role": "system",
        "content": "Ты полезный ассистент, отвечай кратко и точно."
    },
    {
        "role": "user",
        "content": "Расскажи о API Perplexity."
    }
]

# Синхронный запрос (без стриминга)
response = client.chat.completions.create(
    model="sonar-small-online",  # Или "sonar-pro", "llama-3.1-sonar-small-128k-online"
    messages=messages,
    max_tokens=1024,
    temperature=0.1,
    stream=False
)

print("Ответ:", response.choices[0].message.content)
print("Использовано токенов:", response.usage.total_tokens)

# Пример стриминга (для реального времени)
print("\n--- Стриминг ---")
stream = client.chat.completions.create(
    model="sonar-small-online",
    messages=messages,
    stream=True
)
for chunk in stream:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="")
