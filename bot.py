import logging
from telegram import Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes
from datetime import datetime
from csvHandling import CSV, plot_temperature_and_humidity_readings
from connectivity import send_data
from apscheduler.schedulers.background import BackgroundScheduler

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Date format to parse the dates
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"  # Modify as necessary

# Start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm ESPClimateBot, please talk to me! Use /help to find out my functionalities")

# Help command handler
async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="List of commads : \n /start - welcome message \n /help - get informed about commands \n /sensor_data - get real time temperature and humidity from sensor \n /climate_graph - returns a graph with the evolution of temperature and humidity over a given period on time \n /send_photo - returns a possible profile photo for the bot \n /caps - returns the given text with caps \n /echo - returns the given text\n")

# Echo command handler
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

# Caps command handler
async def caps(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text_caps = ' '.join(context.args).upper()
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)

# climate_graph command handler
async def climate_graph(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Extract the full message text after the command '/climateGraph'
    message_text = update.message.text

    # Remove the command part '/climate_graph' from the message and strip extra spaces
    date_args = message_text.replace('/climate_graph', '').strip()

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
            plot_path = plot_temperature_and_humidity_readings(df)
        # Send the parsed dates back to the user
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"Start Date: {start_date.strftime(DATE_FORMAT)}\nEnd Date: {end_date.strftime(DATE_FORMAT)}"
        )
        
        # Send the plot image
        with open(plot_path, 'rb') as photo:
            await context.bot.send_photo(chat_id=update.effective_chat.id, photo=photo)

    except ValueError:
        # If parsing fails, send an error message back to the user
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Invalid date format. Please use dd-mm-yyyy hh:mm & dd-mm-yyyy hh:mm."
        )

# Test telegram command for sending a photo
async def send_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Define the path to the local image or a URL
    photo_path = 'botProfilePicture.png' 
    
    # Send the photo to the user
    await context.bot.send_photo(chat_id=update.effective_chat.id, photo=open(photo_path, 'rb'))

# Commands that sends the sensor readings in real time
async def sensor_data(update: Update, context: ContextTypes.DEFAULT_TYPE):
    response = send_data()
    # Split the response into temperature and humidity
    try:
        # Assume response_on is something like "22.33 26.77"
        temperature, humidity = response.split()
        
        # Format the output string
        formatted_response = f"Temperature: {temperature}°C\nHumidity: {humidity}%"
    except ValueError:
        # In case the response does not split correctly
        formatted_response = "Invalid data format received from ESP32."

    await context.bot.send_message(chat_id=update.effective_chat.id, text=formatted_response)


# Function to fetch data from the sensor at specific times
def scheduled_sensor_data_fetch():
    response = send_data()
    try:
        CSV.initialize_csv()
        temperature, humidity = response.split()
        CSV.add_entry(datetime.now(),temperature = temperature, humidity = humidity+'\n')
    except ValueError:
        formatted_response = "Invalid data format received from ESP32."
    
  


if __name__ == '__main__':
    # Create the application
    application = ApplicationBuilder().token('YOUR_BOT_TOKEN').build()
    
    # Handlers
    start_handler = CommandHandler('start', start)
    help_handler = CommandHandler('help', help)
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    caps_handler = CommandHandler('caps', caps)
    climate_graph_handler = CommandHandler('climate_graph', climate_graph)  
    send_photo_handler = CommandHandler('send_photo', send_photo)
    sensor_data_handler = CommandHandler('sensor_data', sensor_data)
    # Add handlers to the application
    application.add_handler(start_handler)
    application.add_handler(help_handler)
    application.add_handler(echo_handler)
    application.add_handler(caps_handler)
    application.add_handler(send_photo_handler)
    application.add_handler(climate_graph_handler)  
    application.add_handler(sensor_data_handler)

    # Set up APScheduler
    scheduler = BackgroundScheduler()

    # Schedule jobs at specific times (00:00, 04:00, 08:00, 12:00, 16:00, 20:00)
    scheduler.add_job(scheduled_sensor_data_fetch, 'cron', hour='0,4,8,12,16,20')
    
    # Start the scheduler
    scheduler.start()

    # Run the bot
    application.run_polling()
