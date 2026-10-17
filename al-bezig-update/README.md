# AL-BEZIG: update-pagina en updates voor alle toestellen

Dit is een kleine site met de nieuwste APK en `version.json`. De app kijkt bij het openen of er een nieuwere versie is
en laat met één tik installeren (zie `UPDATER-SPEC.md`).

## Eenmalig instellen (Netlify)
1. Netlify > Add new project > **Upload your project files** (of "Deploy manually").
2. Sleep de map `site/` erin (met `AL-BEZIG-debug.apk`, `version.json`, `index.html`, `_headers`).
3. Geef het project een vaste naam, bv. `al-bezig`. Adres: `https://al-bezig.netlify.app`.

## Bij elke nieuwe versie
1. Bouw de debug-APK zoals altijd (zelfde handtekening, hogere `versionCode` in `app/build.gradle`).
2. Kopieer de APK naar `site/AL-BEZIG-debug.apk`.
3. Pas `site/version.json` aan: `versionCode` (+1), `versionName`, `notes`.
   (Optioneel `sha256`: `sha256sum AL-BEZIG-debug.apk`.)
4. Netlify > Deploys > sleep de map `site/` opnieuw in het uploadvak.
5. Toestellen met de nieuwe app-versie zien bij het openen: "Nieuwe versie beschikbaar".

## Let op
- Een APK installeren vraagt op Android altijd één bevestiging van de gebruiker. Stil/automatisch updaten kan niet zonder Play Store of beheerdersrechten.
- `versionCode` moet altijd hoger zijn dan die van de geïnstalleerde app, anders weigert Android.
- Gebruik dezelfde handtekening (debug-keystore) als de vorige versie, anders kan de update niet over de oude heen.
- Leerinhoud (lessen) kan later ook zonder nieuwe APK worden bijgewerkt; zie sectie 6 in `UPDATER-SPEC.md`.
