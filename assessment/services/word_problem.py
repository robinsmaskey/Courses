import operator as op
import random
import string
from typing import Dict, List

from .utils import generate_answer_options

NAMES: List[str] = ["Tenzin", "Pemba", "Pasang", "Dorji", "Chhiring", "Appa"]
TIME: List[str] = ["Yesterday", "Day before yesterday", "Last Saturday", "Last Friday"]

OBJECTS: List[tuple] = [
    {"singular": "khata", "plural": "khatas"},
    {"singular": "copy", "plural": "copies"},
    {"singular": "chocolate", "plural": "chocolates"},
    {"singular": "pen", "plural": "pens"},
]

LEVELS: List[Dict] = {
    "1": {"min": 1, "max": 10, "operator": "+"},
    "2": {"min": 1, "max": 10, "operator": "-"},
    "3": {"min": 11, "max": 50, "operator": "+"},
    "4": {"min": 11, "max": 50, "operator": "-"},
}

PATTERN: Dict = "<person_one> had <number_before> <object_before> . \
                <time>, <person_one> <past_tense_verb> some <object_before> <preposition> <person_two> . \
                Now <person_one> has <number_after> <object_after> in total . \
                How many <object_before> did <person_one> <present_tense_verb> <preposition> <person_two>"

# Solve this.
def generate_equation_options(
    equation: str, min: int, max: int, correct_answer: int
) -> List[str]:
    """
    Generates four equations for which the unknown variable is switched.
    Example:
    For a equation 2 + 3 = 5, the function generates,
    ? + 3 = 5,
    2 + ? = 5,
    2 + 3 = ?,
    3 + ? = 5
    """
    equation = equation.split()
    all_equations = []
    for i in range(0, 7, 2):
        if i == 6:
            new_equation = list(equation)
            new_equation[0], new_equation[2] = new_equation[2], new_equation[0]
            new_equation[2] = "?"
            random_number = random_integer(min=min, max=max)
            while random_number == correct_answer:
                random_number = random_integer(min=min, max=max)
            new_equation[0] = str(random_number)
            new_equation = " ".join([x for x in new_equation])

            all_equations.append(new_equation)
        else:
            new_equation = list(equation)
            new_equation[i] = "?"
            new_equation = " ".join([x for x in new_equation])
            all_equations.append(new_equation)
    print(all_equations)
    return all_equations


def random_integer(min: int, max: int) -> int:
    """
    Generates random integers between a given range
    """
    random_number = random.randint(min, max)
    return random_number


def get_random_item(item_list: List) -> str:
    """
    Returns a unique item from a given list.
    """

    item = random.choice(item_list)
    return item


def get_two_random_items(item_list: List) -> str:
    """
    Returns two unique items from a given list.
    """

    item_one, item_two = random.choice(item_list), random.choice(item_list)

    while item_one is item_two:
        item_two = random.choice(item_list)

    return item_one, item_two


def get_two_unique_random_integers(min: int, max: int) -> int:
    """
    Generates three random numbers based on a specified range.
    """
    number_one = random_integer(min=min, max=max)
    number_two = random_integer(min=min, max=max)

    while number_one < number_two:
        number_two = random_integer(min=min, max=max)

    return number_one, number_two


def get_random_lowecase_alphabet() -> str:
    """
    Generates a random lowercase alphabet.
    """
    LOWERCASE_ALPHABETS = string.ascii_lowercase
    random_letter = random.choice(LOWERCASE_ALPHABETS)
    return random_letter


def get_verbs_from_operator(operator: str) -> Dict:

    """
    Returns a dictionary of tenses and preposition from a given operator.
    """

    map_operator_to_verb = {
        "-": {
            "past_tense_verb": "gave",
            "present_tense_verb": "give",
            "preposition": "to",
        },
        "+": {
            "past_tense_verb": "got",
            "present_tense_verb": "get",
            "preposition": "from",
        },
    }

    return map_operator_to_verb[operator]


def check_cardinality(number: int) -> str:
    """
    Checks whether a number is singular or plural.
    """
    return "plural" if number > 1 else "singular"


def get_two_random_names():
    """
    Gets two random names from a names list.
    """
    person_one, person_two = get_two_random_items(NAMES)
    return person_one, person_two


def populate_random_names_and_time(
    person_one: str, person_two: str, pattern: List[str]
) -> List[str]:
    """
    Populate given names and time in the word problem pattern.
    """
    pattern: List = list(pattern)
    time: str = get_random_item(TIME)
    person_one, person_two = str(person_one), str(person_two)

    for index, word in enumerate(pattern):
        if word == "<person_one>":
            pattern[index] = person_one
        elif word == "<person_two>":
            pattern[index] = person_two
        elif word == "<time>,":
            pattern[index] = f"{time},"
    return pattern


def populate_number_and_objects(
    pattern: List[str], number_one: int, number_two: int, object: Dict
) -> List[str]:
    """
    Populates the pattern with random numbers and objects.
    """
    pattern = list(pattern)
    number_one, number_two = int(number_one), int(number_two)

    object: Dict = dict(object)

    object_cardinality_before, object_cardinality_after = check_cardinality(
        number_one
    ), check_cardinality(number_two)

    for index, word in enumerate(pattern):
        if word == "<number_before>":
            pattern[index] = number_one
        if word == "<number_after>":
            pattern[index] = number_two
        if word == "<object_before>":
            pattern[index] = object[object_cardinality_before]
        if word == "<object_after>":
            pattern[index] = object[object_cardinality_after]

    return pattern


def generate_simplified_word_problem(pattern: List[str]) -> List[str]:
    """
    Generates a simplified version of the word problem.
    """
    pattern: str = list(pattern)
    clause_1, clause_2, clause_3, _ = [item for item in pattern]

    sentence_1 = f"{clause_1.strip()}."
    sentence_2 = f"{(clause_2.split(',')[1]).strip()}."

    clause_3 = (clause_3.strip()).split()
    clause_3.pop(0)

    modified_clause_3 = f"{' '.join([x for x in clause_3])}"
    sentence_3 = f"{''.join([x for x in modified_clause_3])}."

    return [sentence_1, sentence_2, sentence_3]


def generate_word_options(
    person_one_name: str,
    person_two_name: str,
    object: str,
    operator: str,
    answers: List[str],
) -> List[str]:
    """
    Generates four word based options from given names and number
    """

    print("-" * 100)
    print("DEBUGGING")

    print("Printing answers...")
    print(answers)
    print("-" * 100)

    person_one: str = str(person_one_name)
    person_two: str = str(person_two_name)
    object_dict: str = dict(object)

    operator: str = str(operator)
    answers: List[str] = list(answers)
    correct_answer: int = answers.pop()

    correct_answer_cardinality = check_cardinality(int(correct_answer))

    object = object_dict[correct_answer_cardinality]

    received_verbs, given_verbs = get_verbs_from_operator(
        operator="+"
    ), get_verbs_from_operator(operator="-")

    correct_verb = get_verbs_from_operator(operator=operator)["past_tense_verb"]
    correct_preposition = get_verbs_from_operator(operator=operator)["preposition"]

    addition_verb, addition_preposition = (
        received_verbs["past_tense_verb"],
        received_verbs["preposition"],
    )
    subtraction_verb, subtraction_preposition = (
        given_verbs["past_tense_verb"],
        given_verbs["preposition"],
    )

    verb_preposition = [
        (addition_verb, addition_preposition),
        (subtraction_verb, subtraction_preposition),
    ]
    print(correct_verb, correct_preposition, correct_answer)
    correct_option = f"{person_one} {correct_verb} {correct_answer} {object} {correct_preposition} {person_two}"
    options: List[str] = []

    # answers = random.shuffle(answers)
    for answer in answers:
        verb, preposition = random.choice(verb_preposition)
        options.append(
            f"{person_one} {verb} {answer} {object} {preposition} {person_two}"
        )

    options.append(correct_option)

    return correct_option, options


def generate(level: str) -> str:
    ops = {"+": op.add, "-": op.sub}
    level_parameters = LEVELS[level]
    minimum_range, maximum_range, operator = (
        level_parameters["min"],
        level_parameters["max"],
        level_parameters["operator"],
    )

    verbs = get_verbs_from_operator(operator)
    past_tense_verb, present_tense_verb, preposition = (
        verbs["past_tense_verb"],
        verbs["present_tense_verb"],
        verbs["preposition"],
    )

    initial_number, intermediate_number = get_two_unique_random_integers(
        min=minimum_range, max=maximum_range
    )
    final_number = ops[operator](initial_number, intermediate_number)

    pattern = PATTERN.split()

    name_one, name_two = get_two_random_names()
    pattern_with_names = populate_random_names_and_time(name_one, name_two, pattern)

    object = get_random_item(OBJECTS)
    pattern_with_number_and_objects = populate_number_and_objects(
        pattern_with_names, initial_number, final_number, object
    )

    final_pattern = pattern_with_number_and_objects

    for index, word in enumerate(final_pattern):
        if word == "<past_tense_verb>":
            final_pattern[index] = past_tense_verb
        elif word == "<present_tense_verb>":
            final_pattern[index] = present_tense_verb
        elif word == "<preposition>":
            final_pattern[index] = preposition

    problem = " ".join([str(x) for x in final_pattern])

    problem = problem.split(".")

    simplified_word_problem = generate_simplified_word_problem(problem)

    problem = ".".join([x.rstrip() for x in problem])
    final_problem = f"{problem}?"

    correct_answer = intermediate_number
    answer_options = generate_answer_options(
        initial_number=initial_number,
        final_number=final_number,
        correct_answer=correct_answer,
        min=minimum_range,
        max=maximum_range,
    )

    correct_equation = f"{initial_number} {operator} {correct_answer} = {final_number}"

    correct_equation_option = f"{initial_number} {operator} ? = {final_number}"
    equation_options = generate_equation_options(
        correct_equation, minimum_range, maximum_range, correct_answer
    )

    correct_option, word_options = generate_word_options(
        person_one_name=name_one,
        person_two_name=name_two,
        object=object,
        operator=operator,
        answers=answer_options,
    )

    return {
        "level": level,
        "question": final_problem,
        "simplified_question": simplified_word_problem,
        "equation": {
            "correct_equation": correct_equation,
            "correct_option": correct_equation_option,
            "options": equation_options,
        },
        "answer": {"correct_answer": correct_answer, "options": answer_options},
        "word_answer": {"correct_answer": correct_option, "options": word_options},
    }


generate(level="1")
