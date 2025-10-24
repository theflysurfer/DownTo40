# 🔑 Guide de Configuration des Tokens API

Vous avez déjà créé vos comptes RTE et ENTSO-E. Voici comment récupérer vos tokens :

---

## 1️⃣ ENTSO-E Token

### Étape 1 : Se connecter
1. Aller sur : https://transparency.entsoe.eu/
2. Cliquer sur **"Login"** (coin supérieur droit)
3. Entrer vos identifiants

### Étape 2 : Générer le token
1. Une fois connecté, cliquer sur votre nom (coin supérieur droit)
2. Sélectionner **"Account Settings"**
3. Descendre jusqu'à la section **"Web API Security Token"**
4. Si vous n'avez pas encore de token :
   - Cliquer sur **"Generate a new token"**
   - **IMPORTANT** : Si le bouton n'est pas actif, vous devez d'abord envoyer un email à transparency@entsoe.eu avec sujet "Restful API access"
5. **Copier le token** (format : `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`)

### Étape 3 : Ajouter au projet
1. Ouvrir le fichier `.env` dans le projet
2. Coller le token :
   ```
   ENTSOE_API_TOKEN=12345678-1234-1234-1234-123456789abc
   ```

---

## 2️⃣ RTE Client ID et Secret

### Étape 1 : Se connecter
1. Aller sur : https://data.rte-france.com/
2. Cliquer sur **"Sign in"** (coin supérieur droit)
3. Entrer vos identifiants

### Étape 2 : Accéder à votre application
1. Dans le menu en haut, cliquer sur **"My applications"**
2. Si vous n'avez pas encore d'application :
   - Cliquer sur **"Create a new application"**
   - Nom : "Analyse Energie 40EUR"
   - Description : "Analyse énergie disponible"
   - Cliquer sur **"Create"**

### Étape 3 : Souscrire à l'API Wholesale Market
1. Dans votre application, onglet **"APIs"** ou **"Subscribe to APIs"**
2. Rechercher : **"Wholesale Market"** ou **"Wholesale Market v2.0"**
3. Cliquer sur **"Subscribe"**
4. Validation automatique

### Étape 4 : Récupérer les credentials
1. Retourner dans **"My applications"**
2. Cliquer sur votre application
3. Section **"Credentials"** ou **"Authentication"** :
   - **Client ID** : Visible directement (copier)
   - **Client Secret** : Cliquer sur **"Show"** ou icône œil pour afficher, puis copier

### Étape 5 : Ajouter au projet
1. Ouvrir le fichier `.env` dans le projet
2. Coller les credentials :
   ```
   RTE_CLIENT_ID=abc123def456
   RTE_CLIENT_SECRET=votre_secret_ici_tres_long
   ```

---

## 3️⃣ Vérification de la Configuration

Une fois les tokens ajoutés dans `.env`, vérifier que tout fonctionne :

```bash
python check_config.py
```

**Résultat attendu** :
```
✓ Fichier .env
✓ Packages Python
✓ API ODRE
✓ API ENTSO-E
✓ API RTE
✓ Dossiers

Score : 6/6
Configuration complète !
```

---

## ⚠️ Sécurité

**IMPORTANT** :
- ❌ Ne JAMAIS partager vos tokens
- ❌ Ne JAMAIS commit le fichier `.env` sur Git (déjà dans .gitignore)
- ✅ Garder les tokens confidentiels
- ✅ Régénérer si compromis

---

## 🔄 Si vous n'avez pas accès à l'API ENTSO-E

Si le bouton "Generate token" n'est pas actif sur ENTSO-E :

**Action** : Envoyer un email
```
À : transparency@entsoe.eu
Sujet : Restful API access

Bonjour,

Je souhaite obtenir un accès à l'API Restful de la plateforme ENTSO-E Transparency.

Email d'inscription : votre_email@exemple.com

Merci,
Cordialement
```

**Délai** : 3 jours ouvrés pour recevoir l'autorisation

---

## ✅ Checklist de Configuration

- [ ] Compte ENTSO-E créé
- [ ] Email envoyé à transparency@entsoe.eu (si nécessaire)
- [ ] Token ENTSO-E généré
- [ ] Token ENTSO-E copié dans `.env`
- [ ] Compte RTE créé
- [ ] Application RTE créée
- [ ] Souscription "Wholesale Market" validée
- [ ] Client ID RTE copié dans `.env`
- [ ] Client Secret RTE copié dans `.env`
- [ ] `python check_config.py` retourne 6/6

---

## 🚀 Prochaine Étape

Une fois la configuration terminée :

```bash
python run_all.py
```

Cela lancera l'analyse complète sur 2022-2024 !

---

**Besoin d'aide ?** Consultez **FAQ.md** ou **GUIDE_UTILISATION.md**
