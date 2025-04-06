import requests  # type: ignore
import pandas as pd # type: ignore
import datetime
import os

# tkinter imports 
import tkinter as tk
from tkinter import filedialog, messagebox, ttk;

class CardPriceChecker():

    #initalize the class
    def __init__(self):
        #initialize class variables 
        self.card_details = {} # dictionary to store card details

        # Initialize the GUI window with Tkinter 
        self.root = tk.Tk() 

        #set title and geometry of the window 
        self.root.title("MTG Card Price Checker")
        self.root.geometry("1000x1000")

        # create a menu bar 
        self.menuBar = tk.Menu(self.root) 

        # new menu bar option for file operations 
        self.fileMenu = tk.Menu(self.menuBar, tearoff=0)
        self.fileMenu.add_command(label="open", command=self.open_file)# add a command to open a file 

        self.menuBar.add_cascade(menu=self.fileMenu, label="File") # add the file menu to the menu bar
        self.root.config(menu=self.menuBar) # configure the root window to use the menu bar

        self.root.config(bg="gray") #set the background color of the window

        self.root.mainloop() #create the 

    #open a csv file from storage 
    def open_file(self):
        fileName = filedialog.askopenfile(title="Open File", filetypes=(("CSV files", "*.csv"),)) # open a file dialog to select a file, not filetypes expects a tuple hence the , at the end of *.csv
        
        self.card_details = pd.read_csv(fileName) # read the csv file and store it in the card_details dictionary

        print(self.card_details) # print the card details

    def display_card_data(self): 
        #check if attribute 'card_details' already exists 
        if hasattr(self, 'card_details'):
            self.card_details.destroy() # destroy the previous card details if it exists

        cols = list(self.card_details.columns)

        self.card_details = ttk.Treeview(self.root, columns=cols, show='headings') # create a treeview widget to display the card details
        self.card_details.pack(fill=tk.BOTH, expand=True) # pack the treeview widget to fill the window
        #TODO continue here, display the data objects, add scrollbar, searchbar, sort by column, etc. 
        
def searchExact(card_name): # search exact card name
    url = f"https://api.scryfall.com/cards/named?exact={card_name.replace(' ', '+')}"
    response = requests.get(url)

    if response.status_code == 200:
        card_data = response.json()

        card_info = {
            "Name": card_data['name'],
            "Set" : card_data['set_name'],
            "Price (USD)" : card_data['prices']['usd'],
            "Price (Foil)" : card_data['prices']['usd_foil'],
            "Date searched: " : str(datetime.datetime.today()).split()[0]
        }

        df = pd.DataFrame([card_info])
        print(df)

        if os.path.exists('mtgCardPrice.csv'):
            df.to_csv('mtgCardPrice.csv', mode = 'a', index=False, header=False)
        else: 
            df.to_csv('mtgCardPrice.csv', mode = 'a', index=False)
        
    else:
        giveSuggestedNames(card_name)

def giveSuggestedNames(card_name):
    url = f"https://api.scryfall.com/cards/autocomplete?q={card_name.replace(' ','+')}"
    response = requests.get(url)

    if response.status_code == 200:
        suggested = response.json()
        suggestions = "\n".join(suggested['data'])

        print("Do you mean any of these cards? : \n", suggestions)

def main():
    print("Welcome to the MTG Price Checker!")
    # Start a loop that runs until 'exit' is entered
    while True:
        card_name = input("Enter the card name or 'exit' to stop: ")
        
        if card_name.lower() == 'exit':
            print("Exiting the program now")
            break

        searchExact(card_name)

if __name__ == "__main__":
    #main()
    CardPriceChecker()
