# -*- coding: utf-8 -*-
import time, os, sys
import uuid
import random
import pickle
from FSM import FSM, StackFSM

"""
    # TODO :
    Icon
    Mutation X
    Partagé

    PRODUCTION UN TOUR SUR DEUX = modulo voir forêt
    PLUSIEURS PRODUITS = self 1 et self 2
    PRODUITS * x = boucle for

    casse DANS LE TABLEAU à la fin? (le tableau sert à tirer les ressources de début au hasard)




"""

base_path = "/Users/samuel/Desktop"
# base_path = "/home/jdpillon/Bureau/samuel"

class FileIO(object):
    @staticmethod
    def loadStegano(f):
        print("load filename: ", f)
        im = Image.open(f)
        o = stepic.decode(im)
        print("load string:", o)
        print(type(o))
        o = bytes(o, 'UTF-8')
        return pickle.loads(o)

    @staticmethod
    def saveStegano(o):
        s = str(pickle.dumps(o))
        im = Image.open(os.path.join("ressources",o.icon))
        secret = stepic.encode(im, s)
        secret.save(o.id + ".png")
    @staticmethod
    def saveBinaryFile(o):
        pickle.dump(o, open(o.id, "wb"))
    @staticmethod
    def loadBinaryFile(f):
        try:
            return pickle.load(open(f, "rb"))
        except:
            return None
    @staticmethod
    def save(o):
        FileIO.saveBinaryFile(o)
    @staticmethod
    def load(f):
        print("Load", f)
        return FileIO.loadBinaryFile(f)

class Base(object):
    """
        Permet de charger et de sauvegarder un object
        sur le système de fichier de l'utilisateur
    """
    data = []
    def __init__(self, name = None, path = base_path, icon = "default.png"):
        self.path = path
        if not name:
            self.name = self.__class__.__name__
        else:
            self.name = name
        self.id = os.path.join(self.path, self.name)
        self.brain = StackFSM(self.idle)
        self.icon = icon
    def checkPath(self, new_path, new_filename):
        if new_filename != ".config":
            self.path = new_path
            self.name = new_filename
            self.id = os.path.join(self.path, self.name)
    def update(self):
        self.brain.update()
    def save(self):
        pickle.dump(self, open(self.id, "wb"))

    def remove(self):
        for e in Robot.items:
            if e.id == self.id:
                Robot.items.remove(e)
                os.remove(self.id)

    def idle(self): pass

    #@classmethod
    def findOneElement(self, klass):
        for root_path, folders, filenames in os.walk(self.id):
         for t in filenames:
            try:
                 tmp = pickle.load(open(os.path.join(self.id, t), "rb"))
                 if klass == type(tmp) or klass in tmp.__class__.__bases__:
                     return tmp
            except:
                pass
        return None

    def spawn(self, klass = None, path = None):
        if path is None: path = base_path
        o = klass(name = klass.__name__ + "__" + str(uuid.uuid4()) ,path = path)
        o.save()
        return o

    def getCurrentState(self):
        return self.brain.getCurrentState().__name__
    """
    @classmethod
    def findOne(self):
        print("findOne", self.name)

    @classmethod
    def find(self):
        print("find", self.name)
    """
    def __str__(self):
        #return self.name + " : " + str(self.nbOuvriers) + " " + str(self.tracteur) + " " + str(self. ouvrier) + " " + str(self.pesticide)
        return self.name + " " + self.getCurrentState()

class Entite(Base):
    """
        Entités
            - Ville
            - Megapole
            - Megalopole
            - CentraleThermique
            - CentraleAtom
            - CentraleSol
            - Caserne
            - BTP
            - Tissage
            - Acierie
            - GenieMecanique
            - Arsenal
            - IndustrieChimique
            - Universite
            - Hopital
            - Aeronautique
            - Electronique
            - Assurance
            - Banque
            - GisementCharbon
            - GisementPetrole
            - GisementUranium
            - GisementMetaux
            - GisementMetauxPrecieux
            - MineCharbon
            - PuitsPetrole
            - MineUranium
            - MineMetaux
            - MineMetauxPrecieux
            - DechargeAtomique
            - Frontiere
            - Mer

            Représentation sous forme de répertoire

    """
    def countByType(self, klass):
        n = 0
        for root_path, folders, filenames in os.walk(self.id):
            for t in filenames:
                try:
                    tmp = pickle.load(open(os.path.join(self.id, t), "rb"))
                    if klass == type(tmp) or klass in tmp.__class__.__bases__:
                        n += 1
                except:
                    pass
        return n

    def mutate(self, klass):
        for e in Robot.items:
            if e.id == self.id:
                Robot.items.remove(e)
        self.__class__ = klass
        self.__init__(name = self.name)
        self.save()


    def save(self):
        try:
            os.mkdir(os.path.join(self.path, self.name))
        except Exception as e:
            # print(e)
            pass
        pickle.dump(self, open(os.path.join(self.path, self.name, ".config"), "wb"))

    def remove(self, klass):
        o = self.findOneElement(klass)
        if o: o.remove()

    def __str__(self):
        return self.name + " " + self.getCurrentState()

class Robot(object):
    """
        Robot :
            - Créé un Marché avec tous les éléments à disposition pour le joueur
            - sert un nouveau plateau au joueur au démarrage si son plateau (Bureau) est vide
            - met à jour le plateau toutes les 60 secondes
    """
    cycles = 0
    items = []
    def __init__(self, base_path = base_path, secondes = 5):
        self.path = base_path
        self.secondes = secondes
        self.cycles = 0


        self.createOrLoadGame()

    def createOrLoadGame(self):
        # only in macos
        #files = os.listdir(self.path)
        #for f in files:
        #    if f == ".DS_Store":
        #        os.remove(os.path.join(self.path, f))
        filenames = os.listdir(self.path)
        try:
            filenames.remove('.DS_Store')
        except:
            pass

        if not filenames:
            print("Create new game")

# patrimoine de départ ici

            Robot.items.append(Ville())
            Robot.items.append(Ble(icon="Ble.png"))
            Robot.items.append(BTP())
            Robot.items.append(Champ())
            Robot.items.append(Bois(name="bois1"))
            Robot.items.append(Bois(name="bois2"))
            Robot.items.append(Bois(name="bois3"))
            Robot.items.append(Bois(name="bois4"))
            Robot.items.append(Bois(name="bois5"))
            Robot.items.append(Bois(name="bois6"))
            Robot.items.append(Bois(name="bois7"))
            Robot.items.append(Bois(name="bois8"))
            Robot.items.append(Acier(name="Acier1"))
            Robot.items.append(Acier(name="Acier2"))
            Robot.items.append(Acier(name="Acier3"))
            Robot.items.append(Acier(name="Acier4"))
            Robot.items.append(Charbon())
            Robot.items.append(Petrole(name="Petrole1"))
            Robot.items.append(Petrole(name="Petrole2"))
            Robot.items.append(Uranium())
            Robot.items.append(Tracteur())
            Robot.items.append(Metaux())
            Robot.items.append(Travailleur(name="Travailleur1"))
            Robot.items.append(Travailleur(name="Travailleur2"))
            Robot.items.append(Travailleur(name="Travailleur3"))
            Robot.items.append(Travailleur(name="Travailleur4"))
            Robot.items.append(Travailleur(name="Travailleur5"))
            Robot.items.append(Travailleur(name="Travailleur6"))
            Robot.items.append(Foret())
            Robot.items.append(GenieMecanique())
            Robot.items.append(Ingenieur(name="Ingenieur1"))
            Robot.items.append(Ingenieur(name="Ingenieur2"))
            self.save()

    def loadFromFS(self):
        Robot.items = []

        for root_path, folders, filenames in os.walk(self.path):
            try:
                filenames.remove('.DS_Store')
            except:
                pass
            for f in filenames:
                current_file = os.path.join(root_path, f)
                if f != ".config":
                    print(current_file)
                    o = FileIO.load(current_file)
                    o.checkPath(root_path, f)
                    Robot.items.append(o)
                else:
                    o = pickle.load(open(current_file, "rb"))
                    o.checkPath(root_path, f)
                    Robot.items.append(o)
                    #pass

    def save(self):
        for o in Robot.items:
            o.save()

    def run(self):
        while True:
            print("############################################")
            print("Cycle :", self.cycles)
            self.update()
            print("############################################")
            self.cycles += 1
            Robot.cycles = self.cycles
            time.sleep(self.secondes)

    def update(self):
        self.loadFromFS()
        for item in Robot.items:
            item.update()
        self.save()

"""
#ce tableau tu peux t'en servir pour piocher des ressources au hasard
entites = [Champ, Monoculture, Elevage, ElevageIntensif, Tissage, BTP, Hopital, Universite, CentraleSol, CentraleAtom, CentraleThermique, GenieMecanique, Arsenal, IndustrieChimique, Acierie, Aeronautique, Electronique, Banque, Assurance, GisementPetrole, GisementCharbon, GisementMetaux, GisementMetauxPrecieux, GisementUranium, MineCharbon, PuitsPetrole, MineUranium, MineMetaux, MineMetauxPrecieux, Ville, Megapole, Megalopole, Foret, Mer, DechargeAtomique, Frontiere]
bio = [Pollinisateur, Mouton, Boeuf, Volaille, Porc, Anchois, Anguille, Baleine, Carpe, Colin, Hareng, Maquereau, Morue, Sardine, Saumon, Thon, Truite, Coton, Lin]
nourriture = [Mouton, Boeuf, Volaille, Porc, Poisson, Mais, Millet, Patate, Riz, Seigle, Soja, Sorgho, Ble]
fossile = [Bois, Charbon, Petrole, Uranium, Metaux, MetauxPrecieux]
produits = [Tracteur, VehiculeThermique, VehiculeElectrique, BateauUsine, Acier, Arme, Avion, Beton, Chimie, DechetRadioactif, Electricite, Fumier, Fusee, Ordinateur, Sante]
vivants = [Travailleur, Ingenieur, Soldat]
"""

########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################        

class Ville(Entite):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.nbTravailleur = 0
        self.nbVivant = 0
        self.nbNourriture = 0
        self.nbBois = 0
        self.nbBeton = 0
        self.nbVehicule = 0
        self.nbCoton = 0
        self.nbLin = 0
        self.nbAcier = 0
        self.nbCharbon = 0
        self.nbPetrole = 0
        self.produit = Travailleur

    def idle(self):
        condition_pop = self.nbNourriture >= 1 and self.nbVivant >= 1
        condition_newBTP = self.nbBois >= 5 and self.nbTravailleur >= 4
        condition_newAcierie = self.nbBois >= 8 and self.nbTravailleur >= 4
        condition_newTissage = self.nbBois >= 5 and self.nbTravailleur >= 2 and self.nbCoton >= 1 or self.nbLin >= 1
        condition_newGenieMecanique = self.nbBois >= 5 and self.nbTravailleur >= 4 and self.nbAcier >= 1
        condition_newcentraleThermique= self.nbBois >= 5 and self.nbTravailleur >= 2 and self.nbCharbon >= 1 or self.nbPetrole >= 1
        condition_newMegapole = self.nbBeton >= 10 and self.nbVehicule >= 10

#il execute les if de manière séquentielle le mec
#c'est le dernier IF VRAI qui a raison
        if condition_pop : self.brain.setState(self.pop)
        if condition_newBTP : self.brain.setState(self.newBTP)
        if condition_newAcierie : self.brain.setState(self.newAcierie)    
        if condition_newTissage : self.brain.setState(self.newTissage)    
        if condition_newGenieMecanique : self.brain.setState(self.newGenieMecanique)    
        if condition_newcentraleThermique: self.brain.setState(self.newCentraleThermique)    

    def pop(self):
        self.spawn(self.produit)
        if self.nbNourriture <1 or self.nbVivant <1 :
            self.brain.setState(self.idle)
        self.idle()

#alors ce self.idle() c'est un peu chelou mais c'est pour l'aider à sortir de la boucle si jamais
#le client veut fabriquer un truc dans sa ville.

    def newBTP(self):
        newbtp = self.spawn(BTP) 
        for i in range(5):
            self.remove(Bois)
        for u in range(4):
            self.remove(Travailleur)
            self.spawn(Travailleur, newbtp.id)

        if self.nbBois < 5 or self.nbTravailleur < 4:
            self.brain.setState(self.idle)
            self.save()
        
        self.idle()


    def newAcierie(self):
        newacierie = self.spawn(Acierie) 
        for i in range(8):
            self.remove(Bois)
        for u in range(4):
            self.remove(Travailleur)
            self.spawn(Travailleur, newacierie.id)

        if self.nbBois < 8 or self.nbTravailleur < 4:
            self.brain.setState(self.idle)
            self.save()

        self.idle()

    def newTissage(self):
        newtissage = self.spawn(Tissage) 
        for i in range(5):
            self.remove(Bois)
        for u in range(2):
            self.remove(Travailleur)
            self.spawn(Travailleur, newtissage.id)
        if self.nbCoton >= 1 :
            self.remove(Coton)
        else :
            self.remove(Lin)

        if self.nbBois < 5 or self.nbTravailleur < 2 or self.nbCoton < 1 and self.nbLin < 1 :
            self.brain.setState(self.idle)
            self.save()

        self.idle()

    def newGenieMecanique(self):
        newgeniemecanique = self.spawn(GenieMecanique) 
        for i in range(5):
            self.remove(Bois)
        for u in range(4):
            self.remove(Travailleur)
            self.spawn(Travailleur, newgeniemecanique.id)

        self.remove(Acier)

        if self.nbBois < 5 or self.nbTravailleur < 4 or self.nbAcier < 1 :
            self.brain.setState(self.idle)
            self.save()

        self.idle()

    def newCentraleThermique(self):
        newcentralethermique= self.spawn(CentraleThermique) 
        for i in range(5):
            self.remove(Bois)
        for u in range(2):
            self.remove(Travailleur)
            self.spawn(Travailleur, newcentralethermique.id)

        self.remove(Acier)

        if self.nbBois < 5 or self.nbTravailleur < 2 or self.nbPetrole < 1 and self.nbCharbon < 1 :
            self.brain.setState(self.idle)
            self.save()

        if self.nbPetrole >= 1 :
            self.remove(Petrole)
        else :
            self.remove(Charbon)


    def update(self):
        # update Ville here
        self.nbTravailleur = self.countByType(Travailleur)
        self.nbNourriture = self.countByType(Nourriture)
        self.nbBois = self.countByType(Bois)
        self.nbBeton = self.countByType(Beton)
        self.nbVehicule = self.countByType(Vehicule)
        self.nbCoton = self.countByType(Coton)
        self.nbLin = self.countByType(Lin)
        self.nbAcier = self.countByType(Acier)
        self.nbCharbon = self.countByType(Charbon)
        self.nbPetrole = self.countByType(Petrole)
        self.nbVivant = self.countByType(Vivant)

        self.brain.update()

class BTP(Entite):
    def __init__(self, **kwargs): 
        super().__init__(**kwargs)
        self.nbTravailleur = 0
        self.produit = Beton
    def idle(self):
        if self.nbTravailleur >= 2:
            self.brain.setState(self.production)
    def production(self):
        self.spawn(self.produit)
        if self.nbTravailleur < 2:
            self.brain.setState(self.idle)

    def update(self):
        # update BTP here
        self.nbTravailleur = self.countByType(Travailleur)
        self.brain.update()

class CentraleThermique(Entite):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.nbIngenieur = 0
        self.nbFossile = 0
        self.produit = Electricite
    def idle(self):
        if self.nbIngenieur >= 2 and self.nbFossile >= 1:
            self.brain.setState(self.production)
    def production(self):
        self.spawn(self.produit)
        if self.nbIngenieur < 2 or self.nbFossile < 1:
            self.brain.setState(self.idle)

    def update(self):
        self.nbIngenieur = self.countByType(Ingenieur)
        self.nbFossile = self.countByType(Fossile)
        self.brain.update()

class Acierie(Entite):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.nbTravailleur = 0
        self.nbCharbon = 0
        self.nbMetaux = 0
        self.produit = Acier
    def idle(self):
        if self.nbTravailleur >= 4 and self.nbCharbon >= 1 and self.nbMetaux >= 1:
            self.brain.setState(self.production)
    def production(self):
        self.spawn(self.produit)
        if self.nbTravailleur < 4 or self.nbCharbon < 1 or self.nbMetaux < 1:
            self.brain.setState(self.idle)

    def update(self):
        self.nbTravailleur = self.countByType(Travailleur)
        self.nbCharbon = self.countByType(Charbon)
        self.nbMetaux = self.countByType(Metaux)
        self.brain.update()

class Tissage(Entite):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.nbTravailleur = 0
        self.nbLin = 0
        self.nbCoton = 0
        self.produit = Textile
    def idle(self):
        if self.nbTravailleur >= 2 and self.nbLin >= 1 or self.nbCoton >= 1 :
            self.brain.setState(self.production)
    def production(self):
        self.spawn(self.produit)
        if self.nbTravailleur < 2 or self.nbLin < 1 and self.nbCoton < 1 :
            self.brain.setState(self.idle)

    def update(self):
        self.nbTravailleur = self.countByType(Travailleur)
        self.nbCoton = self.countByType(Coton)
        self.nbLin = self.countByType(Lin)
        self.brain.update()

class GenieMecanique(Entite):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.nbTravailleur = 0
        self.nbAcier = 0
        self.nbPetrole = 0
        self.nbMetauxPrecieux = 0

    def idle(self):

        condition_VTH = self.nbPetrole >= 1 and self.nbAcier >= 1 and self.nbTravailleur >= 4
        condition_VTE = self.nbMetauxPrecieux >= 1 and self.nbAcier >= 1 and self.nbTravailleur >= 4
        condition_Tracteur = self.nbPetrole >= 2 and self.nbAcier >= 1 and self.nbTravailleur >= 4
        condition_BateauUsine = self.nbPetrole >= 2 and self.nbAcier >= 2 and self.nbTravailleur >= 4

        if condition_VTH : self.brain.setState(self.newVTH)
        if condition_VTE : self.brain.setState(self.newVTE)
        if condition_Tracteur : self.brain.setState(self.newTracteur)
        if condition_BateauUsine : self.brain.setState(self.newBateauUsine)        
        

    def newVTH(self):
        self.spawn(VehiculeThermique)
        self.remove(Petrole)
        self.remove(Acier)
        if self.nbTravailleur < 4 or self.nbPetrole < 1 or self.nbAcier < 1 :
            self.brain.setState(self.idle)
        self.idle()

    def newVTE(self):
        self.spawn(VehiculeElectrique)
        self.remove(MetauxPrecieux)
        self.remove(Acier)
        if self.nbTravailleur < 4 or self.nbMetauxPrecieux < 1 or self.nbAcier < 1 :
            self.brain.setState(self.idle)
        self.idle()

    def newTracteur(self):
        self.spawn(Tracteur)
        for x in range(2):
            self.remove(Petrole)
        self.remove(Acier)
        if self.nbTravailleur < 4 or self.nbPetrole < 2 or self.nbAcier < 1 :
            self.brain.setState(self.idle)
        self.idle()

    def newBateauUsine(self):
        self.spawn(BateauUsine)
        for x in range(2):
            self.remove(Petrole)
            self.remove(Acier)
        if self.nbTravailleur < 4 or self.nbPetrole < 2 or self.nbAcier < 2 :
            self.brain.setState(self.idle)
        self.idle()

    def update(self):
        self.nbTravailleur = self.countByType(Travailleur)
        self.nbPetrole = self.countByType(Petrole)
        self.nbAcier = self.countByType(Acier)
        self.nbMetauxPrecieux = self.countByType(MetauxPrecieux)
        self.brain.update()

class Megapole(Entite):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.nbTravailleur = 0
        self.nbVivant = 0
        self.nbIngenieur = 0
        self.nbBeton = 0
        self.nbVehiculeThermique = 0
        self.nbSoldat = 0
        self.nbAcier = 0
        self.nbPetrole = 0
        self.nbUranium = 0
        self.nbMetauxPrecieux = 0
        self.produit = Travailleur

    def idle(self):
        condition_pop = self.nbNourriture >= 1 and self.nbVivant >= 1
        condition_newIndustrieChimique = self.nbBeton >= 5 and self.nbPetrole >= 3 and self.nbTravailleur >= 3
        condition_newArsenal = self.nbBeton >= 5 and self.nbAcier >= 3 and self.nbTravailleur >= 4
        condition_newHopital = self.nbBeton >= 5 and self.nbIngenieur >= 4
        condition_newUniversite = self.nbBeton >= 5 and self.nbIngenieur >= 4 and self.nbTravailleur >= 1
        condition_newAeronautique = self.nbBeton >= 5 and self.nbTravailleur >= 4 and self.nbVehiculeThermique >= 3
        condition_newCentraleAtom = self.nbBeton >= 5 and self.nbUranium >= 1 and self.nbIngenieur >= 1
        condition_newCentraleSol = self.nbBeton >= 5 and self.nbIngenieur >= 1 and nbMetauxPrecieux >= 2
        condition_newCaserne = self.nbBeton >= 5 and self.nbSoldat >= 2 and nbTravailleur >= 1

#il execute les if de manière séquentielle le mec
#c'est le dernier IF VRAI qui a raison
        if condition_pop : self.brain.setState(self.pop)
        if condition_newIndustrieChimique : self.brain.setState(self.newIndustrieChimique)
        if condition_newArsenal : self.brain.setState(self.newArsenal)    
        if condition_newHopital : self.brain.setState(self.newHopital)    
        if condition_newUniversite : self.brain.setState(self.newUniversite)    
        if condition_newAeronautique : self.brain.setState(self.newAeronautique)    
        if condition_newCentraleAtom : self.brain.setState(self.newCentraleAtom)    
        if condition_newCentraleSol : self.brain.setState(self.newCentraleSol)    
        if condition_newCaserne : self.brain.setState(self.newCaserne)    

    def pop(self):
        self.spawn(self.produit)
        if self.nbNourriture <1 or self.nbVivant <1 :
            self.brain.setState(self.idle)
        self.idle()

#alors ce self.idle() c'est un peu chelou mais c'est pour l'aider à sortir de la boucle si jamais
#le client veut fabriquer un truc dans sa ville.

    def newIndustrieChimique(self):
        newindustriechimique = self.spawn(IndustrieChimique) 
        for i in range(5):
            self.remove(Beton)
        for z in range(3):
            self.remove(Petrole)
        for u in range(4):
            self.remove(Travailleur)
            self.spawn(Travailleur, newindustriechimique.id)

        if self.nbBeton < 5 or self.nbTravailleur < 4 or self.nbAcier < 3 :
            self.brain.setState(self.idle)
            self.save()
        
        self.idle()


    def newArsenal(self):
        newarsenal = self.spawn(Arsenal) 
        for i in range(5):
            self.remove(Beton)
        for z in range(3):
            self.remove(Acier)
        for u in range(4):
            self.remove(Travailleur)
            self.spawn(Travailleur, newarsenal.id)

        if self.nbBeton < 5 or self.nbTravailleur < 4 or self.nbAcier < 3:
            self.brain.setState(self.idle)
            self.save()

        self.idle()

    def newHopital(self):
        newhopital = self.spawn(Hopital) 
        for i in range(5):
            self.remove(Beton)
        for u in range(4):
            self.remove(Ingenieur)
            self.spawn(Ingenieur, newhopital.id)

        if self.nbBeton < 5 or self.nbIngenieur < 4 :
            self.brain.setState(self.idle)
            self.save()

        self.idle()

    def newUniversite(self):
        newuniversite = self.spawn(Universite) 
        for i in range(5):
            self.remove(Beton)
        for u in range(3):
            self.remove(Ingenieur)
            self.spawn(Ingenieur, newuniversite.id)
        self.remove(Travailleur)
        self.spawn(Travailleur, newuniversite.id)

        if self.nbBeton < 5 or self.nbTravailleur < 1 or self.nbIngenieur < 3 :
            self.brain.setState(self.idle)
            self.save()

        self.idle()

    def newAeronautique(self):
        newaeronautique = self.spawn(Aeronautique) 
        for i in range(5):
            self.remove(Beton)
        for z in range(3):
            self.remove(VehiculeThermique)
        for u in range(4):
            self.remove(Travailleur)
            self.spawn(Travailleur, newaeronautique.id)

        if self.nbBeton < 5 or self.nbTravailleur < 4 or self.nbVehiculeThermique < 3 :
            self.brain.setState(self.idle)
            self.save()

        self.idle()

    def newCentraleAtom(self):
        newcentraleatom = self.spawn(CentraleAtom) 
        for i in range(5):
            self.remove(Beton)
        self.remove(Uranium)
        self.remove(Ingenieur)
        self.spawn(Ingenieur, newcentraleatom.id)

        if self.nbBeton < 5 or self.nbIngenieur < 1 or self.nbUranium < 1 :
            self.brain.setState(self.idle)
            self.save()

        self.idle()

    def newCentraleSol(self):
        newcentralesol = self.spawn(CentraleSol) 
        for i in range(5):
            self.remove(Beton)
        self.remove(MetauxPrecieux)
        self.remove(Ingenieur)
        self.spawn(Ingenieur, newcentralesol.id)

        if self.nbBeton < 5 or self.nbTravailleur < 4 or self.nbVehiculeThermique < 3 :
            self.brain.setState(self.idle)
            self.save()

        self.idle()

    def newCaserne(self):
        newcaserne = self.spawn(Caserne) 
        for i in range(5):
            self.remove(Beton)
        for u in range(2):
            self.remove(Soldat)
            self.spawn(Soldat, newcaserne.id)
        self.remove(Travailleur)
        self.spawn(Travailleur, newcaserne.id)

        if self.nbBeton < 5 or self.nbTravailleur < 1 or self.nbSoldat < 2 :
            self.brain.setState(self.idle)
            self.save()

        self.idle()


    def update(self):
        # update Ville here
        self.nbTravailleur = self.countByType(Travailleur)
        self.nbNourriture = self.countByType(Nourriture)
        self.nbBois = self.countByType(Bois)
        self.nbBeton = self.countByType(Beton)
        self.nbVehicule = self.countByType(Vehicule)
        self.nbCoton = self.countByType(Coton)
        self.nbLin = self.countByType(Lin)
        self.nbAcier = self.countByType(Acier)
        self.nbCharbon = self.countByType(Charbon)
        self.nbPetrole = self.countByType(Petrole)
        self.nbVivant = self.countByType(Vivant)

        self.brain.update()

class Arsenal(Entite):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.nbTravailleur = 0
        self.nbAcier = 0
        self.nbVehicule = 0
        self.nbAvion = 0
        self.nbFusee = 0

    def idle(self):

        condition_Fusil = self.nbAcier >= 1 and self.nbTravailleur >= 4
        condition_Tank = self.nbVehicule >= 1 and self.nbTravailleur >= 4
        condition_Bombardier = self.nbAvion >= 1 and self.nbTravailleur >= 4
        condition_Missile = self.nbFusee >= 1 and self.nbTravailleur >= 4

        if condition_Fusil : self.brain.setState(self.newFusil)
        if condition_Tank : self.brain.setState(self.newTank)
        if condition_Bombardier : self.brain.setState(self.newBombardier)
        if condition_Missile : self.brain.setState(self.newMissile)        
        
    def newTank(self):
        self.spawn(Arme)
        self.remove(Acier)

        if self.nbTravailleur < 4 or self.nbAcier < 1 :
            self.brain.setState(self.idle)
        self.idle()

    def newTank(self):
        for x in range(3):
            self.spawn(Arme)

        self.remove(Vehicule)

        if self.nbTravailleur < 4 or self.nbVehicule < 1 :
            self.brain.setState(self.idle)
        self.idle()

    def newBombardier(self):
        for x in range(6):
            self.spawn(Arme)

        self.remove(Avion)

        if self.nbTravailleur < 4 or self.nbAvion < 1 :
            self.brain.setState(self.idle)
        self.idle()

    def newMissile(self):
        for x in range(9):
            self.spawn(Arme)

        self.remove(Fusee)

        if self.nbTravailleur < 4 or self.nbFusee < 1 :
            self.brain.setState(self.idle)
        self.idle()

    def update(self):
        self.nbTravailleur = self.countByType(Travailleur)
        self.nbVehicule = self.countByType(Vehicule)
        self.nbAcier = self.countByType(Acier)
        self.nbAvion = self.countByType(Avion)
        self.nbFusee = self.countByType(Fusee)
        self.brain.update()


class Hopital(Entite):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.nbIngenieur = 0
        self.produit = Sante
    def idle(self):
        if self.nbIngenieur >= 4 :
            self.brain.setState(self.production)
    def production(self):
        self.spawn(self.produit)
        if self.nbIngenieur < 4 :
            self.brain.setState(self.idle)

    def update(self):
        # update BTP here
        self.nbIngenieur = self.countByType(Ingenieur)
        self.brain.update()

class Universite(Entite):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.nbIngenieur = 0
        self.nbTravailleur = 0
        self.produit = Ingenieur
    def idle(self):
        if self.nbIngenieur >= 4 and self.nbTravailleur >= 1:
            self.brain.setState(self.production)
    def production(self):
        self.spawn(self.produit)
        if self.nbIngenieur < 4 or self.nbTravailleur < 1:
            self.brain.setState(self.idle)

    def update(self):
        self.nbIngenieur = self.countByType(Ingenieur)
        self.nbTravailleur = self.countByType(Travailleur)
        self.brain.update()

class IndustrieChimique(Entite):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.nbIngenieur = 0
        self.nbPetrole = 0
        self.produit = Chimie
    def idle(self):
        if self.nbIngenieur >= 4 and self.nbPetrole >= 1:
            self.brain.setState(self.production)
    def production(self):
        self.spawn(self.produit)
        if self.nbIngenieur < 4 or self.nbPetrole < 1:
            self.brain.setState(self.idle)

    def update(self):
        self.nbIngenieur = self.countByType(Ingenieur)
        self.nbTravailleur = self.countByType(Petrole)
        self.brain.update()

class CentraleAtom(Entite):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.nbIngenieur = 0
        self.nbUranium = 0
        self.produit1 = Electricite
        self.produit2 = DechetRadioactif
    def idle(self):
        if self.nbIngenieur >= 2 and self.nbUranium >= 1:
            self.brain.setState(self.production)
    def production(self):
        for i in range(3):
           self.spawn(self.produit1)
        if Robot.cycles%3 == 0 :
           self.spawn(self.produit2)
        if self.nbIngenieur < 2 or self.nbUranium < 1:
           self.brain.setState(self.idle)

    def update(self):
        self.nbIngenieur = self.countByType(Ingenieur)
        self.nbUranium = self.countByType(Uranium)
        self.brain.update()

class CentraleSol(Entite):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.nbIngenieur = 0
        self.produit = Electricite
    def idle(self):
        if self.nbIngenieur >= 1 :
            self.brain.setState(self.production)
    def production(self):
        if Robot.cycles%2 == 0 : self.spawn(self.produit)
        if self.nbIngenieur < 1 :
            self.brain.setState(self.idle)

    def update(self):
        self.nbIngenieur = self.countByType(Ingenieur)
        self.brain.update()

class Electronique(Entite):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.nbIngenieur = 0
        self.nbMetauxPrecieux = 0
        self.produit = Ordinateur
    def idle(self):
        if self.nbIngenieur >= 2 and self.nbMetauxPrecieux >= 2:
            self.brain.setState(self.production)
    def production(self):
        self.spawn(self.produit)
        if self.nbIngenieur < 2 or self.nbMetauxPrecieux < 2:
            self.brain.setState(self.idle)

    def update(self):
        self.nbIngenieur = self.countByType(Ingenieur)
        self.nbTravailleur = self.countByType(MetauxPrecieux)
        self.brain.update()

class Caserne(Entite):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.nbSoldat = 0
        self.nbTravailleur = 0
        self.nbArme = 0
        self.produit = Soldat
    def idle(self):
        if self.nbSoldat >= 2 and self.nbTravailleur >= 1 and self.nbArme >= 1 :
            self.brain.setState(self.production)
    def production(self):
        self.spawn(self.produit)
        if self.nbSoldat < 2 or self.nbTravailleur < 1 or self.nbArme < 1 :
            self.brain.setState(self.idle)

    def update(self):
        self.nbSoldat = self.countByType(Soldat)
        self.nbArme = self.countByType(Arme)
        self.nbTravailleur = self.countByType(Travailleur)
        self.brain.update()

class Megalopole(Entite):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.nbVivant = 0
        self.nbIngenieur = 0
        self.nbBeton = 0
        self.nbAcier = 0
        self.nbOrdinateur = 0
        self.nbMetauxPrecieux = 0
        self.produit = Travailleur

    def idle(self):
        condition_pop = self.nbNourriture >= 1 and self.nbVivant >= 1
        condition_newElectronique = self.nbBeton >= 5 and self.nbMetauxPrecieux >= 2 and self.nbIngenieur >= 2
        condition_newBanque = self.nbBeton >= 5 and self.nbAcier >= 5 and self.nbIngenieur >= 4
        condition_newAssurance = self.nbBeton >= 5 and self.nbOrdinateur >= 3 and self.nbIngenieur >= 4

#il execute les if de manière séquentielle le mec
#c'est le dernier IF VRAI qui a raison
        if condition_pop : self.brain.setState(self.pop)
        if condition_newElectronique : self.brain.setState(self.newElectronique)
        if condition_newBanque : self.brain.setState(self.newBanque)    
        if condition_newAssurance : self.brain.setState(self.newAssurance)    

    def pop(self):
        self.spawn(self.produit)
        if self.nbNourriture <1 or self.nbVivant <1 :
            self.brain.setState(self.idle)
        self.idle()

#alors ce self.idle() c'est un peu chelou mais c'est pour l'aider à sortir de la boucle si jamais
#le client veut fabriquer un truc dans sa ville.

    def newElectronique(self):
        newelectronique = self.spawn(Electronique) 
        for i in range(5):
            self.remove(Beton)
        for z in range(2):
            self.remove(MetauxPrecieux)
        for u in range(2):
            self.remove(Ingenieur)
            self.spawn(Ingenieur, newelectronique.id)

        if self.nbBeton < 5 or self.nbMetauxPrecieux < 2 or self.nbIngenieur < 2 :
            self.brain.setState(self.idle)
            self.save()
        
        self.idle()

    def newBanque(self):
        newbanque = self.spawn(Banque) 
        for i in range(5):
            self.remove(Beton)
        for z in range(5):
            self.remove(Acier)
        for u in range(2):
            self.remove(Ingenieur)
            self.spawn(Ingenieur, newelectronique.id)

        if self.nbBeton < 5 or self.nbMetauxPrecieux < 2 or self.nbIngenieur < 2 :
            self.brain.setState(self.idle)
            self.save()
        
        self.idle()

    def newElectronique(self):
        newelectronique = self.spawn(Electronique) 
        for i in range(5):
            self.remove(Beton)
        for z in range(2):
            self.remove(MetauxPrecieux)
        for u in range(2):
            self.remove(Ingenieur)
            self.spawn(Ingenieur, newelectronique.id)

        if self.nbBeton < 5 or self.nbMetauxPrecieux < 2 or self.nbIngenieur < 2 :
            self.brain.setState(self.idle)
            self.save()
        
        self.idle()

    def update(self):
        # update Ville here
        self.nbTravailleur = self.countByType(Travailleur)
        self.nbNourriture = self.countByType(Nourriture)
        self.nbBeton = self.countByType(Beton)
        self.nbAcier = self.countByType(Acier)
        self.nbMetauxPrecieux = self.countByType(MetauxPrecieux)
        self.nbOrdinateur = self.countByType(Ordinateur)
        self.nbVivant = self.countByType(Vivant)

        self.brain.update()


class MineMetauxPrecieux(Entite):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.nbTravailleur = 0
        self.produit = MetauxPrecieux
    def idle(self):
        if  self.nbTravailleur >= 3 :
            self.brain.setState(self.production)
    def production(self):
        self.spawn(self.produit*2)
        if self.nbTravailleur < 3 :
            self.brain.setState(self.idle)

    def update(self):
        self.nbTravailleur = self.countByType(Travailleur)
        self.brain.update()

class MineMetaux(Entite):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.nbTravailleur = 0
        self.produit = Metaux
    def idle(self):
        if self.nbTravailleur >= 3 :
            self.brain.setState(self.production)
    def production(self):
        self.spawn(self.produit*2)
        if self.nbTravailleur < 3 :
            self.brain.setState(self.idle)

    def update(self):
        self.nbTravailleur = self.countByType(Travailleur)
        self.brain.update()

class MineCharbon(Entite):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.nbTravailleur = 0
        self.produit = Charbon
    def idle(self):
        if  self.nbTravailleur >= 3 :
            self.brain.setState(self.production)
    def production(self):
        self.spawn(self.produit*2)
        if self.nbTravailleur < 3 :
            self.brain.setState(self.idle)

    def update(self):
        self.nbTravailleur = self.countByType(Travailleur)
        self.brain.update()

class MinePetrole(Entite):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.nbTravailleur = 0
        self.produit = Petrole
    def idle(self):
        if  self.nbTravailleur >= 3 :
            self.brain.setState(self.production)
    def production(self):
        self.spawn(self.produit*2)
        if self.nbTravailleur < 3 :
            self.brain.setState(self.idle)

    def update(self):
        self.nbTravailleur = self.countByType(Travailleur)
        self.brain.update()

class MineUranium(Entite):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.nbTravailleur = 0
        self.produit = Uranium
    def idle(self):
        if  self.nbTravailleur >= 3 :
            self.brain.setState(self.production)
    def production(self):
        self.spawn(self.produit*2)
        if self.nbTravailleur < 3 :
            self.brain.setState(self.idle)

    def update(self):
        self.nbTravailleur = self.countByType(Travailleur)
        self.brain.update()

class Champ(Entite):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tracteur = False
        self.ouvrier = False
        self.pesticide = False
        self.nbOuvriers = self.countByType(Travailleur)
        self.aliment = random.choice([Ble, Mais])
        self.rendement = 0
    def idle(self):
        if self.nbOuvriers >= 5:
            self.brain.setState(self.production)
        if self.tracteur and self.ouvrier and self.pesticide:
            self.brain.setState(self.monoculture)
    def production(self):
        self.rendement += 1
        self.spawn(self.aliment)
        if self.nbOuvriers < 5:
            self.brain.setState(self.idle)
        if self.tracteur and self.ouvrier and self.pesticide:
            self.brain.pushState(self.monoculture)

    def monoculture(self):
        for k in range(5):
            self.rendement += 1
            self.spawn(self.aliment)

        if not (self.tracteur and self.ouvrier and self.pesticide):
            self.brain.popState()

    def update(self):
        # update champ here
        self.nbOuvriers = self.countByType(Travailleur)
        self.tracteur = self.ouvrier = self.pesticide = False
        if self.countByType(Tracteur) >= 1:
            self.tracteur = True
        if self.countByType(Chimie) >= 1:
            self.pesticide = True
        if self.countByType(Travailleur) >= 1:
            self.ouvrier = True
        self.brain.update()

class Foret(Entite):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.nbArbres = 0
        self.nbTravailleur = 0
    def idle(self):
        if Robot.cycles%3 == 0: self.spawn(Arbre, self.id)
        if self.nbTravailleur >= 2 and self.nbArbres > 2:
            self.brain.setState(self.production)

    def production(self):
        if self.nbArbres < 2 or self.nbTravailleur < 1:
            self.brain.setState(self.idle)
        else:
            self.spawn(Bois)
            self.remove(Arbre)

    def update(self):
        self.nbTravailleur = self.countByType(Travailleur)
        self.nbArbres = self.countByType(Arbre)
        self.brain.update()

class Bio(Base):
    """
        bio
            - Arbre
            - Bois
            - Coton
            - Lin
            - Sucre
            - Vin
            - Pollinisateur (§)
            - Mouton 
            - Boeuf 
            - Volaille 
            - Porc
            - Anchois  (§)
            - Anguille 
            - Baleine 
            - Carpe 
            - Colin 
            - Hareng 
            - Maquereau 
            - Morue (§)
            - Sardine 
            - Saumon 
            - Thon 
            - Truite 

            Représentation sous forme de fichier

    """
    pass

class Arbre(Bio): pass
class Bois(Bio): pass
class Coton(Bio): pass
class Lin(Bio): pass
class Sucre(Bio): pass
class Vin(Bio): pass
class Pollinisateur(Bio): pass
class Mouton(Bio): pass
class Boeuf(Bio): pass
class Volaille(Bio): pass
class Porc(Bio): pass
class Anchois(Bio): pass
class Anguille(Bio): pass
class Baleine(Bio): pass
class Carpe(Bio): pass
class Colin(Bio): pass
class Hareng(Bio): pass
class Maquereau(Bio): pass
class Morue(Bio): pass
class Sardine(Bio): pass
class Saumon(Bio): pass
class Thon(Bio): pass
class Truite(Bio): pass

class Produit(Base):
    """
    Produits
        - Acier
        - Arme
        - Avion
        - BateauUsine
        - Beton
        - Chimie
        - DechetRadioactif
        - Electricite
        - Fumier
        - Fusee
        - Ordinateur
        - Tracteur
        - Sante
        - Vehicule

    Représentation sous forme de fichier

    """
    pass

class Acier(Produit): pass
class Arme(Produit): pass
class Avion(Produit): pass
class BateauUsine(Produit): pass
class Beton(Produit): pass
class Chimie(Produit): pass
class DechetRadioactif(Produit): pass
class Electricite(Produit): pass
class Fumier(Produit): pass
class Fusee(Produit): pass
class Ordinateur(Produit): pass
class Tracteur(Produit): pass
class Sante(Produit): pass

class Vehicule(Produit): 
    """
        Vehicules
            -VehiculeThermique
            -VehiculeElectrique

    """

    pass

class VehiculeThermique(Vehicule): pass
class VehiculeElectrique(Vehicule): pass

class Fossile(Base):
    """
        Fossiles
            - Petrole
            - Charbon
            - Metaux
            - MetauxPrecieux
            - Uranium

        Représentation sous forme de fichier

    """
    pass

class Bois(Fossile): pass
class Petrole(Fossile): pass
class Charbon(Fossile): pass
class Uranium(Fossile): pass
class Metaux(Fossile): pass
class MetauxPrecieux(Fossile): pass

class Vivant(Base):
    """
        Vivants
            - Travailleur
            - Ingenieur
            - Soldat
        Représentation sous forme de fichier

    """
    pass
class Travailleur(Vivant): pass
class Ingenieur(Vivant): pass
class Soldat(Vivant): pass

class Nourriture(Base): 
    """
        Nourritures
            - Ble
            - Mais
            - Millet
            - Patate
            - Riz
            - Seigle
            - Soja
            - Sorgho
            - Poisson
            - Viande

    """
    pass
class Ble(Nourriture): pass
class Mais(Nourriture): pass
class Millet(Nourriture): pass
class Patate(Nourriture): pass
class Riz(Nourriture): pass
class Seigle(Nourriture): pass
class Soja(Nourriture): pass
class Sorgho(Nourriture): pass
class Poisson(Nourriture): pass
class Viande(Nourriture): pass

robot = Robot()
# Robot(secondes=1)
robot.run()