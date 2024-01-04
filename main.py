from tkinter import *
from tkinter import messagebox
from random import *
import pyperclip
import json
# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate():

    pass_entry.delete(0, END)

    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_list = []

    [password_list.append(choice(letters)) for char in range(randint(8, 10))]
    [password_list.append(choice(symbols)) for char in range(randint(2, 4))]
    [password_list.append(choice(numbers)) for char in range(randint(2, 4))]

    shuffle(password_list)
    password = "".join(password_list)

    pass_entry.insert(0, password)
    pyperclip.copy(password)
# ---------------------------- ENCODE PASSWORD ------------------------------- #
def encode(text):
    alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    crypted_list = []
    
    for letter in text:
        if letter.lower() not in alphabet:
            crypted_list += letter
        else:
            letter_index = alphabet.index(letter)
            letter = letter_index + 17
            crypted_list += alphabet[letter]
    
    password = "".join(crypted_list)
    return password
# ---------------------------- DECODE PASSWORD ------------------------------- #
def decode(text):
    alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    crypted_list = []
    
    for letter in text:
        if letter not in alphabet:
            crypted_list += letter
        else:
            letter_index = alphabet.index(letter)
            letter = letter_index - 17
            crypted_list += alphabet[letter]
    
    password = "".join(crypted_list)
    return password

# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    website = website_entry.get().capitalize()
    email = email_entry.get()
    text = pass_entry.get()
    
    password = encode(text)

    new_data = {
        website:{
            "email":email,
            "password":password
        }
    }

    if len(website) == 0 or len(email) == 0 or len(password) == 0:
        messagebox.showwarning("MyPass", "Please don't leave any fields empty!")
    else:
        try:
            with open("data.json", "r") as data_file:
                data = json.load(data_file)
        except FileNotFoundError:
            with open("data.json", "w") as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            data.update(new_data)

            with open("data.json", "w") as data_file:

                json.dump(data, data_file, indent=4)
        finally:
            website_entry.delete(0, len(website_entry.get()))
            pass_entry.delete(0, len(pass_entry.get()))
            messagebox.showinfo("MyPass", "Data saved")

def search():
    website = website_entry.get().capitalize()
    try:
        with open("data.json", "r") as data:
            jdata = json.load(data)
            text = jdata[website]["password"]
            if website in jdata:
                email = jdata[website]["email"]
                password = decode(text)
                messagebox.showinfo("MyPass", f"Website: {website}\nEmail/Username: {email}\nPassword: {password}")
            else:
                messagebox.showwarning("MyPass", f'The website "{website}" not found!')
    except FileNotFoundError:
        messagebox.showwarning("MyPass", f'No Data File Found!')

# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("MyPass")
window.config(padx=50, pady=50)

canvas = Canvas(width=200, height=200)
logo = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image = logo)
canvas.grid(row=0, column=1, sticky="w")

# Labels
website_label = Label(text="Website:")
website_label.grid(row=1, column=0)

email_label = Label(text="Email/Username:")
email_label.grid(row=2, column=0)

pass_label = Label(text="Password:")
pass_label.grid(row=3, column=0)

# Entries
website_entry = Entry(width=24)
website_entry.grid(row=1, column=1, columnspan=2, sticky="w")

email_entry = Entry(width=43)
email_entry.grid(row=2, column=1, columnspan=2, sticky="w")

pass_entry = Entry(width=24)
pass_entry.grid(row=3, column=1, sticky="w")

# Buttons
pass_button = Button(text="Generate Password", command=generate)
pass_button.grid(row=3, column=1, columnspan=2, sticky="e")

add_button = Button(text="Add", width=36, command=save)
add_button.grid(row=4, column=1, columnspan=2, sticky="w")

search_button = Button(text="Search", width=14, command=search)
search_button.grid(row=1, column=1, columnspan=2, sticky="e")


window.mainloop()