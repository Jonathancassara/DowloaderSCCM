import os
import requests
from tkinter import Tk, Label, Entry, Button, filedialog

def download_file(url, path):
    response = requests.get(url)
    if response.status_code == 200:
        with open(path, 'wb') as f:
            f.write(response.content)

def browse_folder():
    folder_selected = filedialog.askdirectory()
    folder_path_entry.delete(0, 'end')
    folder_path_entry.insert(0, folder_selected)

def start_download():
    base_url = url_entry.get()
    folder_path = folder_path_entry.get()
    # Ici, ajoutez la logique pour parcourir les fichiers et sous-dossiers de base_url
    # Puis téléchargez-les un par un en utilisant download_file
    # Exemple simplifié pour télécharger un seul fichier:
    # download_path = os.path.join(folder_path, 'nom_de_votre_fichier.ext')
    # download_file(f"{base_url}/chemin/vers/le/fichier", download_path)
    print("Téléchargement terminé")

app = Tk()
app.title("Téléchargeur de fichiers SCCM")

Label(app, text="URL du serveur SCCM:").pack()
url_entry = Entry(app, width=50)
url_entry.pack()

Label(app, text="Chemin de sauvegarde:").pack()
folder_path_entry = Entry(app, width=50)
folder_path_entry.pack()

Button(app, text="Parcourir", command=browse_folder).pack()
Button(app, text="Télécharger", command=start_download).pack()

app.mainloop()
