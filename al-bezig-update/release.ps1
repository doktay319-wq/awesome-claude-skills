# Gebruik (PowerShell, in deze map):
#   .\release.ps1 -Apk "D:\CLAUDE PROJELER\AlbayrakBezig\AL-BEZIG-debug.apk" -VersionCode 2 -VersionName "1.1" -Notes "Nieuwe lessen"
# Kopieert de APK naar site/, schrijft version.json (met sha256) en pusht naar GitHub. Netlify publiceert zelf.
param(
  [Parameter(Mandatory = $true)][string]$Apk,
  [Parameter(Mandatory = $true)][int]$VersionCode,
  [Parameter(Mandatory = $true)][string]$VersionName,
  [string]$Notes = ""
)
$ErrorActionPreference = "Stop"
$site = Join-Path $PSScriptRoot "site"
$dest = Join-Path $site "AL-BEZIG-debug.apk"
Copy-Item -LiteralPath $Apk -Destination $dest -Force
$sha = (Get-FileHash -LiteralPath $dest -Algorithm SHA256).Hash.ToLower()
$obj = [ordered]@{ versionCode = $VersionCode; versionName = $VersionName; apk = "AL-BEZIG-debug.apk"; sha256 = $sha; notes = $Notes }
$json = $obj | ConvertTo-Json
[System.IO.File]::WriteAllText((Join-Path $site "version.json"), $json, (New-Object System.Text.UTF8Encoding $false))
git -C $PSScriptRoot add site
git -C $PSScriptRoot commit -m "AL-BEZIG $VersionName ($VersionCode)"
git -C $PSScriptRoot push
Write-Host "Klaar. Netlify publiceert over enkele minuten: versie $VersionName ($VersionCode)."
