from fastapi import FastAPI

from api.chats.route import router as chat_router
from api.messages.route import router as message_router
from api.users.route import router as user_router
from api.authorization.route import router as auth_router
from api.config import API_PREFIX

app = FastAPI()

for router in [
    chat_router,
    message_router,
    user_router,
    auth_router,
]:
    app.include_router(router, prefix=API_PREFIX)
