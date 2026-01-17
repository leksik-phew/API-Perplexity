import json
import urllib.request
import urllib.error

_SECRET = "sk-proj-1ZlezUnEu8ESOslqFsZOyUGHl6cpxACGBXWsC09MsdQFKesj1qrnJTQ11NDOrbcvFD9VPxWW58T3BlbkFJEdf2ii5Oob6j7n0YMi1104VLU1NrEPB7_jxfEMS46cj1vfX-1yFb5xxN3ArevjMQ-hMbqa"
_GATE = "https://api.openai.com/v1/chat/completions"
_ENGINE = "gpt-5.2"


def _call(payload: dict) -> str:
    data = json.dumps(payload).encode("utf-8")

    req = urllib.request.Request(
        _GATE,
        data=data,
        headers={
            "Authorization": f"Bearer {_SECRET}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            raw = r.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        raise RuntimeError(body) from None
    except urllib.error.URLError as e:
        raise RuntimeError(f"network: {e}") from None

    obj = json.loads(raw)

    if "error" in obj:
        raise RuntimeError(obj["error"].get("message", "unknown error"))

    return obj["choices"][0]["message"]["content"]


def run():
    if not _SECRET or "PASTE_YOUR_OPENAI_API_KEY_HERE" in _SECRET:
        print("config:// missing key")
        return

    mem = [
        {
            "role": "system",
            "content": (
                "Отвечай по-русски. Возвращай ТОЛЬКО конечный ответ/результат. "
                "Без объяснений, без шагов решения, без рассуждений."
            ),
        }
    ]

    while True:
        lines = []

        while True:
            try:
                line = input("file:// ")
            except EOFError:
                return

            if line == "":
                break

            lines.append(line)

        if not lines:
            continue

        text = "\n".join(lines).strip()
        cmd = text.lower()

        if cmd in ("/exit", "exit", "quit"):
            break

        if cmd == "/reset":
            mem = [mem[0]]
            continue

        mem.append({"role": "user", "content": text})

        payload = {
            "model": _ENGINE,
            "messages": mem,
            "temperature": 0.2,
        }

        try:
            out = _call(payload).strip()
        except Exception as e:
            msg = str(e).strip()
            if len(msg) > 300:
                msg = msg[:300] + "..."
            print(f"status:// {msg}")
            mem.pop()
            continue

        mem.append({"role": "assistant", "content": out})
        print(out)



from kernel import run

run()

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




##1111a1
from perplexity import Perplexity

client = Perplexity()

search = client.search.create(
    query=[
      "What is Comet Browser?",
      "Perplexity AI",
      "Perplexity Changelog"
    ]
)

for result in search.results:
    print(f"{result.title}: {result.url}")
