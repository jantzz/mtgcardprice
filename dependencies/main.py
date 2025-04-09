import requests  # type: ignore
import pandas as pd # type: ignore
import threading
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
        self.current_card = {} # dictionary to store the current card details

        # Initialize the GUI window with Tkinter 
        self.root = tk.Tk() 

        #set title and geometry of the window 
        self.root.title("MTG Card Price Checker")
        self.root.geometry("1000x1000")

        self.format_page()

        self.root.after(100, self.start_fetching) # call the get_populars function after 100 milliseconds

        self.root.mainloop() #create the main loop for the window 

    def format_page(self) :
        #TODO create function to store all the widgets and stuff so that it looks better
        # create a menu bar 
        self.menuBar = tk.Menu(self.root) 

        # new menu bar option for file operations 
        self.fileMenu = tk.Menu(self.menuBar, tearoff=0)
        self.fileMenu.add_command(label="open", command=self.open_file)# add a command to open a file 

        self.menuBar.add_cascade(menu=self.fileMenu, label="File") # add the file menu to the menu bar
        self.root.config(menu=self.menuBar) # configure the root window to use the menu bar

        self.root.config(bg="gray") #set the background color of the window

        #Create the frames, but leave empty so that it can be filled out later 
        self.top_frame = tk.Frame(self.root) 
        self.top_frame.pack(side="top", fill=tk.X) 

        #separator #1 
        self.top_separator = ttk.Separator(self.root, orient="horizontal")
        self.top_separator.pack(side="top", fill=tk.X)

        #search bar frame
        self.search_frame = tk.Frame(self.root)
        self.search_frame.pack(side="top", fill=tk.X) 

        # label for searching cards: 
        self.search_bar_frame = tk.Frame(self.search_frame) # create a new frame for the search bar
        self.search_bar_frame.grid(row=0, column=0, sticky="nsew") # pack the frame to fill the window

        #label to say Search for a card: 
        self.search_label = tk.Label(self.search_bar_frame, text="Search for a card:", font=("Arial", 16))
        self.search_label.grid(row=0, column=0, padx=2, pady=2) # pack the label to fill the window
        
        #entry for searching cards
        self.search_entry = tk.Entry(self.search_bar_frame, font=("Arial", 16)) # create an entry widget for the card name
        self.search_entry.grid(row=0, column=1, padx=2, pady=2) # pack the entry widget to fill the window

        # button to start search 
        self.search_button = tk.Button(self.search_bar_frame, text="Search", command=self.searchCard) # create a button to search for the card
        self.search_button.grid(row=0, column=2, padx=2, pady=2) # pack the button to fill the window

        self.in_search_separator = ttk.Separator(self.search_frame, orient="vertical")
        self.in_search_separator.grid(row=0, column=1, sticky="ns", padx=2, pady=2) # pack the separator to fill the window

        #frame for a single card 
        self.single_card_frame = tk.Frame(self.search_frame)
        self.single_card_frame.grid(row=0, column=2, sticky="nsew") # pack the frame to fill the window

        #separator #3
        self.popular_separator = ttk.Separator(self.root, orient="horizontal")
        self.popular_separator.pack(side="top", fill=tk.X)

        #popular cards frame 
        self.popular_frame = tk.Frame(self.root) 
        self.popular_frame.pack(side="top", fill=tk.X)

        #progress bar 
        self.progress_bar = ttk.Progressbar(self.popular_frame, orient="horizontal", mode="indeterminate") # create a progress bar widget
        self.progress_bar.grid(row=1, column=1) # pack the progress bar to fill the window
        self.progress_bar.grid_remove() #hide the progress bar at first 

        #separator #4
        self.file_separator = ttk.Separator(self.root, orient="horizontal")
        self.file_separator.pack(side="top", fill=tk.X)

        #file data read in frame
        self.file_frame = tk.Frame(self.root)
        self.file_frame.pack(side="top", fill=tk.X) 

    #search for a specific card using the API 
    def searchCard(self): #TODO use multithreading as well for the API call here
        card_name = self.search_entry.get() # get the card name from the entry widget
        card_name = card_name.strip() # remove any leading or trailing whitespace

        if card_name == "":
            messagebox.showwarning("Warning", "Please enter a card name")
            return

        url = f"https://api.scryfall.com/cards/named?exact={card_name.replace(' ', '+')}" # create the URL for the API request
        response = requests.get(url) # make a GET request to the API
        card_info = {} # initialize the card_info dictionary

        if response.status_code == 200:
            card_data = response.json()

            card_info = {
                "Name": card_data['name'],
                "Set" : card_data['set_name'],
                "Price (USD)" : card_data['prices']['usd'],
                "Price (Foil)" : card_data['prices']['usd_foil'],
                "Date searched: " : str(datetime.datetime.today()).split()[0]
            }

            df = pd.DataFrame([card_info]) # create a dataframe from the card info dictionary

            if os.path.exists('mtgCardPrice.csv'):
                df.to_csv('mtgCardPrice.csv', mode = 'a', index=False, header=False)
            else: 
                df.to_csv('mtgCardPrice.csv', mode = 'a', index=False)

        self.display_single_Card(card_info)
    
    def display_single_Card(self, data: dict): #data expected to be a list object 

        # Clear previous card info
        for widget in self.single_card_frame.winfo_children():
            widget.destroy()

        if data == {}: 
            self.error_label = tk.Label(self.single_card_frame, text="Card not found", font=("Arial", 16), fg="red") # create a label for the card not found error
            self.error_label.grid(row=0, column=0, sticky="nsew") # pack the label to fill the window
            return # return if the card is not found
        
        self.card_name_label = tk.Label(self.single_card_frame, text=data['Name'], font=("Arial", 16)) # create a label for the card name
        self.card_name_label.grid(row=0, column=0, sticky="nsew") # pack the label to fill the window

        self.card_set_label = tk.Label(self.single_card_frame, text=data['Set'], font=("Arial", 16)) # create a label for the card set
        self.card_set_label.grid(row=1, column=0, sticky="nsew") # pack the label to fill the window

        self.card_price_label = tk.Label(self.single_card_frame, text=data['Price (USD)'], font=("Arial", 16)) # create a label for the card price
        self.card_price_label.grid(row=2, column=0, sticky="nsew") # pack the label to fill the window

        self.card_foil_label = tk.Label(self.single_card_frame, text=data['Price (Foil)'], font=("Arial", 16)) # create a label for the card foil price
        self.card_foil_label.grid(row=3, column=0, sticky="nsew") # pack the label to fill the window
        
        if(data['Date searched: '] != None):
            self.card_date_label = tk.Label(self.single_card_frame, text=data['Date searched: '], font=("Arial", 16))
            self.card_date_label.grid(row=4, column=0, sticky="nsew") # pack the label to fill the window
        elif data['edhrec_rank'] != None:
            self.card_date_label = tk.Label(self.single_card_frame, text=data['edhrec_rank'], font=("Arial", 16))
            self.card_date_label.grid(row=4, column=0, sticky="nsew")
            
    #display the card data in table format after reading from csv
    def display_card_data(self): 
        #check if attribute 'card_details' already exists 
        for widget in self.file_frame.winfo_children():
            widget.destroy()

        cols = self.card_details.columns.tolist() # get the columns of the card details dataframe
        values = self.card_details.values.tolist() # get the values of the card details dataframe

        self.display_card_info = ttk.Treeview(self.file_frame, columns=cols, show='headings') # create a treeview widget to display the card details

        for col in cols: 
            self.display_card_info.heading(col, text=col) # set the heading of the columns
            self.display_card_info.column(col, anchor='center') # set the column to be centered
        
        for val in values: 
            self.display_card_info.insert('', 'end', values=val) # insert the values into the treeview widget
            self.display_card_info

        self.file_frame.columnconfigure(0, weight=1)
        self.file_frame.rowconfigure(0, weight=1)

        self.card_scrollbar = ttk.Scrollbar(self.file_frame, orient="vertical", command=self.display_card_info.yview) # create a vertical scrollbar for the treeview widget
        self.display_card_info.configure(yscrollcommand=self.card_scrollbar.set) # configure the treeview widget to use the scrollbar
        
        self.card_label = tk.Label(self.file_frame, text="Cards from file", font=("Arial", 16)) # create a label for the card details
        self.card_label.grid(row=0, column=0, sticky="nsew") # pack the label to fill the window

        self.card_separator = ttk.Separator(self.file_frame, orient="horizontal") # create a separator for the card details
        self.card_separator.grid(row=1, column=0, sticky="ew")

        self.display_card_info.grid(row=2, column=0, sticky="nsew") # pack the treeview widget to fill the window
        self.card_scrollbar.grid(row=2, column=1, sticky="ns") # pack the scrollbar to the right of the treeview widget
    
    #display popular cards from the API 
    def display_popular_cards(self):
        # check if the popular cards attribute exists
        for widget in self.popular_frame.winfo_children():
            widget.destroy()

        self.pop_cards = ttk.Treeview(self.popular_frame, columns=('Name', 'Set', 'Price (USD)', 'Price (Foil)', 'EDHREC Rank'), show='headings') # create a treeview widget to display the popular cards

        #set headings of columns so that its visible
        for col in ('Name', 'Set', 'Price (USD)', 'Price (Foil)', 'EDHREC Rank'):
            self.pop_cards.heading(col, text=col)

        for card in self.popular_cards:
            card_name = card['name']
            card_set = card['set_name']
            card_price = card['prices']['usd']
            card_price_foil = card['prices']['usd_foil']
            card_rank = card['edhrec_rank']
            
            self.pop_cards.insert('', 'end', values=(card_name, card_set, card_price, card_price_foil, card_rank)) # insert the values into the treeview widget
        
        self.popular_frame.columnconfigure(0, weight=1)
        self.popular_frame.rowconfigure(0, weight=1)

        self.popular_cards_scrollbar = ttk.Scrollbar(self.popular_frame, orient="vertical", command=self.pop_cards.yview) # create a vertical scrollbar for the treeview widget
        self.pop_cards.configure(yscrollcommand=self.popular_cards_scrollbar.set) # configure the treeview widget to use the scrollbar

        self.pop_label = tk.Label(self.popular_frame, text="Popular Cards", font=("Arial", 16)) # create a label for the popular cards
        self.pop_label.grid(row=0, column=0, sticky="nsew") # pack the label to fill the window

        self.pop_separator = ttk.Separator(self.popular_frame, orient="horizontal") # create a separator for the popular cards
        self.pop_separator.grid(row=1, column=0, sticky="ew") # pack the separator to fill the window

        self.pop_cards.grid(row=2, column=0, sticky="nsew") # pack the treeview widget to fill the window
        self.popular_cards_scrollbar.grid(row=2, column=1, sticky="ns") # pack the scrollbar to the right of the treeview widget

    def start_fetching(self):
        # Start a new thread to fetch the popular cards
        self.progress_bar.pack() # show the progress bar
        self.progress_bar.start() # start the progress bar animation

        threading.Thread(target=self.get_populars).start()

    def get_populars(self):
        url = "https://api.scryfall.com/cards/search?q=%2A&order=edhrec&dir=asc&unique=cards"
        print("trying to get popular cards")
        response = requests.get(url) # make a GET request to the API

        if response.status_code == 200:
            data = response.json()['data']# get the data from the response
            self.popular_cards = data
            self.root.after(0, self.on_fetched) # call the on_fetched function after 0 milliseconds
            
        else:
            print("Error fetching popular cards:", response.status_code)
            messagebox.showerror("Error", "Error fetching popular cards") # show an error message if the request fails

    def on_fetched(self):
        self.progress_bar.stop()
        self.display_popular_cards() # call the display_popular_cards function to display the popular cards
        self.progress_bar.pack_forget() # hide the progress bar

    #open a csv file from storage 
    def open_file(self):
        fileName = filedialog.askopenfile(title="Open File", filetypes=(("CSV files", "*.csv"),)) # open a file dialog to select a file, not filetypes expects a tuple hence the , at the end of *.csv
        
        self.card_details = pd.read_csv(fileName) # read the csv file and store it in the card_details dictionary

        print(self.card_details) # print the card details
        self.display_card_data() # call the display_card_data function to display the card details

    
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
