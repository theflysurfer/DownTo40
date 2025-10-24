"""
Script de vérification de la configuration
Teste la connectivité aux APIs avant de lancer les analyses
"""
import sys
import os

# Ajouter le dossier config au path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def check_env_file():
    """
    Vérifie que le fichier .env existe
    """
    print("1. Vérification du fichier .env...")

    if os.path.exists(".env"):
        print("   ✅ Fichier .env trouvé")
        return True
    else:
        print("   ❌ Fichier .env non trouvé")
        print("   → Copiez .env.example vers .env et ajoutez vos tokens")
        return False

def check_packages():
    """
    Vérifie que tous les packages sont installés
    """
    print("\n2. Vérification des packages Python...")

    required_packages = [
        'requests',
        'pandas',
        'dotenv',
        'entsoe',
        'openpyxl'
    ]

    missing = []
    for package in required_packages:
        try:
            if package == 'dotenv':
                __import__('dotenv')
            else:
                __import__(package)
            print(f"   ✅ {package}")
        except ImportError:
            print(f"   ❌ {package} manquant")
            missing.append(package)

    if missing:
        print(f"\n   → Installez les packages manquants : pip install -r requirements.txt")
        return False

    return True

def check_odre_api():
    """
    Teste la connectivité à l'API ODRE
    """
    print("\n3. Test de connexion ODRE (Open Data Réseaux Énergies)...")

    try:
        import requests
        url = "https://odre.opendatasoft.com/api/explore/v2.1/catalog/datasets/eco2mix-national-cons-def/records"
        params = {"limit": 1}

        response = requests.get(url, params=params, timeout=10)

        if response.status_code == 200:
            data = response.json()
            if "results" in data:
                print("   ✅ API ODRE accessible")
                print(f"   → Pas de token nécessaire")
                return True

        print(f"   ⚠️ Réponse inattendue : {response.status_code}")
        return False

    except Exception as e:
        print(f"   ❌ Erreur : {e}")
        return False

def check_entsoe_api():
    """
    Teste la connectivité à l'API ENTSO-E
    """
    print("\n4. Test de connexion ENTSO-E...")

    try:
        from config.api_config import ENTSOE_API_TOKEN

        if not ENTSOE_API_TOKEN:
            print("   ⚠️ Token ENTSO-E non configuré")
            print("   → Inscrivez-vous sur https://transparency.entsoe.eu")
            print("   → Envoyez un email à transparency@entsoe.eu")
            print("   → Sujet : 'Restful API access'")
            return False

        # Test avec l'API
        from entsoe import EntsoePandasClient
        import pandas as pd

        client = EntsoePandasClient(api_key=ENTSOE_API_TOKEN)

        # Test simple : récupérer 1 jour de prix
        start = pd.Timestamp('2024-01-01', tz='Europe/Paris')
        end = pd.Timestamp('2024-01-02', tz='Europe/Paris')

        prices = client.query_day_ahead_prices('FR', start=start, end=end)

        if prices is not None and len(prices) > 0:
            print("   ✅ API ENTSO-E accessible")
            print(f"   → Token valide")
            return True
        else:
            print("   ⚠️ Token valide mais pas de données retournées")
            return False

    except Exception as e:
        error_msg = str(e)
        if "401" in error_msg or "Unauthorized" in error_msg:
            print("   ❌ Token invalide")
            print("   → Vérifiez votre token ENTSO-E dans le fichier .env")
        elif "429" in error_msg:
            print("   ⚠️ Quota API dépassé (limite: 400 req/min)")
            print("   → Attendez quelques minutes et réessayez")
        else:
            print(f"   ❌ Erreur : {error_msg}")
        return False

def check_rte_api():
    """
    Teste la connectivité à l'API RTE
    """
    print("\n5. Test de connexion RTE Data Portal...")

    try:
        from config.api_config import RTE_CLIENT_ID, RTE_CLIENT_SECRET, RTE_TOKEN_URL
        import requests
        import base64

        if not RTE_CLIENT_ID or not RTE_CLIENT_SECRET:
            print("   ⚠️ Credentials RTE non configurés")
            print("   → Inscrivez-vous sur https://data.rte-france.com")
            print("   → Créez une application")
            print("   → Récupérez Client ID et Client Secret")
            return False

        # Test OAuth2
        credentials = f"{RTE_CLIENT_ID}:{RTE_CLIENT_SECRET}"
        encoded = base64.b64encode(credentials.encode()).decode()

        headers = {
            "Authorization": f"Basic {encoded}",
            "Content-Type": "application/x-www-form-urlencoded"
        }

        data = {"grant_type": "client_credentials"}

        response = requests.post(RTE_TOKEN_URL, headers=headers, data=data, timeout=10)

        if response.status_code == 200:
            token_data = response.json()
            if "access_token" in token_data:
                print("   ✅ API RTE accessible")
                print("   → Credentials valides")
                return True
        elif response.status_code == 401:
            print("   ❌ Credentials invalides")
            print("   → Vérifiez Client ID et Secret dans .env")
        else:
            print(f"   ⚠️ Erreur {response.status_code}")

        return False

    except Exception as e:
        print(f"   ❌ Erreur : {e}")
        return False

def check_directories():
    """
    Vérifie que les dossiers nécessaires existent
    """
    print("\n6. Vérification des dossiers...")

    directories = [
        'config',
        'scripts',
        'data',
        'data/raw',
        'data/processed',
        'results'
    ]

    all_ok = True
    for directory in directories:
        if os.path.exists(directory):
            print(f"   ✅ {directory}/")
        else:
            print(f"   ⚠️ {directory}/ manquant (sera créé automatiquement)")

    return True

def main():
    """
    Fonction principale
    """
    print("=" * 80)
    print("VÉRIFICATION DE LA CONFIGURATION")
    print("=" * 80)
    print()

    results = []

    # 1. Fichier .env
    results.append(("Fichier .env", check_env_file()))

    # 2. Packages
    results.append(("Packages Python", check_packages()))

    # 3. ODRE API
    results.append(("API ODRE", check_odre_api()))

    # 4. ENTSO-E API
    results.append(("API ENTSO-E", check_entsoe_api()))

    # 5. RTE API
    results.append(("API RTE", check_rte_api()))

    # 6. Dossiers
    results.append(("Dossiers", check_directories()))

    # Résumé
    print("\n" + "=" * 80)
    print("RÉSUMÉ")
    print("=" * 80)

    total = len(results)
    success = sum(1 for _, ok in results if ok)

    for name, ok in results:
        status = "✅" if ok else "❌"
        print(f"{status} {name}")

    print()
    print(f"Score : {success}/{total}")

    if success == total:
        print("\n🎉 Configuration complète ! Vous pouvez lancer les analyses.")
        print("   → Exécutez : python run_all.py")
    elif success >= 3:
        print("\n⚠️ Configuration partielle. Certaines analyses peuvent échouer.")
        print("   → Configurez les APIs manquantes pour analyses complètes")
        print("   → Ou lancez uniquement les scripts disponibles")
    else:
        print("\n❌ Configuration incomplète. Veuillez configurer les prérequis.")
        print("   → Consultez GUIDE_UTILISATION.md pour les instructions")

    print()

if __name__ == "__main__":
    main()
