back-end :
Initialisation :
python3 -m venv venv
source venv/bin/activate

ou

py -m venv venv
venv\Scripts\activate

pip install fastapi uvicorn
python -m uvicorn app.main:app --reload (Lancement du projet)

front-end :
ionic start [nom du projet] (Pour créer le projet)
ionic serve (Pour lancer le serveur)
ionic capacitor add [nom plateform : ios/android] (Pour ajouter la version mobile mais nécssite une version de Node à 22 minimum)