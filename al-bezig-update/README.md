# AL-BEZIG: update-pagina en updates voor alle toestellen

Dit is een kleine site met de nieuwste APK en `version.json`. De app kijkt bij het openen of er een nieuwere versie is
en laat met één tik installeren (zie `UPDATER-SPEC.md`).

## Eenmalig instellen (Netlify, via GitHub, net als Zouff)
1. Netlify > Add new project > Import from Git > GitHub > `awesome-claude-skills`.
2. Branch `ccr-fb6f7349-15zmza`, **Base directory** `al-bezig-update`, build command leeg, publish directory `site`.
3. Geef het project een vaste naam, bv. `al-bezig`, en zet het op **Public**. Adres: `https://al-bezig.netlify.app`.
4. Zet dit adres als `UPDATE_BASE` in de app (zie `UPDATER-SPEC.md`).

## Twee soorten updates

**A. Nieuwe woorden/lessen/wijzigingen in de inhoud: GEEN nieuwe APK nodig**
1. Voeg woorden toe zoals altijd (`node tools/build_extra.mjs` enz.).
2. In `al-bezig-update` uitvoeren:
   `.\publish-content.ps1 -Assets "D:\CLAUDE PROJELER\AlbayrakBezig\app\src\main\assets"`
3. Het script zet de JSON-bestanden op de site en verhoogt `contentVersion`. Netlify publiceert vanzelf.
4. Elk toestel haalt de nieuwe inhoud bij het openen van de app op. Niemand installeert iets.

**B. Echte verandering van de app (code, nieuwe schermen): nieuwe APK**
1. Bouw de debug-APK zoals altijd (zelfde handtekening, hogere `versionCode` in `app/build.gradle`).
2. `.\release.ps1 -Apk "<pad naar APK>" -VersionCode 2 -VersionName "1.1" -Notes "Nieuwe functie"`
3. Toestellen zien bij het openen: "Nieuwe versie beschikbaar" en installeren met één tik.

Geen slepen en neerzetten meer. Elke APK (~60 MB) komt in de git-geschiedenis; prima voor tientallen versies.
Inhoud (A) is klein en kost bijna niets.

## Let op
- Een APK installeren vraagt op Android altijd één bevestiging van de gebruiker. Stil/automatisch updaten kan niet zonder Play Store of beheerdersrechten.
- `versionCode` moet altijd hoger zijn dan die van de geïnstalleerde app, anders weigert Android.
- Gebruik dezelfde handtekening (debug-keystore) als de vorige versie, anders kan de update niet over de oude heen.
- Leerinhoud (lessen) kan later ook zonder nieuwe APK worden bijgewerkt; zie sectie 6 in `UPDATER-SPEC.md`.
