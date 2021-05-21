from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from os.path import basename

fromAddr = 'dev.gr33nt3ch@gmail.com'
toAddr = 'ricsi.sikulitest@gmail.com, tamas.horvath@prosupport.io, ban.adrian.gt@gmail.com'
#ide tömb megy majd a cél email címekkel

def sendReport(filePath,):
    html = open(filePath)
    msg =  msg = MIMEMultipart()
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

    debug = False
    if debug:
        print(msg.as_string())
    else:
        server = smtplib.SMTP('smtp.gmail.com',587)
        server.starttls()
        server.login('dev.gr33nt3ch@gmail.com', 'ucepkwvwjkipford')
        text = msg.as_string('html')
        server.sendmail(fromAddr, toAddr.split(','), text)
        server.quit()


        '''
         msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = COMMASPACE.join(send_to)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject

    msg.attach(MIMEText(text))

    for f in files or []:
        with open(f, "rb") as fil:
            part = MIMEApplication(
                fil.read(),
                Name=basename(f)
            )
        # After the file is closed
        part['Content-Disposition'] = 'attachment; filename="%s"' % basename(f)
        msg.attach(part)
        '''