from tkinter import *
from tkinter import ttk
from tkinter import messagebox


class App(Frame):
    SKILLS_DIFFICULTY = {
        "Very_Hard": [240, 300, 360, 420, 480, 540, 600],
        "Hard": [160, 200, 240, 280, 320, 360, 400],
        "Medium": [120, 150, 180, 210, 240, 270, 300],
        "Easy": [80, 100, 120, 140, 160, 180, 200]
    }
    PROFESSIONS = {
        "DRUID": {
            "Leczenie": "Hard",
            "Odczarowanie": "Hard",
            "Wtapianie": "Hard",
            "Wzmocnienie": "Hard",
            "Źródło natury": "Hard",
            "Leczenie grupowe": "Very_Hard"},
        "BARBARZYŃCA": {
            "Gruboskórność": "Hard",
            "Furia": "Easy"},

        "RYCERZ": {
            "Blok tarczą": "Easy",
            "Trans": "Hard",
            "Ochrona": "Medium",
            "Aura czystości": "Hard",
            "Poświęcenie": "Medium",
            "Siła jedności": "Very_Hard"},

        "SHEED": {
            "Kontrola oddechu": "Medium",
            "Uniki": "Easy", },

        "MAG_OGNIA": {
            "Inkantacja": "Hard",
            "Ognista sfera": "Hard",
            "Aura rozproszenia": "Very_Hard"},
        "ŁUCZNIK": {
            "Wyostrzone zmysły": "Medium"},
        "VOODOO": {}
    }

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.grid()
        self.default_view()

    def combo_click(self, event):
        self.del_widgets()
        self.current_prof = self.myCombo.get()

        for nr, skill in enumerate(App.PROFESSIONS[self.current_prof]):
            # v = StringVar(root,value="7")
            temp_skill = skill.lower()
            myLabel = Label(self.master, text=skill).grid(row=nr + 2, column=3)
            myEntry = Entry(self.master, width=5, name=temp_skill)
            myEntry.insert(0, "7")
            myEntry.grid(row=nr + 2, column=4)
        if self.current_prof != "VOODOO":
            Label(self.master, text="Wymagana wiedza", ).grid(row=0, column=5, columnspan=3)
            Label(self.master, name="1PA", text="1PA", width=5).grid(row=1, column=5)
            Label(self.master, name="2PA", text="2PA", width=5).grid(row=1, column=6)
            Label(self.master, name="3PA", text="3PA", width=5).grid(row=1, column=7)
            mybut = Button(self.master, text="Zatwierdź", bg="red", command=self.validate_all).grid(column=3,
                                                                                                    columnspan=2)

    def val_lvl(self):
        try:
            temp_lvl = int(self.myLvl_Entry.get())
            if temp_lvl < 1 or temp_lvl > 140:
                raise Exception
            else:
                return True
        except:
            messagebox.showerror(title="ERROR", message="Podana wartość jest nieprawidłowa.\nWpisz poziom od 1 do 140.")
            self.myLvl_Entry.delete(0, "end")
            return False

    def validate_all(self):
        lvl_flag = self.val_lvl()
        lvl_wid = self.master.nametowidget("lvl_entry")
        lvl = lvl_wid.get()
        # info = self.grid_info()
        # print((info["row"], info["column"]))
        skill_flag = self.val_skill()

        if lvl_flag == False or skill_flag == False:
            pass
        else:
            for nr, skill in enumerate(App.PROFESSIONS[self.current_prof]):
                # v = StringVar(root,value="7")
                temp_skill = skill.lower()
                skill_tmp = self.master.nametowidget(temp_skill)
                grid_info = skill_tmp.grid_info()
                wid_value = skill_tmp.get()
                # wisdom = self.calc_wisdom(lvl,wid_value,skill,)
                Label(self.master, text=self.calc_wisdom(lvl, wid_value, skill, 1)).grid(row=grid_info["row"], column=5)
                Label(self.master, text=self.calc_wisdom(lvl, wid_value, skill, 2)).grid(row=grid_info["row"], column=6)
                Label(self.master, text=self.calc_wisdom(lvl, wid_value, skill, 3)).grid(row=grid_info["row"], column=7)

    def calc_wisdom(self, char_lvl, skill_lvl, skill_name, pa):
        skill_diff_temp = self.PROFESSIONS[self.current_prof][skill_name]
        skill_diff = int(self.SKILLS_DIFFICULTY[self.PROFESSIONS[self.current_prof][skill_name]][int(skill_lvl) - 1])
        wisdom = (skill_diff / pa) - 40 - int(char_lvl)
        wisdom = round(wisdom)
        if wisdom >= 10:
            if skill_diff > (40 + wisdom + int(char_lvl)) * pa:
                return round(wisdom) + 1
            else:
                return round(wisdom)
        else:
            return 10

    def val_skill(self):
        val_flag = False
        skill_tmp = None
        try:
            for skill in App.PROFESSIONS[self.current_prof]:
                # v = StringVar(root,value="7")
                temp_skill = skill.lower()
                skill_tmp = self.master.nametowidget(temp_skill)
                wid_value = int(skill_tmp.get())
                if wid_value < 1 or wid_value > 7:
                    skill_tmp.delete(0, "end")
                    val_flag = True
            if val_flag == True:
                raise Exception
            else:
                return True
        except:
            messagebox.showerror(title="ERROR", message="Podana wartość jest nieprawidłowa.\nWpisz liczbę od 1 do 7")
            if skill_tmp != None:
                skill_tmp.delete(0, "end")
            return False

    def del_widgets(self):
        widgets = self.master.grid_slaves()
        for wid in widgets:
            temp = str(wid)
            if wid.widgetName == 'ttk::combobox' or wid.widgetName == 'ttk::combobox' or temp == '.lvl_entry' or temp == '.lvl_label':
                pass
            else:
                wid.grid_forget()

    def default_view(self):
        self.clicked = StringVar()
        self.clicked.set("DRUID")
        # self.profession_btn = OptionMenu(self.master, self.clicked,*App.PROFESSIONS.keys())
        # self.profession_btn.grid(column = 0, row = 0)

        self.myCombo = ttk.Combobox(self.master, width=20, value=list(App.PROFESSIONS.keys()))
        self.myCombo.current(0)
        self.myCombo.bind("<<ComboboxSelected>>", self.combo_click)
        self.myCombo.grid(column=0, row=1, columnspan=2)
        self.myLvl_label = Label(self.master, name="lvl_label", text="Poziom postaci", width=15, justify=LEFT).grid(
            row=2, column=0)
        self.myLvl_Entry = Entry(self.master, width=5, name="lvl_entry", justify=RIGHT)
        self.myLvl_Entry.insert(0, "140")
        self.myLvl_Entry.grid(row=2, column=1)
        self.combo_click("whatever")


root = Tk()
root.title("Kalkulator wiedzy by Arystos")
root.geometry("400x200", )
app = App(master=root)

app.mainloop()
