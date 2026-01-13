import json
from groq import Groq

from app.core.config import settings

class GroqSummarizationError(Exception):
    """Raised when Groq summarization fails"""
    pass



class GroqClient:
    def __init__(self):
        self.client = Groq(api_key=settings.GROQ_API_KEY)
        self.model = settings.GROQ_MODEL
        self.timeout = settings.GROQ_TIMEOUT

    def summarize(self, text: str, style: str) -> dict:
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            '''
You are a professional document summarization engine.

Your task is to read the provided document and generate a high-quality summary
according to the requested summarization style.

You MUST return a JSON object with EXACTLY this field:
- "summary": string

Rules:
- Output ONLY valid JSON
- Do NOT include explanations outside the JSON
- Do NOT include extra keys
- Preserve factual accuracy; do not hallucinate
- Do not add information not present in the document
- Use clear, neutral, professional language

Formatting rules:
- You MAY use line breaks and markdown inside the "summary" field
- Use markdown bullets when style = "bullet"
- Do not include code blocks

Style-specific requirements:

If style = "brief":
- 3–5 sentences
- Focus on core idea and main conclusions
- Avoid examples and minor details

If style = "detailed":
- Cover all major sections or ideas
- Preserve logical flow
- Multiple paragraphs are allowed

If style = "bullet":
- Use markdown bullet points ("- ")
- Include at least 6–10 bullets (unless the document is very short)
- Each bullet must represent a distinct key idea
- Cover objectives, core functionality, constraints, and evaluation criteria where applicable

                            '''
                        )
                    },
                    {
                        "role": "user",
                        "content": (
                            f"Summarization style: {style}\n\n"
                            f"Document:\n{text}"
                        )
                    }
                ],
                temperature=0.2,
                response_format={"type": "json_object"},
                timeout=self.timeout,
            )

            raw_output = response.choices[0].message.content
            parsed = json.loads(raw_output)

            self._validate_response(parsed, style)
            return parsed

        except json.JSONDecodeError:
            raise GroqSummarizationError("Invalid JSON returned by LLM")

        except Exception as e:
            raise GroqSummarizationError(str(e))

    def _validate_response(self, data: dict, style: str):
        required_keys = {"summary",}

        if not required_keys.issubset(data.keys()):
            raise GroqSummarizationError("Malformed LLM response")

        if not isinstance(data["summary"], str):
            raise GroqSummarizationError("Summary must be a string")
