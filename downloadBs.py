import os
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup

def download_files(url, local_path):
    if not os.path.exists(local_path):
        os.makedirs(local_path)
    
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    for link in soup.select("a[href]"):
        href = link.get('href')
        if href.endswith('/'):
            # C'est un sous-dossier, appel récursif pour télécharger son contenu
            download_files(urljoin(url, href), os.path.join(local_path, href))
        else:
            # C'est un fichier, le télécharger
            file_url = urljoin(url, href)
            file_path = os.path.join(local_path, href)
            print(f"Téléchargement de {file_url} vers {file_path}")
            with requests.get(file_url, stream=True) as r:
                with open(file_path, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)

if __name__ == "__main__":
    url = input("Entrez l'URL du répertoire à télécharger: ")
    local_path = input("Entrez le chemin du dossier local pour enregistrer les fichiers: ")
    download_files(url, local_path)
