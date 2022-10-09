import codecs
import os
import re
import sys
import threading
from time import sleep
import PyPDF2
from tkinter import filedialog as fd, messagebox
import pyttsx3
import datetime
from os.path import exists

engine = pyttsx3.init("sapi5")
voix = engine.getProperty('voices')
sortedvoices = []
sortedvoicesText = []


def charger_voix():
    resultats = []
    for voice in voix:
        if re.search("French", voice.name):
            res = "Voice: %s" % voice.name + " - ID: %s" % voice.id + " - Languages: %s" % voice.languages + " - Gender: %s" % voice.gender + " - Age: %s" % voice.age + "\n"
        if re.search("Julie", voice.name):
            resultats.append((0, res, voice))
        if re.search("Paul", voice.name):
            resultats.append((2, res, voice))
        if re.search("Hortense", voice.name):
            resultats.append((1, res, voice))
    for voice2 in sorted(resultats, key=lambda tup: tup[0]):
        sortedvoicesText.append(voice2[1])
        sortedvoices.append(voice2[2])
    return 0


charger_voix()


def afficherVoix():
    return sortedvoicesText


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
            engine.setProperty('voice', sortedvoices[2].id)
        elif genre == "Feminin":
            engine.setProperty('voice', sortedvoices[0].id)
        try:
            engine.say(texte)
            engine.runAndWait()
        except Exception as e:
            print(e)

    x = threading.Thread(target=tache)
    x.setDaemon(True)
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
    x.setDaemon(True)
    x.start()


contenu = ""


def importerPdf(page):
    res = []
    filename = fd.askopenfilename(
        title='Open a folder',
        filetypes=[('PDF files', '*.pdf')],
        initialdir='/')
    res.append(filename)

    def tache():
        global contenu
        try:
            f = open(filename, 'rb')
            pdfReader = PyPDF2.PdfFileReader(f)
            pageObj = pdfReader.getPage(page)
            texte = pageObj.extractText()
            res.append(texte)
            res.append(pdfReader.numPages)
            f.close()

            messagebox.showinfo("Resultat", "Fichier pdf importé !\nContenu du fichier chargé et pret a etre lu.")
        except Exception as ex:
            print(ex)
            contenu = "erreur de lecture"
            res.append(contenu)

    file_exists = exists(filename)
    if (file_exists):
        x1 = threading.Thread(target=tache)
        x1.start()
        while len(res) < 2:
            sleep(1)
    else:
        return ["", "fichier non trouvé",0]
    return res


def importerTxt():
    res = []
    filename = fd.askopenfilename(
        title='Open a folder',
        filetypes=[('text files', 'txt')],
        initialdir='/')
    res.append(filename)

    def tache():
        global contenu
        try:
            fd = codecs.open(filename, 'r', encoding='utf-8')
            texte = fd.read()
            res.append(texte)

            messagebox.showinfo("Resultat", "Fichier txt importé !\nContenu du fichier chargé et pret a etre lu.")
        except Exception as ex:
            print(ex)
            contenu = "erreur de lecture"
            res.append(contenu)

    file_exists = exists(filename)
    if (file_exists):
        x1 = threading.Thread(target=tache)
        x1.start()
        while len(res) < 2:
            sleep(1)
    else:
        return ["", "fichier non trouvé"]
    return res


def parlerFromFile(texte, genre, vitesse):
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
            engine.setProperty('voice', sortedvoices[2].id)
        elif (genre == "Feminin"):
            engine.setProperty('voice', sortedvoices[0].id)
        engine.say(texte)
        engine.runAndWait()

    x = threading.Thread(target=tache)
    x.setDaemon(True)
    x.start()
    return res


def exporterFromFile(texte, genre, vitesse):
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
    x.setDaemon(True)
    x.start()


volumePrecedent = 1.0


def setVolume(volume):
    global volumePrecedent
    volumeA = round(volume / 100, 1)
    if volumeA != volumePrecedent:
        engine.setProperty("volume", volumeA)
        engine.runAndWait()
        volumePrecedent = volumeA
