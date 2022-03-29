from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import re


class DjangoValidator:
    def validate_Maxlength(self, value, max_length=24):
        if len(value) > max_length:
            raise ValidationError(
                _("%(value)s doesn't match max length requirements, max length is(max_length)"),
                params={'value': value, 'max_length': max_length},
            )

    def validate_Minlength(self, value, min_length=8):
        if len(value) < min_length:
            raise ValidationError(
                _("%(value)s doesn't match min length requirements, min length is(max_length)"),
                params={'value': value, 'max_length': min_length},
            )

    def validation_numberOfIdentintification(self, value):
        regexOfEgyptionIdentificationNumber = re.compile(
            '(2|3)[0-9][1-9][0-1][0-9][0-3][1-9](01|02|03|04|11|12|13|14|15|16|17|18|19|21|22|23|24|25|26|27|28|29|31|32|33|34|35|88)\d\d\d\d\d')
        if not(re.match(regexOfEgyptionIdentificationNumber, value)):
            raise ValidationError(
                _("%(value)s is not a valid Egyption Identification Number"),
                params={'value': value},
            )

    def validation_EgyptionMobileNumber(self, value):
        regexOfEgyptionMobileNumber = re.compile(
            '(201)[0-9]{9}')
        if not(re.match(regexOfEgyptionMobileNumber, value)):
            raise ValidationError(
                _("%(value)s is not a valid Egyption Mobile Number"),
                params={'value': value},
            )

    def validation_ArabicLettersOrNumbers(self, value):
        regex_arabic_letters_or_numbers = re.compile(
            '^[\u0621-\u064A\u0660-\u0669\s]+$')
        if not(re.match(regex_arabic_letters_or_numbers, value)):
            raise ValidationError(
                _("%(value)s doesn't match araibc letters or numbers"),
                params={'value': value},
            )

    def validation_EnglishLetters(self, value):
        regex_english_letters = re.compile(
            '^[a-zA-Z\s]+$')
        if not(re.match(regex_english_letters, value)):
            raise ValidationError(
                _("%(value)s doesn't match araibc letters or numbers"),
                params={'value': value},
            )
