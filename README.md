# Objectifs
Valider que la stack telco emet et detecte des informations cohérentes de la part du module
# Partie émission
Valider le format des trames envoyées :
- Nom des commandes
- séparateur
- valeur des variables

# Partie réception
Valider la bonne lecture des données transmises par le modem :
- Détection de la commande
- lecture des paramètres
- lecture des envois asynchrones

# Organisation
Il existe plusieurs type de commande à envoyer : 
- Sans argument
- Avec argument

Et plusieurs type de réponse : 
- Simple (OK,ERROR)
- Avec argument
- asynchrone
## Partie émission (format des commandes)
Un fichier contenant les commandes valides est disponible. Pour chaque commande envoyée, on s'assure que la commande qui sera transmise sur le port série est correcte
## Partie réception
Un fichier dump de commande est disponible. Il contient les réponses du modem à une succession de commande définie. On s'assure que l'information réponse reçue ainsi que la valeur des paramètre est correcte
Pour les commandes avec argument, il faut s'assurer que la lecture est correcte
## Partie échange
un mock de modem répond à des commandes prédéfinies. On s'assure que le système est capable de lire le retour du mock et d'extraire les données.
Il faut donc définir un scénario et valider que le code répond bien aux exigences. Les scénarios peuvent être les suivants : 
- ping communication (AT) :
  - Reponse
  - pas de réponse
- configuration du modem
  - succes
  - pas de réponse
  - erreur
- test de connexion au réseau
  - timeout (reboot)
  - connexion réussi
  - connexion échouée

# developpement
* On commencera par le cas le plus simple : format des commandes envoyées 
* On ajoutera ensuite la lecture d'une réponse
* Enfin on realisera un scénario simple (paramétrage par exemple)
* Et on réalisera le parseur pour chaque commande complexe
