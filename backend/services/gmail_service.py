from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

def get_gmail_service(token):
    creds = Credentials(token=token["access_token"])
    service = build("gmail", "v1", credentials=creds)
    return service


def fetch_recent_emails(service, max_results=10):
    results = service.users().messages().list(
        userId="me",
        maxResults=max_results
    ).execute()

    messages = results.get("messages", [])
    email_list = []

    for msg in messages:
        msg_data = service.users().messages().get(
            userId="me",
            id=msg["id"],
            format="metadata",
            metadataHeaders=["Subject", "From", "Date"]
        ).execute()

        headers = msg_data["payload"]["headers"]
        email_info = {"id": msg["id"]}

        for header in headers:
            if header["name"] in ["Subject", "From", "Date"]:
                email_info[header["name"].lower()] = header["value"]

        email_list.append(email_info)

    return email_list


def fetch_full_email(service, message_id):
    msg_data = service.users().messages().get(
        userId="me",
        id=message_id,
        format="full"
    ).execute()

    parts = msg_data["payload"].get("parts", [])
    body = ""

    if parts:
        for part in parts:
            if part["mimeType"] == "text/plain":
                data = part["body"].get("data")
                if data:
                    import base64
                    body = base64.urlsafe_b64decode(data).decode()
    else:
        data = msg_data["payload"]["body"].get("data")
        if data:
            import base64
            body = base64.urlsafe_b64decode(data).decode()

    return body