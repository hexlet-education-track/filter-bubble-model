"""Модель рекомендательной ленты: как появляется пузырь фильтров."""

import random

# ========== Настройки эксперимента: меняйте только этот блок ==========

SEED = 42                 # «зерно» случайности: у всех одинаковое — у всех одинаковый результат
DAYS = 10                 # сколько дней пользователь листает ленту
FEED_SIZE = 20            # сколько постов в ленте за один день
LIKE_BOOST = 1.0          # насколько алгоритм усиливает тему за каждый лайк
RANDOM_SHARE = 0.0        # доля случайных постов в ленте: 0.0 — нет, 0.3 — 30%
LIKED_TOPICS = ["игры"]   # темы, которые пользователь лайкает

# ======================================================================

TOPICS = ["игры", "спорт", "наука", "музыка", "кино", "новости", "юмор", "IT"]
BAR_WIDTH = 20            # длина полоски в отчёте


def pick_topic(weights):
    """Выбирает тему для одного поста.

    С вероятностью RANDOM_SHARE тема случайная: так алгоритм «разведывает».
    Иначе тема выбирается по весам: чем больше вес, тем чаще она выпадает.
    """
    if random.random() < RANDOM_SHARE:
        return random.choice(TOPICS)

    topic_weights = []
    for topic in TOPICS:
        topic_weights.append(weights[topic])

    return random.choices(TOPICS, weights=topic_weights)[0]


def build_feed(weights):
    """Собирает ленту на один день: список тем из FEED_SIZE постов."""
    feed = []
    for _ in range(FEED_SIZE):
        feed.append(pick_topic(weights))
    return feed


def count_liked(feed):
    """Считает, сколько постов в ленте относятся к любимым темам."""
    liked = 0
    for topic in feed:
        if topic in LIKED_TOPICS:
            liked += 1
    return liked


def apply_likes(feed, weights):
    """Пользователь лайкает посты любимых тем, алгоритм усиливает эти темы."""
    for topic in feed:
        if topic in LIKED_TOPICS:
            weights[topic] += LIKE_BOOST


def print_day(day, feed):
    """Печатает строку отчёта за один день."""
    share = count_liked(feed) / len(feed)
    filled = round(share * BAR_WIDTH)
    bar = "#" * filled + "." * (BAR_WIDTH - filled)
    topics_in_feed = len(set(feed))

    print(f"День {day:2} | {bar} | любимые темы: {share:4.0%} | тем в ленте: {topics_in_feed} из {len(TOPICS)}")


def main():
    """Запускает эксперимент и печатает отчёт."""
    random.seed(SEED)

    weights = {}
    for topic in TOPICS:
        weights[topic] = 1.0

    print(f"Лайкаем: {', '.join(LIKED_TOPICS)} | LIKE_BOOST = {LIKE_BOOST} | RANDOM_SHARE = {RANDOM_SHARE}")
    print()

    bubble_day = None
    last_feed = []

    for day in range(1, DAYS + 1):
        feed = build_feed(weights)
        print_day(day, feed)

        share = count_liked(feed) / len(feed)
        if bubble_day is None and share > 0.8:
            bubble_day = day

        apply_likes(feed, weights)
        last_feed = feed

    print()
    print("Итог:")
    print(f"  доля любимых тем в последний день: {count_liked(last_feed) / len(last_feed):.0%}")
    print(f"  тем в ленте в последний день: {len(set(last_feed))} из {len(TOPICS)}")

    if bubble_day is None:
        print("  доля любимых тем ни разу не превысила 80% — пузыря нет")
    else:
        print(f"  день, когда доля любимых тем впервые превысила 80%: {bubble_day}")


if __name__ == "__main__":
    main()
