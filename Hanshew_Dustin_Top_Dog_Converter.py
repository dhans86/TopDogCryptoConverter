# Top Dog Crypto Converter
# Python Project
# Indroduction to Software Development
# Ivy Tech Community College
# 12.14.21
# Dustin Hanshew
# Professor Carver


# My project will allow you to show the fiat rate conversion for USD, EUR, or XAU(Gold) to BTC, SHIB, DOGE, or ELON


# imports from the api, tkinter, and json
from django.core.mail import message
from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
from tkinter import *
import tkinter as tk
from tkinter import ttk
from functools import partial

# Real time data from currency conversion using coinmarketcap api
class CurrencyConverter:

    def validateLogin(username, password):
        global tkWindow
        print("username entered :", username.get())
        print("password entered :", password.get())
        if username == '' or password == '':
            message.set("fill the empty field!!!")
        else:
            if username == "username" and password == "password":
                message.set("Login success")
            else:
                message.set("Wrong username or password!!!")

    # window for username and password
    tkWindow = Tk()
    tkWindow.geometry('1000x300')
    tkWindow.title('Top Dog Converter Log In Form')

    #instructions label
    instructionsLabel = Label(tkWindow, text="Welcome to Top Dog Converter! Enter in the username and password to continue. "
                                             "Username is: username and Password is: password.").grid(row=16, column=2)
    # username label and text entry box
    usernameLabel = Label(tkWindow, text="User Name").grid(row=0, column=0)
    username = StringVar()
    usernameEntry = Entry(tkWindow, textvariable=username).grid(row=0, column=1)
    # password label and password entry box
    passwordLabel = Label(tkWindow, text="Password").grid(row=1, column=0)
    password = StringVar()
    passwordEntry = Entry(tkWindow, textvariable=password, show='*').grid(row=1, column=1)

    validateLogin = partial(validateLogin, username, password)

    # login button
    loginButton = Button(tkWindow, text="Login", command=validateLogin).grid(row=4, column=0)

    # creating SHIB INU image
    photo1 = PhotoImage(file=r"shiba.png")
    photoimage1 = photo1.subsample(3, 3)
    shib_image = tk.Label(tkWindow, image=photoimage1)
    shib_image.place(x=30, y=150)

    # creating DOGECOIN image
    photo2 = PhotoImage(file=r"dogecoin.png")
    photoimage2 = photo2.subsample(3, 3)
    doge_image = tk.Label(tkWindow, image=photoimage2)
    doge_image.place(x=410, y=150)

    photo3 = PhotoImage(file=r"btc_image.png")
    photoimage3 = photo3.subsample(4, 4)
    btc_image = tk.Label(tkWindow, image=photoimage3)
    btc_image.place(x=900, y=150)
    validateLogin()
    tkWindow.mainloop()

    # defining the fiat amount
    def convert(crypto, fiat, amount):

        # url for coinmarket cap api
        url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
        parameters = {
            'symbol': crypto,
            'convert': fiat
        }
        headers = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': '4500cda3-9aea-44d5-8e16-c2bb712d74e4',

        }

        session = Session()
        session.headers.update(headers)
        int_amount = amount

        try:
            response = session.get(url, params=parameters)
            data = json.loads(response.text)
            amount = round(data['data'][crypto]['quote'][fiat]['price'] * int_amount, 2)
        except (ConnectionError, Timeout, TooManyRedirects, KeyError) as e:
            print(e)
            return -1

        return amount

    def get(self):
        pass


# Making the tkinter window
class App(tk.Tk):

    def __init__(self):
        tk.Tk.__init__(self)
        self.title = 'Top Dog Crypto Converter'
        # setting window
        self.configure(background='#856ff8')
        self.geometry("520x400")

        # Title
        self.title = Label(self, text="Top Dog Crypto Converter", fg='white', bg='#2D496D', borderwidth=3)
        self.title.config(font=('Helvetica', 15, 'bold'))
        self.title.place(x=100, y=5)

        # label
        self.crypto_label = Label(self, text='Crypto Currency', fg='white', bg='#2D496D', borderwidth=3)
        self.crypto_label.config(font=('Helvetica', 13, 'bold'))
        self.fiat_label = Label(self, text='Fiat Currency', fg='white', bg='#2D496D', borderwidth=3)
        self.fiat_label.config(font=('Helvetica', 13, 'bold'))

        # retrieve list of currencies from cryptocurrency.txt
        with open('cryptocurrency.txt') as f:
            list = [line.split()[0] for line in f]

        currList = []
        temp = []
        for i in list:
            temp.append(i)
            if i == 'Fiat:':
                currList.append(temp)
                temp = []
        if temp:
            currList.append(temp)

        list_crypto_currency = currList[0]
        list_crypto_currency = list_crypto_currency[1:-1]
        fiat_list_currency = currList[1]

        # Dropdown
        self.crypto_currency_variable = StringVar(self)
        self.crypto_currency_variable.set("SHIB")
        self.fiat_currency_variable = StringVar(self)
        self.fiat_currency_variable.set("USD")

        font = ("Courier", 12, "bold")
        self.option_add('*TCombobox*Listbox.font', font)
        self.cryto_currency_dropdown = ttk.Combobox(self, textvariable=self.crypto_currency_variable, values=list_crypto_currency, font=font, state='readonly', width=12, justify=tk.CENTER)
        self.fiat_currency_dropdown = ttk.Combobox(self, textvariable=self.fiat_currency_variable, values=fiat_list_currency, font=font, state='readonly', width=12, justify=tk.CENTER)

        # Entry box
        valid = (self.register(self.restrictNumberOnly), '%d', '%P')
        self.amount_field = Entry(self, bd=3, relief=tk.RIDGE, justify=tk.CENTER, validate='key', validatecommand=valid)
        self.converted_amount_field = Label(self, text='', fg='black', bg='white', relief=tk.RIDGE, justify=tk.CENTER, width=17, borderwidth=3)
        # Convert button
        self.convert_button = Button(self, text="Convert", fg="black", command=self.function)
        self.convert_button.config(font=('Courier', 10, 'bold'))
        self.convert_button.place(x=225, y=135)

        # Placement
        self.crypto_label.place(x=24, y=90)
        self.fiat_label.place(x=337, y=90)
        self.cryto_currency_dropdown.place(x=30, y=120)
        self.fiat_currency_dropdown.place(x=335, y=120)
        self.amount_field.place(x=37, y=150)
        self.converted_amount_field.place(x=342, y=150)


        # Exit button
        self.exit_button = Button(self, text="Exit", fg="black", command=self.destroy)
        self.exit_button.place(x=245, y=325)

    # defining the exit button
    def Close(self):
        self.destroy()

    # setting up protection in entry field (only numbers can be entered)
    def restrictNumberOnly(action, string):
        regex = re.compile(r"[0-9,]*?(\.)?[0-9,]*$")
        result = regex.match(string)
        return string == "" or (string.count('.') <= 1 and result is not None)

    # defining the fiat and crypto conversion amount functions
    def function(self):
        amount = float(self.amount_field.get())
        crypto_curr = self.crypto_currency_variable.get()
        fiat_curr = self.fiat_currency_variable.get()

        if crypto_curr == fiat_curr:
            converted_amount = amount

        else:

            converted_amount = CurrencyConverter.convert(crypto_curr, fiat_curr, amount)
            if converted_amount == -1:
                self.converted_amount_field.config(text='invalid currency code')
            else:
                converted_amount = round(converted_amount, 2)

                self.converted_amount_field.config(text=str(converted_amount))


# running the loop
if __name__ == '__main__':
    App()
    mainloop()
