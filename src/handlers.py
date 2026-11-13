
from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from src.keyboards import *
from src.state import *
from src.questions import *
from db.users import *
from db.questions import get_all_questions
from db.results import save_result

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

@router.message(F.text == "Профиль")
async def cmd_profile(message: Message):
    user_tg_id = message.from_user.id
    user = get_user(user_tg_id)
    user_db_id = user['id']
    user_db_tg_username = user['username']
    await message.answer(f"Ваш профиль:\n\n"
                         f"Ваш айди в БД: {user_db_id}\n"
                         f"Ваш айди телеграм: {user_tg_id}\n\n"
                         f"Ваш юзернейм в телеграм: @{message.from_user.username}\n"
                         f"Ваш юзернейм в БД: @{user_db_tg_username}", reply_markup=profile_inline_buttons)

@router.message(F.text == "Начать Викторину")
async def start_message_quiz(message: Message, state: FSMContext):
    await state.clear()
    questions = get_all_questions()
    if not questions:
        await message.answer("Вопросов нету в базе")

    await message.answer(f"Вопрос 1: {questions[0]['question_text']}")
    await state.update_data(questions=questions, index=0, score=0)   # сохраняем прогресс
    await state.set_state(Quiz.waiting_answer)
    



# _________________________

@router.callback_query(F.data == "main_menu")
async def callback_main_menu(callback: CallbackQuery):
    await callback.answer("Вы в главном меню")
    await callback.message.answer(
            f"Привет {callback.from_user.full_name} (@{callback.from_user.username}), Ты в главном меню!", reply_markup=reply_buttons
        )

@router.callback_query(F.data == "delete_user")
async def callback_delete_user(callback: CallbackQuery):
    await callback.answer()
    tg_id = callback.from_user.id
    delete_user(tg_id)
    await callback.message.answer("Ваша запись в бд - удалена. Чтобы начать пользоваться ботом, пропишите /start")

@router.callback_query(F.data == "change_username")
async def callback_change_username(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    tg_id = callback.from_user.id
    await callback.message.answer("Введите новый юзернейм для бд")
    await state.set_state(User.waiting_username)
    

@router.callback_query(F.data == "quiz_start")
async def callback_quiz_start(callback: CallbackQuery, state: FSMContext):
    await callback.answer("Начинаем игру", show_alert=True)
    await state.clear()
    questions = get_all_questions()
    if not questions:
        await callback.message.answer("Вопросов нету в базе")

    


    await callback.message.answer(f"Вопрос 1: {questions[0]['question_text']}")
    await state.update_data(questions=questions, index=0, score=0)   # сохраняем прогресс
    await state.set_state(Quiz.waiting_answer)


@router.message(Quiz.waiting_answer)
async def quiz_message(message: Message, state: FSMContext):
    data = await state.get_data()
    questions = data["questions"]
    index = data["index"]
    score = data["score"]

    user_text = message.text.lower()

    user = get_user(message.from_user.id)
    if not user:
        return
    q = questions[index]

    is_correct = user_text == q['correct_answer']
    save_result(
        user_id=user["id"],
        question_id=q["id"],
        is_correct=is_correct
    )

    if is_correct:
        await message.answer(
            f"Правильно! Ответ: {user_text} | +1 балл"
        )
        
        score += 1
    else:
        await message.answer(
            f"Ответ неверный! Правильный ответ: {q["correct_answer"]}"
        )

    index += 1
    if index >= len(questions):
        await message.answer(
            "Викторина окончена! Молодец\n" \
            f"Твой результат: {score}/{len(questions)} очков",
            reply_markup=new_quiz_game
        )
        await state.clear()
    else:
        await state.update_data(index=index, score=score)
        await message.answer(f"Вопрос {index+1}: {questions[index]['question_text']}") 


@router.message(User.waiting_username)
async def state_new_username(message: Message, state: FSMContext):
    tg_id = message.from_user.id
    text = message.text
    update_username(username=text, telegram_id=tg_id)
    await message.answer(f"Ваш юзернейм в базе данных изменено на @{text}")
    await state.clear()