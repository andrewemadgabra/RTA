from Letter.models import LetterDataLogger


class LetterLogger():

    @classmethod
    def create_log(cls, log_message, letter_object, user_object, from_status_object, to_status_obejct):
        LetterDataLogger.objects.create(**{
            "log_message":  log_message,
            "letter_data":  letter_object,
            "user_id": user_object,
            "from_status": from_status_object,
            "to_status":  to_status_obejct
        })
