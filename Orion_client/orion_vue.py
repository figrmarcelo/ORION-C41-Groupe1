# -*- coding: utf-8 -*-
##  version 2022 14 mars - jmd

from tkinter import *
from tkinter.simpledialog import *
from tkinter.messagebox import *
from helper import Helper as hlp
import math

import random


class Vue():
    def __init__(self, parent, urlserveur, mon_nom, msg_initial):
        self.parent = parent
        self.root = Tk()
        self.root.title("Je suis " + mon_nom)
        self.mon_nom = mon_nom
        # attributs
        self.taille_minimap = 240
        self.zoom = 2
        self.ma_selection = None
        self.dernier_selection = None
        self.contour = True
        self.etoile_select = None
        self.cadre_actif = None
        # cadre principal de l'application
        self.cadre_app = Frame(self.root, width=500, height=400, bg="red")
        self.cadre_app.pack(expand=1, fill=BOTH)
        # # un dictionnaire pour conserver les divers cadres du jeu, creer plus bas
        self.cadres = {}
        self.creer_cadres(urlserveur, mon_nom, msg_initial)
        self.changer_cadre("splash")
        # PROTOCOLE POUR INTERCEPTER LA FERMETURE DU ROOT - qui termine l'application
        # self.root.protocol("WM_DELETE_WINDOW", self.demander_abandon)

        # # sera charge apres l'initialisation de la partie, contient les donnees pour mettre l'interface a jour
        self.modele = None
        self.joueur = None
        # # variable pour suivre le trace du multiselect
        self.debut_selection = []
        self.selecteur_actif = None
        self.idSelect = ''
        self.choixBat = None
        self.premier = 0

    def demander_abandon(self):
        rep = askokcancel("Vous voulez vraiment quitter?")
        if rep:
            self.root.after(500, self.root.destroy)

    ####### INTERFACES GRAPHIQUES
    def changer_cadre(self, nomcadre):
        cadre = self.cadres[nomcadre]
        if self.cadre_actif:
            self.cadre_actif.pack_forget()
        self.cadre_actif = cadre
        self.cadre_actif.pack(expand=1, fill=BOTH)

    ###### LES CADRES ############################################################################################
    def creer_cadres(self, urlserveur, mon_nom, msg_initial):
        self.cadres["splash"] = self.creer_cadre_splash(urlserveur, mon_nom, msg_initial)
        self.cadres["lobby"] = self.creer_cadre_lobby()
        self.cadres["partie"] = self.creer_cadre_partie()

    # le splash (ce qui 'splash' à l'écran lors du démarrage)
    # sera le cadre visuel initial lors du lancement de l'application
    def creer_cadre_splash(self, urlserveur, mon_nom, msg_initial):
        self.cadre_splash = Frame(self.cadre_app)
        # un canvas est utilisé pour 'dessiner' les widgets de cette fenêtre voir 'create_window' plus bas
        self.canevas_splash = Canvas(self.cadre_splash, width=600, height=480, bg="pink")
        self.canevas_splash.pack()

        # creation ds divers widgets (champ de texte 'Entry' et boutons cliquables (Button)
        self.etatdujeu = Label(text=msg_initial, font=("Arial", 18), borderwidth=2, relief=RIDGE)
        self.nomsplash = Entry(font=("Arial", 14))
        self.urlsplash = Entry(font=("Arial", 14), width=42)
        self.btnurlconnect = Button(text="Connecter", font=("Arial", 12), command=self.connecter_serveur)
        # on insère les infos par défaut (nom url) et reçu au démarrage (dispo)
        self.nomsplash.insert(0, mon_nom)
        self.urlsplash.insert(0, urlserveur)
        # on les place sur le canevas_splash
        self.canevas_splash.create_window(320, 100, window=self.etatdujeu, width=400, height=30)
        self.canevas_splash.create_window(320, 200, window=self.nomsplash, width=400, height=30)
        self.canevas_splash.create_window(210, 250, window=self.urlsplash, width=360, height=30)
        self.canevas_splash.create_window(480, 250, window=self.btnurlconnect, width=100, height=30)
        # les boutons d'actions
        self.btncreerpartie = Button(text="Creer partie", font=("Arial", 12), state=DISABLED, command=self.creer_partie)
        self.btninscrirejoueur = Button(text="Inscrire joueur", font=("Arial", 12), state=DISABLED,
                                        command=self.inscrire_joueur)
        self.btnreset = Button(text="Reinitialiser partie", font=("Arial", 9), state=DISABLED,
                               command=self.reset_partie)

        # on place les autres boutons
        self.canevas_splash.create_window(420, 350, window=self.btncreerpartie, width=200, height=30)
        self.canevas_splash.create_window(420, 400, window=self.btninscrirejoueur, width=200, height=30)
        self.canevas_splash.create_window(420, 450, window=self.btnreset, width=200, height=30)

        # on retourne ce cadre pour l'insérer dans le dictionnaires des cadres
        return self.cadre_splash

    ######## le lobby (où on attend les inscriptions)
    def creer_cadre_lobby(self):
        # le cadre lobby, pour isncription des autres joueurs, remplace le splash
        self.cadrelobby = Frame(self.cadre_app)
        self.canevaslobby = Canvas(self.cadrelobby, width=640, height=480, bg="lightblue")
        self.canevaslobby.pack()
        # widgets du lobby
        # un listbox pour afficher les joueurs inscrit pour la partie à lancer
        self.listelobby = Listbox(borderwidth=2, relief=GROOVE)

        # bouton pour lancer la partie, uniquement accessible à celui qui a creer la partie dans le splash
        self.btnlancerpartie = Button(text="Lancer partie", state=DISABLED, command=self.lancer_partie)
        # affichage des widgets dans le canevaslobby (similaire au splash)
        self.canevaslobby.create_window(440, 240, window=self.listelobby, width=200, height=400)
        self.canevaslobby.create_window(200, 400, window=self.btnlancerpartie, width=100, height=30)
        # on retourne ce cadre pour l'insérer dans le dictionnaires des cadres
        return self.cadrelobby

    def creer_cadre_partie(self):
        self.cadrepartie = Frame(self.cadre_app, width=600, height=200, bg="yellow")
        self.cadrejeu = Frame(self.cadrepartie, width=600, height=200, bg="teal")

        self.scrollX = Scrollbar(self.cadrejeu, orient=HORIZONTAL, bg="grey11")
        self.scrollY = Scrollbar(self.cadrejeu, orient=VERTICAL)
        self.canevas = Canvas(self.cadrejeu, width=800, height=600,
                              xscrollcommand=self.scrollX.set,
                              yscrollcommand=self.scrollY.set, bg="grey11")

        self.scrollX.config(command=self.canevas.xview)
        self.scrollY.config(command=self.canevas.yview)

        self.canevas.grid(column=0, row=0, sticky=W + E + N + S)
        self.scrollX.grid(column=0, row=1, sticky=W + E)
        self.scrollY.grid(column=1, row=0, sticky=N + S)

        self.cadrejeu.columnconfigure(0, weight=1)
        self.cadrejeu.rowconfigure(0, weight=1)
        self.canevas.bind("<Button>", self.cliquer_cosmos)
        self.canevas.tag_bind(ALL, "<Button>", self.cliquer_cosmos)

        # faire une multiselection
        self.canevas.bind("<Shift-Button-1>", self.debuter_multiselection)
        self.canevas.bind("<Shift-B1-Motion>", self.afficher_multiselection)
        self.canevas.bind("<Shift-ButtonRelease-1>", self.terminer_multiselection)

        # scroll avec roulette
        self.canevas.bind("<MouseWheel>", self.defiler_vertical)
        self.canevas.bind("<Control-MouseWheel>", self.defiler_horizon)

        self.creer_cadre_outils()

        self.cadrejeu.pack(side=LEFT, expand=1, fill=BOTH)

        # self.cadreinfoglobale = self.afficher_info_generales(self.cadrejeu, 0, 0, {'pierre' : 0, 'metal' : 0, 'energie': 0}, 0, 0)
        # self.cadreinfoglobale.grid(row=2, sticky="nsew")

        return self.cadrepartie

    def creer_cadre_outils(self):
        self.cadreoutils = Frame(self.cadrepartie, width=200, height=200, bg="grey11")
        self.cadreoutils.pack(side=LEFT, fill=Y)

        self.cadreinfo = Frame(self.cadreoutils, width=200, height=200, bg="darkgrey")
        self.cadreinfo.pack(fill=BOTH)

        self.cadreinfogen = Frame(self.cadreinfo, width=200, height=200, bg="grey50")
        self.cadreinfogen.pack(fill=BOTH)
        self.labid = Label(self.cadreinfogen, text="Inconnu")
        self.labid.bind("<Button>", self.centrer_planemetemere)
        self.labid.pack()

        self.infoSelection = None
        self.levelUp = self.afficher_level_up(self.cadreoutils)

        self.cadreinfochoix = Frame(self.cadreinfo, height=200, width=200, bg="grey30")
        self.btncreercombat = Button(self.cadreinfochoix, text="Combat")
        self.btncreercombat.bind("<Button>", self.creer_vaisseau)
        self.btncreerexplorer = Button(self.cadreinfochoix, text="Explorer")
        self.btncreerexplorer.bind("<Button>", self.creer_vaisseau)
        self.btncreercargo = Button(self.cadreinfochoix, text="Cargo")
        self.btncreercargo.bind("<Button>", self.creer_vaisseau)

        self.btncreercombat.pack()
        self.btncreerexplorer.pack()
        self.btncreercargo.pack()

        self.cadreinfoliste = Frame(self.cadreinfo)

        self.scroll_liste_Y = Scrollbar(self.cadreinfoliste, orient=VERTICAL)
        self.info_liste = Listbox(self.cadreinfoliste, width=20, height=6, yscrollcommand=self.scroll_liste_Y.set)
        self.info_liste.bind("<Button-3>", self.centrer_liste_objet)
        self.info_liste.grid(column=0, row=0, sticky=W + E + N + S)
        self.scroll_liste_Y.grid(column=1, row=0, sticky=N + S)

        self.cadreinfoliste.columnconfigure(0, weight=1)
        self.cadreinfoliste.rowconfigure(0, weight=1)

        self.cadreinfoliste.pack(side=BOTTOM, expand=1, fill=BOTH)

        self.cadreminimap = Frame(self.cadreoutils, height=200, width=200, bg="black")
        self.canevas_minimap = Canvas(self.cadreminimap, width=self.taille_minimap, height=self.taille_minimap,
                                      bg="black")

        self.canevas_minimap.bind("<Button>", self.positionner_minicanevas)
        self.canevas_minimap.pack()
        self.cadreminimap.pack(side=BOTTOM)

        self.cadres["jeu"] = self.cadrepartie
        # fonction qui affiche le nombre d'items sur le jeu
        self.canevas.bind("<Shift-Button-3>", self.calc_objets)

    def afficher_info_generales(self, source, niveau, exp, res, planetes, vaisseaux):
        frame = Frame(source, width=400, height=30, bg="grey11")

        labelNiveau = Label(frame, text="Niveau : " + str(niveau), bg="grey11", fg="green", font='helvetica 10 bold')
        labelExp = Label(frame, text=str(exp) + " XP", bg="grey11", fg="green", font='helvetica 10 bold')
        labelMetal = Label(frame, text="Me : " + str(res['metal']), bg="grey11", fg="green", font='helvetica 10 bold')
        labelRoche = Label(frame, text="Ro : " + str(res['pierre']), bg="grey11", fg="green", font='helvetica 10 bold')
        labelEnergie = Label(frame, text="En : " + str(res['energie']), bg="grey11", fg="green",
                             font='helvetica 10 bold')
        labelPlanetes = Label(frame, text="Planete conquise : " + str(planetes), bg="grey11", fg="green",
                              font='helvetica 10 bold')
        labelNbVaisseau = Label(frame, text="Vaisseau : " + str(vaisseaux), bg="grey11", fg="green",
                                font='helvetica 10 bold')

        labelNiveau.place(relx=.05, rely=.5, anchor="center")
        labelExp.place(relx=.15, rely=.5, anchor="center")
        labelMetal.place(relx=.35, rely=.5, anchor="center")
        labelRoche.place(relx=.45, rely=.5, anchor="center")
        labelEnergie.place(relx=.55, rely=.5, anchor="center")
        labelPlanetes.place(relx=.75, rely=.5, anchor="center")
        labelNbVaisseau.place(relx=.9, rely=.5, anchor="center")

        return frame

    def afficher_level_up(self, source):
        frame = Frame(source, width=100, height=50, bg="darkgrey")
        up = Button(frame, text="LEVEL UP", width=50, height=3)
        up.place(anchor="center", rely=.5, relx=.5)

        return frame

<<<<<<< HEAD
    def afficher_batiment(self, source):
        self.infoSelection.pack_forget()
        self.choixBat.pack()

    def choix_batiments(self, source):
        frame = Frame(source, width=200, height=200, bg="grey11")
=======
    def afficher_crea_batiment(self, *args):
        self.choixBat.place(relx=.75, rely=.05)


    def creer_batiment(self, evt):
        type = evt.widget.cget("text")
        print(type)
        self.parent.creer_batiment([self.idSelect, type])
        self.choixBat.place_forget()

    def choix_batiments(self):
        frame = Frame(self.cadrepartie, width=200, height=200, bg="grey11", highlightthickness=2, highlightbackground="darkgrey")
>>>>>>> prod_max_official

        mine = Button(frame, text="Mine", fg="green", width=6, height=2, bg="grey19")
        centrale = Button(frame, text="Centrale", fg="green", width=6, height=2, bg="grey19")
        usine = Button(frame, text="Usine", fg="green", width=6, height=2, bg="grey19")
        canon = Button(frame, text="Canon", fg="green", width=6, height=2, bg="grey19")
        balise = Button(frame, text="Balise", fg="green", width=6, height=2, bg="grey19")
        centreRecherche = Button(frame, text="CdR", fg="green", width=6, height=2, bg="grey19")

        titre = Label(frame, text="BATIMENTS", font='helvetica 10 bold', bg="grey11", fg="green")
        titre.place(anchor="center", rely=.1, relx=.5)

<<<<<<< HEAD
=======
        # self.joueur.creerbatiment([self.idSelect, 'mine'])

>>>>>>> prod_max_official
        mine.place(anchor="center", relx=.3, rely=.35)
        centrale.place(anchor="center", relx=.7, rely=.35)
        usine.place(anchor="center", relx=.3, rely=.60)
        canon.place(anchor="center", relx=.7, rely=.60)
        balise.place(anchor="center", relx=.3, rely=.85)
        centreRecherche.place(anchor="center", relx=.7, rely=.85)

<<<<<<< HEAD
=======
        
        mine.bind('<Button>', self.creer_batiment)
        centrale.bind('<Button>', self.creer_batiment)
        usine.bind('<Button>', self.creer_batiment)
        canon.bind('<Button>', self.creer_batiment)
        balise.bind('<Button>', self.creer_batiment)
        centreRecherche.bind('<Button>', self.creer_batiment)

>>>>>>> prod_max_official
        return frame

    def affichage_planete_selectionee(self, source, planete, state):
        self.state = state
        idSelect = planete.id
        planeteSelect = planete
        print(idSelect)
        ressSelect = planeteSelect.getRessources()

        frame = Frame(source, width=200, height=200, bg="grey11")

        txtPlanete = "Planete " + idSelect.split("_")[1]
        txtRoche = "Roche : " + str(ressSelect['pierre'])
        txtMetal = "Metal : " + str(ressSelect['metal'])
        txtEnergie = "Energie : " + str(ressSelect['energie'])

        Label(frame, text=txtPlanete, font='helvetica 10 bold', bg="grey11", fg="green").place(anchor="center", relx=.5,
                                                                                               rely=.1)
        Label(frame, text=txtRoche, bg="grey11", fg="green").place(relx=.2, rely=.25)
        Label(frame, text=txtMetal, bg="grey11", fg="green").place(relx=.2, rely=.40)
        Label(frame, text=txtEnergie, bg="grey11", fg="green").place(relx=.2, rely=.55)

        batiment = Button(frame, text="BATIMENTS", fg="green", width=9, height=1, bg="grey19")
<<<<<<< HEAD
        batiment.bind('<Button>', self.afficher_batiment)
=======
        batiment.bind('<Button>', self.afficher_crea_batiment)
>>>>>>> prod_max_official
        batiment.place(anchor="center", rely=.9, relx=.25)

        return frame

    def connecter_serveur(self):
        self.btninscrirejoueur.config(state=NORMAL)
        self.btncreerpartie.config(state=NORMAL)
        self.btnreset.config(state=NORMAL)
        url_serveur = self.urlsplash.get()
        self.parent.connecter_serveur(url_serveur)

    def centrer_liste_objet(self, evt):
        info = self.info_liste.get(self.info_liste.curselection())
        print(info)
        liste_separee = info.split(";")
        type_vaisseau = liste_separee[0]
        id = liste_separee[1][1:]
        obj = self.modele.joueurs[self.mon_nom].flotte[type_vaisseau][id]
        self.centrer_objet(obj)

    def calc_objets(self, evt):
        print("Univers = ", len(self.canevas.find_all()))

    def defiler_vertical(self, evt):
        rep = self.scrollY.get()[0]
        if evt.delta < 0:
            rep = rep + 0.01
        else:
            rep = rep - 0.01
        self.canevas.yview_moveto(rep)

    def defiler_horizon(self, evt):
        rep = self.scrollX.get()[0]
        if evt.delta < 0:
            rep = rep + 0.02
        else:
            rep = rep - 0.02
        self.canevas.xview_moveto(rep)

    ##### FONCTIONS DU SPLASH #########################################################################

    ###  FONCTIONS POUR SPLASH ET LOBBY INSCRIPTION pour participer a une partie
    def update_splash(self, etat):
        if "attente" in etat or "courante" in etat:
            self.btncreerpartie.config(state=DISABLED)
        if "courante" in etat:
            self.etatdujeu.config(text="Desole - partie encours !")
            self.btninscrirejoueur.config(state=DISABLED)
        elif "attente" in etat:
            self.etatdujeu.config(text="Partie en attente de joueurs !")
            self.btninscrirejoueur.config(state=NORMAL)
        elif "dispo" in etat:
            self.etatdujeu.config(text="Bienvenue ! Serveur disponible")
            self.btninscrirejoueur.config(state=DISABLED)
            self.btncreerpartie.config(state=NORMAL)
        else:
            self.etatdujeu.config(text="ERREUR - un probleme est survenu")

    def reset_partie(self):
        rep = self.parent.reset_partie()

    def creer_partie(self):
        nom = self.nomsplash.get()
        self.parent.creer_partie(nom)

    ##### FONCTION DU LOBBY #############
    def update_lobby(self, dico):
        self.listelobby.delete(0, END)
        for i in dico:
            self.listelobby.insert(END, i[0])
        if self.parent.joueur_createur:
            self.btnlancerpartie.config(state=NORMAL)

    def inscrire_joueur(self):
        nom = self.nomsplash.get()
        urljeu = self.urlsplash.get()
        self.parent.inscrire_joueur(nom, urljeu)

    def lancer_partie(self):
        self.parent.lancer_partie()

    def initialiser_avec_modele(self, modele):
        self.mon_nom = self.parent.mon_nom
        self.modele = modele
        self.joueur = self.modele.joueurs[self.mon_nom]
        self.canevas.config(scrollregion=(0, 0, modele.largeur, modele.hauteur))

        self.labid.config(text=self.mon_nom)
        self.labid.config(fg=self.modele.joueurs[self.mon_nom].couleur)

        self.afficher_decor(modele)

    ####################################################################################################

    def positionner_minicanevas(self, evt):
        x = evt.x
        y = evt.y

        pctx = x / self.taille_minimap
        pcty = y / self.taille_minimap

        xl = (self.canevas.winfo_width() / 2) / self.modele.largeur
        yl = (self.canevas.winfo_height() / 2) / self.modele.hauteur

        self.canevas.xview_moveto(pctx - xl)
        self.canevas.yview_moveto(pcty - yl)
        xl = self.canevas.winfo_width()
        yl = self.canevas.winfo_height()

    def afficher_decor(self, mod):
        # on cree un arriere fond de petites etoieles NPC pour le look
        for i in range(len(mod.etoiles) * 50):
            x = random.randrange(int(mod.largeur))
            y = random.randrange(int(mod.hauteur))
            n = random.randrange(3) + 1
            col = random.choice(["LightYellow", "azure1", "pink"])
            self.canevas.create_oval(x, y, x + n, y + n, fill=col, tags=("fond",))
        # affichage des etoiles
        for i in mod.etoiles:
            t = i.taille * self.zoom
            self.canevas.create_oval(i.x - t, i.y - t, i.x + t, i.y + t,
                                     fill="grey80", outline=col,
                                     tags=(i.proprietaire, str(i.id), "Etoile",))
        # affichage des etoiles possedees par les joueurs
        for i in mod.joueurs.keys():
            for j in mod.joueurs[i].etoilescontrolees:
                t = j.taille * self.zoom
                self.canevas.create_oval(j.x - t, j.y - t, j.x + t, j.y + t,
                                         fill=mod.joueurs[i].couleur,
                                         tags=(j.proprietaire, str(j.id), "Etoile"))
                # on affiche dans minimap
                minix = j.x / self.modele.largeur * self.taille_minimap
                miniy = j.y / self.modele.hauteur * self.taille_minimap
                self.canevas_minimap.create_rectangle(minix, miniy, minix + 5, miniy + 5,
                                                      fill=mod.joueurs[i].couleur, outline=mod.joueurs[i].couleur,
                                                      tags=(j.proprietaire, str(j.id), "Etoile"))

    def afficher_mini(self):  # univers(self, mod):
        self.canevas_minimap.delete("mini")
        for j in self.modele.etoiles:
            minix = j.x / self.modele.largeur * self.taille_minimap
            miniy = j.y / self.modele.hauteur * self.taille_minimap
            self.canevas_minimap.create_rectangle(minix, miniy, minix + 0, miniy + 0,
                                                  fill="yellow", outline="white",
                                                  tags=("mini", "Etoile"))
        # # affichage des etoiles possedees par les joueurs
        # for i in mod.joueurs.keys():
        #   for j in mod.joueurs[i].etoilescontrolees:
        #        t = j.taille * self.zoom
        #        self.canevas.create_oval(j.x - t, j.y - t, j.x + t, j.y + t,
        #                                 fill=mod.joueurs[i].couleur,
        #                                 tags=(j.proprietaire, str(j.id),  "Etoile"))

    def centrer_planemetemere(self, evt):
        self.centrer_objet(self.modele.joueurs[self.mon_nom].etoilemere)

    def centrer_objet(self, objet):
        # permet de defiler l'écran jusqu'à cet objet
        x = objet.x
        y = objet.y

        x1 = self.canevas.winfo_width() / 2
        y1 = self.canevas.winfo_height() / 2

        pctx = (x - x1) / self.modele.largeur
        pcty = (y - y1) / self.modele.hauteur

        self.canevas.xview_moveto(pctx)
        self.canevas.yview_moveto(pcty)

    # change l'appartenance d'une etoile et donc les propriétés des dessins les représentants
    def afficher_etoile(self, joueur, cible):
        joueur1 = self.modele.joueurs[joueur]
        id = cible.id
        couleur = joueur1.couleur
        self.canevas.itemconfig(id, fill=couleur)
        self.canevas.itemconfig(id, tags=(joueur, id, "Etoile",))

    # ajuster la liste des vaisseaux
    def lister_objet(self, obj, id):
        self.info_liste.insert(END, obj + "; " + id)

    def creer_vaisseau(self, evt):
        type_vaisseau = evt.widget.cget("text")
        self.parent.creer_vaisseau(type_vaisseau, self.etoile_select.x, 
                                   self.etoile_select.y)
        self.ma_selection = None
        self.canevas.delete("marqueur")
        self.cadreinfochoix.pack_forget()

    def afficher_jeu(self):
        mod = self.modele
        self.canevas.delete("artefact")
        self.canevas.delete("objet_spatial")
        self.afficher_mini()
        joueur = mod.joueurs[self.mon_nom]

        # Affichage actualisé des informations du joueur (Mis a jour a chaque appel de la boucle jeu)
        self.cadreinfoglobale = self.afficher_info_generales(self.cadrejeu,
                                                             joueur.niveau, joueur.experience,
                                                             joueur.ressources,
                                                             len(joueur.etoilescontrolees),
                                                             len(joueur.flotte['Combat']) + len(joueur.flotte['Explorer']) +
                                                             len(joueur.flotte['Cargo']))
        self.cadreinfoglobale.grid(row=2, sticky="nsew")

        if self.ma_selection != None and self.contour == True:
            joueur = mod.joueurs[self.ma_selection[0]]
            if self.ma_selection[2] == "Etoile":
                for i in joueur.etoilescontrolees:
                    if i.id == self.ma_selection[1]:
                        x = i.x
                        y = i.y
                        t = 10 * self.zoom
                        self.canevas.create_oval(x - t, y - t, x + t, y + t,
                                                 dash=(2, 2), outline=mod.joueurs[self.mon_nom].couleur,
                                                 tags=("multiselection", "marqueur"))
            elif self.ma_selection[2] == "FlotteCombat":
                for j in joueur.flotte:
                    for i in joueur.flotte[j]:
                        i = joueur.flotte[j][i]
                        if i.id == self.ma_selection[1]:
                            x = i.x
                            y = i.y
                            t = 10 * self.zoom
                            self.canevas.create_polygon(x, y - t, x - t, y + t - 5, x + t, y + t - 5,
                                                        dash=(2, 2), outline=mod.joueurs[self.mon_nom].couleur, fill='',
                                                        tags=("multiselection", "marqueur"))
<<<<<<< HEAD
            elif self.ma_selection[2] == "FlotteExplorer" or self.ma_selection[2] == "FlotteCargo":
=======
            elif self.ma_selection[2] == "FlotteExplorer":
>>>>>>> prod_max_official
                for j in joueur.flotte:
                    for i in joueur.flotte[j]:
                        i = joueur.flotte[j][i]
                        if i.id == self.ma_selection[1]:
                            x = i.x
                            y = i.y
                            t = 10 * self.zoom
                            self.canevas.create_rectangle(x - t, (y - (t - (2 * self.zoom))), x + t,
                                                          (y + (t - (5 * self.zoom))),
                                                          dash=(2, 2), outline=mod.joueurs[self.mon_nom].couleur,
                                                          tags=("multiselection", "marqueur"))
        # afficher asset des joueurs
        for i in mod.joueurs.keys():
            i = mod.joueurs[i]
            vaisseau_local = []
            for k in i.flotte:
                for j in i.flotte[k]:
                    j = i.flotte[k][j]
                    tailleF = j.taille * self.zoom
                    if k == "Cargo":
                        self.dessiner_cargo(j, tailleF, i, k)
                    elif k == "Combat":
                        self.dessiner_combat(j, tailleF, i, k)
                    elif k == "Explorer":
                        self.dessiner_explorer(j, tailleF, i, k)
        for t in self.modele.trou_de_vers:
            i = t.porte_a
            for i in [t.porte_a, t.porte_b]:
                self.canevas.create_oval(i.x - i.pulse, i.y - i.pulse,
                                         i.x + i.pulse, i.y + i.pulse, outline=i.couleur, width=2, fill="grey15",
                                         tags=("", i.id, "Porte_de_ver", "objet_spatial"))

                self.canevas.create_oval(i.x - i.pulse, i.y - i.pulse,
                                         i.x + i.pulse, i.y + i.pulse, outline=i.couleur, width=2, fill="grey15",
                                         tags=("", i.id, "Porte_de_ver", "objet_spatial"))

    def dessiner_combat(self, obj, tailleF, joueur, type_obj):

        t = obj.taille * self.zoom
        x, y = hlp.getAngledPoint(obj.angle_cible, int(t / 4 * 3), obj.x, obj.y)
        dt = t / 2

        self.canevas.create_polygon(obj.x,
                                    (obj.y - tailleF),
                                    (obj.x - tailleF),
                                    (obj.y + tailleF),
                                    (obj.x + tailleF),
                                    (obj.y + tailleF),
                                    fill=joueur.couleur, outline='black',
                                    tags=(obj.proprietaire, str(obj.id), "FlotteCombat", type_obj, "artefact"))

    def dessiner_explorer(self, obj, tailleF, joueur, type_obj):
        self.canevas.create_rectangle((obj.x - tailleF), (obj.y - tailleF),
                                      (obj.x + tailleF), (obj.y + tailleF - 5), fill=joueur.couleur,
                                      tags=(obj.proprietaire, str(obj.id), "FlotteExplorer", type_obj, "artefact"))

    def dessiner_cargo(self, obj, tailleF, joueur, type_obj):
        t = obj.taille * self.zoom
        x, y = hlp.getAngledPoint(obj.angle_cible, int(t / 4 * 3), obj.x, obj.y)
        dt = t / 2
        self.canevas.create_oval((obj.x - tailleF), (obj.y - tailleF),
                                 (obj.x + tailleF), (obj.y + tailleF), fill=joueur.couleur,
                                 tags=(obj.proprietaire, str(obj.id), "FlotteCargo", type_obj, "artefact"))
        self.canevas.create_oval((x - dt), (y - dt),
                                 (x + dt), (y + dt), fill="yellow",
                                 tags=(obj.proprietaire, str(obj.id), "FlotteCargo", type_obj, "artefact"))

    def cliquer_cosmos(self, evt):
        t = self.canevas.gettags(CURRENT)
        if t:  # il y a des tags
            if t[0] == self.mon_nom:  # et
                self.ma_selection = [self.mon_nom, t[1], t[2]]
                if t[2] == "Etoile" and self.ma_selection[1] != self.idSelect:
                    self.idSelect = self.ma_selection[1]  # get la planete selectionee
<<<<<<< HEAD
                    if self.infoSelection:
                        self.infoSelection.pack_forget()
                    for i in self.modele.joueurs[self.ma_selection[0]].etoilescontrolees:
                        if i.id == self.idSelect:
                            self.etoile_select = i
                    print(1)
                    self.infoSelection = self.affichage_planete_selectionee(self.cadreoutils, self.etoile_select, True)
                    self.choixBat = self.choix_batiments(self.cadreoutils)
=======
                    if (self.infoSelection):
                        self.infoSelection.pack_forget()
                    for i in self.modele.joueurs[self.ma_selection[0]].etoilescontrolees:

                        #print(self.ma_selection[1])
                        if i.id == self.idSelect:
                            self.etoile_select = i
                            for info in i.batiments:

                                print(info, " :", len(i.batiments[info]))
                                
                    self.infoSelection = self.affichage_planete_selectionee(self.cadreoutils, self.etoile_select, True)
                    self.choixBat = self.choix_batiments()
>>>>>>> prod_max_official
                    self.montrer_etoile_selection()
            elif ("Etoile" in t or "Porte_de_ver" in t) and t[0] != self.mon_nom:
                if self.ma_selection:
                    self.contour = False
                    self.parent.cibler_etoile(self.ma_selection[1], t[1], t[2])
                self.ma_selection = None
                self.contour = True
                self.canevas.delete("marqueur")
        else:  # aucun tag => rien sous la souris - sinon au minimum il y aurait CURRENT
            print("Region inconnue")
            self.idSelect = None
            self.ma_selection = None
            self.canevas.delete("marqueur")
            self.levelUp.pack_forget()
            self.cadreinfochoix.pack_forget()
            self.infoSelection.pack_forget()
<<<<<<< HEAD
            self.choixBat.pack_forget()
=======
            self.choixBat.place_forget()
>>>>>>> prod_max_official

    def montrer_etoile_selection(self):
        self.cadreinfochoix.pack(fill=BOTH)
        self.infoSelection.pack(fill=BOTH)
        # self.levelUp.pack(pady=5)

    def montrer_flotte_selection(self):
        print("À IMPLANTER - FLOTTE de ", self.mon_nom)

    # Methodes pour multiselect#########################################################
    def debuter_multiselection(self, evt):
        self.debutselect = (self.canevas.canvasx(evt.x), self.canevas.canvasy(evt.y))
        x1, y1 = (self.canevas.canvasx(evt.x), self.canevas.canvasy(evt.y))
        self.selecteur_actif = self.canevas.create_rectangle(x1, y1, x1 + 1, y1 + 1, outline="red", width=2,
                                                             dash=(2, 2), tags=("", "selecteur", "", ""))

    def afficher_multiselection(self, evt):
        if self.debutselect:
            x1, y1 = self.debutselect
            x2, y2 = (self.canevas.canvasx(evt.x), self.canevas.canvasy(evt.y))
            self.canevas.coords(self.selecteur_actif, x1, y1, x2, y2)

    def terminer_multiselection(self, evt):
        if self.debutselect:
            x1, y1 = self.debutselect
            x2, y2 = (self.canevas.canvasx(evt.x), self.canevas.canvasy(evt.y))
            self.debutselect = []
            objchoisi = (list(self.canevas.find_enclosed(x1, y1, x2, y2)))
            for i in objchoisi:
                if self.parent.mon_nom not in self.canevas.gettags(i):
                    objchoisi.remove(i)
                else:
                    self.objets_selectionnes.append(self.canevas.gettags(i)[2])

            self.canevas.delete("selecteur")

    ### FIN du multiselect
