# TP ROS 2 — Prénom NOM

Module **Initiation Linux · Git · ROS 2 · RViz · Gazebo · MoveIt 2** — Université Évry Paris-Saclay

**Déjà fait :** vous avez installé Linux sur votre machine, ou vous utilisez une VM de l'université, et vous avez suivi les tutos 01 (terminal Linux), 02 (Markdown), 03 (connexion à GitHub) et 04 (premier dépôt Git). Ce dépôt prend la suite : il couvre ROS 2, RViz, l'URDF et MoveIt, à partir du Tuto 05.

**Comment utiliser ce dépôt.** Ce dépôt est à la fois votre **workspace ROS 2** et votre **rendu**. L'énoncé du TP et les tutos sont sur **Ecampus**. Le TP se fait en **5 étapes** (0 à 4), décrites dans la **Feuille de route** en bas de ce fichier. Pour chaque étape :

1. suivez le **tuto** indiqué et faites au moins le palier 🥉 bronze ;
2. **cochez** les cases réalisées dans la Feuille de route (remplacez `[ ]` par `[x]`) ;
3. complétez le fichier `reponses/etapeN.md` correspondant ;
4. enregistrez et envoyez votre travail : `git add`, `git commit`, `git push` ;
5. **validez l'étape** par un tag : `git tag etapeN` puis `git push origin etapeN`.

L'enseignant suit votre avancement grâce aux cases cochées, aux fichiers de réponses et aux tags.

La mise en place (clonage, compilation, vérification, premier tag) se fait en suivant le **Tuto 05**, étapes 8 et 9.

---

## Organisation du dépôt

```text
tp-ros2/
├── README.md              ← ce fichier : votre feuille de route
├── reponses/              ← vos réponses, un fichier par étape
│   └── images/            ← vos captures d'écran
├── src/                   ← vos packages ROS 2
│   └── tp_moveit_py/      ← fourni : MoveItPy pour l'étape 4
└── build/ install/ log/   ← générés par colcon, ignorés par Git
```

## Le cycle de travail

```bash
cd ~/tp-ros2
git pull                                  # en arrivant
source install/setup.bash                 # dans chaque nouveau terminal
# … travailler, puis à chaque étape qui fonctionne :
git add .
git commit -m "Ce que fait cette étape"
git push                                  # avant de partir
```

## Valider une étape

Quand une étape est terminée, après votre dernier `git push` :

```bash
git tag etape1                            # puis etape2, etape3, etape4
git push origin etape1
```

Un simple `git push` **n'envoie pas** les tags : la seconde commande est indispensable.

---

## Feuille de route

C'est ici que vous suivez votre progression : à la fin de chaque étape, cochez ce que vous avez fait, puis poussez ce fichier.

Cochez les cases au fur et à mesure (remplacez `[ ]` par `[x]`) et poussez ce fichier avec le reste.

- 🥉 **Bronze** : le socle, que tout le monde doit atteindre.
- 🥈 **Argent** : pour aller plus loin.
- 🥇 **Or** : un défi pour les plus à l'aise.

### Étape 0 — Mise en place · Tuto 05

- [ ] 🥉 ROS 2 chargé automatiquement, `ROS_DOMAIN_ID` réglé, talker et listener communiquent
- [ ] 🥉 Tous les paquets du TP sont présents (boucle de vérification du Tuto 05)
- [ ] 🥉 Dépôt créé depuis le modèle, enseignant ajouté en collaborateur
- [ ] 🥉 `ros2 launch tp_moveit_py moveit_py.launch.py` affiche `Vérification réussie`
- [ ] 🥉 `reponses/etape0.md` complété, tag `etape0` poussé

### Étape 1 — Découvrir ROS 2 · Tuto 06

- [ ] 🥉 Piloter la tortue au clavier ; lister et observer les nœuds et les topics (`node list`, `topic list`, `topic echo`, `topic info`, `rqt_graph`)
- [ ] 🥈 Publier sur un topic avec `ros2 topic pub`, appeler un service (`/spawn`), lire et changer un paramètre
- [ ] 🥇 Faire dessiner une figure à la tortue uniquement avec des commandes `ros2`
- [ ] Réponses dans `reponses/etape1.md`, tag `etape1` poussé

### Étape 2 — Publish / subscribe · Tuto 07

- [ ] 🥉 Créer le package `mon_package` et le nœud `bavard` ; le compiler, le lancer, l'observer avec les outils `ros2`
- [ ] 🥈 Écrire le nœud abonné `ecouteur` ; faire les modifications guidées du tuto
- [ ] 🥇 Faire communiquer votre nœud avec celui d'un voisin (même `ROS_DOMAIN_ID`), ou ajouter un paramètre ROS à `bavard`
- [ ] Réponses dans `reponses/etape2.md`, tag `etape2` poussé

### Étape 3 — Décrire et voir un robot · Tuto 08

- [ ] 🥉 Package `mini_bras` : décrire le mini-bras en URDF, le vérifier (`check_urdf`), l'afficher dans RViz et le bouger avec les curseurs
- [ ] 🥉 Observer les repères : `tf2_echo`, `view_frames`
- [ ] 🥈 Ajouter un coude et une pince (trois articulations) ; un fichier launch qui démarre tout
- [ ] 🥇 Réécrire la description en xacro
- [ ] Réponses dans `reponses/etape3.md`, tag `etape3` poussé

### Étape 4 — Planifier avec MoveIt · Tutos 09 et 10 (défi : Tuto 11)

- [ ] 🥉 Dans RViz : planifier et exécuter un mouvement du Panda, aller à une pose nommée, ajouter un obstacle et replanifier
- [ ] 🥉 Lancer `sequence.py` : pose nommée, puis pose cartésienne
- [ ] 🥈 Compléter les TODO de `sequence.py` : pince, obstacle, trois poses qui contournent l'obstacle
- [ ] 🥇 Prise et dépose simulée d'un objet (`prise.py`, Tuto 10), **ou** découvrir Gazebo et ros2_control (Tuto 11)
- [ ] Réponses dans `reponses/etape4.md`, tag `etape4` poussé

---

## Lancer mes réalisations

*(À compléter au fil des étapes : les commandes pour lancer vos nœuds et vos launch files.)*

```bash

```
