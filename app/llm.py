import httpx
from app.config import settings


class LLMClient:
    def __init__(self) -> None:
        self.base_url = settings.openai_base_url.rstrip("/")
        self.headers = {"Authorization": f"Bearer {settings.openai_api_key}"}

    async def embed(self, texts: list[str]) -> list[list[float]]:
        async with httpx.AsyncClient(timeout=60) as client:
            response = await client.post(
                f"{self.base_url}/embeddings",
                headers=self.headers,
                json={"model": settings.embedding_model, "input": texts},
            )
            response.raise_for_status()
            data = response.json()["data"]
            return [item["embedding"] for item in sorted(data, key=lambda x: x["index"])]

    async def answer(self, question: str, context: str) -> str:
        prompt = (
            "Answer only from the supplied context. If the answer is not in the "
            "context, say that the knowledge base does not contain enough information.\n\n"
            f"Context:\n{context}\n\nQuestion: {question}"
        )
        async with httpx.AsyncClient(timeout=60) as client:
            response = await client.post(
                f"{self.base_url}/chat/completions",
                headers=self.headers,
                json={
                    "model": settings.chat_model,
                    "temperature": 0,
                    "messages": [
                        {"role": "system", "content": "You are a precise knowledge-base assistant."},
                        {"role": "user", "content": prompt},
                    ],
                },
            )
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]


llm = LLMClient()
