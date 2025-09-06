from app.domain.models.value_objects.raw_password.constants import PASSWORD_MIN_LEN


def validate_password_length(password_value: str) -> None:
    if len(password_value) < PASSWORD_MIN_LEN:
        raise Exception(
            f"Password must be at least {PASSWORD_MIN_LEN} characters long.",
        )
