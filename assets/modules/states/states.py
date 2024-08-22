from aiogram.fsm.state import StatesGroup, State


class ManageSite(StatesGroup):
    adding_site = State()
    adding_class_name = State()
    removing_site = State()
    removing_class_name = State()
