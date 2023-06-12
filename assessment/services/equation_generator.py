import random
from typing import Dict, List

from .utils import generate_answer_options, generate_random_letter, random_integer


def generate_equation(**kwargs) -> Dict:

    """
    Generates three values that satisfy a simple equation: x + y = z.
    For eg: 2 + 3 = 5.
    """

    LEVELS: Dict[Dict[str:int]] = {
        "1": {"Min": 1, "Max": 10, "Operator": "+"},
        "2": {"Min": 1, "Max": 10, "Operator": "-"},
        "3": {"Min": 11, "Max": 50, "Operator": "+"},
        "4": {"Min": 11, "Max": 50, "Operator": "-"},
    }

    level = str(kwargs.pop("level"))

    min_value = LEVELS.get(level)["Min"]
    max_value = LEVELS.get(level)["Max"]
    operator = LEVELS.get(level)["Operator"]

    random_number_1 = random_integer(min_value, max_value)
    random_number_2 = random_integer(min_value, max_value)

    equals = 0
    if level == "2" or level == "4":
        while random_number_1 < random_number_2:
            random_number_2 = random_integer(min_value, max_value)
        equals = random_number_1 - random_number_2
    else:
        equals = random_number_1 + random_number_2

    wrong_answers = generate_answer_options(
        random_number_1, equals, random_number_2, min_value, max_value
    )
    random_letter = generate_random_letter()

    equation = f"{random_number_1} {operator} {random_letter} = {equals}"
    equation_lhs = equation.split("=")[0]
    question = f"Choose the correct option for {random_letter}"

    return {
        "level": level,
        "question": question,
        "equation": equation,
        "correct_answer": str(random_number_2),
        "options": wrong_answers,
        "letter": random_letter,
        "operator": operator,
        "equation_lhs": equation_lhs,
    }
