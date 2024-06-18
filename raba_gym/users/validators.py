from django.core import validators
from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _

import re

@deconstructible
class PhoneValidator(validators.RegexValidator):
    regex = r"^09\d{9}$"
    message = (
        "Enter a valid mobile number. This value may contain numbers only, "
        'and must be exactly 11 digits starting with "09"'
    )
    flags = 0

phone_validator = PhoneValidator()

def number_validator(password):
    regex = re.compile('[0-9]')
    if regex.search(password) == None:
        raise ValidationError(
                _("password must include number"),
                code="password_must_include_number"
                )

def letter_validator(password):
    regex = re.compile('[a-zA-Z]')
    if regex.search(password) == None:
        raise ValidationError(
                _("password must include letter"),
                code="password_must_include_letter"
                )

def special_char_validator(password):
    regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
    if regex.search(password) == None:
        raise ValidationError(
                _("password must include special char"),
                code="password_must_include_special_char"
                )
