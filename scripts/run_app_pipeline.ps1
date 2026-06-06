param(
  [Parameter(Mandatory = $true)]
  [string]$AppId,
  [string]$Cycle = "cycle_01",
  [string]$Date = "2026-06-05"
)

$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$repoRoot = Split-Path -Parent $scriptDir
$runner = Join-Path $scriptDir "run_pipeline.ps1"

$configPath = Join-Path $repoRoot "apps\active_apps\$AppId\app_config.json"
if (-not (Test-Path $configPath)) {
  throw "Missing app config: $configPath"
}

$config = Get-Content -Raw $configPath | ConvertFrom-Json
$results = @()

foreach ($category in $config.categories) {
  $categoryId = $category.category_id
  & powershell -ExecutionPolicy Bypass -File $runner --app-id $AppId --category $categoryId --cycle $Cycle --date $Date
  $exitCode = $LASTEXITCODE
  $results += [pscustomobject]@{
    category = $categoryId
    exit_code = $exitCode
    status = if ($exitCode -eq 0) { "success" } else { "failed" }
  }
}

$results | ConvertTo-Json -Depth 4
