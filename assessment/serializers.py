from rest_framework import serializers


class EquationSerializer(serializers.Serializer):
    level = serializers.CharField()
    question = serializers.CharField()
    equation = serializers.CharField()
    correct_answer = serializers.CharField()
    options = serializers.ListField(child=serializers.CharField())
    letter = serializers.CharField()
    operator = serializers.CharField()
    equation_lhs = serializers.CharField()


class WordProblemWordAnswerSerializer(serializers.Serializer):
    correct_answer = serializers.CharField()
    options = serializers.ListField()


class WordProblemEquationSerializer(serializers.Serializer):
    correct_equation = serializers.CharField()
    correct_option = serializers.CharField()
    options = serializers.ListField()


class WordProblemAnswerSerializer(serializers.Serializer):
    correct_answer = serializers.CharField()
    options = serializers.ListField()


class WordProblemSerializer(serializers.Serializer):
    level = serializers.CharField()
    question = serializers.CharField()
    simplified_question = serializers.ListField()
    equation = WordProblemEquationSerializer()
    answer = WordProblemAnswerSerializer()
    word_answer = WordProblemWordAnswerSerializer()


class AssessmentLogDataSerializer(serializers.Serializer):
    question_type = serializers.CharField()
    # question = serializers.CharField()
    level = serializers.CharField()
    attempts = serializers.CharField()
    # correct_answer = serializers.CharField()
    correct = serializers.BooleanField()
    incorrect = serializers.BooleanField()
    skipped = serializers.BooleanField()


class AssessmentLogsInputSerializer(serializers.Serializer):
    course_name = serializers.CharField()
    child_username = serializers.CharField()
    data = AssessmentLogDataSerializer(many=True)


class AssessmentLogSerializer(serializers.Serializer):
    assessment_type = serializers.CharField()
    assessment_level = serializers.CharField()
    question_type = serializers.CharField()
    number_of_attempts = serializers.CharField()
    number_of_correct = serializers.CharField()
    number_of_incorrect = serializers.CharField()
    number_of_skips = serializers.CharField()
