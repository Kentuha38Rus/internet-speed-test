import sys
import time
import requests

# Стандартная картинка для теста — мозаика NASA Black Marble (~40 МБ).
DEFAULT_URL = (
    "https://svs.gsfc.nasa.gov/vis/a030000/a030800/a030877/"
    "frames/5760x3240_16x9_01p/BlackMarble_2016_928m_india.tif"
)


def measure_speed(url, iterations=10):
    total_bytes = 0
    total_time = 0.0

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        ),
        "Accept": "image/avif,image/webp,image/apng,image/*,*/*;q=0.8",
    }

    print(f"\nНачинаем тестирование скорости для URL: {url}")
    print(f"Количество запросов: {iterations}\n")

    for i in range(1, iterations + 1):
        try:
            start_time = time.perf_counter()
            response = requests.get(url, headers=headers, timeout=300)
            response.raise_for_status()
            data_size = len(response.content)
            end_time = time.perf_counter()

            request_time = end_time - start_time
            total_bytes += data_size
            total_time += request_time

            print(
                f"Запрос {i:2d}: время = {request_time:.4f} сек., "
                f"размер = {data_size} байт "
                f"({data_size / (1024 * 1024):.2f} МБ)"
            )
        except requests.exceptions.SSLError as e:
            print(f"Ошибка SSL при запросе {i}: {e}")
            print(
                "На Windows с Python 3.13 установите патч для системных\n"
                "сертификатов и перезапустите терминал:\n"
                "  pip install pip-system-certs"
            )
            return
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при запросе {i}: {e}")
            print("Проверьте URL и наличие интернета.")
            return

    if total_time == 0:
        print("Время выполнения равно нулю, невозможно рассчитать скорость.")
        return

    avg_time = total_time / iterations
    speed_bytes_per_sec = total_bytes / total_time
    speed_mbps = (speed_bytes_per_sec * 8) / (1024 * 1024)
    speed_mbs = speed_bytes_per_sec / (1024 * 1024)

    print("-" * 40)
    print(f"Среднее время запроса: {avg_time:.4f} сек.")
    print(
        f"Общий объём скачанных данных: {total_bytes} байт "
        f"({(total_bytes / (1024 * 1024)):.2f} МБ)"
    )
    print("-" * 40)
    print(f"Скорость скачивания: {speed_mbps:.2f} Mbps (Мегабит/сек)")
    print(f"Скорость скачивания: {speed_mbs:.2f} MB/s (Мегабайт/сек)")
    print("-" * 40)


def ask_for_url():
    """Интерактивный выбор: стандартная картинка или свой URL."""
    print("Что будем тестировать?")
    print("  1 — стандартную картинку (NASA Black Marble, ~40 МБ)")
    print("  2 — свой URL картинки")
    choice = input("Введите 1 или 2  и нажмите Enter:").strip()

    if choice == "1":
        return DEFAULT_URL

    if choice == "2":
        url = input("Введите URL картинки: ").strip()
        if not url:
            print("URL не может быть пустым.")
            sys.exit(1)
        if not (url.startswith("http://") or url.startswith("https://")):
            print("URL должен начинаться с http:// или https://")
            sys.exit(1)
        return url

    print("Неверный выбор. Введите 1 или 2.")
    sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) > 2:
        print("Использование:")
        print("  python main.py               # интерактивный выбор")
        print("  python main.py <URL_адрес>   # сразу передать URL")
        sys.exit(1)

    if len(sys.argv) == 2:
        target_url = sys.argv[1]
    else:
        target_url = ask_for_url()

    try:
        measure_speed(target_url)
    except KeyboardInterrupt:
        print("\nПрервано пользователем.")
        sys.exit(130)