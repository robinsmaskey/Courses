import random
import string
from typing import List


def generate_random_letter() -> str:
    """
    Generates a random lowercase letter.
    """
    LOWERCASE_ALPHABETS = string.ascii_lowercase
    random_letter = random.choice(LOWERCASE_ALPHABETS)
    return random_letter


def random_integer(min: int, max: int) -> int:
    """
    Generates random integers between a given range
    """
    random_number = random.randint(min, max)
    return random_number


def generate_answer_options(
    initial_number, final_number, correct_answer, min, max
) -> List[str]:
    """
    Generates three wrong options for a equation along with one correct option.
    1 + 1 = 2
    initial number + correct answer = final number
    1 - 1 = 0
    """

    """"
    Cases:
    Option 1 = initial number, 
    Option 2 = final_number,
    Option 3 = initial_number + final_number
    Option 4 = Correct answer 

    Error cases:
    case 1: initial number and final number are equal, so option 3 and 4 are equal.
    case 2: 
    """

    answer_1 = initial_number
    answer_2 = final_number
    answer_3 = initial_number + final_number
    answer_4 = correct_answer

    while (
        answer_1 == answer_4
        or answer_1 == answer_2
        or answer_2 == answer_4
        or answer_2 == answer_3
        or answer_3 == answer_4
    ):
        answer_1 = random_integer(min=min, max=max)
        answer_2 = random_integer(min=min, max=max)
        answer_3 = random_integer(min=min, max=max)

    answers = [answer_1, answer_2, answer_3, answer_4]
    return [str(x) for x in answers]
