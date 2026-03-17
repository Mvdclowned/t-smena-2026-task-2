import os
from rich.console import Console
from rich.table import Table

cons = Console()

def clr():
    os.system('cls' if os.name == 'nt' else 'clear')

def tbl(lst, pg=1, tp=1):
    t_str = f"Ваша Библиотека (Стр. {pg} из {tp})" if tp > 0 else "Ваша Библиотека"
    tb = Table(title=t_str, show_header=True, header_style="bold blue")
    tb.add_column("ID", justify="right", style="cyan", no_wrap=True)
    tb.add_column("Название", style="magenta")
    tb.add_column("Автор", style="green")
    tb.add_column("Год", justify="right")
    tb.add_column("Жанр", style="yellow")
    tb.add_column("Оценка", justify="center")
    tb.add_column("Статус", justify="center")
    tb.add_column("Изб.", justify="center")
    
    for b in lst:
        r = "[green]Прочитано[/green]" if b['rd'] else "[red]Не прочитано[/red]"
        fv = "[yellow]★[/yellow]" if b['fv'] else "[dim]☆[/dim]"
        rt_str = "[yellow]" + "★" * b['rt'] + "[/yellow][dim]" + "☆" * (5 - b['rt']) + "[/dim]"
        tb.add_row(str(b['id']), b['t'], b['a'], str(b['y']), b['g'], rt_str, r, fv)
    cons.print(tb)

def stat(tot, rd, pct, fv, top):
    tb = Table(title="Статистика Библиотеки", show_header=False)
    tb.add_column("Ключ", style="cyan")
    tb.add_column("Значение", style="magenta")
    tb.add_row("Всего книг", str(tot))
    tb.add_row("Прочитано", f"{rd} ({pct}%)")
    tb.add_row("В избранном", str(fv))
    tb.add_row("Топ жанры", ", ".join(top) if top else "Нет данных")
    cons.print(tb)