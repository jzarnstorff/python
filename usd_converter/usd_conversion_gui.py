#!/usr/bin/python3
import tkinter as tk
from tkinter import ttk
import rates


class Main_App(tk.Frame):
    def __init__(self):
        """Initialize object and create the main frame of the application window"""
        self.root = tk.Tk()
        tk.Frame.__init__(self, self.root)
        self.rate = rates.Rates()

        self.root.title('USD converter')
        self.root.bind('<Return>', self.convert)
        self.create_widgets()
        self.root.resizable(False, False)


    def create_widgets(self):
        """Creates all widgets and places them into main window"""

        # Create label 'USD' for the first row
        self.currency_usd_label = tk.Label(self.root, text='USD:')
        self.currency_usd_label.grid(row=0, sticky='W')

        # Create entry bar and variable to store user input
        self.usd = tk.DoubleVar()
        self.amount = tk.Entry(self.root, width=15, textvariable=self.usd)
        self.amount.grid(row=0, column=1)

        # Create convert button to call the convert method
        self.convert_button = tk.Button(self.root, text='Convert', command=self.convert)
        self.convert_button.grid(row=0, column=2)

        # Create and sort a list of possible country/currency choices
        self.choices = [self.key for self.key in self.rate.exchange_rates]
        self.choices.sort()

        # Create the drop down combobox and select the first choice in self.choices
        self.drop_var = tk.StringVar()
        self.get_exchange_rate(self.choices[0])
        self.combo_box = ttk.Combobox(self.root, width=8, textvariable=self.drop_var, 
                                      values=self.choices, state='readonly')
        self.combo_box.grid(row=1, sticky='W')
        self.combo_box.current(0)
        self.combo_box.bind('<<ComboboxSelected>>', lambda event: self.get_exchange_rate(self.combo_box.get()))

        # Create label and variable which shows the converted currency
        self.total_var = tk.StringVar()
        self.total_label = tk.Label(self.root, textvariable=self.total_var)
        self.total_label.grid(row=1, column=1)

        # Create label 'Last updated'
        self.last_updated_label = tk.Label(self.root, text='Last updated:')
        self.last_updated_label.grid(row=2, sticky='W')

        # Create variable to show when the dictionary was last updated with newest rates
        self.last_updated_var = tk.StringVar()
        self.last_updated_var.set(self.rate.last_updated)
        self.last_update_label = tk.Label(self.root, textvariable=self.last_updated_var)
        self.last_update_label.grid(row=2, column=1)

        # Create update button to update dictionary with current rates
        self.update_button = tk.Button(self.root, text='Update', command=self.update)
        self.update_button.grid(row=2, column=2)


    def update(self):
        """Call update_rates method and print Rates.last_updated variable in GUI"""
        self.rate.update_rates()
        self.last_updated_var.set(self.rate.last_updated)


    def get_exchange_rate(self, value):
        """Get the value of the exchange rate from exchange_rates dictionary"""
        self.exchange_rate = self.rate.exchange_rates.get(value)


    def convert(self, event=None):
        self.root.bind('<Return>', self.convert)
        """Convert entered amount to desired currency"""
        try:
            self.total_var.set(self.usd.get() * float(self.exchange_rate))
        except:
            self.total_var.set('Please enter a number')


    def start(self):
        """Start mainloop"""
        self.root.mainloop()


if __name__ == "__main__":
    Main_App().start()
