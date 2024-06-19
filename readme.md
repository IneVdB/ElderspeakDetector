# Handleiding Elderspeak Detector

## Voorbereiding


1. Download het zip-bestand van deze website door bovenaan te klikken op de groene knop 'code' en daarna op 'download zip', of via deze [link](https://github.com/IneVdB/ElderspeakDetector/archive/refs/heads/main.zip).
2. Pak het zip-bestand uit naar een gewenste locatie.
6. Open de map 'Programs' in de uitgepakte zip
7. Voer zowel python.exe en VC_Redist.exe uit als Administrator en doorloop de installatie van deze programma's.

## Installatie webapplicatie

1. Klik met de rechtermuisknop op install.bat en kies uitvoeren als administrator.
2. Indien een beveiligingsvenster opent, klik op meer info en dan onderaan 'toch uitvoeren'
3. Wacht tot het venster sluit.
4. Dubbelklik op makecert.bat en wacht tot het venster sluit. Indien er een pop-up verschijnt, klik op 'Ja'.

## API key voor Assembly-AI
De speech-to-text gaat via een externe service waarvoor een soort wachtwoord of API key nodig is.
Hiervoor moet zelf een account worden aangemaakt gezien deze keys best niet publiek gedeeld worden.

1. Surf naar [https://www.assemblyai.com/dashboard/signup](https://www.assemblyai.com/dashboard/signup) en maak een account aan.
2. Ga nu naar de account-pagina op [https://www.assemblyai.com/app/account](https://www.assemblyai.com/app/account)
3. Aan de linkerkant kan de API key worden teruggevonden. Kopieer deze.
4. Vervang de eerste lijn in het bestand 'assembly_apikey.txt' in de map 'wordlists' met deze code.

In principe zijn de eerste 100 uur aan transcripties per account gratis.

## Website starten

1. Dubbelklik op start_website.bat
2. Volg de link die tevoorschijn komt, normaalgezien is dit [https://127.0.0.1:5001/](https://127.0.0.1:5001/)

## Gebruik website

- Bij 'Choose file' kan een audio- of videobestand worden opgeladen. 
Hierop gebeurt dan analyse voor audiokenmerken wanneer op de knop 'Verwerk audio' wordt geklikt.
- Wanneer 'extract text' wordt aangevinkt zal ook een automatische transcriptie gebeuren waarna de resulterende tekst geanalyseerd wordt.
- Wanneer een transcriptie wordt ingevuld in het tekstveld zal hierop analyse gebeuren.
- Wanneer beide onaangevuld blijven (geen vinkje en een leeg tekstveld) zal enkel audio-analyse plaatsvinden.
- Wanneer beide zijn aangevuld zal op beide analyse worden uitgevoerd.
- Het is noodzakelijk om een audio- of videobestand op te laden ook om enkel een bestaande transcriptie in het tekstveld te analyseren.

## Zelf woorden toevoegen

Er zijn twee woordenlijsten die gebruikt worden, 'geen_verkleinwoorden.txt' en 'tussenwerpsels.txt'.
Deze kunnen teruggevonden worden in de map 'wordlists'.
Om woorden toe te voegen aan de detectie kunnen ze gewoon op een nieuwe lijn onderaan deze bestanden worden aangevuld.

## Troubleshooting
- Wanneer een probleem opduikt bij installatie kan meer info worden teruggevonden worden in het bestand startup.log.
Indien het probleem zich voortzet kan contact opgenomen worden.
- Indien er een foutmelding komt over een onveilige verbinding bij het openen van de website, kan het zijn dat het gemaakte certificaat is verlopen. 
Dubbelklik nogmaals op makecert.bat om een nieuw certificaat aan te maken.
