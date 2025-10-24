"""
Script principal pour exécuter toutes les analyses
"""
import subprocess
import sys
import os

def run_script(script_path, description):
    """
    Exécute un script Python et affiche le résultat
    """
    print("\n" + "=" * 80)
    print(f"🚀 {description}")
    print("=" * 80)

    try:
        result = subprocess.run(
            [sys.executable, script_path],
            check=True,
            capture_output=True,
            text=True
        )
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ ERREUR lors de l'exécution:")
        print(e.stdout)
        print(e.stderr)
        return False

def main():
    """
    Fonction principale
    """
    print("=" * 80)
    print("ANALYSE COMPLÈTE - ÉNERGIE DISPONIBLE À ≤40€/MWh")
    print("=" * 80)
    print()
    print("Ce script va exécuter toutes les étapes d'analyse:")
    print("  1. Extraction données ODRE (éCO2mix)")
    print("  2. Extraction données ENTSO-E (flux, prix)")
    print("  3. Extraction prix RTE (EPEX SPOT)")
    print("  4. Analyse exports ≤40€/MWh")
    print("  5. Analyse écrêtage renouvelables")
    print("  6. Analyse nucléaire non produit")
    print("  7. Analyse prix négatifs")
    print("  8. Consolidation et rapport final")
    print()

    response = input("Continuer? (o/n): ")
    if response.lower() != 'o':
        print("Annulé.")
        return

    scripts_dir = "scripts"
    scripts = [
        ("1_fetch_odre.py", "Extraction ODRE éCO2mix"),
        ("2_fetch_entsoe.py", "Extraction ENTSO-E"),
        ("3_fetch_rte_prices.py", "Extraction prix RTE"),
        ("4_analyze_exports.py", "Analyse exports"),
        ("5_analyze_curtailment.py", "Analyse écrêtage"),
        ("6_analyze_nuclear.py", "Analyse nucléaire"),
        ("7_analyze_negative_prices.py", "Analyse prix négatifs"),
        ("8_consolidate.py", "Consolidation finale"),
    ]

    results = []

    for script_name, description in scripts:
        script_path = os.path.join(scripts_dir, script_name)
        success = run_script(script_path, description)
        results.append((script_name, success))

        if not success:
            print(f"\n⚠️ Le script {script_name} a échoué")
            response = input("Continuer avec les suivants? (o/n): ")
            if response.lower() != 'o':
                break

    # Résumé final
    print("\n" + "=" * 80)
    print("RÉSUMÉ D'EXÉCUTION")
    print("=" * 80)
    for script_name, success in results:
        status = "✅" if success else "❌"
        print(f"{status} {script_name}")

    successful = sum(1 for _, success in results if success)
    total = len(results)

    print(f"\n{successful}/{total} scripts exécutés avec succès")

    if successful == total:
        print("\n🎉 Analyse complète terminée!")
        print("📊 Consultez les résultats dans le dossier 'results/'")

if __name__ == "__main__":
    main()
