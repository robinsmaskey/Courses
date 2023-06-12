from typing import List

from account.selectors import child_get
from course.models import Course
from course.selectors import course_get_from_name
from django.core.exceptions import ValidationError

from ..models import ChildAssessmentLog


def assessment_log_create(*, course_name: str, child_username: str, data: List):
    """
    Creates assessment logs
    """
    child = child_get(child_username)
    course = course_get_from_name(course_name=course_name)
    equation_logs = {}
    word_problem_logs = {}
    for item in data:
        if item["question_type"] == "EQ":
            log = equation_logs.get(f"EQ_{item['level']}")
            if log is None:
                new_log = equation_logs[f"EQ_{item['level']}"] = {}
                new_log["assessment_level"] = str(item["level"])
                new_log["question_type"] = item["question_type"]
                new_log["number_of_attempts"] = item["attempts"]
                new_log["number_of_correct"] = item["correct"]
                new_log["number_of_incorrect"] = item["incorrect"]
                new_log["number_of_skips"] = item["skipped"]
                # new_log['score_of_correct'] = sum(item['correct'])
            else:
                log["number_of_attempts"] += item["attempts"]
                log["number_of_correct"] += item["correct"]
                log["number_of_incorrect"] += item["incorrect"]
                log["number_of_skips"] += item["skipped"]
                # log['score_of_correct'] += sum(item['correct'])
        elif item["question_type"] == "WP":
            log = word_problem_logs.get(f"WP_{item['level']}")
            if log is None:
                new_log = word_problem_logs[f"WP_{item['level']}"] = {}
                new_log["assessment_level"] = str(item["level"])
                new_log["question_type"] = item["question_type"]
                new_log["number_of_attempts"] = item["attempts"]
                new_log["number_of_correct"] = item["correct"]
                new_log["number_of_incorrect"] = item["incorrect"]
                new_log["number_of_skips"] = item["skipped"]
                # new_log['score_of_correct'] = sum(item['correct'])
            else:
                log["number_of_attempts"] += item["attempts"]
                log["number_of_correct"] += item["correct"]
                log["number_of_incorrect"] += item["incorrect"]
                log["number_of_skips"] += item["skipped"]
                # log['score_of_correct'] += sum(item['correct'])

    equation_entry_list = [
        ChildAssessmentLog(
            child=child,
            course=course,
            assessment_level=value["assessment_level"],
            question_type=value["question_type"],
            number_of_correct=value["number_of_correct"],
            number_of_incorrect=value["number_of_incorrect"],
            number_of_attempts=value["number_of_attempts"],
            number_of_skips=value["number_of_skips"],
        )
        for key, value in equation_logs.items()
    ]
    word_problem_entry_list = [
        ChildAssessmentLog(
            child=child,
            course=course,
            assessment_level=value["assessment_level"],
            question_type=value["question_type"],
            number_of_correct=value["number_of_correct"],
            number_of_incorrect=value["number_of_incorrect"],
            number_of_attempts=value["number_of_attempts"],
            number_of_skips=value["number_of_skips"],
        )
        for key, value in word_problem_logs.items()
    ]

    entry_list = equation_entry_list + word_problem_entry_list

    ChildAssessmentLog.objects.bulk_create(entry_list)
    return "Done"


def generate_log_report(*, course_name: str, child_username: str):
    """
    Generates log report
    """
    child = child_get(child_username)
    course = course_get_from_name(course_name=course_name)

    log_data_report = ChildAssessmentLog.objects.filter(
        child=child, course=course
    ).order_by("-created_date")[:6]
    return log_data_report
