# MTG Card Price Checker

A Python desktop application using Tkinter that allows users to search for Magic: The Gathering cards and view up-to-date prices (including foil prices). Also shows a list of popular cards.

---

## Features

- Search for any Magic: The Gathering card by name
- View current price and foil price
- See card set information and EDHREC rank (if available)
- Display a list of popular cards
- Intuitive, user-friendly GUI built with Tkinter

---

## Getting Started

### Requirements

- Python 3.9+
- `requests` (for API calls)
- `tkinter` (usually comes with Python)
- `ttk` (used for styling widgets)
- `threading` (used for multithreading)

### Installation

1. Clone the repository:

```bash
git clone https://github.com/your-username/mtg-card-price-checker.git
cd mtg-card-price-checker
```

2. optional: create a virtual environment
```bash
python -m venv venv
venv\Scripts\activate
```

3. install dependencies 
```bash
pip install -r requirements.txt
```

4. Run the app 
```bash
cd dependencies
python main.py
```