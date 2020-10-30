from email.mime.text import MIMEText
import smtplib


fromAddr = 'dev.gr33nt3ch@gmail.com'
toAddr = 'ricsi.sikulitest@gmail.com'
#ide tömb megy majd a cél email címekkel


html = open('reports/SeleniumPythonTestSummary.html')
msg = MIMEText(html.read(), 'html')
msg['From'] = fromAddr
msg['To'] = toAddr
msg['Subject'] = "CG Teszt Report"

debug = False
if debug:
    print(msg.as_string())
else:
    server = smtplib.SMTP('smtp.gmail.com',587)
    server.starttls()
    server.login('dev.gr33nt3ch@gmail.com', 'ucepkwvwjkipford')
    text = msg.as_string()
    server.sendmail(fromAddr, toAddr, text)
    server.quit()