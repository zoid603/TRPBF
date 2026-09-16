from datetime import datetime, date


def input_int(prompt: str) -> int:
    """Запрос целого неотрицательного числа с защитой от ошибок ввода."""
    while True:
        raw_val = input(prompt).strip()
        try:
            val = int(raw_val)
            if val < 0:
                print("Число не может быть отрицательным.")
                continue
            return val
        except ValueError:
            print("Ошибка: введите корректное целое число.")


def input_date(prompt: str) -> date:
    """Запрос даты в формате ГГГГ-ММ-ДД с защитой от ошибок."""
    while True:
        raw_val = input(prompt).strip()
        try:
            return datetime.strptime(raw_val, "%Y-%m-%d").date()
        except ValueError:
            print("Ошибка: формат ГГГГ-ММ-ДД (например 2026-09-15).")
