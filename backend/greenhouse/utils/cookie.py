def get_token_max_age():
    from django.conf import settings

    return int(settings.REST_KNOX["TOKEN_TTL"].total_seconds())
