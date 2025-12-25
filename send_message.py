def build_message() -> str:
    now = datetime.now(TZ)

    day = now.day
    month = now.month
    year = now.year

    top = f"{month:02d}{day:02d}"  # МесяцДень сверху
    bottom = f"{year}"              # Год снизу

    # Сложение столбиком без переноса
    result = ""
    for i in range(len(top)-1):
        result += str(int(top[i]) + int(bottom[i]))  # обычное сложение
    # Крайний правый столбик
    result += str(int(top[-1]) + int(bottom[-1]))

    widest = max(len(top), len(bottom), len(result))
    sep = "-" * widest

    msg = (
        f"Пароль на актуальную дату: <b>{day:02d}.{month:02d}.{year}</b>\n\n"
        f"<pre>"
        f"{top.rjust(widest)}\n"
        f"+{bottom.rjust(widest)}\n"
        f"{sep}\n"
        f"{result.rjust(widest)}"
        f"</pre>\n\n"
        f"Пароль: <b>{result}</b>"
    )
    return msg
