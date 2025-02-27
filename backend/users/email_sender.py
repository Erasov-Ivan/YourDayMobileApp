from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import aiosmtplib
import logging


class Sender:
    def __init__(self, login: str, password: str):
        self.login = login
        self.password = password
        self.server = aiosmtplib.SMTP(hostname='smtp.mail.ru', port=25)

    async def run_server(self):
        await self.server.connect()
        await self.server.login(self.login, self.password)
        logging.info("Connected to SMTP server")

    async def send_message(self, subject: str, message: str, send_to: str):
        try:
            msg = MIMEMultipart()
            msg['From'] = self.login
            msg['To'] = send_to
            msg['Subject'] = subject

            msg.attach(MIMEText(message, 'plain'))
            await self.server.sendmail(
                self.login,
                send_to,
                msg.as_string()
            )
            logging.info(f'Sent message to {send_to}')
        except Exception as e:
            logging.error(e)
            raise Exception("Error while sending message, try again")

    async def send_code(self, send_to: str, code: str):
        subject = 'Код подтверждения YourDay'
        message = f'Ваш код: {code}'
        await self.send_message(subject=subject, message=message, send_to=send_to)

    async def quit(self):
        await self.server.quit()
