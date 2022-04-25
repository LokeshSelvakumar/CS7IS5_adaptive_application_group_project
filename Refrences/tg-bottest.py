from tkinter import E
import telebot
import yfinance as yf
from yahoo_fin import stock_info as si
from telebot.callback_data import CallbackData, CallbackDataFilter
from telebot import types
import requests
import json

bot = telebot.TeleBot("5356735903:AAGIUWFapkm7AcpAhyV44n-yojw1Sa3CNl0")

tickers = si.tickers_sp500()
user_dict = {}
score_dict = {'A':1,'B':2,'C':3,'D':4,'E':5}

import re
def valid_email(email):
  return bool(re.search(r"^[\w\.\+\-]+\@[\w]+\.[a-z]{2,3}$", email))

class User:
    def __init__(self, name,id):
        self.user_id = id
        self.name = name
        self.age = None
        self.sex = None
        self.email = None
        self.salary = None
        self.stocksList = []
        self.watchList = []
        self.score_risk = 0
        self.avail_capital = []

    def to_string(self):
        return {"user_id":self.user_id, "name":self.name,"age":self.age,"sex":self.sex,"email":self.email,"salary":self.salary,"stocksList":self.stocksList,"watchList":self.watchList,"score_risk":self.score_risk,"avail_capital":self.avail_capital}

    def test(self):
        return {"user_id":12354, "name":"test_yatheen","age":23,"sex":"MAle","email":"yatheen@mock.com","salary":"4522","stocksList":[],"watchList":[],"score_risk":7,"avail_capital":1300}

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    print(message.chat.id)
    response = bot.reply_to(message, "Howdy, Nice to Meet You!!\nWhat is your name?")
    bot.register_next_step_handler(response, process_name_step)

def process_name_step(message):
    try:
        chat_id = message.chat.id
        name = message.text
        user = User(name,chat_id)
        user_dict[chat_id] = user
        # response = requests.post("http://192.168.0.157:8001/user/createUser/",json = user.test())
        msg = bot.reply_to(message, 'How old are you?')
        # bot.register_next_step_handler(msg, process_age_step)
    except Exception as e:
        bot.reply_to(message, 'oooops')

def process_age_step(message):
    try:
        chat_id = message.chat.id
        age = message.text
        if not age.isdigit():
            msg = bot.reply_to(message, 'Age should be a number. How old are you?')
            bot.register_next_step_handler(msg, process_age_step)
            return
        user = user_dict[chat_id]
        user.age = age
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add('Male', 'Female','Other')
        msg = bot.reply_to(message, 'What is your gender', reply_markup=markup)
        bot.register_next_step_handler(msg, process_sex_step)
    except Exception as e:
        bot.reply_to(message, 'oooops')


def process_sex_step(message):
    try:
        chat_id = message.chat.id
        sex = message.text
        user = user_dict[chat_id]
        if (sex == u'Male') or (sex == u'Female'):
            user.sex = sex
        else:
            user.sex = "Other"
        # bot.send_message(chat_id, 'Nice to meet you ' + user.name + '\n Age:' + str(user.age) + '\n Sex:' + user.sex)
        # bot.send_message(chat_id, "You can check the real-time price of any stocks. Try 'price ticker_name'")
        msg = bot.reply_to(message,'What is your email-id?')
        bot.register_next_step_handler(msg, process_email_step)
    except Exception as e:
        bot.reply_to(message, 'oooops')

def process_email_step(message):
    try:
        chat_id = message.chat.id
        email = message.text
        user = user_dict[chat_id]
        
        #Validate Email Here.
        if valid_email(email):
            user.email = email
        else:
            msg = bot.reply_to(message,'Can\'t you even give a proper email id?',reply_markup=markup)
            bot.register_next_step_handler(msg, process_email_step)
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add('<$40000', '$50000-$100000','>$100000')
        msg = bot.reply_to(message,'What is your salary range?',reply_markup=markup)
        bot.register_next_step_handler(msg, process_salary_step)
    except Exception as e:
        bot.reply_to(message, 'oooops')


def process_salary_step(message):
    try:
        chat_id = message.chat.id
        salary = message.text
        user = user_dict[chat_id]
        user.salary = salary
        msg = bot.reply_to(message, 'How much are you interested to invest?')
        bot.register_next_step_handler(msg, process_avail_capital)
    except Exception as e:
        bot.reply_to(message, 'problem with process_salary_step')

def process_avail_capital(message):
    try:
        chat_id = message.chat.id
        user = user_dict[chat_id]
        if not message.text.isdigit():
            msg = bot.reply_to(message, 'It should be a number. Enter the amount')
            bot.register_next_step_handler(msg, process_avail_capital)
            return
        user.avail_capital = message.text
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add('Yes', 'No')
        msg = bot.reply_to(message, 'Have you invested in stocks?',reply_markup=markup)
        bot.register_next_step_handler(msg, check_portfolio)
    except Exception as e:
        bot.reply_to(message, 'oooops')

def check_portfolio(message):
    try:
        chat_id = message.chat.id
        text = message.text
        user = user_dict[chat_id]
        user.stock_invested = text
        if text == 'Yes':
            msg = bot.reply_to(message, 'Lets create a portfolio for you \n\
To add stock to your portfolio follow the format: <stock_symbol> <units>\n eg: amzn 100\n\
Please refer the stock symbols in the link below')
            bot.send_message(chat_id,"https://www.slickcharts.com/sp500",parse_mode='HTML')
            bot.register_next_step_handler(msg, add_portfolio)
        elif text == 'No':
            msg = bot.reply_to(message,"what are the stocks you wish to add to your watchlist?\n\
Reply 'N' to skip this step or try adding symbol name one by one. Eg: amzn")
            bot.register_next_step_handler(msg,add_watchList)
    except:
        bot.reply_to(message,"problem with port folio")
        

def add_portfolio(message):
    try:
        chat_id = message.chat.id
        user = user_dict[chat_id]
        if message.text != 'N':
            print("printing before splti")
            print(message.text.split()[0])
            validationBool = validate_ticker(message.text.split()[0])
            if validationBool:
               user.stocksList.append(message.text)
               bot.send_message(chat_id, 'stock added to portfolio')
               msg = bot.reply_to(message, 'to stop adding stock press N')
               bot.register_next_step_handler(msg, add_portfolio)
            else:
               msg = bot.reply_to(message, 'Stock Symbol is not valid. Try adding a valid one')
               bot.register_next_step_handler(msg, add_portfolio)

        else:
            msg = bot.reply_to(message,"what are the stocks you wish to add to your watchlist?\n\
Reply 'N' to skip this step or try adding symbol name one by one. Eg: amzn")
            bot.register_next_step_handler(msg,add_watchList)
#           
    except:
         bot.send_message("problem with stock price")


def add_watchList(message):
    try:
        user = user_dict[message.chat.id]
        if message.text != 'N':
            validationBool = validate_ticker(message.text.split()[0])
            if validationBool:
               user.watchList.append(message.text)
               msg = bot.reply_to(message, "to stop adding to watchList reply 'N'")
               bot.register_next_step_handler(msg, add_watchList)
            else:
               msg = bot.reply_to(message, 'Stock Symbol is not valid. Try adding a valid one')
               bot.register_next_step_handler(msg, add_watchList)

        else:
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            markup.add('HealthCare', 'Tech','Automobile','Sports','Energy Source')
            msg = bot.reply_to(message,"what is the sector you are interested in?", reply_markup=markup)
            bot.register_next_step_handler(msg, save_sector)
        
    except:
        bot.reply_to(message, "problem with watchList")

def save_sector(message):
    try:
        print(message.text)
        user = user_dict[message.chat.id]
        user.sector = message.text
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add('A', 'B','C','D','E')
        msg = bot.send_message(message.chat.id,"Over the next several years, you expect your annual income to:\n\
A) Decrease substantially\nB) Decrease moderately\nC) Stay about the same\nD) Grow moderately\nE) Grow substantially\n",reply_markup = markup)
        bot.register_next_step_handler(msg, save_preference)
    except:
        bot.reply_to(message, "problem with save sector")

def save_preference(message):
    try:
        user = user_dict[message.chat.id]
        user.score_risk = user.score_risk + score_dict[message.text]
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add('A', 'B','C')
        msg = bot.send_message(message.chat.id,"Due to a general market correction, one of your investments loses 14% \
of its value a short time after you buy it. What do you do?\n A) Sell the investment so you will not have to worry if it\
continues to decline\n B) Hold on to it and wait for it to climb back up\n C) Buy more of the same investment...because at the\
current lower price, it looks even better than when you bought it",reply_markup = markup)
        bot.register_next_step_handler(msg,save_investment_risk)
    except:
        bot.reply_to(message, "problme with save_preference")

def save_investment_risk(message):
    try:
        user = user_dict[message.chat.id]
        user.score_risk = user.score_risk + score_dict[message.text]
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add('A', 'B','C')
        msg = bot.send_message(message.chat.id,"Which of these investing plans would you choose for your investment dollars?\n\
A) You would go for maximum diversity, dividing your portfolio among all available investments, \
including those ranging from highest return/greatest risk to lowest return/lowest risk\n\
B) You are concerned about too much diversification, so you would divide your portfolio among two investments\
with historically high rates of return and moderate risk\n\
C) You would put your investment dollars in the investment with the highest rate of return and most risk",reply_markup = markup)
        bot.register_next_step_handler(msg,save_inv_diversity)
    except:
        bot.reply_to(message,"problme with save investment risk")

def save_inv_diversity(message):
    try:
        user = user_dict[message.chat.id]
        user.score_risk = user.score_risk + score_dict[message.text]
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add('A', 'B','C')
        msg = bot.send_message(message.chat.id,"Assuming you are investing in a stock, which one do you choose?\n\
A) 'Blue chip' stocks that pay dividends\n\
B) Established, well-known companies that have a potential for continued growth\n\
C) Companies that may make significant technological advances that are still selling at their low initial\
offering price",reply_markup = markup)
        bot.register_next_step_handler(msg,save_companies_pref)
    except:
        bot.reply_to(message,"problem with saving investments risk")

def save_companies_pref(message):
    try:
        user = user_dict[message.chat.id]
        user.score_risk = user.score_risk + score_dict[message.text]
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add('A', 'B','C')
        msg = bot.send_message(message.chat.id,"Assuming you are investing in only one bond, which bond do you choose?\n\
A)  A tax-free bond, since minimizing taxes is your primary investment objective\n\
B) The bond of a well-established company that pays a rate of interest somewhere between the other two bonds\n\
C) A high-yield (junk) bond that pays a higher interest rate than the other two bonds, but also gives\
you the least sense of security with regard to a possible default",reply_markup = markup)
        bot.register_next_step_handler(msg,save_bond_pref)
    except:
        bot.reply_to(message,"problem with comp_pref")

def save_bond_pref(message):
    try:
        user = user_dict[message.chat.id]
        user.score_risk = user.score_risk + score_dict[message.text]
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add('A', 'B','C','D')
        msg = bot.send_message(message.chat.id,"You expect inflation to return and it has been suggested that you invest in\
'hard' assets, which have historically outpaced inflation. Your only financial assets are long-term bonds. What do you do?\n\
A) Ignore the advice and hold on to the bonds\n\
B) Sell the bonds, putting half the proceeds in 'hard' assets and the other half in money market funds\n\
C) Sell the bonds and put all the proceeds in 'hard' assets\n\
D) Sell the bonds, put the proceeds in 'hard' assets, and borrow additional money so you can buy even more 'hard' assets",reply_markup = markup)
        bot.register_next_step_handler(msg,save_risk_longterm_bonds)
    except:
        bot.reply_to(message,"problem with bond_pref")

def save_risk_longterm_bonds(message):
    try:
        user = user_dict[message.chat.id]
        user.score_risk = user.score_risk + score_dict[message.text]
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add('A', 'B','C','D')
        msg = bot.send_message(message.chat.id,"You have just reached the $10,000 plateau on a TV game show.\n\
Now you must choose between quitting with the $10,000 in hand or betting the entire $10,000 in one of\
three alternative scenarios. Which do you choose?\n\
A) The $10,000 -- you take the money and run\n\
B) A 50 percent chance of winning $50,000\n\
C) A 20 percent chance of winning $75,000\n\
D) A 5 percent chance of winning $100,000",reply_markup = markup)
        bot.register_next_step_handler(msg,save_betting_pref)
    except:
        bot.reply_to(message,"problem with save_risk_longterm_pref")

def save_betting_pref(message):
    try:
        user = user_dict[message.chat.id]
        user.score_risk = user.score_risk + score_dict[message.text]
        print("before requests")
        response = requests.post("http://192.168.0.157:8001/user/createUser/",json = user.to_string())
        response = json.loads(response.text)
        bot.send_message(message.chat.id,"Your preferences are stored. Use these credentials to login\n\
userid:"+str(message.chat.id) +"\npassword: "+response['password'])
        msg = bot.reply_to(message, "You can check the real-time price of any stocks. Try 'price ticker_name'\n\
for stock symbol list please refer:")
        bot.send_message(message.chat.id,"https://www.slickcharts.com/sp500",parse_mode='HTML')

    except:
        bot.reply_to(message,"problem with save_betting_pref")

def validate_ticker(ticker_name):
    ticker = yf.Ticker(ticker_name)
    try:
        if (ticker.info['regularMarketPrice'] == None):
            print(f"Cannot get info of {ticker_name}, it probably does not exist")
            return False
    except:
        print("error in validate ticker")
    # Got the info of the ticker, do more stuff with it
    print(f"Info of {ticker_name}: {ticker.info}")
    return True

def is_price_message(message):
    data = message.text.split()
    if len(data) < 2 or data[0].lower() != "price":
        return False
    else:
        return True
        
@bot.message_handler(func=is_price_message)
def get_stock_price(message):
    chat_id = message.chat.id
    user = user_dict[chat_id]
    request_ticker = message.text.split()[1]
    validBool = validate_ticker(request_ticker)
    if not validBool:
        msg = bot.reply_to(message,"stock symbol not found. Try again")
        bot.register_next_step_handler(msg, get_stock_price)
    data = yf.download(tickers=request_ticker, period='5m', interval='1m')
    if data.size > 0:
        data = data.reset_index()
        data["format_date"] = data['Datetime'].dt.strftime('%m/%d %I:%M %p')
        data.set_index('format_date', inplace=True)
        print(data.to_string())
        bot.reply_to(message, data['Close'].to_string(header=False))
    else:
        bot.send_message(message, "No data.")  

bot.enable_save_next_step_handlers(delay=2)

# Load next_step_handlers from save file (default "./.handlers-saves/step.save")
# WARNING It will work only if enable_save_next_step_handlers was called!
bot.load_next_step_handlers()
bot.infinity_polling()
