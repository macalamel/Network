#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 13 15:45:53 2024

@author: m.calamel
"""

#10.12.217.148

import socket,os,sys,time,random,csv
import threading

class Client:
    def __init__(self,ip_adresse:str="localhost",port:int=55028)->None:
        if self.verifie_variable_type(ip_adresse,str):
            self.ip_adresse=ip_adresse
        if self.verifie_variable_type(port,int):
            self.port=port
        self.client_socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.is_connected=False
    def verifie_variable_type(self,variable,_type:object)->bool:
        """
        vérifie le type de la variable
        """
        return type(variable)==_type
    
    def connect_to_server(self)->None:
        """
        fonction pour essayer de se connecter au serveur
        """
        try:
            self.client_socket.connect((self.ip_adresse, self.port))
            print("Serveur connecté")
        except socket.error:
            print("liaison échouée")
            sys.exit()
    
    def send_message(self,msg:str)->None:
        """
        fonction pour l'envoie des message 
        """
        try:
            self.client_socket.send(msg.encode("Utf8"))
        except:
            print("socket error")
    
    def receive_message(self)->str:
        """
        fonction pour la reception des message 
        """
        try:
            message=self.client_socket.recv(1024).decode("Utf8")
            return message
        except:
            print("Serveur Déconnecté")
            self.is_connected=False

        
    
    def stop_connection(self)->None:
        """
        fonction pour fermer la connexion avec le serveur
        """
        self.client_socket.close()
        self.is_connected=False
    
    def run(self)->None:
        """
        fonction principale du client
        """
        self.connect_to_server()
        self.is_connected=True
        
class Messagerie:
    def __init__(self):
        self.client=Client()
        self.is_running=True
        self.key_vigenere=""
        self.conversation=[]
        self.tunnel=False
    def send_message(self)->None:
        """
        fonction principal pour l'envoie des messages
        """

        while self.client.is_connected:
            msg=input()
            self.add_to_conv(msg)
            if msg=="exit":
                print("exiting...")
                time.sleep(1)
                self.is_running=False
                self.client.stop_connection()
                sys.exit()
            if self.tunnel:
                msg=Cryptographie().vigenaire(msg,self.key_vigenere,0)
            self.affichage()
            self.client.send_message(msg)
            
                
    def receive_message(self)->None:
        """
        fonction principal pour recevoir les message et traiter les différentes commandes spéciales
        """
        while self.is_running:
            if not self.is_running:
                break
            try:
                message=self.client.receive_message()
            except:
                sys.exit()
            if self.tunnel:
                try:
                    message=Cryptographie().vigenaire(message,self.key_vigenere,1)
                except:
                    sys.exit()
            if message=="exit":
                self.is_running=False
                self.client.stop_connection()
                print("fin de la connection appuyez sur enter...")
            elif message=="!tunnel":
                print("tunneling")
                self.client.send_message("!tunnel")
                self.security_protocole()
                self.set_tunnel()
            elif self.client.is_connected:
                self.add_to_conv("<-- "+message)
                self.affichage()
            else:
                break
    def set_tunnel(self)->None:
        """
        protocole pour établir un tunnel de connection privée
        """
        key=self.client.receive_message()
        key=Cryptographie().vigenaire(key,self.key_vigenere,1)
        self.key_vigenere=key
        key=""
        self.tunnel=True
        print("tunnel [OK]")


    def security_protocole(self)->None:
        """
        fonction pour établir une connection sécurisée
        """
        
        #  generation de la clef Vigenère 

        key=Cryptographie().generate_key(100)
        new_key=Cryptographie().seg(key)

        #  mise en place de la clef publique rsa

        rsa_key=self.client.receive_message()
        rsa_key=list(rsa_key[:].split(','))
        for i in range(len(rsa_key)):
            rsa_key[i]=int(rsa_key[i])
        #  encodage de la clef
        
        new_key=Cryptographie().RSA(rsa_key,new_key)
        new_key=str(new_key)
        self.client.send_message(new_key)

        self.key_vigenere=key

    def affichage(self)->None:
        os.system('cls')
        print(" __    __              __                                        __       ")
        print("/  \\  /  |            /  |                                      /  |      ")
        print("$$  \\ $$ |  ______   _$$ |_    __   __   __   ______    ______  $$ |   __ ")
        print("$$$  \\$$ | /      \\ / $$   |  /  | /  | /  | /      \\  /      \\ $$ |  /  |")
        print("$$$$  $$ |/$$$$$$  |$$$$$$/   $$ | $$ | $$ |/$$$$$$  |/$$$$$$  |$$ |_/$$/ ")
        print("$$ $$ $$ |$$    $$ |  $$ | __ $$ | $$ | $$ |$$ |  $$ |$$ |  $$/ $$   $$<  ")
        print("$$ |$$$$ |$$$$$$$$/   $$ |/  |$$ \\_$$ \\_$$ |$$ \\__$$ |$$ |      $$$$$$  \\ ")
        print("$$ | $$$ |$$       |  $$  $$/ $$   $$   $$/ $$    $$/ $$ |      $$ | $$  |")
        print("$$/   $$/  $$$$$$$/    $$$$/   $$$$$/$$$$/   $$$$$$/  $$/       $$/   $$/\n\n")
        print("============================================================================")
        for i in self.conversation:
            print(i)
    
    def add_to_conv(self,msg:str)->None:
        """
        fonction pour géré l'affichage
        """
        if len(self.conversation)<10:
            self.conversation.append(msg)
        else:
            self.conversation=self.conversation[1:]+[msg,]

    def connect_protocole(self)->None:
        """
        protocole d’authentification
        """

        self.connected=False
        
        while not self.connected:
            choix=""
            while choix!="1" and choix!="2":
                self.add_to_conv("[ 1 ] Ancien compte\n[ 2 ] Nouveau compte\n")
                self.affichage()
                choix=input(">>> ")
            user=input("Username : ")
            password=input("Password : ")
            msg=Cryptographie().vigenaire(choix+","+user+","+password,self.key_vigenere,0)
            self.client.send_message(msg)
            reponse=Cryptographie().vigenaire(self.client.receive_message(),self.key_vigenere,1).split(",")
            self.add_to_conv(reponse[1])
            self.connected=reponse[0]=="True"
    

    def run(self)->None:
        """
        fonction principale de la messagerie
        """
        self.client.run()
        time.sleep(1)
        self.security_protocole()
        self.connect_protocole()
        thread_send=threading.Thread(target=self.send_message)
        thread_receive=threading.Thread(target=self.receive_message)
        thread_send.start()
        time.sleep(1)
        thread_receive.start()


class Cryptographie:
    def __init__(self):
        self.alpha="azertyuiopqsdfghjklmwxcvbn,;:&é'(-è_çà)=12345678#~{[|`^@]90°+?./§AZERTYUIOPQSDFGHJKLMWXCVBN!"
        self.dico_lettre_to_nombre={self.alpha[i]:100+i for i in range(len(self.alpha))}
        self.dico_nombre_to_lettre={v:k for k,v in self.dico_lettre_to_nombre.items()}
    def generate_key(self,long)->str:
        """
        generation d'une clef vigenere, long permet de contrôler la longueur de la clef 
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
        """
        segmente le message en block de 6 chiffre
        """

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
        """
        passe de block de 6 chiffre a un str
        """
        res=""
        for i in msg:
            x=str(i)
            for j in range(0,len(x),3):
                res+=self.dico_nombre_to_lettre[int(x[j:j+3])]
        return res
    def RSA(self,clef:tuple,msg:list)->list:
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
