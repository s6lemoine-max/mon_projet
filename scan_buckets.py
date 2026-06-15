import os
from pathlib import Path
from tabulate import tabulate
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

# Définir le dossier à scanner
folder_path = "."

# Lister tous les dossiers (sauf .git)
folders = [f for f in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, f)) and f != '.git']

# Pour chaque dossier, compter les fichiers et calculer la taille
results = []
for folder in folders:
    folder_full_path = os.path.join(folder_path, folder)
    files = [f for f in os.listdir(folder_full_path) if os.path.isfile(os.path.join(folder_full_path, f))]
    nb_files = len(files)
    
    # Calculer la taille totale du dossier
    total_size = 0
    for file in files:
        file_path = os.path.join(folder_full_path, file)
        total_size += os.path.getsize(file_path)
    
    results.append([folder, nb_files, f"{total_size} bytes"])

# Afficher le tableau
headers = ["Dossier", "Nombre de fichiers", "Taille"]
tableau = tabulate(results, headers=headers, tablefmt="grid")
print(tableau)

# Sauvegarder le tableau dans un fichier
with open("rapport.txt", "w") as f:
    f.write(tableau)

# Envoyer le mail
sender_email = "s6.lemoine@gmail.com"  # À remplacer
sender_password = "lobb mewt toim qgbz"  # Le mot de passe qu'on vient de générer
receiver_email = "s6.lemoine@gmail.com"  # À remplacer

# Créer le message
msg = MIMEMultipart()
msg['From'] = sender_email
msg['To'] = receiver_email
msg['Subject'] = "Rapport de scan des buckets"

# Body du mail
body = "Voici le rapport de scan des buckets en pièce jointe."
msg.attach(MIMEText(body, 'plain'))

# Ajouter le fichier en pièce jointe
with open("rapport.txt", "rb") as attachment:
    part = MIMEBase("application", "octet-stream")
    part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header("Content-Disposition", f"attachment; filename= {'rapport.txt'}")
    msg.attach(part)

# Envoyer le mail
try:
    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.login(sender_email, sender_password)
    server.send_message(msg)
    server.quit()
    print("Mail envoyé avec succès !")
except Exception as e:
    print(f"Erreur : {e}")
