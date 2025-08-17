import os
import io
import ssl
import smtplib
from email.message import EmailMessage
import pandas as pd

def df_to_excel_bytes(df: pd.DataFrame, sheet_name: str = "Sheet1") -> bytes:
    bio = io.BytesIO()
    with pd.ExcelWriter(bio, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name=sheet_name)
    return bio.getvalue()

def get_admin_code() -> str:
    return os.environ.get("TRACKER_ADMIN_CODE", "admin")

def send_email_with_attachment(
    to_addrs,
    subject: str,
    body: str,
    attachment_bytes: bytes,
    attachment_filename: str,
):
    host = os.environ["SMTP_HOST"]
    port = int(os.environ.get("SMTP_PORT", "587"))
    user = os.environ["SMTP_USER"]
    pwd = os.environ["SMTP_PASS"]
    from_addr = os.environ["SMTP_FROM"]
    starttls = os.environ.get("SMTP_STARTTLS", "true").lower() in ("1", "true", "yes")

    msg = EmailMessage()
    msg["From"] = from_addr
    msg["To"] = ", ".join(to_addrs)
    msg["Subject"] = subject
    msg.set_content(body)
    msg.add_attachment(
        attachment_bytes,
        maintype="application",
        subtype="vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        filename=attachment_filename,
    )

    if starttls:
        context = ssl.create_default_context()
        with smtplib.SMTP(host, port) as server:
            server.starttls(context=context)
            server.login(user, pwd)
            server.send_message(msg)
    else:
        with smtplib.SMTP_SSL(host, port) as server:
            server.login(user, pwd)
            server.send_message(msg)
