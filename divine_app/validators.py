from django.core.exceptions import ValidationError

def max_20_words(value):
    words = value.split()
    if len(words) > 20:
        raise ValidationError(
            f'Description must not exceed 20 words. You entered {len(words)} words.'
        )