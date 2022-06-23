from guizero import App, Combo, Text, Window, PushButton, ListBox
import sqlite3

# Globals
selectedYear = 2006

def do_query(q):
    con = sqlite3.connect('ps3.db')
    cur = con.cursor()
    cur.execute(q)
    rows = cur.fetchall()
    cur.close()
    return(rows)

q1 = """
    select Publisher, year, count(*) as NumberOfGames, sum(Global_Sales) as TotalGlobalSales
    from ps3 
    group by Publisher, year
    order by year desc, TotalGlobalSales desc
"""
qyears = "select DISTINCT year from ps3 order by year asc"
years = do_query(qyears)
yearlist = [y[0] for y in years]

def handleCombo(selected_value):
    global selectedYear
    selectedYear = selected_value
    print(selected_value)
    for item in listbox.items:
        listbox.remove(item)
    for item in secondlistbox.items:
        secondlistbox.remove(item)
    for item in thirdlistbox.items:
        thirdlistbox.remove(item)
    q1 = f"""
    select Publisher, year, count(*) as NumberOfGames, sum(Global_Sales) as TotalGlobalSales
    from ps3 where year = {selected_value}
    group by Publisher, year
    order by year desc, TotalGlobalSales desc
    """
    rows = do_query(q1)
    for row in rows[0:4]:
        listbox.append(f'{row[0]}')

def handleListItem(value):
    global selectedYear
    global selectedPublisher
    selectedPublisher = value
    for item in secondlistbox.items:
        secondlistbox.remove(item)
    for item in thirdlistbox.items:
        thirdlistbox.remove(item)
    q1 = f"select * from ps3 where year = {selectedYear} and Publisher = '{selectedPublisher}' order by Global_Sales desc"
    print(q1)
    rows = do_query(q1)
    for row in rows:
        secondlistbox.append(row[0])

def handlesecondlistitem(value):
    global selectedYear
    global selectedPublisher
    for item in thirdlistbox.items:
        thirdlistbox.remove(item)
    q1 = f'select * from ps3 where year = {selectedYear} and Publisher = "{selectedPublisher}" and Name = "{value}"'
    rows = do_query(q1)
    for row in rows:
        onerow = f"Name:{row[0]}. Global Sales:{row[8]}"
        thirdlistbox.append(onerow)


app = App()
combo = Combo(app, options=yearlist, command = handleCombo)
listbox = ListBox(app, width='fill', command = handleListItem)
secondlistbox = ListBox(app, width='fill', command = handlesecondlistitem)
thirdlistbox = ListBox(app, width='fill')
app.display()
