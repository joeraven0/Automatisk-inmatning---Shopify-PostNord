import tkinter as tk
from tkinter import messagebox
from pynput.keyboard import Controller, Key
import time
import re

# Skapa en tangentbordskontroll
keyboard = Controller()

# Tid mellan knapptryckningar
delay = 0.01  # 50 ms
start_delay = 2  # Fördröjning innan inmatningen börjar (2 sekunder)

# Funktion för att bearbeta inmatad text
def process_input(pasted_text):
    try:
        # Dela upp texten i rader
        lines = pasted_text.strip().split("\n")
        
        # Extrahera data
        namn = lines[0]
        adress = lines[1]
        postnummer = re.search(r"\d{3} \d{2}", lines[2]).group(0)  # Hämta endast postnummer
        telefon = lines[4].replace(" ", "")  # Ta bort alla mellanslag från telefonnumret
        email = lines[5]
        
        return {
            "Namn": namn,
            "Adress": adress,
            "Postnummer": postnummer,
            "Telefonnummer": telefon,
            "E-post": email
        }
    except Exception as e:
        messagebox.showerror("Fel", f"Fel i inmatningen: {e}")
        return None

# Funktion för att fylla i datan i GUI
def fill_preview():
    pasted_text = text_input.get("1.0", tk.END)
    data = process_input(pasted_text)
    if data:
        name_var.set(data["Namn"])
        address_var.set(data["Adress"])
        postal_var.set(data["Postnummer"])
        phone_var.set(data["Telefonnummer"])
        email_var.set(data["E-post"])

# Funktion för att simulera tangentbordstryckningar
def write_data():
    data = {
        "Namn": name_var.get(),
        "Adress": address_var.get(),
        "Postnummer": postal_var.get(),
        "Telefonnummer": phone_var.get(),
        "E-post": email_var.get(),
    }
    
    # Fördröjning innan tangentbordssimulering börjar
    time.sleep(start_delay)
    
    fields = [
        ("Namn", data["Namn"], 2),
        ("Adress", data["Adress"], 3),
        ("Postnummer", data["Postnummer"], 4),
        ("Telefonnummer", data["Telefonnummer"], 1),
        ("E-post", data["E-post"], 0),
    ]
    
    for field_name, value, tabs in fields:
        for char in value:
            keyboard.press(char)
            keyboard.release(char)
            time.sleep(delay)
        for _ in range(tabs):
            keyboard.press(Key.tab)
            keyboard.release(Key.tab)
            time.sleep(delay)

    messagebox.showinfo("Klar", "Inmatningen är färdig!")

# Funktion för att rensa alla fält
def clear_fields():
    text_input.delete("1.0", tk.END)
    name_var.set("")
    address_var.set("")
    postal_var.set("")
    phone_var.set("")
    email_var.set("")

# GUI med tkinter
root = tk.Tk()
root.title("Automatisk inmatning")

# Textfält för att klistra in data
tk.Label(root, text="Klistra in data:").grid(row=0, column=0, sticky="w")
text_input = tk.Text(root, height=10, width=50)
text_input.grid(row=1, column=0, columnspan=2, padx=10, pady=5)

# Knapp för att förhandsgranska
tk.Button(root, text="Förhandsgranska", command=fill_preview).grid(row=2, column=0, pady=5)

# Knapp för att rensa alla fält
tk.Button(root, text="Rensa fält", command=clear_fields).grid(row=2, column=1, pady=5)

# Variabler för att visa data
name_var = tk.StringVar()
address_var = tk.StringVar()
postal_var = tk.StringVar()
phone_var = tk.StringVar()
email_var = tk.StringVar()

# Förhandsgranskning av fälten
tk.Label(root, text="Namn:").grid(row=3, column=0, sticky="w")
tk.Entry(root, textvariable=name_var, state="readonly").grid(row=3, column=1, sticky="w")

tk.Label(root, text="Adress:").grid(row=4, column=0, sticky="w")
tk.Entry(root, textvariable=address_var, state="readonly").grid(row=4, column=1, sticky="w")

tk.Label(root, text="Postnummer:").grid(row=5, column=0, sticky="w")
tk.Entry(root, textvariable=postal_var, state="readonly").grid(row=5, column=1, sticky="w")

tk.Label(root, text="Telefonnummer:").grid(row=6, column=0, sticky="w")
tk.Entry(root, textvariable=phone_var, state="readonly").grid(row=6, column=1, sticky="w")

tk.Label(root, text="E-post:").grid(row=7, column=0, sticky="w")
tk.Entry(root, textvariable=email_var, state="readonly").grid(row=7, column=1, sticky="w")

# Knapp för att börja skriva
tk.Button(root, text="Börja skriva", command=write_data).grid(row=8, column=0, columnspan=2, pady=10)

# Starta huvudloopen
root.mainloop()
