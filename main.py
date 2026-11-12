import argparse
import logging
import sys
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from pathlib import Path

LOG_PATH = Path(__file__).resolve().parent / "errors.log"
logging.basicConfig(
    filename=LOG_PATH,
    level=logging.ERROR,
    format="[%(asctime)s] %(levelname)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    encoding="utf-8",
)


class LoggedArgumentParser(argparse.ArgumentParser):
    """Сохраняет ошибки разбора командной строки в журнал."""

    def error(self, message):
        error = ValueError(message)
        logging.error("%s: %s | Операция: разбор аргументов командной строки", type(error).__name__, error)
        super().error(message)


def positive_price(value):
    """Проверяет цену и преобразует её в Decimal."""
    try:
        price = Decimal(str(value).replace(",", "."))
        if not price.is_finite() or price <= 0:
            raise ValueError("Цена должна быть положительным конечным числом.")
        return price
    except InvalidOperation as exc:
        raise ValueError(f"Некорректная цена '{value}': введите число больше нуля.") from exc


def positive_quantity(value):
    try:
        quantity = int(value)
    except (TypeError, ValueError) as exc:
        raise ValueError("Количество должно быть целым числом.") from exc
    if quantity <= 0:
        raise ValueError("Количество должно быть больше нуля.")
    return quantity


def discount_value(value):
    try:
        discount = Decimal(str(value).replace(",", "."))
    except InvalidOperation as exc:
        raise ValueError("Скидка должна быть числом от 0 до 100.") from exc
    if not discount.is_finite() or not 0 <= discount <= 100:
        raise ValueError("Скидка должна быть числом от 0 до 100.")
    return discount


def get_discount_percent(total):
    """Правила автоматической скидки из практических №1 и №2."""
    if total >= 15000:
        return Decimal("15")
    if total >= 10000:
        return Decimal("10")
    if total >= 5000:
        return Decimal("5")
    return Decimal("0")


def amount_to_next_discount(total):
    for limit, discount in ((5000, 5), (10000, 10), (15000, 15)):
        if total < limit:
            return Decimal(limit) - total, discount
    return Decimal("0"), None


def money(value):
    return str(value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))


def calculate(products, requested_discount=None):
    total = sum((item["price"] * item["quantity"] for item in products), Decimal("0"))
    percent = get_discount_percent(total) if requested_discount is None else requested_discount
    reduction = (total * percent / 100).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    return total, percent, reduction, total - reduction


def show_result(products, currency="RUB", requested_discount=None, verbose=False):
    total, percent, reduction, final = calculate(products, requested_discount)
    print("\n=== Расчёт стоимости покупки ===")
    for item in products:
        print(f"Товар: {item['name']}")
        print(f"Цена: {money(item['price'])} {currency}")
        print(f"Количество: {item['quantity']}")
        if verbose or len(products) > 1:
            subtotal = item["price"] * item["quantity"]
            print(f"Стоимость товара: {money(subtotal)} {currency}")
    print(f"Общая стоимость: {money(total)} {currency}")
    print(f"Скидка: {percent}%")
    print(f"Размер скидки: {money(reduction)} {currency}")
    print(f"Итоговая стоимость: {money(final)} {currency}")
    if verbose:
        print(f"Тип скидки: {'автоматическая' if requested_discount is None else 'задана вручную'}")
        print(f"Формула: {money(total)} - {money(reduction)} = {money(final)} {currency}")
        if requested_discount is None:
            remaining, next_percent = amount_to_next_discount(total)
            if next_percent is None:
                print("Достигнута максимальная автоматическая скидка: 15%.")
            else:
                print(f"До скидки {next_percent}% осталось: {money(remaining)} {currency}")


def interactive_mode():
    """Режим практической №2: ввод нескольких товаров с повтором при ошибке."""
    products = []
    print("=== Интерактивный режим ===")
    while True:
        try:
            name = input("Название товара: ").strip()
            if not name:
                raise ValueError("Название товара не должно быть пустым.")
            price = positive_price(input("Цена товара: "))
            quantity = positive_quantity(input("Количество товара: "))
        except ValueError as exc:
            logging.error("%s: %s | Операция: добавление товара", type(exc).__name__, exc)
            print(f"Ошибка: {exc} Повторите ввод товара.\n")
            continue

        products.append({"name": name, "price": price, "quantity": quantity})
        while True:
            answer = input("Добавить ещё товар? (да/нет): ").strip().lower()
            if answer in ("да", "нет"):
                break
            exc = ValueError("Ответ должен быть 'да' или 'нет'.")
            logging.error("%s: %s | Операция: выбор продолжения", type(exc).__name__, exc)
            print(f"Ошибка: {exc}")
        if answer == "нет":
            break
    show_result(products, verbose=True)


def make_parser():
    parser = LoggedArgumentParser(
        description="Расчёт стоимости покупки с автоматической или заданной скидкой."
    )
    parser.add_argument("product", nargs="?", help="Название товара (в кавычках, если есть пробелы)")
    parser.add_argument("price", nargs="?", help="Цена одного товара")
    parser.add_argument("--quantity", type=str, help="Количество товара (целое число больше нуля)")
    parser.add_argument("--discount", help="Скидка от 0 до 100%% (по умолчанию автоматическая)")
    parser.add_argument("--currency", default="RUB", help="Валюта: RUB, USD или EUR (по умолчанию RUB)")
    parser.add_argument("--verbose", action="store_true", help="Показать подробный расчёт")
    return parser


def main(argv=None):
    parser = make_parser()
    arguments = sys.argv[1:] if argv is None else argv
    args = parser.parse_args(arguments)
    try:
        if not arguments:
            interactive_mode()
            return 0
        if args.product is None or args.price is None or args.quantity is None:
            raise ValueError("Для командного режима нужны название, цена и --quantity.")
        name = args.product.strip()
        if not name:
            raise ValueError("Название товара не должно быть пустым.")
        price = positive_price(args.price)
        quantity = positive_quantity(args.quantity)
        discount = discount_value(args.discount) if args.discount is not None else None
        currency = args.currency.upper()
        if currency not in ("RUB", "USD", "EUR"):
            raise ValueError("Валюта должна быть RUB, USD или EUR.")
        show_result([{"name": name, "price": price, "quantity": quantity}], currency, discount, args.verbose)
        return 0
    except (ValueError, ArithmeticError, EOFError, KeyboardInterrupt) as exc:
        logging.error("%s: %s | Операция: ввод данных и расчёт покупки", type(exc).__name__, exc)
        print(f"Ошибка: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
