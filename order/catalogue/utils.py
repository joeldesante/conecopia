import requests, os

def send_email(to_address: str, from_adress: str, subject: str, message: str):
    
    MAILGUN_API_URL = os.environ.get(MAILGUN_API_URL)
    
    try:
        api_key = os.environ.get("MAILGUN_API_KEY")
        resp = requests.post(MAILGUN_API_URL, 
                             auth=("api", api_key),
                             data = { 
                                "from": from_adress, 
                                "to": to_address, 
                                "subject": subject, 
                                "text": message
                            },
        )
        
        if resp.status_code == 200: # success
            print(f"Successfully sent an email to '{to_address}' via Mailgun API.")
        else: # error
            print(f"Could not send the email, reason: {resp.text}")
    
    except Exception as ex:
        print(f"Mailgun error: {ex}")