import requests  # type: ignore
import pandas as pd # type: ignore
import datetime
import os

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
    main()

