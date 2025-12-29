# 🚀 Installation & Lancement du Projet

Ce guide explique clairement comment installer toutes les dépendances nécessaires (Node, NVM, Bun) et lancer le projet sur Windows.

---

# 📌 1. Installation de l’environnement

## ✅ 1.1 Installer NVM pour Windows (Si n'est pas installer)

Téléchargez NVM :

👉 https://github.com/coreybutler/nvm-windows/releases

Téléchargez le fichier :

📌 **nvm-setup.exe**

Puis installez-le avec les paramètres par défaut :
- `C:\Program Files\nvm`
- `C:\Program Files\nodejs`

---

## ✅ 1.2 Installer Node.js 20

Ouvrez un nouveau terminal PowerShell :

```powershell
nvm install 20
nvm use 20
```
Vérifiez
```
node -v
npm -v
```
# 📌 2. Installer Bun (Windows)
```
powershell -c "irm bun.sh/install.ps1 | iex"
```
# 📌 3. Ajouter Bun au PATH Windows

Tapez Variables d’environnement dans le menu Démarrer

Cliquez Modifier les variables d’environnement pour votre compte

Sélectionnez Path

Cliquez Modifier

Cliquez Nouveau

Ajoutez (exemple):
```
Exemple : C:\Users\(ton_user)\.bun\bin\
```
Cliquez OK

Redémarrez le terminal, puis vérifiez :
```
bun -v
```

# 📌 4. Installation du projet
Placez-vous dans votre dossier :
exemple:
```
cd "C:\Users\..."
```
Installez les dépendances :
```
bun install
```

# 📌 5. Lancer l'application
Lancer via Expo CLI
```
npx expo start
```


# 🔧 Configuration de l’adresse IP pour l’API

L’application mobile communique avec le serveur backend (FastAPI) en utilisant l’adresse IP locale de votre machine.
Pour que l’app puisse envoyer les images analysées, vous devez mettre à jour cette adresse dans services/api.ts.

## 1. Trouver l’adresse IPv4 de votre ordinateur

Sur Windows, ouvrez un terminal puis tapez :
```
ipconfig
```

Repérez ensuite la section :
```
Carte réseau sans fil Wi-Fi
```

Dans celle-ci, récupérez la ligne :
```
Adresse IPv4. . . . . . . . . . . . : xx.xx.xx.xx
```

C’est cette adresse qu’il faut utiliser.

## 2. Mettre à jour l’adresse dans services/api.ts

Ouvrez le fichier :
```
/services/api.ts
```

Puis remplacez :
```
const BASE_IP = "Adresse IPv4";
```

par votre véritable IPv4, par exemple :
```
const BASE_IP = "192.168.1.15";
```
🔁 Pourquoi ?

Lorsque vous lancez l’app mobile sur votre téléphone via Expo, celui-ci doit contacter votre backend en local.
Si l’adresse IP n’est pas correcte, aucune analyse d’image ne fonctionnera.

🔁 Remarque importante (⚠️ OBLIGATOIRE)

💡 Votre ordinateur (backend / modèles) doivent être connectés au même réseau **Wi-Fi**.



