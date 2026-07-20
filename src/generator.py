import json

from src.database import search_facts
from src.config import client
from src.prompts import QUIZ_PROMPT


def generate_quiz(topic, num_questions=3, difficulty="Medium"):

    print("Generating quiz...")
    print("Topic:", topic)
    print("Difficulty:", difficulty)

    # -----------------------------
    # Retrieve context from ChromaDB
    # -----------------------------
    results = search_facts(
        query=topic,
        sport=topic.capitalize()
    )

    documents = results.get("documents", [])

    if documents and len(documents[0]) > 0:
        context = "\n".join(documents[0])
    else:
        print("No documents found in ChromaDB.")
        context = f"""
        General knowledge about {topic}.
        Create factual sports quiz questions.
        """

    # -----------------------------
    # Build Prompt
    # -----------------------------
    prompt = QUIZ_PROMPT.format(
        context=context,
        num_questions=num_questions,
        difficulty=difficulty
    )

    print("Sending request to Gemini...")

    # -----------------------------
    # Generate Quiz
    # -----------------------------
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    print("Gemini response received")

    text = response.text.strip()

    print(text)

    # -----------------------------
    # Remove Markdown if present
    # -----------------------------
    if text.startswith("```json"):
        text = text.replace("```json", "").replace("```", "").strip()

    elif text.startswith("```"):
        text = text.replace("```", "").strip()

    # -----------------------------
    # Parse JSON safely
    # -----------------------------
    try:
        return json.loads(text)

    except json.JSONDecodeError:
        print("Invalid JSON returned by Gemini")
        print(text)
        return []