# vvot15_homework_2
## Журавлёв Алексей Константинович 11-007
### Запуск:
1. ```git clone https://github.com/UnMelow/vvot15_homework_2.git```
2. ```cd vvot15_homework_2```
3. ```pip install -r requirements.txt```
4. Не обходимо создать конфигурационный файл по пути - .config/cloudphoto/cloudphotorc
Примерный вариант данного файла:
```
    bucket = INPUT_BUCKET_NAME 
    aws_access_key_id = INPUT_AWS_ACCESS_KEY_ID 
    aws_secret_access_key = INPUT_AWS_SECRET_ACCESS_KEY 
    region = ru-central1 
    endpoint_url = https://storage.yandexcloud.net
```
5. Запускать с помощью команды
```python -m cloudphoto {command} {args}```

## Возможности

- **Загрузка фотографий (upload)**: Отправка фотографий в облачное хранилище.
- **Скачивание фотографий (download)**: Загрузка фотографий из облачного хранилища.
- **Просмотр списка альбомов (list)**: Вывод списка альбомов в облачном хранилище.
- **Удаление альбомов и фотографий (delete)**: Удаление альбомов и фотографий.
- **Создание веб-сайта (mksite)**: Формирование и публикация веб-страниц фотоархива.
- **Инициализация (init)**: Настройка и инициализация программы.

### Инициализация

Перед началом использования необходимо инициализировать программу:

```bash
python cloudphoto.py init
```

### Загрузка фотографий

Для отправки фотографий в облачное хранилище используйте команду `upload`:

```bash
python cloudphoto.py upload --album ALBUM_NAME [--path PHOTOS_DIR]
```

### Скачивание фотографий

Для загрузки фотографий из облачного хранилища используйте команду `download`:

```bash
python cloudphoto.py download --album ALBUM_NAME [--path PHOTOS_DIR]
```

### Просмотр списка альбомов

Для просмотра списка альбомов в облачном хранилище используйте команду `list`:

```bash
python cloudphoto.py list [--album ALBUM_NAME]
```

### Удаление альбомов и фотографий

Для удаления альбомов и фотографий используйте команду `delete`:

```bash
python cloudphoto.py delete --album ALBUM_NAME [--photo PHOTO_NAME]
```

### Создание веб-сайта

Для формирования и публикации веб-страниц фотоархива используйте команду `mksite`:

```bash
python cloudphoto.py mksite
```

