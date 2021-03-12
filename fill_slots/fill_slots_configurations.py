# import fill_slots
# import fill_money
# import fill_manufacturer
# import fill_duration
from fill_slots import fill_money, fill_manufacturer, fill_duration, fill_slots, fill_victim


def basic_fill_slots(text):
    return fill_slots.fill_slots(
        text,
        money_func=fill_money.fill_money,
        manufacturer_func=fill_manufacturer.fill_manufacturer,
        duration_func=fill_duration.fill_duration,
        victim_func=fill_victim.fill_victim
    )
