import PySimpleGUI as sg
import smtplib
import ssl
from email.message import EmailMessage


def connect_to_gmail(username, password):
    # Create a secure SSL context
    context = ssl.create_default_context()

    # Try to log in to server and send email
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls(context=context)  # Secure the connection
        server.login(username, password)
        return server

    except Exception as e:
        # Print any error messages
        print(e)
        server.quit()


def login():
    layout = [
        [sg.Text('Login to Gmail', font=('Helvetica', 15))],
        [sg.Text('E-Mail', size=(10, 1)), sg.InputText()],
        [sg.Text('Password', size=(10, 1)), sg.InputText(password_char='*')],
        [sg.Button('Login', key='gmail_login'), sg.Exit()]

    ]

    window = sg.Window('Login to Gmail').Layout(layout)
    event, values = window.Read()
    window.Close()

    if event is None or event == 'Exit':
        return None

    server = connect_to_gmail(values[0], values[1])

    if server is None:
        sg.Popup('Login failed, try again!', no_titlebar=True)
    else:
        send_email(server)


def send_email(server):
    layout = [
        [sg.Text('Send an E-Mail', font=('Helvetica', 15))],
        [sg.Text('To', size=(10, 1)), sg.InputText(size=(50, 1))],
        [sg.Text('From', size=(10, 1)), sg.InputText(size=(50, 1))],
        [sg.Text('Subject', size=(10, 1)), sg.InputText(size=(50, 1))],
        [sg.Text('Message', size=(10, 1)), sg.Multiline(size=(50, 10))],
        [sg.Button('Send', key='gmail_send'), sg.Exit()]
    ]

    window = sg.Window('Send an E-Mail').Layout(layout)
    event, values = window.Read()
    window.Close()

    if event is None or event == 'Exit':
        return None

    msg = EmailMessage()
    msg['To'] = values[0]
    msg['From'] = values[1]
    msg['Subject'] = values[2]
    msg.set_content(values[3])

    server.send_message(msg)
    server.quit()

    sg.Popup('Message sent!', no_titlebar=True, auto_close=True, auto_close_duration=1)

login()
