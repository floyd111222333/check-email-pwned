import requests
import time
import sys

# === Configuration ===
email = input("Entre ton adresse Gmail (ou autre) : ").strip()

# API Have I Been Pwned (gratuite, mais il faut un User-Agent et un léger délai)
url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}"
headers = {
    "hibp-api-key": "",  # Optionnel : laisse vide si tu n’as pas de clé (rate limit plus strict)
    "User-Agent": "CheckGmail-HIBP-Script/1.0",
    "Accept": "application/json"
}

# Respect des rate limits (même sans clé : max 1 requête toutes les 1,5 secondes)
time.sleep(1.5)

try:
    response = requests.get(url, headers=headers, timeout=10)
    
    if response.status_code == 200:
        breaches = response.json()
        print("\n⚠️  TON COMPTE A ÉTÉ COMPROMIS ! ⚠️")
        print(f"Il apparaît dans {len(breaches)} fuite(s) de données :\n")
        for breach in breaches:
            name = breach["Name"]
            date = breach["BreachDate"]
            data = ", ".join(breach["DataClasses"])
            pwn_count = breach.get("PwnCount", "inconnu")
            print(f"• {name} ({date}) → {pwn_count} comptes touchés")
            print(f"   Données exposées : {data}\n")
        print("➡️ Change immédiatement ton mot de passe Gmail et active l’authentification à deux facteurs (2FA) !")
    
    elif response.status_code == 404:
        print("\n✅ Bonne nouvelle ! Ton adresse n’a été trouvée dans AUCUNE fuite connue sur Have I Been Pwned.")
        print("Ça ne veut pas dire 100 % safe, mais c’est déjà très bon signe.")
    
    elif response.status_code == 429:
        print("⏱ Trop de requêtes. Attends 2 minutes et réessaie.")
    
    else:
        print(f"Erreur {response.status_code} : {response.text}")

except requests.exceptions.RequestException as e:
    print("Erreur de connexion :", e)
except KeyboardInterrupt:
    print("\nArrêt du script.")
    sys.exit()