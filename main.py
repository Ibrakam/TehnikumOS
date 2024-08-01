import asyncio
import logging
from config import dp, bot
from db import Base, engine
from handlers.main import router


async def main() -> None:
    dp.include_router(router)
    await bot.delete_webhook()
    await dp.start_polling(bot)


#
#
if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
