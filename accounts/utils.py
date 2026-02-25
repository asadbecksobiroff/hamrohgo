import hashlib
import hmac
import json
import urllib.parse
from django.conf import settings

def verify_telegram_init_data(init_data: str) -> dict | None:
    """
    Verifies the data received from the Telegram Mini App.
    Returns the parsed user data if valid, else None.
    """
    if not init_data:
        return None

    try:
        parsed_data = dict(urllib.parse.parse_qsl(init_data))
        hash_str = parsed_data.pop('hash', None)
        if not hash_str:
            return None

        data_check_string = "\n".join([f"{k}={v}" for k, v in sorted(parsed_data.items())])
        
        secret_key = hmac.new(
            b"WebAppData",
            settings.TELEGRAM_BOT_TOKEN.encode(),
            hashlib.sha256
        ).digest()
        
        calculated_hash = hmac.new(
            secret_key,
            data_check_string.encode(),
            hashlib.sha256
        ).hexdigest()

        if calculated_hash != hash_str:
            return None

        user_data = json.loads(parsed_data.get('user', '{}'))
        return user_data
    except Exception as e:
        print(f"Error verifying Telegram initData: {e}")
        return None
