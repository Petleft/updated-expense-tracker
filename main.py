from tkinter import *
import tkinter
import sqlite3
from tkcalendar import *


# Vytvoření  okna a pojmenování
root = Tk()
root.title("Kalendář s výdaji")
root.geometry("600x600")

# Vytvoření a napojení databáze
conn = sqlite3.connect("expensses_book.db")
# vytvoření kurzoru
c = conn.cursor()


#Vytvoření odrážek
#c.execute("""CREATE TABLE expensses (
#    nazev_obchodu text,
#    nazev_produktu text,
#    cena float,
#    typ_produktu text,
#    datum_nakupu test
#    )""")


# Funkce uložení
def save():
    # Připojení se do databáze
    conn = sqlite3.connect("expensses_book.db")
    # vytvoření kurzoru
    c = conn.cursor()

    c.execute("""UPDATE expensses SET
        nazev_obchodu = :obchod
        nazev_produktu = :produkt
        cena = :cena
        typ_produktu = :typ
        datum_nakupu = :datum

        WHERE oid = :oid""",
              {"obchod": obchod_editor.get(),
               "produkt": produkt_editor.get(),
               "cena": cena_editor.get(),
               "typ": typ_editor.get(),
               "datum": datum_editor.get()
               })

    # Aplikace změn
    conn.commit()
    # Zavření databáze
    conn.close()


# Změna záznamu
def edit():
    edit = Tk()
    edit.title("Změna detailů")
    edit.geometry("500x500")

    # Připojení se do databáze
    conn = sqlite3.connect("expensses_book.db")
    # Vytvoření kurzoru
    c = conn.cursor()

    record_id = delete_box.get()
    c.execute("SELECT * FROM expensses WHERE oid = " + record_id)
    records = c.fetchall()

    # Nastavení globálních variables
    global obchod_editor
    global produkt_editor
    global cena_editor
    global typ_editor
    global datum_editor

    # Vytvoření boxů pro psaní
    obchod_editor = Entry(edit, width=30)
    obchod_editor.grid(row=0, column=1)
    produkt_editor = Entry(edit, width=30)
    produkt_editor.grid(row=1, column=1, padx=20)
    cena_editor = Entry(edit, width=30)
    cena_editor.grid(row=2, column=1, padx=20)
    typ_editor = Entry(edit, width=30)
    typ_editor.grid(row=3, column=1, padx=20)
    datum_editor = DateEntry(edit, date_pattern='mm/dd/y', width=12, background="darkblue", foreground="white", borderwidth=2)
    datum_editor.grid(row=5, column=1)

    # Vytvoření popisu boxů
    obchod_editor_label = Label(edit, text="Obchod")
    obchod_editor_label.grid(row=0, column=0)
    produkt_editor_label = Label(edit, text="Produkt")
    produkt_editor_label.grid(row=1, column=0)
    cena_editor_label = Label(edit, text="cena")
    cena_editor_label.grid(row=2, column=0)
    typ_editor_label = Label(edit, text="Typ produktu")
    typ_editor_label.grid(row=3, column=0)
    datum_editor_label = Label(edit, text="Datum nákupu!")
    datum_editor_label.grid(row=5, column=0)

    for record in records:
        obchod_editor.insert(0, record[0])
        produkt_editor.insert(0, record[1])
        cena_editor.insert(0, record[2])
        typ_editor.insert(0, record[3])
        datum_editor.insert(0, record[4])

    save_button = Button(edit, text="Uložit změny", command=save)
    save_button.grid(row=6, column=0, columnspan=2)

    # Aplikace změn
    conn.commit()
    # Zavření databáze
    conn.close()


# Funkce pro vymazání záznamu
def delete():
    # připojení do databáze
    conn = sqlite3.connect("expensses_book.db")
    # Vytvoření kurzoru
    c = conn.cursor()
    # Vymazání záznamu
    c.execute("DELETE from expensses WHERE oid= " + delete_box.get())

    # Aplikace změn
    conn.commit()
    # Zavření databáze
    conn.close()


# nadefinování uložení
def submit():
    # Připojení do databáze
    conn = sqlite3.connect("expensses_book.db")
    # Vytvoření kurzoru
    c = conn.cursor()

    # Vložení do záznamu
    c.execute("INSERT INTO expensses VALUES (:obchod, :produkt, :cena, :typ, :datum)",
              {
                  "obchod": obchod.get(),
                  "produkt": produkt.get(),
                  "cena": cena.get(),
                  "typ": typ.get(),
                  "datum": datum.get()
              })
    # Aplikace změn
    conn.commit()
    # Zavření databáze
    conn.close()

    # Vyčištění psacích boxů
    obchod.delete(0, END)
    produkt.delete(0, END)
    cena.delete(0, END)
    typ.delete(0, END)
    datum.delete(0, END)


# Vytvoření funce pro vypsání záznamů
def query():
    # Připojení do databáze
    conn = sqlite3.connect("expensses_book.db")
    # Vytvoření kurzoru
    c = conn.cursor()
    # vypsání databáze
    c.execute("SELECT *,oid FROM expensses")
    records = c.fetchall()

    print_records = ""
    for record in records:
        print_records += str(record[0]).upper() + "\t" + " " + str(record[1]) + "\t" + " " + str(record[2]) + " " + "\t" + str(
            record[3]) + " " + "\t" + str(record[4]) + "\n"
        barevnost()

    query_label = Label(root, text=print_records)
    query_label.grid(row=12, column=0, columnspan=2)

    # Aplikace změn
    conn.commit()
    # Zavření databáze
    conn.close()



# nadefinování typů nákupu
nákupy = [
    "Vyber Typ produktu",
    "----",
    "Oblečení",
    "Jídlo",
    "Elektronika",
    "Zahrada",
    "Dovolená",
    "Zábava"
]

# vložení vybraného typu
typ = Entry(
    bd=0,
    bg="#d9d9d9",
    highlightthickness=0,
    font='halvetica 12')
typ.insert(tkinter.END, "")
typ.grid()

# datatyp menu
clicked = StringVar()
# basic zpráva v políčku
clicked.set("Vyber typ")


def show(choice):
    typ.delete(0, END)
    typ.insert(tkinter.END, choice)


# vytvoření dropdown menu
drop = OptionMenu(root, clicked, *nákupy, command=show)
drop.grid(row=4, column=1)


# Vytvoření barevného zobrazení záznamu podle toho ke kterému typu výdaje spadají
def barevnost():
    # Vstoupení do databáze
    conn = sqlite3.connect("expensses_book.db")
    # Vytvoření kurzoru
    c = conn.cursor()
    # vypsání databáze
    c.execute("SELECT typ_produktu FROM expensses")
    typ_výdaje = c.fetchall()
    for typ_nákupu in typ_výdaje:
        if typ_nákupu == "Oblečení":
            typ(background="red")
        if typ_nákupu == "Jídlo":
            typ(background="green")
        if typ_nákupu == "Elektronika":
            typ(background="blue")
        if typ_nákupu == "Zahrada":
            typ(background="yellow")
        if typ_nákupu == "Dovolená":
            typ(background="purple")
        if typ_nákupu == "Zábava":
            typ(background="grey")
    # Aplikace změn
    conn.commit()
    # Zavření databáze
    conn.close()


# Vytvoření textových polí
obchod = Entry(root, width=30)
obchod.grid(row=0, column=1, padx=20, pady=(10, 0))
produkt = Entry(root, width=30)
produkt.grid(row=1, column=1, padx=20)
cena = Entry(root, width=30)
cena.grid(row=2, column=1, padx=20)
typ = Entry(root, width=30)
typ.grid(row=3, column=1, padx=20)
datum = DateEntry(root, date_pattern='mm/dd/y', width=12, background="darkblue", foreground="white", borderwidth=2)
datum.grid(row=5, column=1)
delete_box = Entry(root, width=30)
delete_box.grid(row=9, column=1, pady=5)

# Vytvoření tlačítka
# typ_button = Entry(root, text = "Vyber typ")
# typ_button.grid(row=4, column=1, padx=20)

# Vytvoření popisu textových polí
obchod_label = Label(root, text="Obchod")
obchod_label.grid(row=0, column=0, pady=(10, 0))
produkt_label = Label(root, text="Produkt")
produkt_label.grid(row=1, column=0)
cena_label = Label(root, text="Cena")
cena_label.grid(row=2, column=0)
typ_label = Label(root, text="Typ produktu")
typ_label.grid(row=3, column=0)
datum_label = Label(root, text="Datum nákupu")
datum_label.grid(row=5, column=0)
delete_box_label = Label(root, text="Delete ID")
delete_box_label.grid(row=9, column=0, pady=5)

# vytvoření popisu pole
# typ_button_label = Label(root, text =" Vyber typ ")
# typ_button_label.grid(row=4, column=0, columnspan=2)

# Vytvoření submit tlačítka
submit_btn = Button(root, text="Přidat do záznamů o výdajích", command=submit)
submit_btn.grid(row=6, column=0, columnspan=2, pady=10, padx=10, ipadx=117)

# Vytvoření tlačítka pro ukázkuseznamu
query_button = Button(root, text="Ukázat záznamy o výdajích", command=query)
query_button.grid(row=7, column=0, columnspan=2, pady=10, padx=10, ipadx=136)

# Vytvoření tlačítka pro vymazání
delete_button = Button(root, text="Vymazat záznam o výdaji", command=delete)
delete_button.grid(row=10, column=0, columnspan=2, pady=10, padx=10, ipadx=137)

# Vytvoření tlačítka pro úpravu
edit_button = Button(root, text="Upravit záznam o výdaji", command=edit)
edit_button.grid(row=11, column=0, columnspan=2, pady=10, padx=10, ipadx=134)

# Aplikace změn
conn.commit()

# Zavření databáze
conn.close()

root.mainloop()








