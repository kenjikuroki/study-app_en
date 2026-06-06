param(
  [string]$AppId = "linux"
)

$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$repoRoot = Split-Path -Parent $scriptDir
$baseDir = Join-Path $repoRoot "input\source_documents\$AppId"

$downloads = @(
  @{ Category = "filesystem"; Url = "https://www.gnu.org/software/coreutils/manual/html_node/cp-invocation.html"; File = "cp-invocation.html" },
  @{ Category = "filesystem"; Url = "https://www.gnu.org/software/coreutils/manual/html_node/mv-invocation.html"; File = "mv-invocation.html" },
  @{ Category = "filesystem"; Url = "https://www.gnu.org/software/coreutils/manual/html_node/mkdir-invocation.html"; File = "mkdir-invocation.html" },
  @{ Category = "filesystem"; Url = "https://www.gnu.org/software/coreutils/manual/html_node/ln-invocation.html"; File = "ln-invocation.html" },
  @{ Category = "filesystem"; Url = "https://www.gnu.org/software/coreutils/manual/html_node/readlink-invocation.html"; File = "readlink-invocation.html" },
  @{ Category = "filesystem"; Url = "https://www.gnu.org/software/coreutils/manual/html_node/realpath-invocation.html"; File = "realpath-invocation.html" },
  @{ Category = "filesystem"; Url = "https://www.gnu.org/software/coreutils/manual/html_node/rm-invocation.html"; File = "rm-invocation.html" },
  @{ Category = "filesystem"; Url = "https://www.gnu.org/software/coreutils/manual/html_node/rmdir-invocation.html"; File = "rmdir-invocation.html" },
  @{ Category = "filesystem"; Url = "https://www.gnu.org/software/coreutils/manual/html_node/df-invocation.html"; File = "df-invocation.html" },
  @{ Category = "filesystem"; Url = "https://www.gnu.org/software/coreutils/manual/html_node/du-invocation.html"; File = "du-invocation.html" },
  @{ Category = "filesystem"; Url = "https://www.gnu.org/software/coreutils/manual/html_node/stat-invocation.html"; File = "stat-invocation.html" },

  @{ Category = "permissions"; Url = "https://www.gnu.org/software/coreutils/manual/html_node/chmod-invocation.html"; File = "chmod-invocation.html" },
  @{ Category = "permissions"; Url = "https://www.gnu.org/software/coreutils/manual/html_node/chown-invocation.html"; File = "chown-invocation.html" },
  @{ Category = "permissions"; Url = "https://www.gnu.org/software/coreutils/manual/html_node/chgrp-invocation.html"; File = "chgrp-invocation.html" },
  @{ Category = "permissions"; Url = "https://www.gnu.org/software/coreutils/manual/html_node/File-permissions.html"; File = "file-permissions.html" },

  @{ Category = "users_groups"; Url = "https://www.gnu.org/software/coreutils/manual/html_node/id-invocation.html"; File = "id-invocation.html" },
  @{ Category = "users_groups"; Url = "https://www.gnu.org/software/coreutils/manual/html_node/logname-invocation.html"; File = "logname-invocation.html" },
  @{ Category = "users_groups"; Url = "https://www.gnu.org/software/coreutils/manual/html_node/whoami-invocation.html"; File = "whoami-invocation.html" },
  @{ Category = "users_groups"; Url = "https://www.gnu.org/software/coreutils/manual/html_node/groups-invocation.html"; File = "groups-invocation.html" },
  @{ Category = "users_groups"; Url = "https://www.gnu.org/software/coreutils/manual/html_node/users-invocation.html"; File = "users-invocation.html" },
  @{ Category = "users_groups"; Url = "https://www.gnu.org/software/coreutils/manual/html_node/who-invocation.html"; File = "who-invocation.html" },

  @{ Category = "processes"; Url = "https://www.gnu.org/software/coreutils/manual/html_node/timeout-invocation.html"; File = "timeout-invocation.html" },
  @{ Category = "processes"; Url = "https://www.gnu.org/software/coreutils/manual/html_node/nohup-invocation.html"; File = "nohup-invocation.html" },
  @{ Category = "processes"; Url = "https://www.gnu.org/software/coreutils/manual/html_node/nice-invocation.html"; File = "nice-invocation.html" },
  @{ Category = "processes"; Url = "https://www.gnu.org/software/coreutils/manual/html_node/sleep-invocation.html"; File = "sleep-invocation.html" },
  @{ Category = "processes"; Url = "https://www.gnu.org/software/coreutils/manual/html_node/nproc-invocation.html"; File = "nproc-invocation.html" },
  @{ Category = "processes"; Url = "https://man7.org/linux/man-pages/man7/signal.7.html"; File = "signal.7.html" },

  @{ Category = "package_management"; Url = "https://www.debian.org/doc/manuals/apt-guide/index.en.html"; File = "apt-guide.html" },
  @{ Category = "package_management"; Url = "https://docs.fedoraproject.org/en-US/quick-docs/dnf-package-manager-quick-reference/"; File = "dnf-package-manager-quick-reference.html" },

  @{ Category = "networking"; Url = "https://www.gnu.org/software/coreutils/manual/html_node/hostname-invocation.html"; File = "hostname-invocation.html" },
  @{ Category = "networking"; Url = "https://man7.org/linux/man-pages/man8/ip-address.8.html"; File = "ip-address.8.html" },
  @{ Category = "networking"; Url = "https://man7.org/linux/man-pages/man8/ip-link.8.html"; File = "ip-link.8.html" },
  @{ Category = "networking"; Url = "https://man7.org/linux/man-pages/man8/ping.8.html"; File = "ping.8.html" },
  @{ Category = "networking"; Url = "https://man7.org/linux/man-pages/man8/ss.8.html"; File = "ss.8.html" },

  @{ Category = "shell_scripting"; Url = "https://www.gnu.org/software/bash/manual/bash.html"; File = "bash-reference-manual.html" },
  @{ Category = "shell_scripting"; Url = "https://www.gnu.org/software/bash/manual/html_node/Shell-Scripts.html"; File = "shell-scripts.html" },
  @{ Category = "shell_scripting"; Url = "https://www.gnu.org/software/bash/manual/html_node/Conditional-Constructs.html"; File = "conditional-constructs.html" },
  @{ Category = "shell_scripting"; Url = "https://www.gnu.org/software/bash/manual/html_node/Shell-Parameters.html"; File = "shell-parameters.html" },
  @{ Category = "shell_scripting"; Url = "https://www.gnu.org/software/bash/manual/html_node/Bash-Builtins.html"; File = "bash-builtins.html" }
)

$downloadLog = @()

foreach ($item in $downloads) {
  $targetDir = Join-Path $baseDir $item.Category
  if (-not (Test-Path $targetDir)) {
    New-Item -ItemType Directory -Path $targetDir | Out-Null
  }

  $targetPath = Join-Path $targetDir $item.File
  Invoke-WebRequest -Uri $item.Url -OutFile $targetPath
  $downloadLog += [pscustomobject]@{
    category = $item.Category
    file = $item.File
    url = $item.Url
    saved_to = $targetPath
  }
}

$downloadLog | ConvertTo-Json -Depth 4
