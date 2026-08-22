import smtplib
from email.message import EmailMessage


def send_shopping_list_email(shopping_list):
    body = "Weekly Shopping List\n\n"

    for item in shopping_list:
        body += (
            f"{item['ingredient']} - "
            f"{item['quantity']} {item['unit']}\n"
        )

    msg = EmailMessage()
    msg["Subject"] = "Weekly Shopping List"
    msg["From"] = "your_email@gmail.com"
    msg["To"] = "your_email@gmail.com"
    msg.set_content(body)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login("your_email@gmail.com", "APP_PASSWORD")
        smtp.send_message(msg)