
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
    """Определяет процент скидки."""
    if total >= 15000:
        return 15
    elif total >= 10000:
        return 10
    elif total >= 5000:
        return 5
    return 0


def amount_to_next_discount(total):
    """Определяет сумму до следующего уровня скидки."""
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

    products = []

    while True:
        print("\n--- Добавление товара ---")

        product = input("Введите название товара: ").strip()

        while not product:
            print("Ошибка: название товара не должно быть пустым.")
            product = input("Введите название товара: ").strip()

        price = read_positive_float("Введите цену: ")
        quantity = read_positive_int("Введите количество: ")

        product_total = price * quantity

        products.append({
            "name": product,
            "price": price,
            "quantity": quantity,
            "total": product_total
        })

        while True:
            answer = input(
                "Добавить ещё один товар? (да/нет): "
            ).strip().lower()

            if answer in ("да", "нет"):
                break

            print("Ошибка: введите 'да' или 'нет'.")

        if answer == "нет":
            break

    original_total = sum(item["total"] for item in products)

    discount_percent = get_discount_percent(original_total)
    discount_amount = original_total * discount_percent / 100
    final_total = original_total - discount_amount

    print("\n=== Список товаров ===")

    for item in products:
        print(
            f"{item['name']}: "
            f"{money(item['price'])} руб. x "
            f"{item['quantity']} = "
            f"{money(item['total'])} руб."
        )

    print("\n=== Результат покупки ===")
    print(f"Общая стоимость: {money(original_total)} руб.")
    print(f"Скидка: {discount_percent}%")
    print(f"Размер скидки: {money(discount_amount)} руб.")
    print(f"Итоговая стоимость: {money(final_total)} руб.")

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
