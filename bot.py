from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram.error import TelegramError, Unauthorized, BadRequest, TimedOut, NetworkError
import logging
import json

# HANDLERS

def handle_help(bot, update):
    msg = update.effective_message
    bot.send_message(
        msg.chat_id,
        "FrogIT 서비스에 관련한 것을 최대한 도와드립니다.\n== 사용 가능한 명령어 ==\n/help - <i>이 도움말을 봅니다</i>",
        reply_to_message_id=msg.message_id,
        parse_mode="HTML"
    )

#####

def register_handlers(dispatcher):
    dispatcher.add_handler(CommandHandler(["start", "help"], handle_help))

def error_callback(bot, update, error):
    try:
        raise error
    except Unauthorized:
        logging.warning("권한이 없음")
    except BadRequest:
        logging.warning("잘못된 요청임")
    except TimedOut:
        pass
    except NetworkError:
        logging.warning("네트워크 에러 발생")
    except TelegramError:
        logging.warning("기타 에러 발생")

def get_config(configname):
    with open("config.json") as f:
        config = json.load(f)
    return config[configname]

def main():
    logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

    updater = Updater(get_config("api_token"))
    dispatcher = updater.dispatcher

    register_handlers(dispatcher)
    dispatcher.add_error_handler(error_callback)

    updater.start_polling(clean=True)
    logging.info("서버가 시작되었습니다.")
    updater.idle()
    logging.info("서버가 종료되었습니다.")

if __name__ == "__main__":
    main()
