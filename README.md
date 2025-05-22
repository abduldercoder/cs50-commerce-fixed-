# CS50W Project 2: Commerce

This is a Django-based eBay-style auction web application built for Harvard’s **CS50 Web Programming with Python and JavaScript** course (Project 2: Commerce).

🎥 **Demo Video:** [Watch on YouTube](https://youtu.be/z-CQdcSCAX4)

---

## 📦 Features

- **User Authentication**
  - Register, log in, and log out
  - Only logged-in users can create listings, place bids, or comment

- **Creating Listings**
  - Authenticated users can create new auction listings
  - Listings include title, description, starting bid, category, and optional image

- **Bidding**
  - Logged-in users can place bids
  - Bid must be higher than the current highest bid or the starting bid

- **Watchlist**
  - Add or remove any listing from your watchlist
  - Watchlist page shows all listings the user is watching

- **Categories**
  - Listings are categorized and browsable by category via the navigation bar

- **Listing Page**
  - Displays current highest bid, item info, image, seller, and comments
  - Authenticated users can comment or bid
  - Listing creator can close or reopen the auction
  - Once closed, the highest bidder is shown as the winner

- **Comments**
  - Logged-in users can post comments on listings
  - Comments are timestamped and shown below the listing
 
  
---

## 🚀 How to Deploy Locally

1. **Clone the repo**

```bash
git clone https://github.com/abduldercoder/cs50w-commerce.git
cd cs50w-commerce
Create a virtual environment
python3 -m venv venv
source venv/bin/activate
Install requirements
pip install -r requirements.txt
If you don’t have a requirements.txt, generate one with:
pip freeze > requirements.txt
Run migrations
python manage.py migrate
Run the server
python manage.py runserver
Then open http://127.0.0.1:8000 in your browser.
