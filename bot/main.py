import logging
import os

from dotenv import dotenv_values, load_dotenv
from telegram import Bot, Update
from telegram.ext import CallbackContext, CommandHandler, Updater
from telegram.parsemode import ParseMode
from telegram.utils.request import Request

from audio import get_wav_audio
from utils import get_hash, url_validator
from video.youtube import download_video_and_subtitles

_logger = logging.getLogger(__name__)
load_dotenv()
config = dotenv_values("local.env")  # take environment variables from local.env files

TOKEN: str = config.get("TOKEN", "some_my_token")
PROXY_URL: str = config.get("PORT", None)

DESCRIPTION = """/help - Show help
/start - Start working
/description {LINK} - Get description of sent link"""


def log_errors(f):
    def inner(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            error_message = f"Some error: {e}"
            _logger.error(error_message)
            raise e

    return inner


@log_errors
def show_help(update: Update, context: CallbackContext):
    update.message.reply_text(text=f"Supported commands:\n{DESCRIPTION}")


@log_errors
def process_description(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    try:
        url = context.args.pop()
    except IndexError:
        update.message.reply_text(text="Need {LINK} to the video")
        return
    if not url_validator(url):
        update.message.reply_text(text="You input link to the video isn't valid")
        return

    sender = {"external_id": chat_id, "defaults": {"name": update.message.from_user.username}}
    _logger.debug(f"{sender=}, {url=}")

    reply_text = f"Your ID = {chat_id}\n{url} will be processed soon."
    update.message.reply_text(text=reply_text, disable_web_page_preview=True)

    path = os.path.join("data", get_hash(url))
    video_path = download_video_and_subtitles(url, path)
    file_name = os.path.basename(video_path)
    audio_path = get_wav_audio(video_path)


@log_errors
def start(update: Update, context: CallbackContext):
    """the callback for handling start command"""
    bot: Bot = context.bot
    bot.send_message(
        chat_id=update.effective_chat.id,
        text="Hello User, You have used <b>start</b> command for working with <b>YTEssence</b>.",
        parse_mode=ParseMode.HTML,
    )


if __name__ == "__main__":
    # 1 -- connections
    request = Request(connect_timeout=0.5, read_timeout=1.0)
    bot = Bot(request=request, token=TOKEN, base_url=PROXY_URL)
    _logger.info(bot.get_me())

    # 2 -- handles
    updater = Updater(bot=bot, use_context=True)

    # Add handlers for Telegram messages
    updater.dispatcher.add_handler(CommandHandler("start", start))
    updater.dispatcher.add_handler(CommandHandler("help", show_help))
    updater.dispatcher.add_handler(CommandHandler("description", process_description, pass_args=True))

    # 3 -- Run processing loop of input messages
    updater.start_polling()
    updater.idle()
