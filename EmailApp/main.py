import os

import yagmail
from dotenv import load_dotenv

load_dotenv()
EMAIL_CLIENT_MAIL_ID = os.getenv('EMAIL_CLIENT_MAIL_ID')
EMAIL_CLIENT_PASSWORD = os.getenv('EMAIL_CLIENT_PASSWORD')

email = yagmail.SMTP(EMAIL_CLIENT_MAIL_ID, EMAIL_CLIENT_PASSWORD)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    recipients = {
        'jishnu@microverselabs.com': 'Jishnu MLs',
        'jishnugs3223@gmail.com': 'Jishnu G S'
    }
    to = ['jishnu@microverselabs.com']
    contents = ['<h1>This is a bigG title!</h1>', '<h3>This is a smaLL title!</h3>']
    bcc = ['albin.shaji@qburst.com']
    
    print('START!')
    email.send(to=to, subject='Test Subject 8', contents=contents, bcc=[], attachments=['test.csv'])
    email.close()

    # email.send(to=to, subject='Test Subject 3', contents=contents)
    print('END!')


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
