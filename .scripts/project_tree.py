"""Отрисовка файловой структуры проекта"""

import argparse
from pathlib import Path


def print_tree(directory: Path, ignore_dirs: list[str] = None, prefix: str = ""):
    """
    Рекурсивно выводит древовидную структуру папок и файлов,
    игнорируя указанные директории.

    :param directory: Директория для отображения
    :param ignore_dirs: Список директорий для игнорирования
    :param prefix: Префикс для отступов
    :return: Генератор строк с древовидной структурой
    """
    ignore_dirs = [] if ignore_dirs is None else ignore_dirs
    space = "    "
    branch = "│   "
    tee = "├── "
    last = "└── "

    try:
        contents = sorted(list(directory.iterdir()))
    except (PermissionError, FileNotFoundError) as e:
        print(f"{prefix}{last} [Ошибка: {e}]")
        return

    visible_contents = [path for path in contents if path.name not in ignore_dirs]

    pointers = [tee] * (len(visible_contents) - 1) + [last]

    for pointer, path in zip(pointers, visible_contents):
        yield prefix + pointer + path.name
        if path.is_dir():
            extension = branch if pointer == tee else space
            yield from print_tree(path, ignore_dirs, prefix=prefix + extension)


def main():
    parser = argparse.ArgumentParser(
        description="Отображение древовидной структуры проекта"
    )
    parser.add_argument(
        "directory",
        nargs="?",
        default=".",
        help="Директория для отображения (по умолчанию: текущая)",
    )
    parser.add_argument(
        "-i",
        "--ignore",
        nargs="+",
        default=["__pycache__", ".venv", ".git"],
        help="Директории для игнорирования (через пробел)",
    )

    args = parser.parse_args()

    path_to_display = Path(args.directory)
    ignore_list = args.ignore

    print(f"Структура: {path_to_display.absolute()}")
    print(f"Игнорируемые директории: {', '.join(ignore_list)}")
    print()

    print(path_to_display.name)
    for line in print_tree(path_to_display, ignore_dirs=ignore_list):
        print(line)


if __name__ == "__main__":
    main()
