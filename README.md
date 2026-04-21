# IPTV Parser Project

Python-проект ООП для работы с репозиторием `Free-TV/IPTV`.

## Возможности

- получить список всех доступных стран;
- сохранить список стран в `txt`;
- скачать и распарсить плейлист конкретной страны;
- сохранить каналы страны в M3U-структуре: `#EXTM3U`, далее блоки `#EXTINF + URL`;
- сохранить каналы сразу для всех стран в тот же формат;
- искать каналы по названию и группе;
- получать статистику по каналам и группам.

## Установка

```bash
pip install -r requirements.txt
```

## Примеры запуска

### 1. Показать все страны

```bash
python main.py countries
```

### 2. Сохранить страны в txt

```bash
python main.py countries-save
```

### 3. Сохранить M3U-структуру по стране

```bash
python main.py export-country "Spain"
```

### 4. Алиас той же команды

```bash
python main.py export-country-blocks "Spain"
```

### 5. Экспорт для всех стран

```bash
python main.py export-all-countries
```

### 6. Показать группы каналов

```bash
python main.py groups "Spain"
```

### 7. Поиск канала

```bash
python main.py search "Spain" news
```

### 8. Статистика по стране

```bash
python main.py stats "Spain"
```

## Пример запуска всех основных команд подряд

```bash
python main.py countries
python main.py countries-save
python main.py export-country "Spain"
python main.py export-country-blocks "Spain"
python main.py export-all-countries
python main.py groups "Spain"
python main.py search "Spain" news
python main.py stats "Spain"
```

## Структура

```text
iptv_parser_project/
├── iptv_parser/
│   ├── __init__.py
│   ├── client.py
│   ├── exporter.py
│   ├── models.py
│   ├── parser.py
│   └── service.py
├── main.py
├── README.md
└── requirements.txt
```
