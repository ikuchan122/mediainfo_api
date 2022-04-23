from django.core.exceptions import ValidationError
from django.core.validators import URLValidator


def valid_url(to_validate: str) -> bool:
    validator = URLValidator()
    try:
        validator(to_validate)
        # url is valid here
        # do something, such as:
        return True
    except ValidationError as exception:
        # URL is NOT valid here.
        # handle exception..
        print(exception)
        return False
