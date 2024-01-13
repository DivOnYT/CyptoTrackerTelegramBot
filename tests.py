import requests
requete_recherche = "WBNB USDC"
url = f"https://api.dexscreener.io/latest/dex/tokens/0x2170Ed0880ac9A755fd29B2688956BD959F933F8"
reponse = requests.get(url)
if reponse.status_code == 200:
    donnees = reponse.json()["pairs"][0]
    print(donnees)
