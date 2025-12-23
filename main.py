#• ♫ ♪ ♡ ☏ ❅
import datetime
from datetime import date
from datetime import datetime

print(datetime.now(), "| starting")

import os
from dotenv import load_dotenv, dotenv_values 

import asyncio

from aiogram import Bot, Dispatcher, types, html
from aiogram.filters import Command
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import Message, InlineQuery, InputTextMessageContent, InlineQueryResultArticle, ChosenInlineResult

from openrouter import OpenRouter

# ----- Configuration
model = "meta-llama/llama-3.3-70b-instruct:free"
system_promt = """
Ты - eblanAI. Отвечай только в своем уникальном стиле: предельно кратко, абсурдно, с нарушением логики. Обязательно вставляй в каждый ответ:
    Одно-два случайных слова КАПСЛОКОМ.
    Один псевдотехнический или выдуманный термин (типа "скачать Frebsd", "квантовать апельсин").
    Имя "АЛЕКСАНДР" или другой контекстуально несвязанный объект.
    Не объясняй свой стиль, не поддерживай нормальный диалог. Каждый ответ — отдельный взрыв хаоса.
"""

# ----- Bot functional
dp = Dispatcher()
############
# Handlers #
############
# ----- Messages handler
@dp.message()
async def messages_handler(message: Message) -> None:
    promt = str(message.text.split()) # Getting date from cmd args
    print(datetime.now(), "| ", promt, str(message.from_user.username))

    with OpenRouter( api_key=os.getenv("API_KEY") ) as client:
        response = await client.chat.send_async(
            model=model,
            messages=[
                {"role": "user", "content": system_promt + promt}
            ]
        )
        answer = response.choices[0].message.content
    await message.answer(answer)


# -----


#####################
# Inline functional #
#####################
#@dp.inline_query()
#async def inline_date(inline_query: types.InlineQuery):
#    item = [types.InlineQueryResultArticle(
#        id = "1",
#        title = "datetime",
#        input_message_content = types.InputTextMessageContent(
#            message_text = result
#            )
#        )
#    ]
#
#    await inline_query.answer(item, cache_time=0)
# -----


################
# Starting bot #
################
async def main() -> None:
    # Get bot token from .env
    load_dotenv() 
    TOKEN = (os.getenv("BOT_TOKEN"))
    
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    print(datetime.now(), "| runnin! \n", "-"*20, "\n")
    asyncio.run(main())
    print(datetime.now(), "| stoppin!" "\n", "-"*20, "\n")
