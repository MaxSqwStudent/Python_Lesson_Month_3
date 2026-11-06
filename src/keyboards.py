from aiogram.types import (ReplyKeyboardMarkup, 
                           KeyboardButton,
                           
                           InlineKeyboardButton, InlineKeyboardMarkup)

reply_buttons = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Корзина"), KeyboardButton(text="Профиль")],
        [KeyboardButton(text="Каталог"), KeyboardButton(text="Контакты")]
    ],
    resize_keyboard=True,
    input_field_placeholder="Выберите пункт меню"
)


inline_buttons = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Наш сайт", url="https://geeks.kg")],
        [InlineKeyboardButton(text="Начать игру", callback_data="quiz_start")]
    ]
)