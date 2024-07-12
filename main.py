import json
import telebot

# TOKEN DETAILS
TOKEN = "COIN"
BOT_TOKEN = "7217893693:AAH-kuewVPbfhldeiL5SjS7HRJ8BKvyWVjE"
PAYMENT_CHANNEL = "https://t.me/cyberlearnhub"  # add payment channel here
OWNER_ID = 5151868182  # write owner's user id here.. get it from @MissRose_Bot by /id
CHANNELS = [
    "https://t.me/everycookies",
    "https://t.me/pslifafa",
    "https://t.me/+Rkp_uJG9aeU3ODA1",
    "https://t.me/cyberlearnhub",
    "https://t.me/+vrj6OzPQwbZmMGJl",
    "https://t.me/addlist/ngUfzgUh4wU0YzBl",
    "https://t.me/Hacking_WOULD",
    "https://t.me/+UEtTsdCwPDk0YzE1"
]
Daily_bonus = 1  # Put daily bonus amount here!
Mini_Withdraw = 0.5  # remove 0 and add the minimum withdraw u want to set
Per_Refer = 0.0001  # add per refer bonus here

bot = telebot.TeleBot(BOT_TOKEN)

def check_if_joined(chat_id):
    try:
        chat_member = bot.get_chat_member('@cyberlearnhub', chat_id)
        return chat_member.status != 'left'
    except telebot.apihelper.ApiTelegramException as e:
        print(f"Error checking member status: {e}")
        return False

def menu(id):
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    keyboard.add('🆔 Account')
    keyboard.add('🙌🏻 Referrals', '🎁 Bonus', '💸 Withdraw')
    keyboard.add('⚙️ Set Wallet', '📊 Statistics')
    bot.send_message(id, "*🏡 Home*", parse_mode="Markdown", reply_markup=keyboard)

@bot.message_handler(commands=['start'])
def start(message):
    try:
        user = message.chat.id
        msg = message.text
        if msg == '/start':
            user = str(user)
            data = json.load(open('users.json', 'r'))
            if user not in data['referred']:
                data['referred'][user] = 0
                data['total'] = data['total'] + 1
            if user not in data['referby']:
                data['referby'][user] = user
            if user not in data['checkin']:
                data['checkin'][user] = 0
            if user not in data['DailyQuiz']:
                data['DailyQuiz'][user] = "0"
            if user not in data['balance']:
                data['balance'][user] = 0
            if user not in data['wallet']:
                data['wallet'][user] = "none"
            if user not in data['withd']:
                data['withd'][user] = 0
            if user not in data['id']:
                data['id'][user] = data['total'] + 1
            json.dump(data, open('users.json', 'w'))
            print(data)
            markup = telebot.types.InlineKeyboardMarkup()
            
            # Adding channels in a specific pattern
            row = []
            pattern = [3, 1, 3, 2]  # 3 buttons, 1 button, 3 buttons, 2 buttons per line
            current_index = 0

            for size in pattern:
                for _ in range(size):
                    if current_index < len(CHANNELS):
                        row.append(telebot.types.InlineKeyboardButton(
                            text=f"Join", url=CHANNELS[current_index]
                        ))
                        current_index += 1
                markup.add(*row)
                row = []
            
            # Add the "Joined" button at the end
            markup.add(telebot.types.InlineKeyboardButton(
                text='🤼‍♂️ Joined', callback_data='check'))
            
            msg_start = "*🍔 To Use This Bot You Need To Join These Channels:*"
            bot.send_message(user, msg_start, parse_mode="Markdown", reply_markup=markup)
        else:
            data = json.load(open('users.json', 'r'))
            user = message.chat.id
            user = str(user)
            refid = message.text.split()[1]
            if user not in data['referred']:
                data['referred'][user] = 0
                data['total'] = data['total'] + 1
            if user not in data['referby']:
                data['referby'][user] = refid
            if user not in data['checkin']:
                data['checkin'][user] = 0
            if user not in data['DailyQuiz']:
                data['DailyQuiz'][user] = 0
            if user not in data['balance']:
                data['balance'][user] = 0
            if user not in data['wallet']:
                data['wallet'][user] = "none"
            if user not in data['withd']:
                data['withd'][user] = 0
            if user not in data['id']:
                data['id'][user] = data['total'] + 1
            json.dump(data, open('users.json', 'w'))
            print(data)
            markups = telebot.types.InlineKeyboardMarkup()
            
            # Adding channels in a specific pattern
            row = []
            pattern = [3, 1, 3, 2]
            current_index = 0

            for size in pattern:
                for _ in range(size):
                    if current_index < len(CHANNELS):
                        row.append(telebot.types.InlineKeyboardButton(
                            text=f"Join", url=CHANNELS[current_index]
                        ))
                        current_index += 1
                markups.add(*row)
                row = []
            
            # Add the "Joined" button at the end
            markups.add(telebot.types.InlineKeyboardButton(
                text='🤼‍♂️ Joined', callback_data='check'))

            msg_start = "*🍔 To Use This Bot You Need To Join These Channels:*"
            bot.send_message(user, msg_start, parse_mode="Markdown", reply_markup=markups)
    except Exception as e:
        handle_error(message, e)

@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    try:
        if call.data == 'check':
            if check_if_joined(call.message.chat.id):
                data = json.load(open('users.json', 'r'))
                user_id = call.message.chat.id
                user = str(user_id)
                bot.answer_callback_query(
                    callback_query_id=call.id, text='✅ You joined. Now you can earn money.')
                bot.delete_message(call.message.chat.id, call.message.message_id)
                if user not in data['refer']:
                    data['refer'][user] = True

                    if user not in data['referby']:
                        data['referby'][user] = user
                        json.dump(data, open('users.json', 'w'))
                    if int(data['referby'][user]) != user_id:
                        ref_id = data['referby'][user]
                        ref = str(ref_id)
                        if ref not in data['balance']:
                            data['balance'][ref] = 0
                        if ref not in data['referred']:
                            data['referred'][ref] = 0
                        json.dump(data, open('users.json', 'w'))
                        data['balance'][ref] += Per_Refer
                        data['referred'][ref] += 1
                        bot.send_message(
                            ref_id, f"*🏧 New Referral on Level 1, You Got : +{Per_Refer} {TOKEN}*", parse_mode="Markdown")
                        json.dump(data, open('users.json', 'w'))
                        return menu(call.message.chat.id)

                    else:
                        json.dump(data, open('users.json', 'w'))
                        return menu(call.message.chat.id)

                else:
                    json.dump(data, open('users.json', 'w'))
                    menu(call.message.chat.id)

            else:
                bot.answer_callback_query(
                    callback_query_id=call.id, text='❌ You have not joined @cyberlearnhub.')
                bot.delete_message(call.message.chat.id, call.message.message_id)
                markup = telebot.types.InlineKeyboardMarkup()
                
                # Adding channels in a specific pattern
                row = []
                pattern = [3, 1, 3, 2]
                current_index = 0

                for size in pattern:
                    for _ in range(size):
                        if current_index < len(CHANNELS):
                            row.append(telebot.types.InlineKeyboardButton(
                                text=f"Join", url=CHANNELS[current_index]
                            ))
                            current_index += 1
                    markup.add(*row)
                    row = []
                
                # Add the "Joined" button at the end
                markup.add(telebot.types.InlineKeyboardButton(
                    text='🤼‍♂️ Joined', callback_data='check'))
                
                msg_start = "*🍔 To Use This Bot You Need To Join These Channels:*"
                bot.send_message(call.message.chat.id, msg_start,
                                 parse_mode="Markdown", reply_markup=markup)
    except Exception as e:
        handle_error(call.message, e)

@bot.message_handler(content_types=['text'])
def send_text(message):
    try:
        if message.text == '🆔 Account':
            data = json.load(open('users.json', 'r'))
            accmsg = '*👮 User : {}\n\n⚙️ Wallet : *`{}`*\n\n💸 Balance : *`{}`* {}*'
            user_id = message.chat.id
            user = str(user_id)

            if user not in data['balance']:
                data['balance'][user] = 0
            if user not in data['wallet']:
                data['wallet'][user] = "none"

            json.dump(data, open('users.json', 'w'))

            balance = data['balance'][user]
            wallet = data['wallet'][user]
            msg = accmsg.format(message.from_user.first_name, wallet, balance, TOKEN)
            bot.send_message(message.chat.id, msg, parse_mode="Markdown")
    except Exception as e:
        handle_error(message, e)

def handle_error(message, error):
    bot.send_message(message.chat.id, "This command has encountered an error. Please wait for the admin to fix the issue.")
    bot.send_message(OWNER_ID, f"Your bot encountered an error. Please fix it as soon as possible!\nError on command: {message.text}\n{str(error)}")

if __name__ == "__main__":
    bot.polling(none_stop=True)
