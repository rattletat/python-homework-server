from django import forms

from accounts.models import User, IDENTIFER_MIN_NUMBER, IDENTIFER_MAX_NUMBER

REQUIRED_EMAIL_ERROR = "Du musst eine Email-Adresse angeben!"
INVALID_EMAIL_ERROR = "Du musst eine valide Email-Adresse angeben!"
UNIQUE_EMAIL_ERROR = "Diese Email-Adresse existiert bereits."
UNIQUE_ID_ERROR = "Diese TUM-Kennung existiert bereits."
MIN_ID_LENGTH_ERROR = (
    f"Deine Kennung muss mindestens {len(str(IDENTIFER_MIN_NUMBER))} Zeichen lang sein!"
)
MAX_ID_LENGTH_ERROR = (
    f"Deine Kennung darf maximal {len(str(IDENTIFER_MAX_NUMBER))} Zeichen lang sein!"
)


class LoginForm(forms.models.ModelForm):
    class Meta:
        model = User
        fields = ("email", "identifier")
        widget = {}
        error_messages = {
            "email": {
                "required": REQUIRED_EMAIL_ERROR,
                "invalid": INVALID_EMAIL_ERROR,
                "unique": UNIQUE_EMAIL_ERROR,
            },
            "identifier": {
                "min_value": MIN_ID_LENGTH_ERROR,
                "max_value": MAX_ID_LENGTH_ERROR,
                "unique": UNIQUE_ID_ERROR,
            },
        }
