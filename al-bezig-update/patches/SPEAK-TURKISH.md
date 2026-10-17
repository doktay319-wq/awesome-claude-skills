# Wijziging: "Turks voorlezen na het Nederlands" (aan/uit)

Voor de AL-BEZIG-sessie op de pc. Dit is een CODE-wijziging, dus er komt één nieuwe debug-APK.
Regels uit de memory blijven gelden: eerst vragen voor je een APK bouwt, geen minify, zelfde debug-handtekening, `versionCode` +1.

## Gewenst gedrag
- In het audiogedeelte (automatisch afspelen van een les, ook Android Auto/achtergrond) komt een schakelaar "Turks erbij / Türkçe de okusun".
- AAN: eerst de Nederlandse zin (zoals nu, met `autoRepeat` herhalingen), daarna één keer de Turkse vertaling, dan de pauze (`autoGapSec`).
- UIT (standaard): alleen Nederlands, precies zoals nu.
- De keuze wordt bewaard (DataStore) en geldt ook voor de achtergrondservice.
- Geen Turkse stem op het toestel of vertaling leeg: Turks overslaan, geen crash. Eénmalig een korte melding "Türkçe ses yüklü değil".
- Alleen als `sourceLang == "tr"` (bij Engels als brontaal blijft het Engels uit; zet geen Turks).

## 1. SettingsRepository.kt
In `data class Settings`:
```kotlin
val speakTurkish: Boolean = false,
```
In `private object K`:
```kotlin
val speakTr = booleanPreferencesKey("speakTr")
```
In `val flow` (bij de andere velden):
```kotlin
speakTurkish = p[K.speakTr] ?: d.speakTurkish,
```
Nieuwe functie:
```kotlin
suspend fun setSpeakTurkish(v: Boolean) = edit { it[K.speakTr] = v }
```

## 2. TTS-klasse (`container.tts`, waar `speakAndWait` staat)
Ik kon dit bestand niet inzien; pas het aan zoals past. Voeg een optionele taalparameter toe:
```kotlin
suspend fun speakAndWait(text: String, rate: Float, locale: Locale? = null): Boolean
```
- Zonder `locale`: gedrag ongewijzigd (Nederlands + gekozen `voiceName`).
- Met `locale` (Turks): zet voor deze zin de taal op `Locale("tr", "TR")`, negeer `voiceName` (die is voor Nederlands), spreek, en zet daarna de taal terug naar Nederlands.
- Controleer beschikbaarheid: `tts.isLanguageAvailable(locale) >= TextToSpeech.LANG_AVAILABLE`. Zo niet: geef `true` terug zonder te spreken (overslaan) en meld één keer "Türkçe ses yüklü değil".

## 3. TtsPlaybackService.kt, functie `play(...)`
Huidige code in de lus:
```kotlin
repeat(settings.autoRepeat.coerceAtLeast(1)) {
    if (!container.tts.speakAndWait(s.text, settings.ttsRate)) return@launch
    delay((settings.autoGapSec * 1000).toLong())
}
container.study.markHeard(s.id, lessonId)
```
Wordt:
```kotlin
repeat(settings.autoRepeat.coerceAtLeast(1)) {
    if (!container.tts.speakAndWait(s.text, settings.ttsRate)) return@launch
    delay((settings.autoGapSec * 1000).toLong())
}
if (settings.speakTurkish && settings.sourceLang == "tr" && s.translation.isNotBlank()) {
    if (!container.tts.speakAndWait(s.translation, settings.ttsRate, Locale("tr", "TR"))) return@launch
    delay((settings.autoGapSec * 1000).toLong())
}
container.study.markHeard(s.id, lessonId)
```
(`import java.util.Locale`.) Let op: de service leest `settings` één keer aan het begin van `play`. Wil je dat het wisselen tijdens het afspelen meteen werkt, lees dan binnen de lus opnieuw `container.settings.current()`.
`s.translation` is de vertaling in de gekozen brontaal; controleer de veldnaam in de sentence-entity.

## 4. LessonDetailVm en schermen
- `LessonDetailVm.speak(...)` (een zin aantikken): als `speakTurkish` aan is, na het Nederlands ook het Turks voorlezen, op dezelfde manier.
- `LessonScreens.kt`: zet naast de knop voor automatisch afspelen (`toggleAuto`) een kleine `FilterChip`/schakelaar "TR" (met uitleg-tekst "Turks erbij"), gekoppeld aan `settings.speakTurkish` met `setSpeakTurkish`.
- Instellingenscherm: dezelfde schakelaar onder de audio-instellingen, tekst NL en TR.
- Strings (apostrof escapen):
  - tr: `Nederlandsca'dan sonra Türkçesini de oku`
  - nl: `Lees ook de Turkse vertaling voor`

## 5. Testen
1. Schakelaar uit: gedrag exact als voorheen.
2. Schakelaar aan, bron Turks: Nederlands (×herhalingen), dan Turks, dan pauze, volgende zin.
3. Schakelaar aan met scherm uit/vergrendeld en via Android Auto: werkt ook.
4. Toestel zonder Turkse stem: slaat Turks over, geen crash, één melding.
5. Pauze/hervatten (`autoResume`) blijft werken.

## 6. Publiceren
`versionCode` +1, debug-APK bouwen (na akkoord van de eigenaar), dan:
`.\release.ps1 -Apk "<pad>" -VersionCode N -VersionName "x.y" -Notes "Turks erbij (aan/uit)"` in `al-bezig-update`.
