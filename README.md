Programme pour jouer des tournois d'échec. Installation: Commencez tout d'abord par installer Python. Lancez ensuite la console, placez vous dans le dossier de votre choix puis clonez ce répertoire: git clone https://github.com/ChristopherOC/P4OC.git Placez vous dans le dossier P4OC, puis créez un nouvel environnement virtuel:

python -m venv env

Ensuite, activez-le :

Windows: env\scripts\activate.bat

Linux: source env/bin/activate

Il ne reste plus qu'à installer les packages requis: pip install -r requirements.txt

Vous pouvez ensuite lancer le programme: python main.py

Pour générer le rapport Flake8 Installez flake8 avec la commande: pip intall flake8-html

S'il n'existe pas, créer un fichier setup.cfg Ecrire le texte suivant dedans: [flake8]exclude = .git, env, pycache, .gitignore max-line-length = 119

Tapez la commande: flake8 --format=html --htmldir=flake-report Le rapport sera généré dans le dossier flake8.
