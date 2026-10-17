# NIEUWE WOORDEN/LESSEN publiceren, ZONDER nieuwe APK (alle toestellen halen het zelf op).
#   .\publish-content.ps1 -Assets "D:\CLAUDE PROJELER\AlbayrakBezig\app\src\main\assets"
# Voer eerst `node tools/build_extra.mjs` uit zoals gewoonlijk. Dit script kopieert de JSON-bestanden uit de assets
# naar site/content/, verhoogt contentVersion in version.json en pusht naar GitHub.
param(
  [Parameter(Mandatory = $true)][string]$Assets,
  [string]$Notes = ""
)
$ErrorActionPreference = "Stop"
$site = Join-Path $PSScriptRoot "site"
$cdir = Join-Path $site "content"
$vf = Join-Path $site "version.json"
$names = @("lessons.json", "words.json", "glossary.json", "extra_lessons.json", "extra_glossary.json")
$map = [ordered]@{}
foreach ($n in $names) {
  $src = Join-Path $Assets $n
  if (Test-Path -LiteralPath $src) {
    Get-Content -LiteralPath $src -Raw | ConvertFrom-Json | Out-Null   # geldige JSON?
    Copy-Item -LiteralPath $src -Destination (Join-Path $cdir $n) -Force
    $map[$n] = (Get-FileHash -LiteralPath (Join-Path $cdir $n) -Algorithm SHA256).Hash.ToLower()
  }
}
if ($map.Count -eq 0) { throw "Geen JSON-bestanden gevonden in $Assets" }
$old = Get-Content -LiteralPath $vf -Raw | ConvertFrom-Json
$obj = [ordered]@{
  versionCode = [int]$old.versionCode; versionName = $old.versionName; apk = $old.apk; sha256 = $old.sha256; notes = $old.notes
  contentVersion = ([int]$old.contentVersion + 1); content = $map
}
[System.IO.File]::WriteAllText($vf, ($obj | ConvertTo-Json -Depth 5), (New-Object System.Text.UTF8Encoding $false))
git -C $PSScriptRoot add site
git -C $PSScriptRoot commit -m "AL-BEZIG content v$($obj.contentVersion) $Notes"
git -C $PSScriptRoot push
Write-Host "Klaar. Inhoud v$($obj.contentVersion) staat online. Toestellen halen het bij het openen van de app op."
