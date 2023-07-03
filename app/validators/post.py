def is_text(field):
    ERROR_MSG = (
        'Поле не может быть пустой строкой '
        'или быть последовательностью одного символа!')
    if field in ('', ' ') or len(set(field)) < 2:
        raise ValueError(ERROR_MSG)
