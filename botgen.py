import random, datetime, telebot, os

bot = telebot.TeleBot("1604506094:AAESuZOkIY_8kz0ziVqWhuzf-JFew-NsZrY")

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    welcome_message = (
"""Welcome to Cards Generator Bot!
Usage: /gen [bin] [count] [month] [year] [cvv]
All fields can be left empty."""
    )
    bot.reply_to(message, welcome_message)

@bot.message_handler(commands=['gen'])
def generate_cards(message):
    try:
        command_args = message.text.split()[1:]
        a = command_args[0] if len(command_args) > 0 else ""
        e = int(command_args[1]) if len(command_args) > 1 else 1000
        b = command_args[2] if len(command_args) > 2 else ""
        c = command_args[3] if len(command_args) > 3 else ""
        d = command_args[4] if len(command_args) > 4 else ""

        cards_data = ""
        f = 0
        while f < e:
            card_number, exp_m, exp_y, cvv = gen_card(a, b, c, d)
            cards_data += f"{card_number}|{exp_m}|{exp_y}|{cvv}\n"
            f += 1
       
        file_name = "generated_cards.txt"
        with open(file_name, "w") as file:
            file.write(cards_data)
        
        with open(file_name, "rb") as file:
            bot.send_document(message.chat.id, file)
        
        os.remove(file_name)
    except Exception as ex:
        bot.reply_to(message, f"An error occurred: {str(ex)}")

def gen_card(bin, exp_m, exp_y, cvv):
    #card number
    card_number = bin
    for _ in range(15-len(bin)):
        digit = random.randint(0, 9)
        card_number += str(digit)
    digits = [int(x) for x in card_number]
    for i in range(0, 16, 2):
        digits[i] *= 2
        if digits[i] > 9:
            digits[i] -= 9
    total = sum(digits)
    check_digit = (10 - (total % 10)) % 10
    card_number += str(check_digit)
    #exp month
    if exp_m == "":
        exp_m = str(random.randint(1, 12)).zfill(2)
    else:
        exp_m = exp_m.zfill(2)
    #exp year
    if exp_y == "":
        current_year = datetime.datetime.now().year
        random_offset = random.randint(1, 5)
        exp_y = current_year + random_offset
    elif int(exp_y) >= 10 and int(exp_y) <= 99:
        exp_y = "20" + exp_y
    if cvv == "":
        cvv = str(random.randint(0, 999)).zfill(3)
    else:
        cvv = cvv.zfill(3)
    return card_number, exp_m, exp_y, cvv

bot.polling()
