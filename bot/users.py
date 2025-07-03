from tinydb import TinyDB, Query
db = TinyDB("db/users.json")
User = Query()

def get_or_create_user(tg_id):
    user = db.get(User.telegram_id == tg_id)
    if not user:
        db.insert({"telegram_id": tg_id, "credits": 2, "caller_id": "", "is_admin": False})
    return db.get(User.telegram_id == tg_id)

def update_user(tg_id, **kwargs):
    db.update(kwargs, User.telegram_id == tg_id)

def add_credits(tg_id, amount):
    user = get_or_create_user(tg_id)
    new_credits = user["credits"] + amount
    update_user(tg_id, credits=new_credits)

def deduct_credit(tg_id):
    user = get_or_create_user(tg_id)
    if user["credits"] > 0:
        update_user(tg_id, credits=user["credits"] - 1)
        return True
    return False

def list_all_users():
    return db.all()

def is_admin(tg_id):
    from .config import AUTHORIZED_ADMINS
    return tg_id in AUTHORIZED_ADMINS