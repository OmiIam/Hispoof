from .users import add_credits

def process_payment_success(tg_id, amount):
    credit_mapping = {
        500: 5,
        1000: 12,
        2000: 25
    }
    credits = credit_mapping.get(amount, 0)
    if credits > 0:
        add_credits(tg_id, credits)
        return True
    return False