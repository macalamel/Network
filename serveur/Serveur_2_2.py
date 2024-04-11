import socket,sys,csv,os,time
import threading
from hashlib import sha256
import random

class Serveur:
    
    def __init__(self,ip_adresse:str="localhost",port:int=55028) -> None:
        self.ip_adresse=ip_adresse
        self.port=port
        self.server_socket=self.set_server_socket()
    def set_server_socket(self)->socket.socket:
        """
        Met en place le socket pour la communication
        """
        return socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    def run(self)->None:
        """
        lance le serveur si tout est bon sinon sort du programme
        """
        try:
            self.server_socket.bind((self.ip_adresse,self.port))
        except:
            print("liaison échoué")
            sys.exit()
        print("Serveur Prêt ,en attente de requête... ")
        self.server_socket.listen(5)

class Fichier:
    def __init__(self,file):
        self.file=file
    def check_file(self,file:str)->bool:
        """
        Fonction pour vérifier que le fichier est bien existant
        """
        try:
            file_data=open(file)
            file_data.close()
            return True
        except FileNotFoundError:
            print("le fichier n'existe pas")
            return False
    def read(self)->dict:
        """
        renvoi les données du fichier spécifier après avoir vérifier sont existence
        """
        if self.check_file(self.file):
            file=open(self.file,"r")
            content= csv.reader(file,delimiter=';')
            data={}
            for ligne in content:
                data[ligne[0]]=ligne[1]
            file.close()
            return data
    def write_file(self,content:str) -> None:
        """
        Remplace le texte d'un fichier par celui du paramètre content
        """
        if self.check_file(self.file):
            file=open(file,"w")
            file.write(content)
            file.close()
    def add_to_file(self,content:str)->None:
        """
        Ajoute le texte content à la fin du fichier
        """
        if self.check_file(self.file):
            file=open(self.file,"a")
            file.write(content)
            file.close()


class Authentification:
    def __init__(self,username:str,password:str) -> None:
        self.username=username
        self.password=password
        self.user_file=".\\fichier\\compte.txt"
    def connect(self)->tuple:
        """
        vérifie si la combinaison mot de passe, nom d'utilisateur est la bonne
        """
        user=Fichier(self.user_file).read()
        if self.username in user.keys():
            verif=user[self.username]==sha256(self.password.encode('utf-8')).hexdigest()
            self.username=""
            self.password=""
            if verif:
                return(verif,"Mot de passe bon")
            else:
                return (verif,"Mot de passe faux")
        else:
            self.username=""
            self.password=""
            return (False,"Utilisateur Non existant")
    def add_new_user(self)->tuple:
        """
        ajoute un utilisateur dans la base si il n'existe pas déjà
        """
        user=Fichier(self.user_file).read().keys()
        if self.username not in user:
            Fichier(self.user_file).add_to_file("\n"+self.username+";"+sha256(self.password.encode('utf-8')).hexdigest())
            self.username=""
            self.password=""
            return (True,"Utilisateur ajouté")
        self.username=""
        self.password=""
        return (False,"Utilisateur déjà existant")
        


class Client(threading.Thread):
    def __init__(self,connection_name:socket,messagerie) -> None:
        threading.Thread.__init__(self)
        self.connection_name=connection_name
        self.messagerie=messagerie
        self.user=None
        self.key_vigenere=""
        self.user_tunnel=[]
        self.tunnel=False
    def security_protocole(self)->None:
        """
        protocole pour établir une connection sécurisé
        """
        
        # Definition et envoie de la clef
        n,x,y=Cryptographie().generate_RSA("fichier\\nb_premiers.txt") #generation de la clef
        message=str(n)+","+str(x)
        self.connection_name.send(message.encode('Utf8'))   #on envoie la clef publique
        
        # Reception et décodage de la clef Vigenère
        key_vig=self.connection_name.recv(1024).decode("Utf8")
        key_vig=list(key_vig[1:-1].split(', '))
        key_vig=[int(i) for i in key_vig]

        # Mise en place de la clef
        key_vig=Cryptographie().RSA([n,y],key_vig)
        self.key_vigenere=Cryptographie().deseg(key_vig)

        

    def connect_protocole(self)->None:
        """
        protocole de connection avec authentification:\n
        1- le serveur écoute la requête sous la forme (mode,user,pass)\n
        2- le serveur traite l'information (code bon, utilisateur non existant,...)\n
        3- le serveur envoie l'information sous la forme (Bool, msg)
        """
        user_connect=False
        while not user_connect:
            request=Cryptographie().vigenaire(self.connection_name.recv(1024).decode("Utf8"),self.key_vigenere,1)
            request=request.split(",")
            if request[1] in self.messagerie.user.keys():
                msg=Cryptographie().vigenaire("False,utilisateur déjà connecté",self.key_vigenere,0)
                self.connection_name.send(msg.encode("Utf8"))
            elif request[0]=="1":
                auth=Authentification(request[1],request[2]).connect()
                if auth[0]:
                    self.user=request[1]
                    user_connect=True
                    self.messagerie.user[self.user]=self
                msg=Cryptographie().vigenaire(str(auth[0])+","+auth[1],self.key_vigenere,0)
                self.connection_name.send(msg.encode("Utf8"))

            elif request[0]=="2":
                add_use=Authentification(request[1],request[2]).add_new_user()
                if add_use[0]:
                    self.user=request[1]
                    user_connect=True
                    self.messagerie.user[self.user]=self
                msg=Cryptographie().vigenaire(str(add_use[0])+","+add_use[1],self.key_vigenere,0)
                self.connection_name.send(msg.encode("Utf8"))
        # message pour avertir tous les utilisateur que le client vient de se connecter 
        msg=self.user+" joined"
        for i in self.messagerie.client:
            if not i.connection_name==self.connection_name:
                i.connection_name.send(msg.encode("Utf8"))

    def tunnel_protocole(self,username:list)->None:
        """
        fonction pour établir une connection privé
        """
        for i in username:
            if i in self.messagerie.user.keys():
                self.user_tunnel.append(self.messagerie.user[i])
        
        for i in self.user_tunnel:
            i.connection_name.send("!tunnel".encode("Utf8"))
        
        time.sleep(5)

        key=Cryptographie().generate_key(100)

        for i in self.user_tunnel:
            msg=Cryptographie().vigenaire(key,i.key_vigenere,0)
            i.connection_name.send(msg.encode("Utf8"))
        
        self.tunnel=True
        key=""

    def run(self)->None:
        """
        fonction principal pour chaque clients.
        """
        self.security_protocole()
        self.connect_protocole()
        while True:
            try:
                msg=self.connection_name.recv(1024).decode("Utf8")
            except:
                break
            if msg=="exit":
                break
            elif msg=="! list user":
                msg=str(list(self.messagerie.user.keys()))
                self.connection_name.send(msg.encode("Utf8"))
            elif "!make tunnel" in msg:
                user=msg.split(",")[1:]
                thread_tunnel=threading.Thread(target=self.tunnel_protocole,args=(user,))
                thread_tunnel.start()
            elif msg=="!tunnel":
                time.sleep(2)
                self.security_protocole()
            # print(msg)
            else:
                # if self.tunnel:
                #     for i in self.user_tunnel:
                #         if not i.connection_name==self.connection_name:
                #             i.connection_name.send(msg.encode("Utf8"))
                # else:
                
                for i in self.messagerie.client:
                    if not i.connection_name==self.connection_name:
                        i.connection_name.send(msg.encode("Utf8"))
        
        # protocole de déconnexion
        msg=self.user+" left"
        for i in self.messagerie.client:
            if not i.connection_name==self.connection_name:
                i.connection_name.send(msg.encode("Utf8"))
        self.connection_name.close()
        self.messagerie.client.remove(self)
        del self.messagerie.user[self.user]
        print("Client déconnecté...")
        self.messagerie.show_state()

class Messagerie:
    def __init__(self):
        self.serveur=Serveur()
        self.is_running=True
        self.client=[]
        self.user={}
    
    def show_state(self)->None:
        """
        fonction pour montrer l'état du serveur
        """
        os.system("cls")
        print("=================================")
        print(f"client connecté :         {len(self.client)}")
        print(f"les thread on été lancé : {self.is_lunched}")
        print(f"le serveur fonctionne:    {self.is_running}")
        print("=================================")
    

    def run(self)->None:
        """
        fonction principal pour le serveur
        """
        self.serveur.run()
        self.is_connected=False
        self.is_lunched=False
        # thread_stop=threading.Thread(target=self.exit)
        # thread_stop.start()
        while self.is_running:
            connection_name,adresse_info=self.serveur.server_socket.accept()
            self.client.append(Client(connection_name,self))
            print(f"Client connecté, adresse IP {adresse_info[0]}, port {adresse_info[1]}")
            self.is_connected=True
            self.is_lunched=False
            if not self.is_lunched:
                self.client[-1].start()
                self.is_lunched=True
                self.show_state()
        sys.exit()

class Cryptographie:
    def __init__(self):
        self.alpha="azertyuiopqsdfghjklmwxcvbn,;:&é'(-è_çà)=12345678#~{[|`^@]90°+?./§AZERTYUIOPQSDFGHJKLMWXCVBN!"
        self.dico_lettre_to_nombre={self.alpha[i]:100+i for i in range(len(self.alpha))}
        self.dico_nombre_to_lettre={v:k for k,v in self.dico_lettre_to_nombre.items()}
    def generate_key(self,long:int)->str:
        """
        generation de clef vigenere
        """
        key=""
        for i in range(long):
            key+=self.alpha[random.randint(0,len(self.alpha)-1)]
        return key
    
    def vigenaire(self,msg:str,clef:str,sens:int)->str:
        """
        sens peut prendre la valeur 0 pour coder et 1 pour décoder
        """
        text=""
        if sens==0:
            for i in range(len(msg)):
                if msg[i]!=" ":
                    text+=self.alpha[(self.alpha.index(msg[i])+self.alpha.index(clef[i%len(clef)]))%len(self.alpha)]
                else:
                    text+=" "
        elif sens==1:
            for i in range(len(msg)):
                if msg[i]!=" ":
                    text+=self.alpha[(self.alpha.index(msg[i])-self.alpha.index(clef[i%len(clef)]))%len(self.alpha)]
                else:
                    text+=" "
        return text
    def dec(self,N:int)->list:
        """
        fonction pour décomposer le nombre N en produit de facteur premier
        """
        Resultat=[]
        d=2
        while N%d==0:
            Resultat.append(d)
            q=int(N/d)
            N=q
        d=3
        while d<=N**0.5:
            while N%d==0:
                Resultat.append(d)
                q=int(N/d)
                N=q
            d+=2
        return Resultat
    def seg(self,msg:str)->list:
        res=[]
        for i in range(0,len(msg),2):
            res.append(msg[i:i+2])
        segmented=[]
        for i in range(len(res)):
            segmented.append(int("".join([str(self.dico_lettre_to_nombre[list(res)[i][j]]) for j in range(len(res[i]))])))
        return(segmented)
    
    def generate_RSA(self,path:str)->list:
        """
        fonction pour générer un paire de clef RSA la clef sous la forme
        (n,x,y) avec pour clef publique (n,x) et pour clef privé (n,y)
        """
        a=open(path)
        f= csv.reader(a,delimiter=',')
        nb_prem=[]
        for line in f:
            for el in line:
                nb_prem.append(el)
        a.close()
        choix=True
        while choix:
            choix=False
            try:
                p=int(nb_prem[random.randint(0,len(nb_prem)-1)])
                q=int(nb_prem[random.randint(0,len(nb_prem)-1)])
                n=p*q
                phi=(p-1)*(q-1)
                e=max(self.dec(phi))
                nb=e*phi+1
                x=self.dec(nb)
                if len(x)!=1:
                    l=len(x)//2
                    res=1
                    for i in range(l):
                        res*=max(x)
                        x.remove(max(x))
                else:
                    res=max(x)
                x=res
                y=nb//x
                #print('n=',n,'e=',x,'d=',y)
            except:
                choix=False
            if x<40000 or y<40000:
                choix=True
        return [n,x,y]
    def deseg(self,msg:str)->str:
        res=""
        for i in msg:
            x=str(i)
            for j in range(0,len(x),3):
                res+=self.dico_nombre_to_lettre[int(x[j:j+3])]
        return res
    def RSA(self,clef:list,msg:list)->list:
        """
        fonction pour coder un message (list[int])
        la clef a la forme (n,y)
        """
        a=[]
        for i in range(len(msg)):
            x=msg[i]
            p=clef[0]
            y=clef[1]
            res=1
            while y>0:
                if (y & 1)!=0:
                    res=res*x%p
                y=y>>1
                x=(x*x)%p
            a.append(res)
            # print(i,"/50",end='\r')
        return a
