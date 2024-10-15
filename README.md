# Descriptions (описание)

Бот мониторит сообщения в вашей телеграмм группе с помощью ML.  
Это облегченная модель [cointegrated_rubert-tiny-sentiment-balanced](https://huggingface.co/cointegrated/rubert-tiny-sentiment-balanced) настроенная для классификации тонов коротких русских текстов.
Подробнее про модель [здесь](https://huggingface.co/cointegrated/rubert-tiny-sentiment-balanced)

## Solves the problem (для каких задач)

Текст сообщения обрабатывается через модель "text-classification" для определения в нем негатива.
При обнаружении негативного сообщения бот выводит предупреждение `Warning!!! You message toxic on 81%`
После третьего предупреждения бот блокирует пользователя на заданное время, после чего счетчик обнуляется.

(Результат негатива накапливается 0.83 + 0.75 + 0.92) Это сделано потому что некоторые словосочетания модель определяет как негатив на 0.45 или 0.54, а это не очевидные моменты (нужно доп наблюдение) при блокировке счетчик сбрасывается.  
Результаты определения работы модели записываются в лог файл
`[INFO] - (main.py).get_message(51) - True -> [{'label': 'negative', 'score': 0.9785379767417908}] -> негативный текст`

### Deploy (развертывание)

```bash
mkdir telegram_check_comments
git clone git@github.com:gusevskiy/telegram_check_comments.git
py -3.12 -m venv venv
pip install -r requirements.txt
```

Заполнить файл .env

```bash
API_ID=
API_HASH=
TOKEN=
BLOCK_TIME_HOUR=1
CHAT_ID=
```

Для работы приложения нужно поднять сессию https://docs.pyrogram.org/start/auth

- нужно передать в файл `add_session.py` `api_id` и `api_hash` и запустить скрипт

```bash
python .\utils\add_session.py
```

- Enter phone number or bot token: указать номер
- Enter confirmation code: ввести код (пришлет телеграм)  
Создаться файл сессии `my_client.session`

Модель загружаем локально в папку, так работает быстрее чем из venv.  
Загрузим модель локально в папку. Выполнить команду

```bash
python ./handlers/basic.py
# log = True -> [{'label': 'negative', 'score': 0.9392933249473572}]
```
скрип создаст папку `model` и загрузит в нее модель,

### Run (запуск)

```bash
python main.py
```

#### Technologies (технологии)

python-dotenv==1.0.1  
torch==2.4.1  
transformers==4.45.22

#### Plans for completion (планы/мечты)

- сделать обезличенного бота (сейчас он отвечает от воадельца акаунта).
- возможность добавлять в стороние чаты с правами администратора и без.
- тесты.
- deploy на сервер.
