# Reddit-Stock-Bot
*A simple Reddit bot that can be called to proivde information on a specific stock.*

**How does it work?**
---------------------------------

**Call**
The syntax is simple, to retrive information about a stock simply place `!stock AAPL` somewhere in your Reddit comment. `AAPL` can obviously be replaced by and other stock on any exchange (`GOOG`, `AMZN`, `MSFT`, etc).

**Response**
The bot will respond with a host of information on the stock. Below is an example of a response for the comment `!stock AAPL`.

    Up to date stock info for $AAPL (Apple Inc.):
    -----------------------------------
    Price: $119.78
    Open: $119.40
    Change: -0.21 (-0.18%)
    Volume: 25,590,494.00
    Mkt Cap: 638.70B
    Average (50 day): 115.59
    Exchange: NMS
    -----------------------------------
    Don't abuse me, I'm merely a robot! | Source Code | Report Bug | Suggest Feature
    
**Step by step process**

1. Creates a database to store comment IDs (so as not to reply to the same comment twice)
2. Iterates through every comment in /r/all over and over until it finds a comment with `!stock`
3. Checks the database to make sure the ID isn't a duplicate, if not it will add the comment ID to the database
4. Isolates the stock symbol following `!stock` (ex. `!stock AAPL` would isolate AAPL)
5. Gather information about the stock specified via yahoo_finance
6. Reply to the comment with all information pertaining to the specific stock
7. Repeat

**Requirements**

Use `pip` to install the following packages/modules:

1. praw: `pip install praw`

2. yahoo_finance: `pip install yahoo_finance`

3. sqlalchemy: `pip install sqlalchemy`

4. time: (built into Python 3.X)

5. datetime: (built into Python 3.X)

---------------------------------

**Enjoy!**
