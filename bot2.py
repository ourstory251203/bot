import requests
from telegram import Update, Bot, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext, CallbackQueryHandler, ConversationHandler
from telegram.error import BadRequest
import re

# Replace 'YOUR_TELEGRAM_BOT_TOKEN' with your actual Telegram bot token
TELEGRAM_BOT_TOKEN = '7893174235:AAGrHWXLLhPWhsJWpIdkLzmr98oh3nFrrPA'

THUMBNAIL, TITLE, YEAR, LANGUAGE, RATING, URL1, URL2, URL3 = range(8)

async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Hello! Send me a movie name and I will fetch the details for you.')

async def create(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text('Please provide the Thumbnail URL:')
    return THUMBNAIL

async def thumbnail(update: Update, context: CallbackContext) -> int:
    url = update.message.text
    if not re.match(r'^https?://', url):
        await update.message.reply_text('Invalid URL format. Please provide a valid Thumbnail URL:')
        return THUMBNAIL
    context.user_data['thumbnail'] = url
    await update.message.reply_text('Please provide the Title:')
    return TITLE

async def title(update: Update, context: CallbackContext) -> int:
    context.user_data['title'] = update.message.text
    await update.message.reply_text('Please provide the Year:')
    return YEAR

async def year(update: Update, context: CallbackContext) -> int:
    context.user_data['year'] = update.message.text
    await update.message.reply_text('Please provide the Language:')
    return LANGUAGE

async def language(update: Update, context: CallbackContext) -> int:
    context.user_data['language'] = update.message.text
    await update.message.reply_text('Please provide the Rating:')
    return RATING

async def rating(update: Update, context: CallbackContext) -> int:
    context.user_data['rating'] = update.message.text
    await update.message.reply_text('Please provide the URL for 2160p:')
    return URL1

async def url1(update: Update, context: CallbackContext) -> int:
    context.user_data['url1'] = update.message.text
    await update.message.reply_text('Please provide the URL for 1080p:')
    return URL2

async def url2(update: Update, context: CallbackContext) -> int:
    context.user_data['url2'] = update.message.text
    await update.message.reply_text('Please provide the URL for 720p:')
    return URL3

async def url3(update: Update, context: CallbackContext) -> int:
    context.user_data['url3'] = update.message.text
    thumbnail = context.user_data['thumbnail']
    title = context.user_data['title']
    year = context.user_data['year']
    language = context.user_data['language']
    rating = context.user_data['rating']
    url1 = context.user_data['url1']
    url2 = context.user_data['url2']
    url3 = context.user_data['url3']
  
    links = []
    watch_links = []
    if url1 != '0000':
        links.append(f"<a href='{url1}'>2160p</a>")
        watch_links.append(f"<a href='http://streamless.kesug.com?link={url1}'>2160p</a>")
    if url2 != '0000':
        links.append(f"<a href='{url2}'>1080p</a>")
        watch_links.append(f"<a href='http://streamless.kesug.com?link={url2}'>1080p</a>")
    if url3 != '0000':
        links.append(f"<a href='{url3}'>720p</a>")
        watch_links.append(f"<a href='http://streamless.kesug.com?link={url3}'>720p</a>")
   
    links_text = " ⠀⠀ ".join(links)
    watch_links_text = " ⠀⠀ ".join(watch_links)
    post = (
        f"\n○⠀<b>Title:</b>⠀{title}\n\n"
        f"○⠀<b>Year:</b>⠀{year}\n\n"
        f"○⠀<b>Language:</b>⠀{language}\n\n"
        f"○⠀<b>Rating:</b>⠀{rating}\n\n"
        f"○⠀<b>Download:</b>⠀{links_text}\n\n"
        f"○⠀<b>Watch:</b>⠀{watch_links_text}\n\n"  # Added Watch section
    )
    try:
        await update.message.reply_photo(photo=thumbnail, caption=f"<blockquote>{post}</blockquote>", parse_mode='HTML')
    except BadRequest as e:
        await update.message.reply_text(f"Error: {e.message}. Please provide a valid Thumbnail URL:")
        return THUMBNAIL
    return ConversationHandler.END

async def handle_message(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Please provide the Thumbnail URL:")
    return THUMBNAIL

def create_movie_post(movie_data: dict, url1: str = '', url2: str = '', url3: str = '' ) -> str:
    if movie_data['Response'] == 'False':
        return 'Movie not found!'
    
    title = movie_data.get('Title', 'N/A')
    year = movie_data.get('Year', 'N/A')
    language = movie_data.get('Language', 'N/A')
    rating = movie_data.get('imdbRating', 'N/A')

    links = []
    watch_links = []
    if url1 != '0000':
        links.append(f"<a href='{url1}'>2160p</a>")
        watch_links.append(f"<a href='https://streamless.kesug.com?link={url1}'>2160p</a>")
    if url2 != '0000':
        links.append(f"<a href='{url2}'>1080p</a>")
        watch_links.append(f"<a href='https://streamless.kesug.com?link={url2}'>1080p</a>")
    if url3 != '0000':
        links.append(f"<a href='{url3}'>720p</a>")
        watch_links.append(f"<a href='https://streamless.kesug.com?link={url3}'>720p</a>")
  
    links_text = " ⠀⠀ ".join(links)
    watch_links_text = " ⠀⠀ ".join(watch_links)

    post = (
        f"\n○⠀<b>Title:</b>⠀{title}\n\n"
        f"○⠀<b>Year:</b>⠀{year}\n\n"
        f"○⠀<b>Language:</b>⠀{language}\n\n"
        f"○⠀<b>Rating:</b>⠀{rating}\n\n"
        f"○⠀<b>Download:</b>⠀{links_text}\n\n"
        f"○⠀<b>Watch:</b>⠀{watch_links_text}\n\n"  # Added Watch section
    )
    return f"<blockquote>{post}</blockquote>"

def main() -> None:
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)],
        states={
            THUMBNAIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, thumbnail)],
            TITLE: [MessageHandler(filters.TEXT & ~filters.COMMAND, title)],
            YEAR: [MessageHandler(filters.TEXT & ~filters.COMMAND, year)],
            LANGUAGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, language)],
            RATING: [MessageHandler(filters.TEXT & ~filters.COMMAND, rating)],
            URL1: [MessageHandler(filters.TEXT & ~filters.COMMAND, url1)],
            URL2: [MessageHandler(filters.TEXT & ~filters.COMMAND, url2)],
            URL3: [MessageHandler(filters.TEXT & ~filters.COMMAND, url3)],
            
        },
        fallbacks=[CommandHandler("cancel", start)],
    )

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("create", create))
    application.add_handler(conv_handler)

    print("Bot is running...")
    application.run_polling()

if __name__ == '__main__':
    main()
