$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$repoRoot = Split-Path -Parent $scriptDir
$pipelineScript = Join-Path $scriptDir "studyapp_pipeline.py"

$pythonExe = "C:\Users\kurok\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe"
if (-not (Test-Path $pythonExe)) {
  $pythonCmd = Get-Command python -ErrorAction SilentlyContinue
  if ($pythonCmd) {
    $pythonExe = $pythonCmd.Source
  } else {
    $pyCmd = Get-Command py -ErrorAction SilentlyContinue
    if ($pyCmd) {
      $pythonExe = $pyCmd.Source
    } else {
      throw "Python runtime not found. Install Python or use the bundled Codex runtime."
    }
  }
}

Push-Location $repoRoot
try {
  & $pythonExe $pipelineScript @args
  exit $LASTEXITCODE
}
finally {
  Pop-Location
}
