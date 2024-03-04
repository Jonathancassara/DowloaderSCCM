import tkinter as tk
from tkinter import filedialog
import requests

def download_files(url, destination_folder):
    """Télécharge les fichiers et les sous-dossiers d'une URL SCCM."""

    # En-tête HTTP pour simuler un navigateur web
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36"
    }

    # Requête GET pour obtenir le contenu du dossier
    response = requests.get(url, headers=headers)

    # Si la requête est réussie
    if response.status_code == 200:

        # Création du dossier de destination
        if not os.path.exists(destination_folder):
            os.makedirs(destination_folder)

        # Analyse du contenu HTML
        soup = BeautifulSoup(response.content, "html.parser")

        # Parcours des liens
        for link in soup.find_all("a"):

            # Obtention du nom du fichier ou du dossier
            name = link.text

            # Si c'est un dossier
            if link.has_attr("href") and link["href"].endswith("/"):

                # Téléchargement du dossier
                download_files(url + link["href"], os.path.join(destination_folder, name))

            # Si c'est un fichier
            else:

                # Téléchargement du fichier
                file_url = url + link["href"]
                with requests.get(file_url, headers=headers, stream=True) as r:
                    with open(os.path.join(destination_folder, name), "wb") as f:
                        for chunk in r.iter_content(chunk_size=8192):
                            f.write(chunk)

    else:
        print(f"Échec de la requête : {response.status_code}")


def main():
    # Création de la fenêtre
    window = tk.Tk()
    window.title("Téléchargement de fichiers SCCM")

    # Définition des variables
    url_var = tk.StringVar()
    destination_folder_var = tk.StringVar()

    # Fonction pour lancer le téléchargement
    def download():
        url = url_var.get()
        destination_folder = destination_folder_var.get()

        if not url or not destination_folder:
            print("Veuillez renseigner tous les champs.")
            return

        # Début du téléchargement
        download_files(url, destination_folder)

        # Affichage d'un message de confirmation
        tk.messagebox.showinfo("Téléchargement terminé", "Les fichiers ont été téléchargés avec succès.")

    # Champ pour l'URL
    url_label = tk.Label(text="URL du dossier SCCM :")
    url_entry = tk.Entry(textvariable=url_var)

    # Champ pour le dossier de destination
    destination_folder_label = tk.Label(text="Dossier de destination :")
    destination_folder_entry = tk.Entry(textvariable=destination_folder_var)

    # Bouton de sélection du dossier
    browse_button = tk.Button(text="Parcourir...", command=lambda: destination_folder_var.set(filedialog.askdirectory()))

    # Bouton de téléchargement
    download_button = tk.Button(text="Télécharger", command=download)

    # Disposition des widgets
    url_label.pack()
    url_entry.pack()
    destination_folder_label.pack()
    destination_folder_entry.pack()
    browse_button.pack()
    download_button.pack()

    # Lancement de la boucle principale
    window.mainloop()


if __name__ == "__main__":
    main()
