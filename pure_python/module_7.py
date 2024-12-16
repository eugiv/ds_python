from rate_cls import Rate


def currency_name():
    currencies = Rate().exchange_rates()

    refined_currencies = {}
    for cur_value in currencies.values():
        refined_currencies[cur_value["Name"]] = cur_value["Value"]

    cur_name_max_value = max(refined_currencies, key=refined_currencies.get)

    return cur_name_max_value


print(currency_name())
