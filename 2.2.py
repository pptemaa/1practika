import toml
import sys
import os
import urllib.request
import tarfile
import io

try:
    cfg = toml.load("config.toml")
except Exception as e:
    print(f"Ошибка загрузки: {e}", file=sys.stderr)
    sys.exit(1)

params = [
    ("package_name", str),
    ("repository_url", str),
    ("repo_mode", str),
    ("output_image", str),
    ("ascii_tree", (bool, str)),
    ("max_depth", int),
]

for k, t in params:
    if k not in cfg:
        print(f"Нет параметра: {k}", file=sys.stderr)
        sys.exit(1)
    if not isinstance(cfg[k], t):
        print(f"Неверный тип у {k}", file=sys.stderr)
        sys.exit(1)

if cfg["repo_mode"] not in {"clone", "local", "none"}:
    print("repo_mode: допустимые значения — clone/local/none", file=sys.stderr)
    sys.exit(1)

if cfg["repo_mode"] == "local" and not os.path.exists(cfg["repository_url"]):
    print(f"Файл или каталог не найден: {cfg['repository_url']}", file=sys.stderr)
    sys.exit(1)

if cfg["max_depth"] < 0:
    print("max_depth < 0", file=sys.stderr)
    sys.exit(1)

for k, v in cfg.items():
    print(f"{k} = {v!r}")

print("-" * 20)

repo_url = cfg["repository_url"].rstrip('/')
index_url = f"{repo_url}/APKINDEX.tar.gz"
package_name = cfg["package_name"]

print(f"Поиск зависимостей для пакета: {package_name}")
print(f"Индекс репозитория: {index_url}")
try:
    print("Скачивание индекса...")
    with urllib.request.urlopen(index_url) as response:
        data = response.read()
    print("Распаковка индекса...")
    with tarfile.open(fileobj=io.BytesIO(data), mode="r:gz") as tar:
        try:
            apkindex_member = tar.getmember("APKINDEX")
        except KeyError:
            print("Ошибка: файл 'APKINDEX' не найден в архиве.", file=sys.stderr)
            sys.exit(1)
        apkindex_file = tar.extractfile(apkindex_member)
        apkindex_content = apkindex_file.read().decode('utf-8')
    print("Поиск пакета в индексе...")
    package_record = None
    records = apkindex_content.strip().split('\n\n')
    for record in records:
        if record.startswith(f"P:{package_name}"):
            package_record = record
            break

    if not package_record:
        print(f"Ошибка: пакет '{package_name}' не найден в индексе.", file=sys.stderr)
        sys.exit(1)
    dependencies_line = None
    for line in package_record.split('\n'):
        if line.startswith("D:"):
            dependencies_line = line
            break

    # 5. Извлечение и форматирование прямых зависимостей
    direct_dependencies = []
    if dependencies_line:
        # Строка зависимостей имеет вид 'D:dep1 dep2 dep3...'
        # Удаляем префикс 'D:' и разбиваем строку по пробелам
        deps_string = dependencies_line[2:].strip()
        
        if deps_string:
            # Зависимости могут включать ограничения версий, например: 'libssl3>=3.0.0-r0'
            # Для "прямых зависимостей" нам достаточно имени. 
            # Ограничения версий (например, >=3.0.0-r0) игнорируем для минимализма.
            # Также могут быть альтернативы, разделенные '|', например: 'pkg1|pkg2'
            raw_deps = deps_string.split()
            
            for dep in raw_deps:
                # Отделяем имя пакета от ограничений версий, например, 'pkg>=ver' -> 'pkg'
                # Игнорируем альтернативы для простоты, берем первое имя
                clean_dep = dep.split('>')[0].split('<')[0].split('=')[0].split('~')[0]
                # Учитываем возможность альтернатив (разделитель '|')
                clean_dep = clean_dep.split('|')[0]
                direct_dependencies.append(clean_dep.strip())

    # 6. Вывод на экран
    print("\n--- Прямые зависимости ---")
    if direct_dependencies:
        # Удаляем дубликаты и выводим
        unique_dependencies = sorted(list(set(direct_dependencies)))
        for dep in unique_dependencies:
            print(f"- {dep}")
    else:
        print("Прямые зависимости не найдены (или пакет не имеет зависимостей).")
except Exception as e:
    # Исправленный блок: теперь внешний try имеет соответствующий except
    print(f"Ошибка при обработке индекса/пакета: {e}", file=sys.stderr)
    sys.exit(1)
