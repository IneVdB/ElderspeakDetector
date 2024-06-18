# Handleiding Elderspeak Detector

## Voorbereiding


1. Download het zip-bestand van deze website door bovenaan te klikken op de groene knop 'code' en daarna op 'download zip'.
2. Pak het zip-bestand uit naar een gewenste locatie.
6. Open de map 'Programs' in de uitgepakte zip
7. Voer zowel python.exe en VC_Redist.exe uit als Administrator en doorloop de installatie van deze programma's.

## Installatie webapplicatie

1. Dubbelklik op install.bat
2. Indien een beveiligingsvenster opent, klik op meer info en dan onderaan 'toch uitvoeren'
3. Wacht tot het venster sluit.

##API key voor Assembly-AI
De speech-to-text gaat via een externe service waarvoor een soort wachtwoord of API key nodig is.
Hiervoor moet zelf een account worden aangemaakt gezien deze keys best niet publiek gedeeld worden.

1. Surf naar [https://www.assemblyai.com/dashboard/signup](https://www.assemblyai.com/dashboard/signup) en maak een account aan.
2. Ga nu naar de account-pagina op [https://www.assemblyai.com/app/account](https://www.assemblyai.com/app/account)
3. Aan de linkerkant kan de API key worden teruggevonden. Kopieer deze.
4. Vervang de eerste lijn in het bestand 'assembly_apikey.txt' in de map 'wordlists' met deze code.

In principe zijn de eerste 100 uur aan transcripties per account gratis.

## Website starten

1. Dubbelklik op install.bat
2. Volg de link die tevoorschijn komt, normaalgezien is dit [https://127.0.0.1:5001/](https://127.0.0.1:5001/)

## Zelf woorden toevoegen

Er zijn twee woordenlijsten die gebruikt worden, 'geen_verkleinwoorden.txt' en 'tussenwerpsels.txt'.
Deze kunnen teruggevonden worden in de map 'wordlists'.
Om woorden toe te voegen aan de detectie kunnen ze gewoon op een nieuwe lijn onderaan deze bestanden worden aangevuld.

## Troubleshooting
- Wanneer een probleem opduikt bij installatie kan meer info worden teruggevonden worden in het bestand startup.log.
Indien het probleem zich voortzet kan contact opgenomen worden.
- Indien er een foutmelding komt over een onveilige verbinding bij het openen van de website, klik op 'geavanceerd' en 'ga verder naar deze pagina'. Dit wil zeggen dat er iets is misgegaan met het certificaat. 
Omdat de website enkel lokaal draait vormt dit in eerste instantie geen probleem, bij online websites is dit minder veilig.
