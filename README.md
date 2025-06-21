# mutual-friends-spark

## Objectifs  
Ce projet utilise Apache Spark pour identifier les amis communs entre utilisateurs à partir d’un fichier listant les utilisateurs et leurs amis.

## Jeu de données  
Le fichier `social_network.txt` contient les utilisateurs et leurs amis au format tabulé :  

ID \t Nom \t Liste_des_IDs_amis_separés_par_virgules

Exemple :  
1 Sidi 2,3,4

Cela signifie que l’utilisateur avec l’ID 1, nommé Sidi, est ami avec les utilisateurs ayant les IDs 2, 3 et 4.

## Étapes d'exécution  

1. Installer Apache Spark si ce n’est pas déjà fait.  
2. Placer le fichier `social_network.txt` dans le dossier du projet.  
3. Lancer la commande suivante pour exécuter le script :  
```bash
spark-submit mutual_friends.py social_network.txt
Résultats

Le script produit une liste des amis communs entre chaque paire d’utilisateurs.

Le format du résultat est :
<ID1><Nom1><ID2><Nom2><Liste_des_amis_communs>
Par exemple :
1<Sidi>3<Ahmed>2,4
indique que Sidi (ID 1) et Ahmed (ID 3) ont en commun les amis ayant les IDs 2 et 4.

Si deux utilisateurs n’ont aucun ami commun, le script affiche "Aucun".

Tests et résultats

    Pour tester le script, vous pouvez créer un fichier test similaire à social_network.txt avec des données d’exemple.

    Les résultats s’affichent directement dans la console ou peuvent être redirigés vers un fichier.
