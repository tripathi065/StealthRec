import os
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

def send_alert_message(to_number: str, message: str) -> bool:
    """
    Send an SMS alert using Twilio.
    Returns True if message was sent successfully, False otherwise.
    """
    
    try:
        # Get credentials from environment variables
        account_sid = 'account_sid'
        auth_token = 'auth_token'
        from_number = 'from_number'
        # Validate all required credentials are present
        if not all([account_sid, auth_token, from_number, to_number]):
            missing_vars = [var for var, val in {
                "TWILIO_ACCOUNT_SID": account_sid,
                "TWILIO_AUTH_TOKEN": auth_token,
                "TWILIO_PHONE_NUMBER": from_number,
                "EMERGENCY_CONTACT_NUMBER": to_number
            }.items() if not val]
            print(f"\nError: Missing required environment variables: {', '.join(missing_vars)}")
            return False

        # Initialize Twilio client
        try:
            client = Client(account_sid, auth_token)
        except Exception as e:
            print(f"\nError initializing Twilio client: {str(e)}")
            return False

        # Send message
        try:
            msg_response = client.messages.create(
                body=message,
                from_=from_number,
                to=to_number
            )
            print(f"\nAlert message sent successfully (SID: {msg_response.sid})")
            return True
        except TwilioRestException as e:
            print(f"\nTwilio API Error: {str(e)}")
            print(f"Error Code: {e.code}")
            print(f"Error Message: {e.msg}")
            return False

    except Exception as e:
        print(f"\nUnexpected error sending alert message: {str(e)}")
        return False
