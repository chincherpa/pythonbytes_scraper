#!/usr/bin/env python3
# encoding: utf-8

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import requests
from bs4 import BeautifulSoup as bs

with open('data.txt', 'r') as f:
    data = f.read().splitlines()

def get_pythonbytes_ep_desc(ep: int):
    # print(ep)
    url = "https://pythonbytes.fm/episodes/show/" + str(ep)
    page = requests.get(url)

    # print(page.status_code)
    if page.status_code != 200:
        return None, None

    soup = bs(page.text, 'lxml')
    title = soup.title.text
    if title == 'PythonBytes: Page not found (404)':
        return None, None

    html_description = soup.find_all('div', {'class' : 'container full-page-content show-episode-page'})[0]
    return title, html_description


def send_gmail_html(subject, body=''):
    gmail_user = 'lutzcollum@googlemail.com'
    gmail_pwd = data[0]
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = gmail_user
    msg['To'] = gmail_user
    msg.attach(MIMEText(body, 'html'))
    mail = smtplib.SMTP('smtp.gmail.com', 587)
    mail.ehlo()
    mail.starttls()
    mail.login(gmail_user, gmail_pwd)
    mail.sendmail(gmail_user, gmail_user, msg.as_string())
    mail.quit()


if __name__ == '__main__':
    last_ep = int(data[1])
    for ep in range(last_ep + 1, 999):
        title, body = get_pythonbytes_ep_desc(ep)

        if title:
            print(title)
            send_gmail_html(title, body)
        else:
            with open('data.txt', 'w') as f:
                f.write(data[0] + '\n' + str(ep - 1))

            print('last episode:', str(ep - 1))
            print('up to date')
            break
    else:
        print('for else')

    print('\ndone!')
