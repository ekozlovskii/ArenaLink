import random

# структура секторов
sectors = [
    "VIP 200", "ПРЕССА 201", "202", "203", "204", "205", "206",
    "207", "ПРЕМИУМ 208", "VIP 209", "VIP 210", "ПРЕМИУМ 211", "212",
    "213", "214", "215", "216", "217", "ПРЕМИУМ 218",
    "501", "502", "ЛЮКС 500", "ЛЮКС 509", "ЛЮКС 510", "ЛЮКС 519",
    "503", "504", "505", "506", "507", "508", "511", "512",
    "513", "514", "515", "516", "517", "518"
]

stadium_id = 1  # Лужники
sector_id = 1
sql_statements = []

# Создание таблиц (если ещё не созданы)
sql_statements.append("""
CREATE TABLE IF NOT EXISTS stadium (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  image_url TEXT
);

CREATE TABLE IF NOT EXISTS sector (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  stadium_id INTEGER NOT NULL,
  name TEXT NOT NULL,
  FOREIGN KEY (stadium_id) REFERENCES stadium(id)
);

CREATE TABLE IF NOT EXISTS row (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  sector_id INTEGER NOT NULL,
  number INTEGER NOT NULL,
  seat_count INTEGER NOT NULL,
  FOREIGN KEY (sector_id) REFERENCES sector(id)
);

INSERT INTO stadium (id, name, image_url) VALUES (1, 'Лужники', '/static/images/luzhniki.png');
""")

# Вставка секторов и рядов
for sector in sectors:
    sql_statements.append(
        f"\n-- {sector}\nINSERT INTO sector (id, stadium_id, name) VALUES ({sector_id}, {stadium_id}, '{sector}');"
    )
    for row_number in range(1, 11):  # 10 рядов
        seats = random.randint(10, 30)  # случайное количество мест
        sql_statements.append(
            f"INSERT INTO row (sector_id, number, seat_count) VALUES ({sector_id}, {row_number}, {seats});"
        )
    sector_id += 1

# Запись в файл
with open("stadium_schema.sql", "w", encoding="utf-8") as f:
    f.write("\n".join(sql_statements))

print("✅ Файл 'stadium_schema.sql' успешно создан.")
