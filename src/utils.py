"""
utils.py
Reusable helper functions.
"""

import time


def calculate_percentage(score, total):
    """
    Calculate percentage.
    """

    if total == 0:
        return 0

    return round((score / total) * 100, 2)


def format_time(seconds):
    """
    Convert seconds into MM:SS format.
    """

    minutes = seconds // 60
    seconds = seconds % 60

    return f"{minutes:02}:{seconds:02}"


def get_performance_message(percentage):
    """
    Return performance message.
    """

    if percentage == 100:
        return "Perfect Score!"

    elif percentage >= 80:
        return "Excellent Performance!"

    elif percentage >= 60:
        return "Good Job!"

    elif percentage >= 40:
        return "Keep Improving!"

    return "Keep Practicing!"


def current_date():
    """
    Return today's date.
    """

    return time.strftime("%Y-%m-%d")