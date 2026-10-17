# AL-BEZIG: update-pagina en updates voor alle toestellen

Dit is een kleine site met de nieuwste APK en `version.json`. De app kijkt bij het openen of er een nieuwere versie is
en laat met één tik installeren (zie `UPDATER-SPEC.md`).

## Eenmalig instellen (Netlify, via GitHub, net als Zouff)
1. Netlify > Add new project > Import from Git > GitHub > `awesome-claude-skills`.
2. Branch `ccr-fb6f7349-15zmza`, **Base directory** `al-bezig-update`, build command leeg, publish directory `site`.
3. Geef het project een vaste naam, bv. `al-bezig`, en zet het op **Public**. Adres: `https://al-bezig.netlify.app`.
4. Zet dit adres als `UPDATE_BASE` in de app (zie `UPDATER-SPEC.md`).

## Bij elke nieuwe versie (één commando)
1. Bouw de debug-APK zoals altijd (zelfde handtekening, hogere `versionCode` in `app/build.gradle`).
2. Clone deze repo op de pc (eenmalig) en voer uit in `al-bezig-update`:
   `.\release.ps1 -Apk "<pad naar APK>" -VersionCode 2 -VersionName "1.1" -Notes "Nieuwe lessen"`
3. Het script kopieert de APK, schrijft `version.json` (met sha256) en pusht naar GitHub. Netlify publiceert vanzelf.
4. Toestellen met de app zien bij het openen: "Nieuwe versie beschikbaar".

Geen slepen en neerzetten meer nodig. Elke APK (~60 MB) komt in de git-geschiedenis; dat is prima voor tientallen versies.

## Let op
- Een APK installeren vraagt op Android altijd één bevestiging van de gebruiker. Stil/automatisch updaten kan niet zonder Play Store of beheerdersrechten.
- `versionCode` moet altijd hoger zijn dan die van de geïnstalleerde app, anders weigert Android.
- Gebruik dezelfde handtekening (debug-keystore) als de vorige versie, anders kan de update niet over de oude heen.
- Leerinhoud (lessen) kan later ook zonder nieuwe APK worden bijgewerkt; zie sectie 6 in `UPDATER-SPEC.md`.
