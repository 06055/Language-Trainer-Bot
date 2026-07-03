import random

import aiosqlite
from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import KeyboardButton, Message, ReplyKeyboardMarkup


router = Router()

DB_NAME = "language_trainer.db"


LANGUAGES = {
    "🇬🇧 English": "English",
    "🇩🇪 Deutsch": "Deutsch",
    "🇵🇱 Polski": "Polski",
}

LEVELS = {
    "🟢 Початковий (Beginner)": "Beginner",
    "🟡 Junior": "Junior",
    "🟠 Middle": "Middle",
    "🔴 Advanced": "Advanced",
}

WORDS = {
    "English": {
        "Beginner": [
            ("apple", "яблуко", "I eat an apple every morning."),
            ("book", "книга", "This book is interesting."),
            ("water", "вода", "I drink water after training."),
            ("house", "будинок", "My house is small but cozy."),
            ("friend", "друг", "My friend lives nearby."),
            ("school", "школа", "The children go to school."),
            ("family", "сім'я", "My family is very friendly."),
            ("sun", "сонце", "The sun is bright today."),
            ("city", "місто", "Kyiv is a beautiful city."),
            ("food", "їжа", "This food is tasty."),
        ],
        "Junior": [
            ("travel", "подорожувати", "We travel by train in summer."),
            ("improve", "покращувати", "I want to improve my English."),
            ("choose", "обирати", "Choose the correct answer."),
            ("explain", "пояснювати", "Can you explain this rule?"),
            ("busy", "зайнятий", "She is busy today."),
            ("healthy", "здоровий", "Healthy food gives you energy."),
            ("quickly", "швидко", "He answered quickly."),
            ("lesson", "урок", "The lesson starts at nine."),
            ("mistake", "помилка", "This mistake is easy to fix."),
            ("practice", "практика", "Daily practice helps a lot."),
        ],
        "Middle": [
            ("achieve", "досягати", "You can achieve your goal."),
            ("support", "підтримувати", "Friends support each other."),
            ("environment", "довкілля", "We should protect the environment."),
            ("opportunity", "можливість", "This is a great opportunity."),
            ("challenge", "виклик", "Learning a language is a challenge."),
            ("decision", "рішення", "It was a difficult decision."),
            ("experience", "досвід", "Experience is important for this job."),
            ("necessary", "необхідний", "Sleep is necessary for health."),
            ("confident", "впевнений", "She feels confident before the test."),
            ("conversation", "розмова", "We had a long conversation."),
        ],
        "Advanced": [
            ("nevertheless", "проте", "It was raining; nevertheless, we went out."),
            ("sophisticated", "складний", "The app has a sophisticated design."),
            ("assumption", "припущення", "Your assumption may be correct."),
            ("consequence", "наслідок", "Every action has a consequence."),
            ("prioritize", "розставляти пріоритети", "You need to prioritize your tasks."),
            ("sustainable", "сталий", "They support sustainable development."),
            ("perspective", "точка зору", "Try to see another perspective."),
            ("significant", "значний", "The result is significant."),
            ("comprehensive", "всебічний", "We need a comprehensive plan."),
            ("efficient", "ефективний", "This method is efficient."),
        ],
    },
    "Deutsch": {
        "Beginner": [
            ("das Haus", "будинок", "Das Haus ist groß."),
            ("das Buch", "книга", "Ich lese ein Buch."),
            ("das Wasser", "вода", "Ich trinke Wasser."),
            ("der Freund", "друг", "Mein Freund ist hier."),
            ("die Schule", "школа", "Die Schule beginnt um acht."),
            ("die Familie", "сім'я", "Meine Familie ist groß."),
            ("die Sonne", "сонце", "Die Sonne scheint."),
            ("die Stadt", "місто", "Berlin ist eine Stadt."),
            ("das Essen", "їжа", "Das Essen ist gut."),
            ("der Tag", "день", "Heute ist ein guter Tag."),
        ],
        "Junior": [
            ("reisen", "подорожувати", "Wir reisen nach Polen."),
            ("verbessern", "покращувати", "Ich verbessere mein Deutsch."),
            ("wählen", "обирати", "Wählen Sie eine Antwort."),
            ("erklären", "пояснювати", "Kannst du das erklären?"),
            ("beschäftigt", "зайнятий", "Ich bin heute beschäftigt."),
            ("gesund", "здоровий", "Sport ist gesund."),
            ("schnell", "швидко", "Sie läuft schnell."),
            ("die Stunde", "урок", "Die Stunde ist interessant."),
            ("der Fehler", "помилка", "Der Fehler ist klein."),
            ("üben", "практикуватися", "Wir üben jeden Tag."),
        ],
        "Middle": [
            ("erreichen", "досягати", "Du kannst dein Ziel erreichen."),
            ("unterstützen", "підтримувати", "Wir unterstützen unser Team."),
            ("die Umwelt", "довкілля", "Die Umwelt braucht Schutz."),
            ("die Gelegenheit", "можливість", "Das ist eine gute Gelegenheit."),
            ("die Herausforderung", "виклик", "Das ist eine neue Herausforderung."),
            ("die Entscheidung", "рішення", "Die Entscheidung ist wichtig."),
            ("die Erfahrung", "досвід", "Ich habe viel Erfahrung."),
            ("notwendig", "необхідний", "Hilfe ist notwendig."),
            ("selbstbewusst", "впевнений", "Sie ist sehr selbstbewusst."),
            ("das Gespräch", "розмова", "Das Gespräch war lang."),
        ],
        "Advanced": [
            ("trotzdem", "проте", "Es regnet, trotzdem gehen wir spazieren."),
            ("anspruchsvoll", "складний", "Diese Aufgabe ist anspruchsvoll."),
            ("die Annahme", "припущення", "Die Annahme ist logisch."),
            ("die Folge", "наслідок", "Das ist die Folge der Entscheidung."),
            ("priorisieren", "розставляти пріоритети", "Wir müssen Aufgaben priorisieren."),
            ("nachhaltig", "сталий", "Nachhaltige Energie ist wichtig."),
            ("die Perspektive", "точка зору", "Deine Perspektive ist interessant."),
            ("bedeutend", "значний", "Das ist ein bedeutender Erfolg."),
            ("umfassend", "всебічний", "Wir brauchen eine umfassende Analyse."),
            ("effizient", "ефективний", "Der Prozess ist effizient."),
        ],
    },
    "Polski": {
        "Beginner": [
            ("dom", "будинок", "To jest mój dom."),
            ("książka", "книга", "Czytam książkę."),
            ("woda", "вода", "Piję wodę."),
            ("przyjaciel", "друг", "Mój przyjaciel jest miły."),
            ("szkoła", "школа", "Szkoła jest blisko."),
            ("rodzina", "сім'я", "Moja rodzina mieszka w Lublinie."),
            ("słońce", "сонце", "Słońce świeci."),
            ("miasto", "місто", "Warszawa to duże miasto."),
            ("jedzenie", "їжа", "Jedzenie jest smaczne."),
            ("dzień", "день", "To dobry dzień."),
        ],
        "Junior": [
            ("podróżować", "подорожувати", "Lubię podróżować latem."),
            ("poprawiać", "покращувати", "Chcę poprawiać swój polski."),
            ("wybierać", "обирати", "Wybieraj dobrą odpowiedź."),
            ("wyjaśniać", "пояснювати", "Proszę wyjaśniać powoli."),
            ("zajęty", "зайнятий", "Dzisiaj jestem zajęty."),
            ("zdrowy", "здоровий", "Zdrowy styl życia jest ważny."),
            ("szybko", "швидко", "On mówi szybko."),
            ("lekcja", "урок", "Lekcja zaczyna się rano."),
            ("błąd", "помилка", "To jest mały błąd."),
            ("ćwiczyć", "практикуватися", "Ćwiczę codziennie."),
        ],
        "Middle": [
            ("osiągać", "досягати", "Możesz osiągać swoje cele."),
            ("wspierać", "підтримувати", "Rodzina mnie wspiera."),
            ("środowisko", "довкілля", "Chronimy środowisko."),
            ("okazja", "можливість", "To dobra okazja."),
            ("wyzwanie", "виклик", "Nowa praca to wyzwanie."),
            ("decyzja", "рішення", "To trudna decyzja."),
            ("doświadczenie", "досвід", "Mam doświadczenie w nauce."),
            ("konieczny", "необхідний", "Odpoczynek jest konieczny."),
            ("pewny siebie", "впевнений", "On jest pewny siebie."),
            ("rozmowa", "розмова", "Rozmowa była długa."),
        ],
        "Advanced": [
            ("jednakże", "проте", "Pada deszcz, jednakże idziemy dalej."),
            ("zaawansowany", "складний", "To zaawansowany poziom."),
            ("założenie", "припущення", "To założenie jest rozsądne."),
            ("konsekwencja", "наслідок", "To konsekwencja wyboru."),
            ("priorytetyzować", "розставляти пріоритети", "Musimy priorytetyzować zadania."),
            ("zrównoważony", "сталий", "Zrównoważony rozwój jest ważny."),
            ("perspektywa", "точка зору", "Twoja perspektywa pomaga."),
            ("znaczący", "значний", "To znaczący postęp."),
            ("kompleksowy", "всебічний", "Potrzebujemy kompleksowego planu."),
            ("wydajny", "ефективний", "Ten system jest wydajny."),
        ],
    },
}

ACTIVE_TESTS = {}


MAIN_KEYBOARD = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🌍 Обрати мову")],
        [KeyboardButton(text="📖 Почати навчання"), KeyboardButton(text="📝 Міні-тест")],
        [KeyboardButton(text="📊 Мій прогрес"), KeyboardButton(text="⚙️ Налаштування")],
    ],
    resize_keyboard=True,
)

LANGUAGE_KEYBOARD = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🇬🇧 English")],
        [KeyboardButton(text="🇩🇪 Deutsch")],
        [KeyboardButton(text="🇵🇱 Polski")],
        [KeyboardButton(text="⬅️ Головне меню")],
    ],
    resize_keyboard=True,
)

LEVEL_KEYBOARD = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🟢 Початковий (Beginner)")],
        [KeyboardButton(text="🟡 Junior")],
        [KeyboardButton(text="🟠 Middle")],
        [KeyboardButton(text="🔴 Advanced")],
        [KeyboardButton(text="⬅️ Головне меню")],
    ],
    resize_keyboard=True,
)

SETTINGS_KEYBOARD = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🌍 Обрати мову")],
        [KeyboardButton(text="Змінити рівень")],
        [KeyboardButton(text="⬅️ Головне меню")],
    ],
    resize_keyboard=True,
)


async def init_db():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                language TEXT,
                level TEXT,
                correct_answers INTEGER DEFAULT 0
            )
            """
        )
        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS studied_words (
                user_id INTEGER,
                language TEXT,
                level TEXT,
                word TEXT,
                translation TEXT,
                example TEXT,
                PRIMARY KEY (user_id, language, level, word)
            )
            """
        )
        await db.commit()


async def get_user(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        db.row_factory = aiosqlite.Row
        await db.execute(
            "INSERT OR IGNORE INTO users (user_id) VALUES (?)",
            (user_id,),
        )
        await db.commit()

        cursor = await db.execute(
            "SELECT * FROM users WHERE user_id = ?",
            (user_id,),
        )
        return await cursor.fetchone()


async def set_language(user_id, language):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            "INSERT OR IGNORE INTO users (user_id) VALUES (?)",
            (user_id,),
        )
        await db.execute(
            "UPDATE users SET language = ?, level = NULL WHERE user_id = ?",
            (language, user_id),
        )
        await db.commit()


async def set_level(user_id, level):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            "INSERT OR IGNORE INTO users (user_id) VALUES (?)",
            (user_id,),
        )
        await db.execute(
            "UPDATE users SET level = ? WHERE user_id = ?",
            (level, user_id),
        )
        await db.commit()


async def save_studied_word(user_id, language, level, word_data):
    word, translation, example = word_data

    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            """
            INSERT OR IGNORE INTO studied_words
            (user_id, language, level, word, translation, example)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (user_id, language, level, word, translation, example),
        )
        await db.commit()


async def get_studied_words(user_id, language, level):
    async with aiosqlite.connect(DB_NAME) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute(
            """
            SELECT word, translation, example
            FROM studied_words
            WHERE user_id = ? AND language = ? AND level = ?
            """,
            (user_id, language, level),
        )
        return await cursor.fetchall()


async def get_studied_words_count(user_id, language, level):
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute(
            """
            SELECT COUNT(*)
            FROM studied_words
            WHERE user_id = ? AND language = ? AND level = ?
            """,
            (user_id, language, level),
        )
        row = await cursor.fetchone()
        return row[0]


async def add_correct_answer(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            """
            UPDATE users
            SET correct_answers = correct_answers + 1
            WHERE user_id = ?
            """,
            (user_id,),
        )
        await db.commit()


def get_language_button(language):
    for button_text, language_name in LANGUAGES.items():
        if language_name == language:
            return button_text
    return "Не обрано"


def get_level_button(level):
    for button_text, level_name in LEVELS.items():
        if level_name == level:
            return button_text
    return "Не обрано"


def get_next_word(language, level, studied_words):
    learned_words = {row["word"] for row in studied_words}
    all_words = WORDS[language][level]
    new_words = [word_data for word_data in all_words if word_data[0] not in learned_words]

    if new_words:
        return random.choice(new_words), True

    return random.choice(all_words), False


def make_test_keyboard(options):
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=options[0]), KeyboardButton(text=options[1])],
            [KeyboardButton(text=options[2]), KeyboardButton(text=options[3])],
            [KeyboardButton(text="⬅️ Головне меню")],
        ],
        resize_keyboard=True,
    )


async def ask_to_choose_language(message):
    await message.answer(
        "🌍 Оберіть мову для навчання:",
        reply_markup=LANGUAGE_KEYBOARD,
    )


async def ask_to_choose_level(message):
    await message.answer(
        "Тепер оберіть рівень:",
        reply_markup=LEVEL_KEYBOARD,
    )


async def show_main_menu(message):
    await message.answer(
        "Головне меню:",
        reply_markup=MAIN_KEYBOARD,
    )


@router.message(Command("start"))
@router.message(F.text.lower() == "старт")
async def start(message: Message):
    await get_user(message.from_user.id)
    await message.answer(
        "Привіт! Я Language Trainer Bot.\n"
        "Допоможу вивчати слова, повторювати переклад і перевіряти себе у міні-тестах."
    )
    await ask_to_choose_language(message)


@router.message(Command("help"))
async def help_command(message: Message):
    await message.answer(
        "Команди:\n"
        "<b>/start</b> - запуск бота і вибір мови\n"
        "<b>/help</b> - список команд\n"
        "<b>/about</b> - про бота\n\n"
        "У головному меню можна почати навчання, пройти міні-тест і подивитися прогрес.",
        parse_mode="HTML",
        reply_markup=MAIN_KEYBOARD,
    )


@router.message(Command("about"))
async def about_command(message: Message):
    await message.answer(
        "Це бот для вивчення іноземних мов на Python, aiogram 3 і SQLite.\n"
        "Він зберігає вашу мову, рівень, вивчені слова та правильні відповіді.",
        reply_markup=MAIN_KEYBOARD,
    )


@router.message(F.text == "Допомога")
async def help_button(message: Message):
    await help_command(message)


@router.message(F.text == "Про бота")
async def about_button(message: Message):
    await about_command(message)


@router.message(F.text == "⬅️ Головне меню")
async def back_to_menu(message: Message):
    ACTIVE_TESTS.pop(message.from_user.id, None)
    await show_main_menu(message)


@router.message(F.text == "🌍 Обрати мову")
async def choose_language(message: Message):
    await ask_to_choose_language(message)


@router.message(F.text.in_(LANGUAGES.keys()))
async def language_selected(message: Message):
    language = LANGUAGES[message.text]
    await set_language(message.from_user.id, language)
    await message.answer(
        f"Мову обрано: {message.text}",
    )
    await ask_to_choose_level(message)


@router.message(F.text.in_(LEVELS.keys()))
async def level_selected(message: Message):
    user = await get_user(message.from_user.id)

    if not user["language"]:
        await message.answer(
            "Спочатку оберіть мову.",
            reply_markup=LANGUAGE_KEYBOARD,
        )
        return

    level = LEVELS[message.text]
    await set_level(message.from_user.id, level)
    await message.answer(
        f"Рівень обрано: {message.text}\n\n"
        "Тепер можна натиснути «📖 Почати навчання».",
        reply_markup=MAIN_KEYBOARD,
    )


@router.message(F.text == "📖 Почати навчання")
async def start_learning(message: Message):
    user = await get_user(message.from_user.id)

    if not user["language"]:
        await message.answer(
            "Спочатку оберіть мову.",
            reply_markup=LANGUAGE_KEYBOARD,
        )
        return

    if not user["level"]:
        await message.answer(
            "Спочатку оберіть рівень.",
            reply_markup=LEVEL_KEYBOARD,
        )
        return

    language = user["language"]
    level = user["level"]
    studied_words = await get_studied_words(message.from_user.id, language, level)
    word_data, is_new_word = get_next_word(language, level, studied_words)
    await save_studied_word(message.from_user.id, language, level, word_data)

    word, translation, example = word_data
    status = "Нове слово додано до вашого прогресу." if is_new_word else "Усі слова рівня вже були показані. Повторюємо."

    await message.answer(
        f"📖 Слово: <b>{word}</b>\n"
        f"Переклад: <b>{translation}</b>\n"
        f"Приклад: <i>{example}</i>\n\n"
        f"{status}",
        parse_mode="HTML",
        reply_markup=MAIN_KEYBOARD,
    )


@router.message(F.text == "📝 Міні-тест")
async def mini_test(message: Message):
    user = await get_user(message.from_user.id)

    if not user["language"]:
        await message.answer(
            "Спочатку оберіть мову.",
            reply_markup=LANGUAGE_KEYBOARD,
        )
        return

    if not user["level"]:
        await message.answer(
            "Спочатку оберіть рівень.",
            reply_markup=LEVEL_KEYBOARD,
        )
        return

    language = user["language"]
    level = user["level"]
    studied_words = await get_studied_words(message.from_user.id, language, level)

    if not studied_words:
        await message.answer(
            "Поки що немає вивчених слів для тесту. Натисніть «📖 Почати навчання».",
            reply_markup=MAIN_KEYBOARD,
        )
        return

    question = random.choice(studied_words)
    correct_answer = question["translation"]
    all_translations = [word_data[1] for word_data in WORDS[language][level]]
    wrong_answers = [translation for translation in all_translations if translation != correct_answer]
    options = random.sample(wrong_answers, 3) + [correct_answer]
    random.shuffle(options)

    ACTIVE_TESTS[message.from_user.id] = {
        "word": question["word"],
        "correct_answer": correct_answer,
    }

    await message.answer(
        f"📝 Міні-тест\n\n"
        f"Як перекладається слово <b>{question['word']}</b>?",
        parse_mode="HTML",
        reply_markup=make_test_keyboard(options),
    )


@router.message(F.text == "📊 Мій прогрес")
async def my_progress(message: Message):
    user = await get_user(message.from_user.id)
    language = user["language"]
    level = user["level"]

    if language and level:
        learned_words = await get_studied_words_count(message.from_user.id, language, level)
    else:
        learned_words = 0

    await message.answer(
        "📊 Мій прогрес\n\n"
        f"Мова: {get_language_button(language)}\n"
        f"Рівень: {get_level_button(level)}\n"
        f"Вивчено слів: {learned_words}\n"
        f"Правильних відповідей у тестах: {user['correct_answers']}",
        reply_markup=MAIN_KEYBOARD,
    )


@router.message(F.text == "⚙️ Налаштування")
async def settings(message: Message):
    user = await get_user(message.from_user.id)
    await message.answer(
        "⚙️ Налаштування\n\n"
        f"Поточна мова: {get_language_button(user['language'])}\n"
        f"Поточний рівень: {get_level_button(user['level'])}\n\n"
        "Тут можна змінити мову або рівень.",
        reply_markup=SETTINGS_KEYBOARD,
    )


@router.message(F.text == "Змінити рівень")
async def change_level(message: Message):
    user = await get_user(message.from_user.id)

    if not user["language"]:
        await message.answer(
            "Спочатку оберіть мову.",
            reply_markup=LANGUAGE_KEYBOARD,
        )
        return

    await ask_to_choose_level(message)


@router.message(lambda message: message.from_user.id in ACTIVE_TESTS)
async def check_test_answer(message: Message):
    test = ACTIVE_TESTS.pop(message.from_user.id)

    if message.text == test["correct_answer"]:
        await add_correct_answer(message.from_user.id)
        await message.answer(
            "✅ Правильно! Гарна робота.",
            reply_markup=MAIN_KEYBOARD,
        )
    else:
        await message.answer(
            f"❌ Неправильно.\n"
            f"Слово «{test['word']}» перекладається як «{test['correct_answer']}».",
            reply_markup=MAIN_KEYBOARD,
        )


@router.message()
async def clear_message(message: Message):
    await message.answer(
        "Такої команди немає. Скористайтесь кнопками головного меню.",
        reply_markup=MAIN_KEYBOARD,
    )
