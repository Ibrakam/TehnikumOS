import logging

from aiogram.enums import ReactionTypeType
from aiogram.types import Message, MessageReactionUpdated, ReactionTypeEmoji
from aiogram import F, Router, Bot
from trello import TrelloClient

from config import TRELLO_API_KEY, TRELLO_API_SECRET, TRELLO_BOARD_ID, TRELLO_TOKEN
from db import get_db, MessageModel

router = Router()

trello_client = TrelloClient(
    api_key=TRELLO_API_KEY,
    api_secret=TRELLO_API_SECRET,
    token=TRELLO_TOKEN
)


def get_message(message_id):
    with next(get_db()) as db:
        message = db.query(MessageModel).filter(MessageModel.message_id == message_id).first()
        return message.message_text if message else None


def add_message(message_id, message_text):
    try:
        with next(get_db()) as db:
            if get_message(message_id):
                logging.info(f"Сообщение с id {message_id} уже существует в базе данных")
                return
            new_message = MessageModel(message_id=message_id, message_text=message_text)
            db.add(new_message)
            db.commit()
            logging.info(f"Сообщение с id {message_id} успешно добавлено в базу данных")
    except Exception as e:
        logging.error(f"Ошибка при добавлении сообщения в базу данных: {e}")


@router.message(F.text)
async def message_to_save(message: Message):
    if message.text and message.text.startswith("Обратная связь:"):
        add_message(message.message_id, message.text)


@router.message_reaction()
async def message_reaction_handler(reaction: MessageReactionUpdated, bot: Bot):
    reaction_ = reaction.new_reaction
    print(reaction)
    emoji = [react.emoji for react in reaction_]
    # if emoji[0] == "🖋️":
    # if emoji[0] == "🔥"
    if emoji[0] == "🖋️":
        message = get_message(reaction.message_id)

        # Извлечение информации из сообщения
        lines = message.split('\n')
        course = next((line.split(': ')[1] for line in lines if line.startswith("Курс:")), "Неизвестно")
        date = next((line.split(': ')[1] for line in lines if line.startswith("Дата:")), "Неизвестно")
        feedback = next((line.split(': ')[1] for line in lines if line.startswith("Отзыв:")), "Нет отзыва")
        # Создание карточки в Trello
        board = trello_client.get_board(TRELLO_BOARD_ID)
        lists = board.list_lists()
        print(lists)
        target_list = lists[0]  # Выберите нужный список

        card = target_list.add_card(
            name=f"Отзыв о курсе {course} дата {date} отзыв: {feedback}",
            desc=feedback
        )
        try:
            await bot.set_message_reaction(
                chat_id=reaction.chat.id,
                message_id=reaction.message_id,
                reaction=[ReactionTypeEmoji(emoji="👀")]
            )
            db = next(get_db())
            db.query(MessageModel).filter(MessageModel.message_id == reaction.message_id).delete()
            db.commit()
        except Exception as e:
            logging.error(f"Ошибка при обработке реакции: {e}")


# logging.info(f"Создана карточка в Trello: {card.short_url}")
