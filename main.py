def read_positive_float(prompt):
    """Считывает положительное вещественное число."""
    while True:
        try:
            value = float(input(prompt).replace(",", "."))
            if value <= 0:
                print("Ошибка: значение должно быть больше нуля.")
                continue
            return value
        except ValueError:
            print("Ошибка: введите корректное число.")


def read_positive_int(prompt):
    """Считывает положительное целое число."""
    while True:
        try:
            value = int(input(prompt))
            if value <= 0:
                print("Ошибка: количество должно быть больше нуля.")
                continue
            return value
        except ValueError:
            print("Ошибка: введите целое число.")


def get_discount_percent(total):
    """Определяет процент скидки по исходной стоимости покупки."""
    if total >= 15000:
        return 15
    elif total >= 10000:
        return 10
    elif total >= 5000:
        return 5
    return 0


def amount_to_next_discount(total):
    """
    Дополнительный функционал:
    возвращает сумму, которой не хватает до следующего уровня скидки.
    """
    if total < 5000:
        return 5000 - total, 5
    elif total < 10000:
        return 10000 - total, 10
    elif total < 15000:
        return 15000 - total, 15
    return 0, None


def money(value):
    return f"{value:.2f}"


def main():
    print("=== Расчёт стоимости покупки ===")

    product = input("Название товара: ").strip()
    while not product:
        print("Ошибка: название товара не должно быть пустым.")
        product = input("Название товара: ").strip()

    price = read_positive_float("Цена товара: ")
    quantity = read_positive_int("Количество товара: ")

    original_total = price * quantity
    discount_percent = get_discount_percent(original_total)
    discount_amount = original_total * discount_percent / 100
    final_total = original_total - discount_amount
    saving_per_item = discount_amount / quantity

    print("\n=== Результат ===")
    print(f"Товар: {product}")
    print(f"Исходная стоимость: {money(original_total)} руб.")
    print(f"Скидка в процентах: {discount_percent}%")
    print(f"Скидка в рублях: {money(discount_amount)} руб.")
    print(f"Итоговая стоимость: {money(final_total)} руб.")
    print(f"Экономия на единицу товара: {money(saving_per_item)} руб.")

    remaining, next_percent = amount_to_next_discount(original_total)
    if next_percent is not None:
        print(
            f"До скидки {next_percent}% не хватает: "
            f"{money(remaining)} руб."
        )
    else:
        print("Достигнут максимальный уровень скидки: 15%.")


if __name__ == "__main__":
    main()
