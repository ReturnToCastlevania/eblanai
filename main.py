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


async def get_openrouter_response(promt):
    with OpenRouter( api_key=os.getenv("OPENROUTER_KEY") ) as client:
        response = await client.chat.send_async(
            model=model,
            messages=[
                {"role": "user", "content": system_promt + promt}
            ]
        )
        return str(response.choices[0].message.content)





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
    await message.answer(await get_openrouter_response(promt))


# -----


#####################
# Inline functional #
#####################
@dp.inline_query()
async def inline_awnswer(inline_query: types.InlineQuery):
    promt = str(inline_query.query)
    
    if not promt:
        promt = "умоляй пользователя о том, чтобы он дал тебе промт"
    
    try:
        answer = await get_openrouter_response(promt)
        item = [types.InlineQueryResultArticle(
            id = "1",
            title = "EblanAI",
            description = f"query: {promt}",
            input_message_content = types.InputTextMessageContent(
                message_text = "> " + promt + "\n----------\n" + answer
                )
            )
        ]
        print(datetime.now(), "| ", promt, " / ", str(inline_query.from_user.username))
        await inline_query.answer(item, cache_time=0)

    except Exception as e:
        item = [types.InlineQueryResultArticle(
            id = "error",
            title = str(e),
            input_message_content = types.InputTextMessageContent(
                message_text = str(e)
                )
            )
        ]
        await inline_query.answer(item, cache_time=0)
        
        
        
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
    print(datetime.now(), "-"*20, "\n", "| stoppin!" "\n")
