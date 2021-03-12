# import fill_slots
# import fill_money
# import fill_manufacturer
# import fill_duration
# import fill_victim


def main():
    filled_slots = fill_slots.fill_slots(
        'Google released new feature. It costs 25 dollars. '
        'Developers from Facebook are going to create similar feature in next two weeks.',
        money_func=fill_money.fill_money,
        manufacturer_func=fill_manufacturer.fill_manufacturer,
        duration_func=fill_duration.fill_duration,
        victim_func=fill_victim.fill_victim
    )
    print(filled_slots)


if __name__ == '__main__':
    main()
