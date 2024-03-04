import os
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from datetime import datetime

def download_files(url, local_path):
    if not os.path.exists(local_path):
        os.makedirs(local_path)
    
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Erreur lors de l'accès à {url}: Statut {response.status_code}")
        return

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
                if r.status_code == 200:
                    with open(file_path, 'wb') as f:
                        for chunk in r.iter_content(chunk_size=8192):
                            f.write(chunk)
                else:
                    print(f"Erreur lors du téléchargement de {file_url}: Statut {r.status_code}")

if __name__ == "__main__":
    url = input("Entrez l'URL du répertoire à télécharger: ")
    
    # Création du chemin basé sur la date du jour
    date_str = datetime.now().strftime("%Y-%m-%d")
    local_path = os.path.join("C:/Temp", date_str)
    
    download_files(url, local_path)
