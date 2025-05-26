import textwrap


def print_highlighted(text: str, title: str = "Output"):
    print(f"\n\033[92m{'=' * 40}")
    print(title)
    print('-' * 40)
    print(textwrap.fill(text, width=100))
    print("=" * 40 + "\033[0m\n")
