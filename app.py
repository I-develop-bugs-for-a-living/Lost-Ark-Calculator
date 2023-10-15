import customtkinter
import pandas as pd

customtkinter.set_appearance_mode('dark')
customtkinter.set_default_color_theme('dark-blue')

# read csv
#df = pd.read_csv('data.csv')


def calc(e1, e2, e3, e4, e5, be6):
    # suche aus allen kombinationen die aus wo alle 6 erfüllt werden
    # suche mir die billigste kombination aus
    pass

screen = customtkinter.CTk()
screen.geometry("1000x600")
screen.title("Lost-Ark Irgendwie gute Items machen")
engravings = ['Grudge', 'Ultimate Skill: Taijutsu', 'Cursed Doll', 'Ambush Master', 'Raid Captain', 'Adrenalin']

frame = customtkinter.CTkFrame(master=screen)
frame.pack(pady=20, padx=60, fill=customtkinter.BOTH, expand=True)

label = customtkinter.CTkLabel(master=frame, text='Lost Ark Item Calculator', font=('Roboto', 40))
label.grid(row=0, column=0, columnspan=6)

engraving1_variable = customtkinter.StringVar(screen)
engraving1_variable.set('')

engraving2_variable = customtkinter.StringVar(screen)
engraving2_variable.set('')

engraving3_variable = customtkinter.StringVar(screen)
engraving3_variable.set('')

engraving4_variable = customtkinter.StringVar(screen)
engraving4_variable.set('')

engraving5_variable = customtkinter.StringVar(screen)
engraving5_variable.set('')

engraving6_variable = customtkinter.StringVar(screen)
engraving6_variable.set('')

engraving1_select = customtkinter.CTkOptionMenu(master=frame, variable=engraving1_variable, values=engravings)
engraving1_select.grid(row=1, column=0, columnspan=1)

engraving2_select = customtkinter.CTkOptionMenu(master=frame, variable=engraving2_variable, values=engravings)
engraving2_select.grid(row=1, column=1, columnspan=1)

engraving3_select = customtkinter.CTkOptionMenu(master=frame, variable=engraving3_variable, values=engravings)
engraving3_select.grid(row=1, column=2, columnspan=1)

engraving4_select = customtkinter.CTkOptionMenu(master=frame, variable=engraving4_variable, values=engravings)
engraving4_select.grid(row=1, column=3, columnspan=1)

engraving5_select = customtkinter.CTkOptionMenu(master=frame, variable=engraving5_variable, values=engravings)
engraving5_select.grid(row=1, column=4, columnspan=1)

engraving6_select = customtkinter.CTkOptionMenu(master=frame, variable=engraving6_variable, values=engravings)
engraving6_select.grid(row=1, column=5, columnspan=1)

button = customtkinter.CTkButton(master=frame, text='Find best combination', command=lambda: calc(engraving1_variable, engraving2_variable, engraving3_variable, engraving4_variable, engraving5_variable, engraving6_variable))
button.grid()

screen.mainloop()


