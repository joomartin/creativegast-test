import os
from email.mime.application import MIMEApplication
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from os.path import basename
from shared.TestData import TestData as data

fromAddr = 'dev.gr33nt3ch@gmail.com'
toAddr = 'ricsi.sikulitest@gmail.com, tamas.horvath@prosupport.io, ban.adrian.gt@gmail.com'
#toAddr = 'ricsi.sikulitest@gmail.com, ban.adrian.gt@gmail.com'


def sendReport(filePath):
    html = open(filePath)
    msg = msg = MIMEMultipart()
    msg['From'] = fromAddr
    msg['To'] = toAddr
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

    debug = False
    if debug:
        print(msg.as_string())
    else:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login('dev.gr33nt3ch@gmail.com', 'ucepkwvwjkipford')
        text = msg.as_string('html')

        server.sendmail(fromAddr, toAddr.split(','), text)
        server.quit()

