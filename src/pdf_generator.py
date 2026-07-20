from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

styles = getSampleStyleSheet()


def create_pdf(quiz, answers, score, filename="quiz_result.pdf"):

    pdf = SimpleDocTemplate(filename)

    story = []

    story.append(Paragraph("<b>Sports Quiz Result</b>", styles["Title"]))

    story.append(Paragraph(f"Score : {score}/{len(quiz)}", styles["Heading2"]))

    for i, q in enumerate(quiz):

        story.append(Paragraph(f"<b>Question {i+1}</b>", styles["Heading3"]))

        story.append(Paragraph(q["question"], styles["BodyText"]))

        story.append(
            Paragraph(
                f"Your Answer : {answers.get(i)}",
                styles["BodyText"]
            )
        )

        story.append(
            Paragraph(
                f"Correct Answer : {q['answer']}",
                styles["BodyText"]
            )
        )

        story.append(
            Paragraph(
                q["explanation"],
                styles["Italic"]
            )
        )

    pdf.build(story)

    return filename