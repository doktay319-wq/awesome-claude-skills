# Opdracht voor de AL-BEZIG-sessie: in-app updater

Doel: Als de eigenaar een nieuwe APK op de update-site zet, tonen alle toestellen bij het openen "Nieuwe versie" en installeren met één tik.
Geen minify, geen nieuwe handtekening: dezelfde debug-APK als altijd (zie memory `ask-before-building-apk`). Vraag eerst voor je een APK bouwt.

Update-site (vervang door het echte adres): `https://al-bezig.netlify.app`

## 1. Manifest
```xml
<uses-permission android:name="android.permission.INTERNET"/>
<uses-permission android:name="android.permission.REQUEST_INSTALL_PACKAGES"/>
<application ...>
  <provider
      android:name="androidx.core.content.FileProvider"
      android:authorities="${applicationId}.fileprovider"
      android:exported="false"
      android:grantUriPermissions="true">
    <meta-data android:name="android.support.FILE_PROVIDER_PATHS" android:resource="@xml/file_paths"/>
  </provider>
</application>
```
`res/xml/file_paths.xml`:
```xml
<paths><cache-path name="updates" path="updates/"/></paths>
```

## 2. Versie
`app/build.gradle`: verhoog `versionCode` bij elke release (en `versionName`). `version.json` op de site moet dezelfde `versionCode` hebben.

## 3. Check bij het opstarten (max 1× per 6 uur)
```kotlin
data class RemoteVersion(val versionCode: Long, val versionName: String, val apk: String, val sha256: String, val notes: String)

suspend fun fetchRemoteVersion(base: String): RemoteVersion? = withContext(Dispatchers.IO) {
    try {
        val c = URL("$base/version.json").openConnection() as HttpURLConnection
        c.connectTimeout = 8000; c.readTimeout = 8000; c.useCaches = false
        val j = JSONObject(c.inputStream.bufferedReader().readText())
        RemoteVersion(j.getLong("versionCode"), j.optString("versionName"), j.getString("apk"),
                      j.optString("sha256"), j.optString("notes"))
    } catch (e: Exception) { null }
}

fun installedVersionCode(ctx: Context): Long =
    ctx.packageManager.getPackageInfo(ctx.packageName, 0).longVersionCode
```
Als `remote.versionCode > installedVersionCode(ctx)`: toon een dialoog (NL + TR) met de `notes`, knoppen "Bijwerken / Güncelle" en "Later / Sonra".

## 4. Downloaden
```kotlin
suspend fun downloadApk(ctx: Context, base: String, v: RemoteVersion, onProgress: (Int) -> Unit): File = withContext(Dispatchers.IO) {
    val dir = File(ctx.cacheDir, "updates").apply { mkdirs(); listFiles()?.forEach { it.delete() } }
    val out = File(dir, "al-bezig.apk")
    val c = URL("$base/${v.apk}").openConnection() as HttpURLConnection
    val total = c.contentLengthLong
    c.inputStream.use { i -> out.outputStream().use { o ->
        val buf = ByteArray(64 * 1024); var done = 0L
        while (true) { val n = i.read(buf); if (n < 0) break; o.write(buf, 0, n); done += n
            if (total > 0) onProgress((done * 100 / total).toInt()) } } }
    if (v.sha256.isNotBlank()) {
        val h = MessageDigest.getInstance("SHA-256").digest(out.readBytes()).joinToString("") { "%02x".format(it) }
        require(h.equals(v.sha256, ignoreCase = true)) { "checksum" }
    }
    out
}
```
Toon een voortgangsbalk. Bij een fout: korte melding, app blijft gewoon werken.

## 5. Installeren
```kotlin
fun installApk(ctx: Context, apk: File) {
    if (!ctx.packageManager.canRequestPackageInstalls()) {
        ctx.startActivity(Intent(Settings.ACTION_MANAGE_UNKNOWN_APP_SOURCES, Uri.parse("package:${ctx.packageName}"))
            .addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)); return   // na toestemming: opnieuw op "Bijwerken" tikken
    }
    val uri = FileProvider.getUriForFile(ctx, "${ctx.packageName}.fileprovider", apk)
    ctx.startActivity(Intent(Intent.ACTION_VIEW).setDataAndType(uri, "application/vnd.android.package-archive")
        .addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION or Intent.FLAG_ACTIVITY_NEW_TASK))
}
```
De gebruiker bevestigt de installatie zelf. Gegevens blijven bewaard (zelfde package + handtekening).

## 6. HOOFDDOEL: inhoud bijwerken zonder nieuwe APK (doe dit eerst)
De eigenaar wil nieuwe woorden/lessen toevoegen of iets in de inhoud wijzigen zonder dat iemand de APK opnieuw installeert.
De site heeft daarom naast de APK een map `content/` met dezelfde JSON-bestanden als in `assets/`:
`lessons.json`, `words.json`, `glossary.json`, `extra_lessons.json`, `extra_glossary.json` (alleen aanwezig als ze bestaan).
`version.json` bevat `contentVersion` (geheel getal, +1 bij elke publicatie) en `content` (bestandsnaam → sha256).

Gedrag in de app:
1. Bij het opstarten (en max. 1× per 6 uur, op de achtergrond, zonder het scherm te blokkeren): haal `UPDATE_BASE/version.json` op.
2. Als `contentVersion` > de lokaal opgeslagen waarde (DataStore, standaard 0): download alle bestanden uit `content` naar een tijdelijke map,
   controleer sha256 en of het geldige JSON is, verplaats ze dan pas naar `filesDir/content/` (alles-of-niets).
3. `SeedLoader` en `ExtraContentLoader` lezen eerst uit `filesDir/content/<naam>` en vallen terug op `assets/<naam>`.
4. Verhoog de seed-versie als `contentVersion` verandert, zodat Room herlaadt. Ids blijven stabiel (lessonId*10000 + positie), dus voortgang, "gekend"-markeringen en Privé blijven behouden. Overschrijf nooit bestaande gebruikersgegevens.
5. Geen internet of fout: stil doorgaan met de laatst bekende inhoud (lokaal of assets). Geen foutmelding voor de gebruiker.
6. Toon na een succesvolle update een korte melding: "Nieuwe lessen toegevoegd / Yeni dersler eklendi".
7. Wanneer een nieuwe APK wordt geïnstalleerd, geldt: gebruik de nieuwste van (assets in de APK, gedownloade inhoud), op basis van `contentVersion` (bewaar in assets een `content_version.txt`).

Alleen als de CODE verandert (nieuwe schermen, functies) is een nieuwe APK nodig (secties 1 tot 5).

## Testen
1. Installeer versie N. Zet versie N+1 op de site. Open de app: de dialoog verschijnt.
2. Kijk of de data (voortgang, sleutels) na de update nog aanwezig is.
3. Zonder internet: de app start gewoon, geen foutmelding.
