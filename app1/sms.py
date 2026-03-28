import base64
import json
import urllib.error
import urllib.parse
import urllib.request

from django.conf import settings


class SMSDeliveryError(Exception):
    pass


def send_otp_sms(phone_number, otp_code):
    account_sid = getattr(settings, "TWILIO_ACCOUNT_SID", "")
    auth_token = getattr(settings, "TWILIO_AUTH_TOKEN", "")
    from_number = getattr(settings, "TWILIO_FROM_NUMBER", "")

    if not account_sid or not auth_token or not from_number:
        raise SMSDeliveryError(
            "Twilio is not fully configured. Add TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, and TWILIO_FROM_NUMBER."
        )

    body = f"Your Krushi Settu OTP is {otp_code}. Do not share it with anyone."
    payload = urllib.parse.urlencode(
        {
            "To": _normalize_indian_number(phone_number),
            "From": from_number,
            "Body": body,
        }
    ).encode()

    request = urllib.request.Request(
        url=f"https://api.twilio.com/2010-04-01/Accounts/{account_sid}/Messages.json",
        data=payload,
        method="POST",
    )
    auth_value = base64.b64encode(f"{account_sid}:{auth_token}".encode()).decode()
    request.add_header("Authorization", f"Basic {auth_value}")
    request.add_header("Content-Type", "application/x-www-form-urlencoded")

    try:
        with urllib.request.urlopen(request, timeout=15) as response:
            response_body = response.read().decode()
    except urllib.error.HTTPError as exc:
        error_body = exc.read().decode(errors="ignore")
        raise SMSDeliveryError(f"Twilio rejected the OTP request: {error_body}") from exc
    except urllib.error.URLError as exc:
        raise SMSDeliveryError("Unable to reach Twilio. Check your internet connection and Twilio credentials.") from exc

    parsed = json.loads(response_body)
    if parsed.get("error_message"):
        raise SMSDeliveryError(parsed["error_message"])


def _normalize_indian_number(phone_number):
    digits = "".join(filter(str.isdigit, phone_number))
    if digits.startswith("91") and len(digits) == 12:
        return f"+{digits}"
    return f"+91{digits}"
