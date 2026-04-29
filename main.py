import subprocess
import time

EXE_PATH = "D:/reps/durak_offline/x64/Release/durak_offline.exe"
OUTPUT_FILE = "results.csv"
HEADER = "номер_теста, конфигурация, первый ход, победители, вес, козыри"

# 5 конфигураций: (лёгкие, сложные, метка)
CONFIGS = [
    (2, 0, "ЛЛ"),  # 2 лёгких
    (0, 2, "СС"),  # 2 сложных
    (1, 1, "ЛС"),  # 1 лёгкий + 1 сложный
    (2, 1, "ЛЛС"),  # 2 лёгких + 1 сложный
    (1, 2, "ЛСС"),  # 1 лёгкий + 2 сложных
]

RUNS_PER_CONFIG = 100
TIMEOUT = 30


def run_game(easy, hard):
    input_data = f"fst\n{easy}\n{hard}\n".encode('utf-16le')
    proc = subprocess.run(
        [EXE_PATH],
        input=input_data,
        capture_output=True,
        timeout=TIMEOUT
    )
    # Декодируем вывод (программа пишет в UTF-16LE)
    out = proc.stdout.decode('utf-16le', errors='replace')
    lines = [line.strip() for line in out.splitlines() if line.strip()]

    return lines[-1][83:]  # последняя строка = результат + скип мусора


def parse_result(line):
    parts = line.split(';')
    return f"{parts[0].strip()},{parts[1].strip()},{parts[2].strip()},{parts[3].strip()}"



with open(OUTPUT_FILE, "w", encoding="utf-8") as f:

    f.write(HEADER + "\n")
    total = len(CONFIGS) * RUNS_PER_CONFIG
    done = 0

    for easy, hard, label in CONFIGS:
        print(f"\n{label} (лёгкий={easy}, сложный={hard})")
        for run_num in range(1, RUNS_PER_CONFIG + 1):
            raw = run_game(easy, hard)
            #в генераторе используется time, код работает слишком быстро
            #теперь данные разные
            time.sleep(1)
            csv_part = parse_result(raw)
            f.write(f"{run_num}, {label}, {csv_part}\n")
            done += 1
            print(f"  Выполнено {done}/{total}")
        f.flush()
print(f"\nГотово! {total} записей в {OUTPUT_FILE}")