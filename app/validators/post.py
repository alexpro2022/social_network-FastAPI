def is_text(field):
    error_msg = (
        'Поле не может быть пустой строкой '
        'или быть последовательностью одного символа!')
    if field in ('', ' ') or len(set(field)) < 2:
        raise ValueError(error_msg)
