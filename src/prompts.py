QUIZ_PROMPT = """
You are an expert Sports Quiz Generator.

Using ONLY the context below, generate {num_questions} {difficulty} level multiple-choice quiz questions.

Context:
{context}

Return ONLY valid JSON.

Format:

[
  {{
    "question":"Question text",
    "options":[
      "A",
      "B",
      "C",
      "D"
    ],
    "answer":"Correct Answer",
    "explanation":"Explanation"
  }}
]

Rules:

- Easy → Direct factual questions.
- Medium → Mix facts with reasoning.
- Hard → Analytical/comparative questions.
- Exactly four options.
- Use only the supplied context.
- Return JSON only.
"""