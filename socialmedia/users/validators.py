from django.utils.translation import gettext_lazy as _ 
from django.core.exceptions import ValidationError
import re 

def number_validator(password):

    regex = re.compile('[0-9]')
    if regex.search(password) == None:
        raise ValidationError(_("password must include at least a number"),
                              code="password_must_include_number"
                              )

def letter_validator(password):

    regex = re.compile('[a-zA-Z]')
    if regex.search(password) == None:
        raise ValidationError(_("password must include at least a letter"),
                              code="password_must_include_letter"
                              )


def special_char_validator(password):

    regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
    if regex.search(password) == None:
        raise ValidationError(_("password must include at least a special character"),
                              code="password_must_include_special_char"
                              )