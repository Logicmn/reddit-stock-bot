#Reddit username: Pick-a-Stock
#Created by Logicmn

#--------Dependencies---------#
import praw
import time
import datetime
from yahoo_finance import Share

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Sequence, MetaData, create_engine
from sqlalchemy.orm import sessionmaker
#-----------------------------#

#-------OAuth2--------#
r = praw.Reddit('bot1')
#---------------------#

engine = create_engine('sqlite:///new_db.db', echo=True) # Link the database to the SQLAlchemy engine
Session = sessionmaker(bind=engine)
Base = declarative_base()
metadata = MetaData()
session = Session()

class Comment(Base):
    __tablename__ = 'comments'
    id = Column(Integer, Sequence('comment_id_seq'), primary_key=True)
    rcomment = Column(String)
    rtime = Column(String)

    def __repr__(self):
        return "<Comment(rcomment='{0}', rtime='(1)')>".format(self.rcomment, self.rtime)

#-----------------------------------------Check for the keyword !stock------------------------------------------#
def check_condition(c):
    counter = 0
    text = c.body
    tokens = text.split()                # Separate the comment into a word by word list
    if '!stock' in tokens:
        for comment in session.query(Comment.rcomment).order_by(Comment.id.desc()).all():
            if comment == c:
                respond = False
                symbol = None
                print("found duplicate")
                return symbol, respond
        print (c)
        new_comment = Comment(rcomment = c, rtime = datetime.datetime.now())
        session.add(new_comment)
        session.commit()
        respond = True                   # If !stock is in the comment set respond to true
        for word in tokens:
            counter += 1
            if word == '!stock':
                symbol = tokens[counter] # Isolate the stock symbol (word following !stock) by using a counter
                return symbol, respond
    else:
        respond = False
        symbol = None
        return symbol, respond
#---------------------------------------------------------------------------------------------------------------#

#--------------------------------------Respond with appropriate stock info--------------------------------------#
def bot_action(c, symbol):
    stock = Share(symbol)                # Link stock with yahoo_finance module
    print(stock)
    if stock.get_price() == None:
        main()
    head = 'Up to date stock info for **${0}** ({1}):\n\n'.format(symbol.upper(), stock.get_name())
    price = '**Price:** ${0:.2f}\n\n'.format(float(stock.get_price()))
    price_open = '**Open:** ${0:.2f}\n\n'.format(float(stock.get_open()))
    change = '**Change:** {0:.2f} ({1})\n\n'.format(float(stock.get_change()), stock.get_percent_change())
    vol = '**Volume:** {0:,.2f}\n\n'.format(float(stock.get_volume()))
    market_cap = '**Mkt Cap:** {0}\n\n'.format(stock.get_market_cap())
    average = '**Average (50 day):** {0:.2f}\n\n'.format(float(stock.get_50day_moving_avg()))
    exchange = '**Exchange:** {0}\n\n'.format(stock.get_stock_exchange())
    divider = '-----------------------------------------------------------------------------------------\n\n'
    tail = "Don't abuse me, I'm merely a robot! | [Source Code](https://github.com/Logicmn/Reddit-Stock-Bot) " \
           "| [Report Bug](https://www.reddit.com/message/compose/?to=Pick-a-Stock) " \
           "| [Suggest Feature](https://www.reddit.com/message/compose/?to=Pick-a-Stock)"
    c.reply(head + divider + price + price_open + change + vol + market_cap + average + exchange+ divider + tail)
#----------------------------------------------------------------------------------------------------------------#

"""
def write_log(c):
    f = open("log.txt", "w+")
    f.write("{0}\n".format(c))
    f.close
"""



#-----------------------------------------------------Main-------------------------------------------------------#
def main():
    Base.metadata.create_all(engine)
    session.commit()
    """
    new_comment = Comment(rcomment='begin', rtime=datetime.datetime.now())
    session.add(new_comment)
    session.commit()
    """
    while True:
        run = True
        while run:
            counter_two = 0
            for c in r.subreddit('all').stream.comments(): # Iterate through all new comments in /r/all
                counter_two += 1
                #print(counter_two)
                symbol, respond = check_condition(c)       # Check for keyword !stock
                if respond:
                    bot_action(c, symbol)                  # Respond with stock info
                    #time.sleep(600)                       # This might be needed because Reddit prevents new accounts from posting more than 2 ever 10 mins
                    #quit()
                if counter_two >= 1000:                    # Restart iteration after 1000 comments so as not to miss new comments
                    break
#----------------------------------------------------------------------------------------------------------------#

#-----Run the program-----#
if __name__ == "__main__":
    main()
#-------------------------#