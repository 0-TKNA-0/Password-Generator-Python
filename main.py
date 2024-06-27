import customtkinter
from PIL import Image, ImageTk
import json
import random
import string


# https://github.com/dwyl/english-words/blob/master/words_alpha.txt
# Read words from the text file
"""
with open('words_alpha.txt', 'r') as file:
    word_list = file.read().splitlines()

# Save words to a nicely formatted JSON file
with open('words.json', 'w') as json_file:
    json.dump(word_list, json_file, indent=2)
"""

window = customtkinter.CTk()
window.title("Password Generator")
window.geometry("450x700")
window.config(background="#374A67")
window.resizable(False,False)

switch_toggle = "dark"

light_image = customtkinter.CTkImage(Image.open("light.png"), size=(30,30))
dark_image = customtkinter.CTkImage(Image.open("dark.png"), size=(30,30))

# This section creates 2 functions that allow the light and dark mode buttons to switch between there corresponding modes
def light_mode():
    global switch_toggle
    customtkinter.set_appearance_mode("light")
    switch_toggle = "light"
    window.config(background="white")
    
    light_button.place_forget()
    dark_button.place(x=390, y=35)

def dark_mode():
    global switch_toggle
    customtkinter.set_appearance_mode("dark")
    switch_toggle = "dark"
    window.config(background="#374A67")

    dark_button.place_forget()
    light_button.place(x=390, y=35)



def save_password(selected_words):
    try:
        with open("passwords.json", "r") as file:
            passwords = json.load(file)
    except FileNotFoundError:
        passwords = []

    password_str = ''.join(selected_words)

    # Check if the password is already saved
    if password_str in passwords:
        message_label = customtkinter.CTkLabel(
            inputframe,
            height=25,
            width=300,
            corner_radius=5,
            text="This password has already been saved",
            font=("Ubuntu", 15, "bold"),
            fg_color=("#FF0000"))
        message_label.place(x=29, y=345)

        inputframe.after(3000, lambda: message_label.place_forget())
        return

    passwords.append(password_str)

    with open("passwords.json", "w") as file:
        json.dump(passwords, file, indent=2)


def generate_password():
    passwordLength = int(passwordLength_entry.get())

    if passwordLength <= 2 or passwordLength == 32 or passwordLength > 33 or passwordLength == 28:
        error_label = customtkinter.CTkLabel(
            inputframe,
            width=200,
            height=40,
            corner_radius=5,
            text=f"No words with the length {passwordLength - 2}\nwere found in the dictionary",
            font=("Ubuntu", 15, "bold"),
            fg_color=("#FF0000"))
        error_label.place(x=79, y=252)

        inputframe.after(3000, lambda: error_label.destroy())

    # Read words from the JSON file
    with open("words.json", "r") as file:
        word_list = json.load(file)

    # Filter words based on length
    valid_words = [word for word in word_list if len(word) == passwordLength - 2]

    # Select a random word from the filtered list
    selected_word = random.choice(valid_words)

    # Initialize an empty list to store selected words
    selected_words = [selected_word]

    # Randomly select a position to insert a special character
    special_char_position = random.randint(0, len(selected_words))
    selected_words.insert(special_char_position, random.choice(string.punctuation))

    # Randomly select a position to insert a digit
    digit_position = random.randint(0, len(selected_words))
    selected_words.insert(digit_position, random.choice(string.digits))

    # Display the generated password
    password_label.configure(text=f"Password\n {''.join(selected_words)}")

    save_button = customtkinter.CTkButton(
        inputframe,
        width=250,
        height=40,
        text="Save Password",
        font=("Ubuntu", 20, "bold"),
        fg_color=("#2E3A4E"),
        corner_radius=10,
        command=lambda: save_password(selected_words))
    save_button.place(x=55, y=300)

# This section contains all of the parameters for each widget and packs / places them on the window
framebar = customtkinter.CTkFrame(
    window,
    width=450,
    height=100,
    fg_color="#0E1116")
framebar.pack()


hidingframe = customtkinter.CTkFrame(
    window,
    width=400,
    height=225,
    fg_color=("white", "#374A67"))
hidingframe.pack(pady = 50)

inputframe = customtkinter.CTkFrame(
    hidingframe,
    width=350,
    height=375,
    corner_radius= 20,
    fg_color="#0E1116")
inputframe.pack()


passwordGeneratorLabel = customtkinter.CTkLabel(
    framebar, 
    text = "Random Password\nGenerator",
    font = ("Ubuntu", 30, "bold"),    
    text_color = "white",
    width=450,
    height=100,
    corner_radius = 10)
passwordGeneratorLabel.pack()


dark_button = customtkinter.CTkButton(
    framebar,
    width=35,
    height=35,
    text="",
    image=dark_image,
    font=("Ubuntu", 15, "bold"),
    fg_color=("#374A67"),
    command=dark_mode)
dark_button.place(x=390, y=35)


light_button = customtkinter.CTkButton(
    framebar,
    width=35,
    height=35,
    text="",
    image=light_image,
    font=("Ubuntu", 15, "bold"),
    fg_color=("#374A67"),
    command=light_mode)
light_button.place(x=390, y=35)


passwordLength_entry = customtkinter.CTkEntry(
    inputframe,
    text_color="white",
    font=("Ubuntu", 15, "bold"),
    width=200,
    height=40, 
    placeholder_text="12345",
    validate="key",
    validatecommand=(window.register(lambda s: s.isdigit()), "%S"))
passwordLength_entry.place(x=75, y=50)

generate_button = customtkinter.CTkButton(
    inputframe,
    width=250,
    height=40,
    text="Generate Password",
    font=("Ubuntu", 20, "bold"),
    fg_color=("#2E3A4E"),
    corner_radius=10,
    command=generate_password)
generate_button.place(x=50, y=120)

password_label = customtkinter.CTkLabel(
    inputframe,
    text_color="white",
    width= 348,
    height=40,
    text="Password",
    corner_radius=20,
    font=("Ubuntu", 20, "bold"),
    fg_color=("#616283"))
password_label.place(x=1, y=200)


window.mainloop()