import logging
from telegram import Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes
from datetime import datetime
from csvHandling import CSV, plot_temperature_and_humidity_readings

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Date format to parse the dates
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"  # Modify as necessary

# Start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

# Echo command handler
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

# Caps command handler
async def caps(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text_caps = ' '.join(context.args).upper()
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)

# Print_dates command handler
async def print_dates(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Extract the full message text after the command '/print_dates'
    message_text = update.message.text

    # Remove the command part '/print_dates' from the message and strip extra spaces
    date_args = message_text.replace('/print_dates', '').strip()

    # Split by the '&' character expecting exactly two date-time values
    if '&' not in date_args:
        await context.bot.send_message(chat_id=update.effective_chat.id, 
                    text="Please provide two dates separated by '&' in the format yyyy-mm-dd hh:mm:ss & yyyy-mm-dd hh:mm:ss")
        return

    # Try splitting the date arguments by '&'
    try:
        # Split the input by '&' and trim any extra spaces around both dates
        start_date_str, end_date_str = map(str.strip, date_args.split('&'))

        # Define the expected date format
        DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

        # Parse both date strings using the provided format
        start_date = datetime.strptime(start_date_str, DATE_FORMAT)
        end_date = datetime.strptime(end_date_str, DATE_FORMAT)
        # Swap if start_date is later than end_date
        if start_date > end_date:
            start_date, end_date = end_date, start_date  # Swap the dates
            start_date_str, end_date_str = end_date_str, start_date_str  # Also swap the string representations for later use

        df = CSV.get_readings(start_date_str, end_date_str)  # This now works correctly
        if df is not None:  # Ensure df is not None before plotting
            print('SSS')
            plot_path = plot_temperature_and_humidity_readings(df)
        # Send the parsed dates back to the user
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"Start Date: {start_date.strftime(DATE_FORMAT)}\nEnd Date: {end_date.strftime(DATE_FORMAT)}"
        )
        
        # Send the plot image
        with open(plot_path, 'rb') as photo:
            await context.bot.send_photo(chat_id=update.effective_chat.id, photo=photo)

        # Optionally, remove the plot image file after sending to save space
        #os.remove(plot_path)
    except ValueError:
        # If parsing fails, send an error message back to the user
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Invalid date format. Please use dd-mm-yyyy hh:mm & dd-mm-yyyy hh:mm."
        )

async def send_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Define the path to the local image or a URL
    photo_path = 'Idei.png'  # For a local image
    # photo_path = 'https://example.com/image.jpg'  # Or use a URL
    
    # Send the photo to the user
    await context.bot.send_photo(chat_id=update.effective_chat.id, photo=open(photo_path, 'rb'))


if __name__ == '__main__':
    # Create the application
    application = ApplicationBuilder().token('7968000892:AAG-fxn8DmR5T4rlLhH6WSQQaSn8ngvM0tA').build()
    
    # Handlers
    start_handler = CommandHandler('start', start)
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    caps_handler = CommandHandler('caps', caps)
    print_dates_handler = CommandHandler('print_dates', print_dates)  # New print_dates command
    send_photo_handler = CommandHandler('send_photo', send_photo)
    # Add handlers to the application
    application.add_handler(start_handler)
    application.add_handler(echo_handler)
    application.add_handler(caps_handler)
    application.add_handler(send_photo_handler)
    application.add_handler(print_dates_handler)  # Add the new command

    # Run the bot
    application.run_polling()
