import os
from email import encoders
from email.mime.application import MIMEApplication
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from os.path import basename
from shared.TestData import TestData as data
import os
from dotenv import load_dotenv
load_dotenv()


separator = ', '

def sendReport(filePath):
    html = open(filePath)
    msg = msg = MIMEMultipart()
    #msg['From'] = os.environ.get('FROMADDRESS')
    #msg['To'] = separator.join(os.environ.get('TOADDRESSES'))
    #msg['To'] = toAddresses
    msg['Subject'] = "CG Teszt Report"

    msg.attach(MIMEText(html.read(), 'html'))

    with open(filePath, "rb") as fil:
        part = MIMEApplication(
            fil.read(),
            Name=basename(filePath)
        )

        part['Content-Disposition'] = 'attachment; filename="%s"' % basename(filePath)
        msg.attach(part)

    path = './/screenShots//' + data.Screenshot['Name']
    for filename in os.listdir(path):
        if filename.endswith('.png'):
            with open(os.path.join(path, filename), 'rb') as f:
                img_data = f.read()
                image = MIMEImage(img_data)
                image.add_header('Content-Disposition', 'attachment',
                                 filename=filename)
                msg.attach(image)

    attach_file_name = './/screenShots//' + data.Screenshot['Name'] + '//log_entries.txt'
    with open(attach_file_name, "rb") as fil:
        part = MIMEApplication(
            fil.read(),
            Name=basename(attach_file_name)
        )

        part['Content-Disposition'] = 'attachment; filename="%s"' % basename(attach_file_name)
        msg.attach(part)

    debug = False
    if debug:
        print(msg.as_string())
    else:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(os.environ.get('FROMADDRESS'), os.environ.get('FROMADDRESSPASS'))
        text = msg.as_string('html')

        server.sendmail(os.environ.get('FROMADDRESS'), os.environ.get('TOADDRESSES').split(','), text)
        server.quit()

