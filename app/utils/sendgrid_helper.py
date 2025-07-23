from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from django.conf import settings

def send_email_via_sendgrid(subject, html_content, from_email, to_emails, attachments=None):
    message = Mail(
        from_email=from_email,
        to_emails=to_emails,
        subject=subject,
        html_content=html_content
    )

    # Optional: add attachments
    if attachments:
        for f in attachments:
            content = f.read()
            import base64
            from sendgrid.helpers.mail import Attachment, FileContent, FileName, FileType, Disposition
            encoded = base64.b64encode(content).decode()
            attachment = Attachment(
                FileContent(encoded),
                FileName(f.name),
                FileType(f.content_type),
                Disposition("attachment")
            )
            message.attachment = attachment

    try:
        sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
        response = sg.send(message)
        print(response.status_code)
        return True
    except Exception as e:
        print(e)
        return False
