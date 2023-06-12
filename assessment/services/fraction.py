"""
Requirements:

- Click on the correct denominator.
    Generate two numbers.
    Put the smaller number on top, lower number on the bottom.
    Create options.
    Send the correct answer.
- Click on the correct numerator.
    Generate two numbers.
    Put the smaller number on top, lower number on the bottom.
    Create options.
    Send the correct answer.
- Identifying fractions.
    Generate a fraction.
    Generate options.
    Send the correct answer.
- Comparison with visual aid: Boxes
    Generate one number.
    Generate a smaller number.
    Compare two things.
    Send the stuff.
- Comparison without visual aid.
    
- Add with visual aid.
- Add without visual aid.
- Subtract with visual aid.
- Subtract without visual aid.

"""


class Fraction:
    def __init__(self, *, level: int) -> None:
        self.level = level
