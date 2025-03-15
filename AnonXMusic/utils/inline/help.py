import random
from typing import Union

from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from AnonXMusic import app


def help_pannel(_, START: Union[bool, int] = None):
    first = [InlineKeyboardButton(text=_["CLOSE_BUTTON"], callback_data="close")]
    second = [
        InlineKeyboardButton(
            text=_["BACK_BUTTON"],
            callback_data="settingsback_helper",
        ),
    ]
    mark = second if START else first

    # Creating a list of all 15 buttons
    buttons = [
        InlineKeyboardButton(text=_["H_B_1"], callback_data="help_callback hb1"),
        InlineKeyboardButton(text=_["H_B_2"], callback_data="help_callback hb2"),
        InlineKeyboardButton(text=_["H_B_3"], callback_data="help_callback hb3"),
        InlineKeyboardButton(text=_["H_B_4"], callback_data="help_callback hb4"),
        InlineKeyboardButton(text=_["H_B_5"], callback_data="help_callback hb5"),
        InlineKeyboardButton(text=_["H_B_6"], callback_data="help_callback hb6"),
        InlineKeyboardButton(text=_["H_B_7"], callback_data="help_callback hb7"),
        InlineKeyboardButton(text=_["H_B_8"], callback_data="help_callback hb8"),
        InlineKeyboardButton(text=_["H_B_9"], callback_data="help_callback hb9"),
        InlineKeyboardButton(text=_["H_B_10"], callback_data="help_callback hb10"),
        InlineKeyboardButton(text=_["H_B_11"], callback_data="help_callback hb11"),
        InlineKeyboardButton(text=_["H_B_12"], callback_data="help_callback hb12"),
        InlineKeyboardButton(text=_["H_B_13"], callback_data="help_callback hb13"),
        InlineKeyboardButton(text=_["H_B_14"], callback_data="help_callback hb14"),
        InlineKeyboardButton(text=_["H_B_15"], callback_data="help_callback hb15"),
    ]

    # Shuffle the buttons
    random.shuffle(buttons)

    # Splitting buttons into exactly 5 rows of 3 buttons each
    button_rows = [buttons[i:i + 3] for i in range(0, 15, 3)]

    # Add the final row (either close or back button)
    button_rows.append(mark)

    # Create the inline keyboard markup
    return InlineKeyboardMarkup(button_rows)


def help_back_markup(_):
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text=_["BACK_BUTTON"],
                    callback_data="settings_back_helper",
                ),
            ]
        ]
    )


def private_help_panel(_):
    return [
        [
            InlineKeyboardButton(
                text=_["S_B_4"],
                url=f"https://t.me/{app.username}?start=help",
            ),
        ],
    ]
