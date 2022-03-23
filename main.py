import os
import sys
import threading
from time import sleep
from tkinter import filedialog as fd, messagebox
import pyttsx3
import datetime
from os.path import exists

engine = pyttsx3.init("sapi5")
voix = engine.getProperty('voices')


def afficherVoix():
    resultats = []
    for voice in voix:
        res = "Voice: %s" % voice.name + " - ID: %s" % voice.id + " - Languages: %s" % voice.languages + " - Gender: %s" % voice.gender + " - Age: %s" % voice.age + "\n"
        resultats.append(res)
    return resultats


def parlerFromTexte(texte, genre, vitesse):
    volume = str(engine.getProperty('volume'))
    res = "texte: '" + texte + "' ---  genre: '" + genre + "'  ----  vitesse: '" + vitesse + "'  ----  volume: '" + volume + "'"

    def tache():
        if vitesse == "lente":
            engine.setProperty('rate', 90)
        elif vitesse == "normale":
            engine.setProperty('rate', 130)
        elif vitesse == "rapide":
            engine.setProperty('rate', 180)

        if genre == "Masculin":
            engine.setProperty('voice', voix[2].id)
        elif genre == "Feminin":
            engine.setProperty('voice', voix[0].id)

        engine.say(texte)
        engine.runAndWait()

    x = threading.Thread(target=tache)
    x.start()
    return res


def exporterFromTexte(texte, genre, vitesse):
    path = fd.askdirectory(
        title='Open a folder',
        initialdir='/')

    def tache():
        os.chdir(path)
        now = datetime.datetime.now()
        name = "le " + str(now.day) + "-" + str(now.month) + "-" + str(now.year) + "  " + str(now.hour) + "h" + str(
            now.minute) + "min" + str(now.second) + "sec"
        filename = "lecture " + name + ".mp3"
        engine.save_to_file(texte, filename)
        engine.runAndWait()
        messagebox.showinfo("Resultat", "Fichier mp3 exporté !")

    x = threading.Thread(target=tache)
    x.start()


contenu = ""


def importer():
    res = []
    filename = fd.askopenfilename(
        title='Open a folder',
        initialdir='/')
    res.append(filename)

    def tache():
        global contenu
        try:
            f = open(filename,'r', encoding=sys.getdefaultencoding())
            contenu = f.read()
            texte=contenu
            res.append(texte)
            f.close()

            messagebox.showinfo("Resultat", "Fichier pdf importé !\nContenu du fichier chargé et pret a etre lu.")
        except Exception as ex:
            print(ex)
            contenu = "erreur de lecture"
            res.append(contenu)

    file_exists = exists(filename)
    if(file_exists):
        x1 = threading.Thread(target=tache)
        x1.start()
        while len(res)<2:
            sleep(1)
    else:
        return ["","fichier non trouvé"]
    return res


def parlerFromPdf(texte, genre, vitesse):
    volume = str(engine.getProperty('volume'))
    res = "pdf:  ---  genre: '" + genre + "'  ----  vitesse: '" + vitesse + "'  ----  volume: '" + volume + "'"

    def tache():
        if (vitesse == "lente"):
            engine.setProperty('rate', 90)
        elif (vitesse == "normale"):
            engine.setProperty('rate', 130)
        elif (vitesse == "rapide"):
            engine.setProperty('rate', 180)

        if (genre == "Masculin"):
            engine.setProperty('voice', voix[2].id)
        elif (genre == "Feminin"):
            engine.setProperty('voice', voix[0].id)
        engine.say(texte)
        engine.runAndWait()

    x = threading.Thread(target=tache)
    x.start()
    return res


def exporterFromPdf(texte, genre, vitesse):
    path = fd.askdirectory(
        title='Open a folder',
        initialdir='/')

    def tache():
        os.chdir(path)
        now = datetime.datetime.now()
        name = "le " + str(now.day) + "-" + str(now.month) + "-" + str(now.year) + "  " + str(now.hour) + "h" + str(
            now.minute) + "min" + str(now.second) + "sec"
        filename = "lecture pdf " + name + ".mp3"
        engine.save_to_file(texte, filename)
        engine.runAndWait()
        messagebox.showinfo("Resultat", "Fichier mp3 exporté !")

    x = threading.Thread(target=tache)
    x.start()


volumePrecedent = 1.0


def setVolume(volume):
    global volumePrecedent
    volumeA = round(volume / 100, 1)
    if volumeA != volumePrecedent:
        engine.setProperty("volume", volumeA)
        engine.runAndWait()
        volumePrecedent = volumeA
