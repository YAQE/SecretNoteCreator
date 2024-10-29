from cryptography.fernet import Fernet
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk  


window = Tk()
window.title("Secret Note Application")



original_image = Image.open("topsecret1.png")
resized_image = original_image.resize((100, 100), Image.LANCZOS)
image = ImageTk.PhotoImage(resized_image)

image_label = Label(window, image=image)
image_label.grid(row=1, column=2)

title_label = Label(text="Enter your title",font='Arial')
title_label.config(padx=20, pady=10)
title_label.grid(row=2,column=2)
title_entry = Entry(width=30)
title_entry.grid(row=3,column=2)
text_entry = Label(text="Enter your text",font='Arial')
text_entry.config(padx=20, pady=10)
text_entry.grid(row=4, column=2)
text_entry = Text(width=30, height=15)
text_entry.grid(row=5,column=2, padx=10)
master_key = Label(text="Enter Master Key", font='Arial')
master_key.grid(row=6, column=2)
master_key.config(padx=20, pady=10)
key_entry = Entry(width=30)
key_entry.grid(row=7, column=2)
wrong = Label()
wrong.grid(row=10, column=2)


key = Fernet.generate_key()
fernet = Fernet(key)

master_key = None

def saveEncrypt():
    global master_key
    title = title_entry.get()
    note = text_entry.get("1.0", "end").strip()
    master = key_entry.get()

    if not note or not title or not master:
        wrong.config(text="Please do not leave blank the tittle or text field", font="Arial")
    else:
        master_key = master
        with open("secret.txt", "a+") as f:
            f.write(title + "\n")
            encrypted_note = fernet.encrypt(note.encode())
            f.write(encrypted_note.decode() + "\n")

    text_entry.delete("1.0", "end")
    title_entry.delete(0, END)
    key_entry.delete(0, END)      
        
def decrypte_it():
    global master_key
    encrypted_note = text_entry.get("1.0", "end").strip()
    if key_entry.get() != master_key:
        text_entry.delete("1.0", "end")
        messagebox.showerror("INCORRECT", "Incorrect master key!")
        return
    
    try:
        decrypted_note = fernet.decrypt(encrypted_note.encode())
        text_entry.delete("1.0", "end")
        text_entry.insert("1.0", decrypted_note.decode())
    except Exception as e:
           messagebox.showerror("ERROR", f"Decryption failed: {str(e)}")


save_button = Button(text="Save and Encrypt", command=saveEncrypt)
save_button.grid(row=8, column=2, pady=20)

decrypte_button = Button(text="Decrypte it", command=decrypte_it)
decrypte_button.grid(row=9, column=2, pady=20)







window.mainloop()
