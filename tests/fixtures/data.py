ENDPOINT = 'post'
AUTH_USER = {"email": "testuser@example.com", "password": "testpass"}
AUTHOR = {"email": "author@example.com", "password": "author"}
POST_PAYLOAD = {"title": "POST New post title.", "content": "POST New post content."}
PUT_PAYLOAD = {"title": "update for title.",  "content": "update for content."}

# Messages
NOT_FOUND_MSG = 'Пост(ы) не найден(ы).'
INVALID_FIELD_MSG_1 = 'Поле не может быть пустой строкой или пробелом!'
INVALID_FIELD_MSG_2 = 'Поле не может быть последовательностью одного символа!'
NO_PERMISSION_MSG = 'У вас нет права доступа к данному посту.'
