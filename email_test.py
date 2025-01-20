from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from fastapi_mail.errors import ConnectionErrors
import os
from dotenv import load_dotenv
import logging

load_dotenv(override=True)

conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
    MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),
    MAIL_FROM=os.getenv("MAIL_USERNAME"),
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_STARTTLS=True,  # Updated field name for TLS
    MAIL_SSL_TLS=False,  # Updated field name for SSL/TLS
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True  # Ensures SSL certificates are validated
)


async def send_reset_email(to_email: str, reset_link: str):
    """
    Asynchronously sends a password reset email to the specified address.
    """
    message = MessageSchema(
        subject="Password Reset Request",
        recipients=[to_email],
        body=f"Click the link to reset your password: {reset_link}",
        subtype="html"
    )
    try:
        fm = FastMail(conf)
        await fm.send_message(message)
        return {"message": "Reset email sent successfully."}
    except ConnectionErrors as e:
        logging.error(f"Failed to send email: {e}")
        return {"error": str(e)}
