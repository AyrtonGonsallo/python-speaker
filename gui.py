import tkinter as tk
from time import sleep
from tkinter import ttk
from tkinter.font import Font
from tkinter.scrolledtext import ScrolledText
from tkinter.ttk import Style

import main
from textes import Textes


class App(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self)

        # Make the app responsive
        for index in [0, 1, 2]:
            self.columnconfigure(index=index, weight=1)
            self.rowconfigure(index=index, weight=1)

        self.var_5 = tk.DoubleVar(value=75.0)
        self.option_files_list = ["Pdf", "Txt"]
        self.filetype = tk.StringVar(value=self.option_files_list[0])

        # Create widgets :)
        self.setup_widgets()

    def setup_widgets(self):

        # Panedwindow
        self.paned = ttk.PanedWindow(self)
        self.paned.grid(row=1, column=1, pady=(25, 5), sticky="nsew", rowspan=3)

        # Notebook, pane #2  partie centrale
        self.pane_2 = ttk.Frame(self.paned, padding=5)
        self.paned.add(self.pane_2, weight=3)

        # Notebook, pane #2
        self.notebook = ttk.Notebook(self.pane_2)
        self.notebook.pack(fill="both", expand=True)

        # Tab #1
        self.tab_1 = ttk.Frame(self.notebook)
        for index in [0, 1]:
            self.tab_1.columnconfigure(index=index, weight=1)
            self.tab_1.rowconfigure(index=index, weight=1)
        self.notebook.add(self.tab_1, text="Parametres")

        # Scale
        self.scale = ttk.Scale(
            self.tab_1,
            from_=0,
            to=100,
            variable=self.var_5,
            command=lambda event: [self.var_5.set(self.scale.get()), main.setVolume(self.scale.get())],
        )
        self.scale.grid(row=2, column=0, padx=(5, 5), pady=(5, 0), sticky="ew")

        # Progressbar
        self.progress = ttk.Progressbar(
            self.tab_1, value=0, variable=self.var_5, mode="determinate"
        )
        self.progress.grid(row=1, column=0, padx=(5, 5), pady=(5, 0), sticky="ew")

        # Label
        self.label = ttk.Label(
            self.tab_1,
            text="Volume",
            justify="center",
            font=("-size", 15, "-weight", "bold"),
        )
        self.label.grid(row=0, column=0)

        def voir():
            resultats = main.afficherVoix()
            for resultat in resultats:
                self.listbox.insert(tk.END, resultat)
            return 0

        self.accentbutton = ttk.Button(
            self.tab_1, text="Afficher les voix", style="Accent.TButton", command=voir
        )
        self.accentbutton.grid(row=3, column=1, padx=5, pady=10, sticky="nsew")

        def speakT():
            texte = self.textfield.get("0.0", tk.END)
            genre = self.genre.get()
            vitesse = self.readonly_combo.get()
            res = main.parlerFromTexte(texte, genre, vitesse)
            self.listbox.insert(tk.END, res)
            return 0

        def exporterT():
            texte = self.textfield.get("0.0", tk.END)
            genre = self.genre.get()
            vitesse = self.readonly_combo.get()
            main.exporterFromTexte(texte, genre, vitesse)
            return 0

        # Tab #2
        self.tab_2 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_2, text="Texte brut")
        self.label = ttk.Label(
            self.tab_2,
            text="Ecrire le texte",
            justify="center",
            font=("-size", 15, "-weight", "bold"),
        )
        self.label.grid(row=0, column=0, pady=10, columnspan=2)
        # zone de texte
        self.textfield = ScrolledText(self.tab_2, wrap=tk.WORD, height=10)
        self.textfield.grid(row=1, column=0, pady=10, columnspan=2)
        # genre
        self.genres = ["", "Masculin", "Feminin"]
        self.genre = tk.StringVar(value=self.genres[1])
        self.optionmenu = ttk.OptionMenu(
            self.tab_2, self.genre, *self.genres
        )
        self.optionmenu.grid(row=2, column=0, padx=5, pady=10, sticky="nsew")
        # vitesse
        self.vitesse = ["lente", "normale", "rapide"]
        self.readonly_combo = ttk.Combobox(
            self.tab_2, state="readonly", values=self.vitesse
        )
        self.readonly_combo.current(1)
        self.readonly_combo.grid(row=3, column=0, padx=5, pady=10, sticky="ew")
        # parler
        self.button = ttk.Button(self.tab_2, text="Parler", command=speakT)
        self.button.grid(row=4, column=0, padx=5, pady=10, sticky="nsew")
        # exporter
        self.accentbutton = ttk.Button(
            self.tab_2, text="Exporter", style="Accent.TButton", command=exporterT
        )
        self.accentbutton.grid(row=4, column=1, padx=5, pady=10, sticky="nsew")

        def speakD():
            texte = self.textfield2.get("0.0", tk.END)
            genre = self.genre2.get()
            vitesse = self.readonly_combo2.get()
            res = main.parlerFromFile(texte, genre, vitesse)
            self.listbox.insert(tk.END, res)
            return 0

        def exporterD():
            texte = self.textfield2.get("0.0", tk.END)
            genre = self.genre2.get()
            vitesse = self.readonly_combo2.get()
            main.exporterFromFile(texte, genre, vitesse)
            return 0

        def importerD():
            filetype = self.filetype.get()

            if filetype == "Pdf":
                page = self.spinbox.get()
                try:
                    int(page) > 0
                except Exception as e:
                    self.listbox.insert(tk.END, "Techniquement: " + str(e))
                    self.listbox.insert(tk.END, "Simplement: Vous avez oublié le numero de page")
                    return 0
                self.textfield2.delete(1.0, tk.END)
                resultats2 = main.importerPdf(int(page))
                self.textfield2.insert(tk.END, resultats2[1])
                self.listbox.insert(tk.END, "Nombre de pages: "+str(resultats2[2]))
            elif filetype == 'Txt':
                self.textfield2.delete(1.0, tk.END)
                resultats2 = main.importerTxt()
                self.textfield2.insert(tk.END, resultats2[1])
            if resultats2[1] != "erreur de lecture" and resultats2[1] != "fichier non trouvé":
                self.listbox.insert(tk.END, "Fichier: " + resultats2[0] + " importé !")

            return 0

        # Tab #3
        self.tab_3 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_3, text="Texte importé")
        self.label2 = ttk.Label(
            self.tab_3,
            text="A partir d'un fichier",
            justify="center",
            font=("-size", 15, "-weight", "bold"),
        )
        self.label2.grid(row=0, column=0, pady=10, columnspan=2)
        self.radio_frame3 = ttk.LabelFrame(self.tab_3, text="Options", padding=(2, 1))
        self.radio_frame3.grid(row=1, column=2, padx=(2, 1), pady=1, sticky="nsew")

        # Radiobuttons
        self.radio_1 = ttk.Radiobutton(
            self.radio_frame3, text="Pdf", variable=self.filetype, value="Pdf"
        )
        self.radio_1.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        self.radio_2 = ttk.Radiobutton(
            self.radio_frame3, text="Txt", variable=self.filetype, value="Txt"
        )
        self.radio_2.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
        self.spinbox = ttk.Spinbox(self.radio_frame3, from_=0, to=1000, increment=1)
        self.spinbox.insert(0, "Page n°")
        self.spinbox.grid(row=2, column=0, padx=5, pady=5, sticky="ew")
        # zone de texte
        self.textfield2 = ScrolledText(self.tab_3, wrap=tk.WORD, height=10)
        self.textfield2.grid(row=1, column=0, pady=10, columnspan=2)
        # importer
        self.togglebutton2 = ttk.Checkbutton(
            self.tab_3, text="Importer", style="Toggle.TButton", command=importerD
        )
        self.togglebutton2.grid(row=2, column=0, padx=5, pady=10, sticky="nsew")
        # genre
        self.genre2 = tk.StringVar(value=self.genres[1])
        self.optionmenu2 = ttk.OptionMenu(
            self.tab_3, self.genre2, *self.genres
        )
        self.optionmenu2.grid(row=3, column=0, padx=5, pady=10, sticky="nsew")
        # vitesse
        self.readonly_combo2 = ttk.Combobox(
            self.tab_3, state="readonly", values=self.vitesse
        )
        self.readonly_combo2.current(1)
        self.readonly_combo2.grid(row=3, column=1, padx=5, pady=10, sticky="ew")
        # parler
        self.button2 = ttk.Button(self.tab_3, text="Parler", command=speakD)
        self.button2.grid(row=4, column=0, padx=5, pady=10, sticky="nsew")
        # exporter
        self.accentbutton2 = ttk.Button(
            self.tab_3, text="Exporter", style="Accent.TButton", command=exporterD
        )
        self.accentbutton2.grid(row=4, column=1, padx=5, pady=10, sticky="nsew")
        # Sizegrip
        self.sizegrip = ttk.Sizegrip(self)
        self.sizegrip.grid(row=100, column=100, padx=(0, 5), pady=(0, 5))

        # Pane #1  infos globales
        self.pane_1 = ttk.Frame(self.paned, padding=5)
        self.paned.add(self.pane_1, weight=1)

        # Scrollbar
        self.scrollbar = ttk.Scrollbar(self.pane_1)
        self.scrollbar.pack(side="right", fill="y")
        self.scrollbar2 = ttk.Scrollbar(self.pane_1, orient='horizontal', )
        self.scrollbar2.pack(side="bottom", fill="x")
        self.listbox = tk.Listbox(
            self.pane_1,
            selectmode="browse",
            yscrollcommand=self.scrollbar.set,
            xscrollcommand=self.scrollbar2.set,
            height=5,
        )

        s = Style()
        s.configure('My.TFrame', background='black')
        self.tab_4 = ttk.Frame(self.notebook,style='My.TFrame')
        self.notebook.add(self.tab_4, text="Dialogue")
        self.label4 = ttk.Label(
            self.tab_4,
            text="Talk to me",
            justify="center",
            font=("-size", 15, "-weight", "bold"),
            background="black"
        )
        myfont = Font(family="Times", size=25, weight="bold", underline=1)
        self.label4.grid(row=0, column=0, pady=10, columnspan=1)
        # zone de texte
        self.textfield4 = ScrolledText(self.tab_4, background="black", font=("-size", 25, "-weight", "bold"),
                                       wrap=tk.WORD, width=40, height=6)
        self.textfield4.grid(row=1, column=0, pady=10, columnspan=3)
        # importer
        self.togglebutton4 = ttk.Button(self.tab_4, text="Parler", style="Accent.TButton", command=None)
        self.togglebutton4.grid(row=2, column=0, padx=5, pady=10, sticky="nsew")
        t = Textes()

        def display_mot(mot):
            # self.textfield4.configure(font=myfont)
            self.textfield4.insert(tk.INSERT, mot)
            # self.textfield4.tag_add('ru', index1='1.2')
            # self.textfield4.tag_config('ru', underline=True, underlinefg='red')
            # self.textfield4.configure(font=("-size", 25, "-weight", "bold"))
            self.textfield4.insert(tk.INSERT, " ")

        def addindex(str):
            try:
                self.textfield4.tag_add('ru', index1=str)  # , index2='1.4')
            except Exception as e:
                # print(e)
                self.textfield4.tag_add('ru', index1=str.replace("0", ""))  # , index2='1.4')

        def underline_words(texte):
            positions = t.getWordsPositions(texte)
            for (deb, fin) in positions:
                # print("de "+str(deb)+" a "+str(fin))
                i = deb
                while i < fin:
                    # print(i)
                    addindex(str(format(i, '.2f')))
                    i += 0.01
                    i = round(i, 2)
            self.textfield4.tag_config('ru', underline=True, underlinefg='red')

        def display(texte):
            # underline_words(texte)
            test_string = texte.split(" ")
            delta = 700
            delay = 0
            for i in range(len(test_string)):
                try:
                    s = test_string[i]
                    update_text = lambda s=s: display_mot(s)
                    self.tab_4.after(delay, update_text)
                    delay += delta
                except Exception as e:
                    print(e)
                    return 0
            underline_words_callback = lambda texte=texte: underline_words(texte)
            self.tab_4.after(delay + 400, underline_words_callback)
            # print(delay+)

        # activer
        def init_dialogue():
            try:
                if "selected" in (self.switch4.state()):
                    main.parlerFromTexte(t.getFirstSentence(), "Feminin", "rapide")
                    phrase = "I WILL PROTECT YOU NOW!"
                    display(phrase)
                else:
                    main.parlerFromTexte(t.getLastSentence(), "Feminin", "rapide")
                    self.textfield4.delete(1.0, tk.END)
            except Exception as e:
                print(e)

        s2 = Style()
        s2.configure('Switch.TCheckbutton', background='black')
        self.switch4 = ttk.Checkbutton(
            self.tab_4, text="Activer le dialogue",style="Switch.TCheckbutton", command=init_dialogue
        )
        self.switch4.grid(row=0, column=1, padx=5, pady=10, sticky="nsew")

        def effacer():
            self.listbox.delete(0, tk.END)

        self.listbox.pack(expand=True, fill="both")
        self.scrollbar2.config(command=self.listbox.xview)
        self.scrollbar.config(command=self.listbox.yview)

        self.listbox.insert(tk.END, "infos ici...")
        # Pane #1  infos globales
        self.pane_3 = ttk.Frame(self.paned, padding=5)
        self.paned.add(self.pane_3, weight=1)
        self.accentbutton3 = ttk.Button(
            self.pane_3, text="Effacer", style="Accent.TButton", command=effacer
        )
        self.accentbutton3.pack()

        """frameCnt = 25
        frames = [tk.PhotoImage(file='C://Users//Dell//PycharmProjects//Machine//samaritan.gif', format ='gif -index %i' % (i)) for i in range(frameCnt)]

        def update(ind):

            frame = frames[ind]
            ind += 1
            if ind == frameCnt:
                ind = 0
            label.configure(image=frame)
            self.tab_4.after(100, update, ind)
        label = tk.Label(self.tab_4)
        label.grid(row=3, column=1, padx=5, pady=10, sticky="nsew")
        self.tab_4.after(0, update, 0)"""


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Machine")
    root.iconbitmap("C:/Users/Dell/PycharmProjects/Machine/speak.ico")
    #  pyinstaller --onefile --icon "speak.ico" --noconsole gui.py
    # Simply set the theme
    root.tk.call("source", "C:/Users/Dell/PycharmProjects/Machine/azure.tcl")
    root.tk.call("set_theme", "dark")

    app = App(root)
    app.pack(fill="both", expand=True)

    # Set a minsize for the window, and place it in the middle
    root.update()
    root.minsize(root.winfo_width(), root.winfo_height())
    x_cordinate = int((root.winfo_screenwidth() / 2) - (root.winfo_width() / 2))
    y_cordinate = int((root.winfo_screenheight() / 2) - (root.winfo_height() / 2))
    root.geometry("+{}+{}".format(x_cordinate, y_cordinate - 20))

    root.mainloop()
