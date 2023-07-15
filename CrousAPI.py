import requests as rq
import time
import smtplib
import ssl
import json
from email.mime.text import MIMEText
from os import getcwd,path


smtp_address = 'smtp.gmail.com'
smtp_port = 465

with open(file=path.join(getcwd(),"data.json"), mode = "r") as f:
    Data = json.loads(f)
    f.close()


def send_mail(content = "Message Automatique: Visionnez les appart disponibles sur le site du crous"):
    try:
        msg = MIMEText(content)
        msg['Subject'] = "Alerte CROUS, Appartement Disponible"
        msg['From'] = Data["Sender"]
        msg['To'] = ', '.join(Data["to"])
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_address, smtp_port, context=context) as srv:
            srv.login(Data["Sender"],Data["SenderPSW"])
            srv.sendmail(from_addr=Data["Sender"],to_addrs = Data["to"],msg=msg.as_string())
    except Exception as e:
        print(e)
        pass


while 1:
    try:
        r = rq.get("https://trouverunlogement.lescrous.fr/tools/31/search?maxPrice=450&occupationModes=alone&bounds=3.8070597_43.6533542_3.9413208_43.5667088")

        content = r.content
        content = content.decode()

        content = content.replace("</","µ")
        content = content.replace("&","")
        HTMLTable = content.split("µ")

        print(HTMLTable[89])

        if HTMLTable[89] != 'ul>':
            send_mail()
    except KeyboardInterrupt:
        print("Arret en cours....")
        quit(0)
    time.sleep(15*60)


send_mail("Test")