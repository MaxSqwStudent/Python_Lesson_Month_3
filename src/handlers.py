
from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from src.keyboards import *
from src.state import *
from src.questions import *
from db.users import get_user, create_user

router = Router()

@router.message(CommandStart())
async def CommandStart(message: Message):
    user = create_user(
        telegram_id=message.from_user.id,
        username=message.from_user.username or "Unknown"
    )
    await message.answer(
        f"Привет {message.from_user.full_name} (@{message.from_user.username}), я Бот! Вот результат который возвращается с SQL \n\n {user}", reply_markup=reply_buttons
    )
    print(f"Пользователь {message.from_user.username} написал команду start")
    print(user)

@router.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer(
        f"/start - команда для запуска\n"
        f"/help - список команд", reply_markup=inline_buttons
    )

@router.message(Command("about"))
async def cmd_about(message: Message):
    await message.answer(
        f"О боте\n\n"
        f"Username: @GeeksRobot\n"
        f"Name: VsCode - Тестирование проектов\n\n"
        f"Бот создан для Группы 71-1, 3 месяц"
    )

@router.message(F.text.lower() == "группа")
async def cmd_group_f(message: Message):
    await message.answer(
        f"Твоя группа: 71-1"
    )

@router.message(F.text == "Корзина")
async def cmd_corzina_f(message: Message):
    await message.answer(
        f"Твоя корзина пуста"
    )

@router.message(F.text.lower() == "пока")
async def cmd_bye(message: Message):
    await message.answer("👋🏻")

# @router.message()
# async def cmd_echo(message:Message):
#     await message.answer(f"Ты написал: {message.text}")


# _________________________

@router.callback_query(F.data == "quiz_start")
async def callback_quiz_start(callback: CallbackQuery, state: FSMContext):
    await callback.answer("Начинаем игру", show_alert=True)
    await callback.message.answer(f"Вопрос 1: {QUESTIONS[0]['q']}")
    await state.update_data(index=0, score=0)   # сохраняем прогресс
    await state.set_state(Quiz.waiting_answer)


@router.message(Quiz.waiting_answer)
async def quiz_message(message: Message, state: FSMContext):
    data = await state.get_data()
    index = data["index"]
    score = data["score"]

    user_text = message.text.lower()

    if user_text == QUESTIONS[index]['a']:
        await message.answer(
            f"Правильно! Ответ: {user_text} | +1 балл"
        )
        
        score += 1
    else:
        await message.answer(
            f"Ответ неверный! Правильный ответ: {QUESTIONS[index]["a"]}"
        )

    index += 1
    if index >= len(QUESTIONS):
        await message.answer(
            "Викторина окончена! Молодец\n" \
            f"Твой результат: {score}/{len(QUESTIONS)} очков"
        )
        await state.clear()
    else:
        await state.update_data(index=index, score=score)
        await message.answer(f"Вопрос {index+1}: {QUESTIONS[index]["q"]}") 