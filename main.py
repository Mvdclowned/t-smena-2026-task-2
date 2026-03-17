import db
import ui
import os
import json

def fnd(d, i_str):
    if i_str.isdigit():
        i_val = int(i_str)
        for b in d:
            if b['id'] == i_val:
                return b
    return None

def main():
    d = db.get_d()
    sz = 10
    
    while True:
        ui.clr()
        ui.cons.print("\n[bold]1[/bold]:Доб [bold]2[/bold]:Все [bold]3[/bold]:Избр [bold]4[/bold]:Статусы [bold]5[/bold]:Редакт [bold]6[/bold]:Удалить [bold]7[/bold]:Поиск [bold]8[/bold]:Стата [bold]9[/bold]:Импорт [bold]10[/bold]:Обновить [bold]0[/bold]:Выход")
        c = input("Выбор: ")
        
        if c == '1':
            ui.clr()
            t = input("Название: ")
            a = input("Автор: ")
            
            dup = False
            for b in d:
                if b['t'].lower() == t.lower() and b['a'].lower() == a.lower():
                    dup = True
                    break
            
            if dup:
                ui.cons.print("\n[bold yellow]Такая книга (Название + Автор) уже есть в библиотеке![/bold yellow]")
                input("Нажмите Enter для возврата в меню...")
            else:
                g = input("Жанр: ")
                y = input("Год: ")
                ds = input("Описание: ")
                rt_str = input("Оценка (0-5): ")
                rt = int(rt_str) if rt_str.isdigit() and int(rt_str) in [0,1,2,3,4,5] else 0
                
                nid = max([x['id'] for x in d]) + 1 if d else 1
                d.append({'id': nid, 't': t, 'a': a, 'g': g, 'y': y, 'ds': ds, 'rd': False, 'fv': False, 'rt': rt})
                db.sv_d(d)
                
                ui.clr()
                ui.tbl(d)
                ui.cons.print("\n[green]Книга добавлена![/green]")
                input("Нажмите Enter...")
                
        elif c == '2':
            flt = '0'
            fg = ''
            srt = '0'
            pg = 1
            d_srt = {'0': 'Нет', '1': 'Название', '2': 'Автор', '3': 'Год', '4': 'Оценка'}
            
            while True:
                ui.clr()
                res = []
                for b in d:
                    if flt == '1' and b['g'] != fg: continue
                    if flt == '2' and not b['rd']: continue
                    if flt == '3' and b['rd']: continue
                    res.append(b)
                
                if srt == '1': res.sort(key=lambda x: x['t'].lower())
                elif srt == '2': res.sort(key=lambda x: x['a'].lower())
                elif srt == '3': res.sort(key=lambda x: x['y'])
                elif srt == '4': res.sort(key=lambda x: x['rt'], reverse=True)
                
                tot_pg = (len(res) + sz - 1) // sz if res else 1
                if pg > tot_pg: pg = tot_pg
                if pg < 1: pg = 1
                
                st = (pg - 1) * sz
                en = st + sz
                vw = res[st:en]
                
                ui.tbl(vw, pg, tot_pg)
                
                if flt == '1': d_flt = f"Жанр ({fg})"
                elif flt == '2': d_flt = "Прочитано"
                elif flt == '3': d_flt = "Непрочитано"
                else: d_flt = "Нет"
                
                ui.cons.print(f"\n[bold]Настройки:[/bold] Сорт: [green]{d_srt.get(srt, 'Нет')}[/green] | Фильтр: [yellow]{d_flt}[/yellow]")
                
                bts = "[bold]N[/bold]:След.стр [bold]P[/bold]:Пред.стр | [bold]1[/bold]:Фильтр [bold]2[/bold]:Сортировка "
                if flt != '0' or srt != '0':
                    bts += "[bold]3[/bold]:Сброс "
                bts += "[bold]0[/bold]:Назад"
                
                ui.cons.print(bts)
                sub = input("Действие: ").lower()
                
                if sub == 'n': pg += 1
                elif sub == 'p': pg -= 1
                elif sub == '1':
                    flt = input("Фильтр (1-Жанр 2-Прочит 3-Непрочит 0-Сброс): ")
                    fg = input("Жанр: ") if flt == '1' else ""
                    if flt not in ['1', '2', '3']: flt = '0'
                    pg = 1
                elif sub == '2':
                    s = input("Сорт (1-Назв 2-Автор 3-Год 4-Оценка 0-Сброс): ")
                    if s in ['1', '2', '3', '4', '0']: srt = s
                    pg = 1
                elif sub == '3' and (flt != '0' or srt != '0'):
                    flt, fg, srt, pg = '0', '', '0', 1
                elif sub == '0':
                    break
                else:
                    ui.cons.print("[bold red]Неизвестная команда![/bold red]")
                    input("\nНажмите Enter...")
                    
        elif c == '3':
            ui.clr()
            ui.tbl([b for b in d if b['fv']])
            input("\nНажмите Enter...")
            
        elif c == '4':
            ui.clr()
            ui.tbl(d)
            i_str = input("\nВведите ID книги для действий: ")
            b = fnd(d, i_str)
            if b:
                ui.clr()
                ui.tbl([b])
                ui.cons.print("\n[bold]1[/bold]:Прочитано [bold]2[/bold]:Не прочитано [bold]3[/bold]:В избранное (вкл/выкл) [bold]4[/bold]:Изменить оценку [bold]0[/bold]:Отмена")
                act = input("Действие: ")
                if act == '1': b['rd'] = True
                elif act == '2': b['rd'] = False
                elif act == '3': b['fv'] = not b['fv']
                elif act == '4':
                    rt_str = input("Оценка (0-5): ")
                    if rt_str.isdigit() and int(rt_str) in [0,1,2,3,4,5]: b['rt'] = int(rt_str)
                db.sv_d(d)
                
                ui.clr()
                ui.tbl(d)
                ui.cons.print("\n[green]Обновлено![/green]")
            else:
                ui.cons.print("[bold red]Книга не найдена![/bold red]")
            input("Нажмите Enter...")
            
        elif c == '5':
            ui.clr()
            ui.tbl(d)
            i_str = input("\nID книги для редактирования: ")
            b = fnd(d, i_str)
            if b:
                ui.clr()
                ui.tbl([b])
                ui.cons.print("\nЧто изменить? [bold]1[/bold]:Название [bold]2[/bold]:Автор [bold]3[/bold]:Жанр [bold]4[/bold]:Год [bold]5[/bold]:Описание [bold]0[/bold]:Отмена")
                act = input("Действие: ")
                if act == '1': b['t'] = input("Новое название: ")
                elif act == '2': b['a'] = input("Новый автор: ")
                elif act == '3': b['g'] = input("Новый жанр: ")
                elif act == '4': b['y'] = input("Новый год: ")
                elif act == '5': b['ds'] = input("Новое описание: ")
                db.sv_d(d)
                
                ui.clr()
                ui.tbl(d)
                ui.cons.print("\n[green]Сохранено![/green]")
            else:
                ui.cons.print("[bold red]Книга не найдена![/bold red]")
            input("Нажмите Enter...")
            
        elif c == '6':
            ui.clr()
            ui.tbl(d)
            i_str = input("\nID книги для удаления: ")
            b = fnd(d, i_str)
            if b:
                d.remove(b)
                db.sv_d(d)
                
                ui.clr()
                ui.tbl(d)
                ui.cons.print("\n[green]Книга удалена![/green]")
            else:
                ui.cons.print("[bold red]Книга не найдена![/bold red]")
            input("Нажмите Enter...")
            
        elif c == '7':
            ui.clr()
            q = input("Запрос: ").lower()
            ui.clr()
            ui.tbl([b for b in d if q in b['t'].lower() or q in b['a'].lower() or q in b['ds'].lower()])
            input("\nНажмите Enter...")
            
        elif c == '8':
            ui.clr()
            tot = len(d)
            rd = sum(1 for x in d if x['rd'])
            pct = round((rd / tot * 100)) if tot > 0 else 0
            fv = sum(1 for x in d if x['fv'])
            
            g_cnt = {}
            for x in d:
                gv = x['g']
                if gv: g_cnt[gv] = g_cnt.get(gv, 0) + 1
            
            srt_g = sorted(g_cnt.items(), key=lambda item: item[1], reverse=True)
            top = [k for k, v in srt_g[:3]]
            
            ui.stat(tot, rd, pct, fv, top)
            input("\nНажмите Enter...")
            
        elif c == '9':
            ui.clr()
            f_in = input("Файл для импорта (например, other.json): ")
            if os.path.exists(f_in) and os.path.getsize(f_in) > 0:
                with open(f_in, 'r', encoding='utf-8') as f:
                    new_d = json.load(f)
                    
                    add_cnt = 0
                    skp_cnt = 0
                    
                    for nb in new_d:
                        nt = nb.get('t', 'Без названия')
                        na = nb.get('a', 'Неизвестно')
                        
                        dup = False
                        for b in d:
                            if b['t'].lower() == nt.lower() and b['a'].lower() == na.lower():
                                dup = True
                                break
                                
                        if not dup:
                            nid = max([x['id'] for x in d]) + 1 if d else 1
                            d.append({
                                'id': nid, 
                                't': nt, 
                                'a': na, 
                                'g': nb.get('g', ''), 
                                'y': nb.get('y', ''), 
                                'ds': nb.get('ds', ''), 
                                'rd': nb.get('rd', False), 
                                'fv': nb.get('fv', False), 
                                'rt': nb.get('rt', 0)
                            })
                            add_cnt += 1
                        else:
                            skp_cnt += 1
                            
                    db.sv_d(d)
                    
                    ui.clr()
                    ui.tbl(d)
                    ui.cons.print(f"\n[green]Успешно добавлено: {add_cnt}. Пропущено (дубликаты): {skp_cnt}[/green]")
            else:
                ui.cons.print("[bold red]Файл не найден или пуст![/bold red]")
            input("Нажмите Enter...")
            
        elif c == '10':
            ui.clr()
            d = db.get_d()
            
            ui.clr()
            ui.tbl(d)
            ui.cons.print("\n[green]База данных успешно обновлена из файла![/green]")
            input("Нажмите Enter...")
            
        elif c == '0':
            ui.clr()
            break
            
        else:
            ui.cons.print("[bold red]Ошибка: Неизвестная команда![/bold red]")
            input("\nНажмите Enter...")

if __name__ == "__main__":
    main()