import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase

def send_email(subject, file_path):
    """ Send email with files attached"""

    from_addr = ""
    to_addr = ""

    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = from_addr
    msg['To'] = ', '.join(to_addr)

    part = MIMEBase('application', "octet-stream")
    part.set_payload(open(file_path, "r").read())

    part.add_header('Content-Disposition', 'attachment; filename=saleslog')

    msg.attach(part)

    server = smtplib.SMTP("mail.gmx.ch")
    server.sendmail(from_addr,to_addr, msg.as_string())

if __name__ == "__main__":
    send_email("test_email","send_email.py")
