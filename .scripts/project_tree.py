"""Отрисовка файловой структуры проекта"""

from pathlib import Path


def print_tree(directory: Path, ignore_dirs: list[str] = None, prefix: str = ""):
    """
    Рекурсивно выводит древовидную структуру папок и файлов, игнорируя указанные директории.
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


if __name__ == "__main__":
    ignore_list = ["__pycache__", ".venv", ".git"]
    path_to_display = Path(".")
    print(path_to_display.name)
    for line in print_tree(path_to_display, ignore_dirs=ignore_list):
        print(line)
