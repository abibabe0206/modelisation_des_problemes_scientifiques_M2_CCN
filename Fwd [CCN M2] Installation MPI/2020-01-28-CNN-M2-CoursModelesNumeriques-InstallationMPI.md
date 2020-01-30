# Installation de l'image Docker MPI

Ce document décrit l'installation de l'image docker pour le module CNN
M2. L'installation se base sur le travail publié sur le site github suivant :
    https://github.com/dispel4py/docker.openmpi


## Installation de docker et de docker-compose

Nous nous basons sur les installations standard de ces outils sur une
ubuntu 18.04 LTS :

```bash
    sudo apt install docker.io docker-compose
```

Le système installé n'est pas la dernière version mais est suffisant
pour les travaux à mener.

## Installation des outils

Les outils sont à récupérer sur le github. Pensez à vous mettre dans
un répertoire propre.

```bash
    git clone https://github.com/dispel4py/docker.openmpi.git
    cd docker.openmpi
```

## Récupération de l'image docker, et construction

L'image peut être reconstruite à partir du fichier Dockerfile (non
traité dans ce document), récupéré des serveurs Docker.io, ou récupéré
sur serveur ArchieFrog.

* A partir du serveur ArchieFrog nous pouvons au préalable télécharger
l'image, puis l'intégrer à la BD de docker.

```bash
    wget -i http://10.42.1.1/docker.openmpi/dispel4py.docker.openmpi.docker
    docker image load -i ./dispel4py.docker.openmpi.docker
```
* La récupération à partir des serveurs de docker.io est faite
automatiquement si l'opération précédente a échouée.  Nous avons
à ce stade à appeler la construction des images par docker-compose.

```bash
    sudo docker-compose up -d
```

## Création des instances MPI

Les instances MPI sont créées à nouveau avec docker-compose:

```bash
    sudo docker-compose scale mpi_node=4 mpi_head=1
```

A ce stade, nous avons plusieurs instances MPI qui tournent avec
docker. Pour visualiser ces instances, saisir:

```bash
    sudo docker ps
```


Les instances ont été allouées sur un pont réseau (bridge). Les
réseaux peuvent être listés, et vérifiés:

```bash
    sudo docker network list
    sudo docker network inspect bridge
```

Il faut vérifier l'addresse IP des noeuds qui ont été créés. Nous
allons désormais considérer que les adresses sont les suivantes
(sortie partielle):

        "Containers": {
            "00a5783e39ece58db8b416f77af5d4c1dced0f806ad149b632ac301b99b98cfc": {
                "Name": "dockeropenmpi_mpi_node_3",
                "IPv4Address": "172.17.0.3/16",
            },
            "3957bc0531833c190ef56694c3ee6d4e2cac501ce6a103685ef66ace903b798c": {
                "Name": "dockeropenmpi_mpi_node_1",
                "IPv4Address": "172.17.0.5/16",
            },
            "b6988a5e9c96d686c07b582bf5ee8c30b6ce1b0cb1e98545df91f63c0b71e68b": {
                "Name": "dockeropenmpi_mpi_node_4",
                "IPv4Address": "172.17.0.2/16",
            },
            "e100f9393570678f78eed46b28202c7dd09fd7987004b44b5fcf537212306d81": {
                "Name": "dockeropenmpi_mpi_node_2",
                "IPv4Address": "172.17.0.4/16",
            },
            "f7b7fdc6626fa089a2a9fd8c5853017c6ba1f506da63037290c7c748506c8e3d": {
                "Name": "dockeropenmpi_mpi_head_1",
                "IPv4Address": "172.17.0.6/16",
            }
        },

Soit :
    172.17.0.6		dockeropenmpi_mpi_head_1 
    172.17.0.5		dockeropenmpi_mpi_node_1
    172.17.0.4		dockeropenmpi_mpi_node_2
    172.17.0.3		dockeropenmpi_mpi_node_3
    172.17.0.2		dockeropenmpi_mpi_node_4

## Connexion sur les noeuds.

Pour se connecter sur les noeuds, nous devons utiliser une clé SSH qui
est présente dans le répertoire ssh: "./ssh/id_rsa.mpi":

```bash
    ls ssh/id_rsa.mpi
```

La connexion se fait en spécifiant le nom et la clé. Vérifier que la
connexion a bien lieu :

```bash
    ssh -i ssh/id_rsa.mpi tutorial@172.17.0.6
```

A partir de maintenant, les commandes "bash" avec la mention
"tutorial@172.17.0.6" doivent se faire sur la machine en question (il
faut donc se connecter avant).

## Configuration de MPI.

La configuration du cluster de machine se fait en créant un fichier
listant les noeuds. Ce fichier doit être installé sur la machine
"head". Vous pouvez le générer de la façon suivante:

* Sur tutorial@172.17.0.6

```bash 
    cat > machines << EOF
    172.17.0.2 slots=1 max_slots=1
    172.17.0.3 slots=1 max_slots=1
    172.17.0.4 slots=1 max_slots=1
    172.17.0.5 slots=1 max_slots=1
    EOF
```

Ou éditer le fichier équivalent sur la machine hôte et le transférer.

```bash
    nano machines # remplir le fichier machine
    scp -i ssh/id_rsa.mpi machines tutorial@172.17.0.6:machines
```

## Exécution de MPI

A ce stade, sur la machine "head" vous pouvez tester si l'exécution en
parallèle se fait correctement.

* Sur tutorial@172.17.0.6

```bash
    mpiexec -hostfile machines -n 4 hostname
```

Afin de résoudre un problème d'affichage, je vous propose de filtrer
la sortie de la commande en ajoutant cet alias. En même temps, vous
pouvez installer les outils d'affichage graphique :

* Sur tutorial@172.17.0.6

```bash
    echo "alias mpiexec='mpiexec  2> >(grep -v mount) '" > .bash_aliases
    . .bash_aliases
    sudo apt install x11-apps
    export DISPLAY=:0.0
```

Relancer l'exécution afin de vérifier si le filtre est en place :

* Sur tutorial@172.17.0.6

```bash
    mpiexec -hostfile machines -n 4 hostname
```

## Exécution d'un code Python

Le développement d'un code python se fera sur la machine hôte. Les
fichiers développés doivent être copiés sur chacune des machines
appartenant au cluster.

Nous faisons l'hypothèse qu'un code python a été développé dans le fichier "testmpi.py" :

```python
    from mpi4py import MPI

    comm= MPI.COMM_WORLD
    rank= comm.Get_rank()
    size= comm.Get_size()

    print("rank=%d size=%d" % (rank, size))
```

Pour effectuer la copie :
```bash
    for node in 172.17.0.{2..5}; do scp -i ssh/id_rsa.mpi testmpi.py tutorial@${node}: ; done
```

Puis exécuter la commande sur la machine "head" (ssh -i ssh/id_rsa.mpi tutorial@172.17.0.6)

* Sur tutorial@172.17.0.6

```bash
     mpiexec -hostfile machines -n 4 python testmpi.py
```
