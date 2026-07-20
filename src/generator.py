import json

from src.database import search_facts
from src.config import client
from src.prompts import QUIZ_PROMPT
from src.search import search_context


def generate_quiz(topic, num_questions=3, difficulty="Medium"):

    results = search_facts(
        query=topic,
        sport=topic.capitalize()
    )

    context = search_context(
    f"{sport} {difficulty}"
    )

    documents = results["documents"][0]

    context = "\n".join(documents)

    prompt = QUIZ_PROMPT.format(
        context=context,
        num_questions=num_questions,
        difficulty=difficulty
    )

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    text = response.text.strip()

    if text.startswith("```json"):
        text = text.replace("```json", "").replace("```", "").strip()

    elif text.startswith("```"):
        text = text.replace("```", "").strip()

    return json.loads(text)