import os
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

MAIL_SERVER = 'email.server.local'

FROM = 'email@example.com'
TO = ['email@example.com', 'email2@example.com']
CC = ['email3@example.com', 'email4@example.com']


class EmailSender:
    """ Email sender. """

    def __init__(self, send_from=FROM, send_to=TO, email_server=MAIL_SERVER, cc=CC):
        """ :param str send_from: Sender's e-mail address.
            :param list send_to: List of recipients.
            :param str email_server: Email server address.
            :param list cc: CC recipients e-mail address. """
        self.send_from = send_from
        self.send_to = send_to
        self.email_server = email_server
        self.cc = cc

    def send(self, subject, content=None, attachment_path=None, body_type='html'):
        """ Send email.
                :param str subject: subject line for the email
                :param str content: html body text
                :param str attachment_path: path to text file attachment (if not None)
                :param str body_type: type of body for the e-mail message (e.g., plain, html) """
        if not (self.send_from or self.send_to):
            raise RuntimeError("FROM and TO fields are required for sending email")

        # Construct email
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = self.send_from
        msg['To'] = r', '.join(self.send_to)
        if self.cc:
            msg['CC'] = r', '.join(self.cc)

        # if the attachment_path exists, add the file to the email as an attachment
        if (attachment_path is not None) and (os.path.exists(attachment_path)):
            fp = open(attachment_path, 'rb')
            attachment = MIMEBase('application', "octet-stream")
            attachment.set_payload(fp.read())
            fp.close()
            encoders.encode_base64(attachment)
            filename = os.path.basename(attachment_path)
            attachment.add_header("Content-Disposition", "attachment", filename=filename)
            msg.attach(attachment)

        if content:
            body = MIMEText(content, body_type)
            msg.attach(body)

        # Send MIME message
        for i in range(2):
            try:
                print("Emailing '{0}' to {1}".format(subject, self.send_to + self.cc))
                smtp = smtplib.SMTP(host=self.email_server, timeout=30)
                smtp.sendmail(self.send_from, self.send_to + self.cc, msg.as_string())
                smtp.quit()
                break
            except RuntimeError:
                print("ERROR: Failed to send mail")
