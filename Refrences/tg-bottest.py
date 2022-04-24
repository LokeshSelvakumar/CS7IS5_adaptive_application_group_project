from tkinter import E
import telebot
import yfinance as yf
from yahoo_fin import stock_info as si
from telebot.callback_data import CallbackData, CallbackDataFilter
from telebot import types

bot = telebot.TeleBot("5356735903:AAGIUWFapkm7AcpAhyV44n-yojw1Sa3CNl0")

tickers = si.tickers_sp500()
user_dict = {}

import re
def valid_email(email):
  return bool(re.search(r"^[\w\.\+\-]+\@[\w]+\.[a-z]{2,3}$", email))

class User:
    def __init__(self, name):
        self.name = name
        self.age = None
        self.sex = None
        self.email = None
        self.salary = None

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    print(message.chat.id)
    response = bot.reply_to(message, "Howdy, Nice to Meet You!!\nWhat is your name?")
    bot.register_next_step_handler(response, process_name_step)

def process_name_step(message):
    try:
        chat_id = message.chat.id
        name = message.text
        user = User(name)
        user_dict[chat_id] = user
        msg = bot.reply_to(message, 'How old are you?')
        bot.register_next_step_handler(msg, process_age_step)
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
        user.stocksList = []
        user.watchList = []
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
        markup.add('Google','Yahoo')
        msg = bot.reply_to(message,"what is your Source preference? ", reply_markup = markup)
        bot.register_next_step_handler(msg, save_preference)
    except:
        bot.reply_to(message, "problem with save sector")

def save_preference(message):
    try:
        user = user_dict[message.chat.id]
        user.source_pref = message.text
        msg = bot.reply_to(message, "You can check the real-time price of any stocks. Try 'price ticker_name'\n\
for stock symbol list please refer:")
        bot.send_message(message.chat.id,"https://www.slickcharts.com/sp500",parse_mode='HTML')
        bot.register_next_step_handler(msg, get_stock_price)
    except:
        bot.reply_to(message, "problme with save_preference")
        
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
    print(user.stocksList)
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
