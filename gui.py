import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
import main


class App(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self)

        # Make the app responsive
        for index in [0, 1, 2]:
            self.columnconfigure(index=index, weight=1)
            self.rowconfigure(index=index, weight=1)

        self.var_5 = tk.DoubleVar(value=75.0)

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
            res = main.parlerFromPdf(texte, genre, vitesse)
            self.listbox.insert(tk.END, res)
            return 0

        def exporterD():
            texte = self.textfield2.get("0.0", tk.END)
            genre = self.genre2.get()
            vitesse = self.readonly_combo2.get()
            main.exporterFromPdf(texte, genre, vitesse)
            return 0

        def importerD():
            self.textfield2.delete(1.0, tk.END)
            resultats2 = main.importer()
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


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Ayrton´s Speaker")
    root.iconbitmap("C:/Users/user/Videos/python/Speaker/speak.ico")
    #  pyinstaller --onefile --icon "scrapping.ico" --noconsole gui.py
    # Simply set the theme
    root.tk.call("source", "azure.tcl")
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
