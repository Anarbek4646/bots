from aiogram import Bot, Dispatcher, types
import logging
from aiogram.utils import executor
from config import dp, bot
from handlers import clients, calback, admin, fsm_anketa, extra
from handlers.clients import on_startup, on_shutdown

admin.register_handler_admin(dp)
clients.register_handler_clients(dp)
calback.register_handler_callback(dp)
fsm_anketa.register_handlers_fsm_anketa(dp)
extra.registrate_handler_extra(dp)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup, on_shutdown=on_shutdown)


