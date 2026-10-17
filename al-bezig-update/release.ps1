# NIEUWE APK publiceren (alleen nodig als de CODE van de app verandert).
#   .\release.ps1 -Apk "D:\CLAUDE PROJELER\AlbayrakBezig\AL-BEZIG-debug.apk" -VersionCode 2 -VersionName "1.1" -Notes "Nieuwe functie"
# Kopieert de APK naar site/, werkt version.json bij (contentVersion blijft behouden) en pusht naar GitHub.
param(
  [Parameter(Mandatory = $true)][string]$Apk,
  [Parameter(Mandatory = $true)][int]$VersionCode,
  [Parameter(Mandatory = $true)][string]$VersionName,
  [string]$Notes = ""
)
$ErrorActionPreference = "Stop"
$site = Join-Path $PSScriptRoot "site"
$dest = Join-Path $site "AL-BEZIG-debug.apk"
$vf = Join-Path $site "version.json"
Copy-Item -LiteralPath $Apk -Destination $dest -Force
$sha = (Get-FileHash -LiteralPath $dest -Algorithm SHA256).Hash.ToLower()
$old = Get-Content -LiteralPath $vf -Raw | ConvertFrom-Json
$obj = [ordered]@{
  versionCode = $VersionCode; versionName = $VersionName; apk = "AL-BEZIG-debug.apk"; sha256 = $sha; notes = $Notes
  contentVersion = [int]$old.contentVersion; content = $old.content
}
[System.IO.File]::WriteAllText($vf, ($obj | ConvertTo-Json -Depth 5), (New-Object System.Text.UTF8Encoding $false))
git -C $PSScriptRoot add site
git -C $PSScriptRoot commit -m "AL-BEZIG APK $VersionName ($VersionCode)"
git -C $PSScriptRoot push
Write-Host "Klaar. Nieuwe APK $VersionName ($VersionCode) wordt door Netlify gepubliceerd."
