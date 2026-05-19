Set-Alias npp "${env:ProgramFiles(x86)}\Notepad++\notepad++.exe"
Set-PSReadLineOption –HistoryNoDuplicates:$True

# Ensure PSReadLine writes history as you type, not just on exit
Set-PSReadLineOption -HistorySaveStyle SaveIncrementally

# Optional: increase max history and avoid duplicates
Set-PSReadLineOption -MaximumHistoryCount 50000 -HistoryNoDuplicates:$true


# oh-my-posh init pwsh --config "$env:POSH_THEMES_PATH\paradox.omp.json" | Invoke-Expression
oh-my-posh init pwsh --config "C:\Users\pjanowski\paradox.omp.json" | Invoke-Expression

# function hist { 
#   $find = $args; 
#   Write-Host "Finding in full history using {`$_ -like `"*$find*`"}"; 
#   Get-Content (Get-PSReadlineOption).HistorySavePath | ? {$_ -like "*$find*"} | Get-Unique | more 
# }

# function hist2 { 
#   $find = $args; 
#   Write-Host "Finding in full history using {`$_ -like `"*$find*`"}"; 
#   Get-Content (Get-PSReadlineOption).HistorySavePath | Select-String -Pattern "$find" | Sort-Object -Property Line -Unique  | more 
# }

$env:PATH += ";C:\Users\pjanowski\bin"
$env:PATH += ";$env:USERPROFILE\.agency\nodejs\node-v22.21.0-win-x64"

function Go-Linux {
    Set-Location "\\wsl$\Ubuntu\home\pjanowski"
}
Set-Alias -Name lhome -Value Go-Linux

# Import the Chocolatey Profile that contains the necessary code to enable
# tab-completions to function for `choco`.
# Be aware that if you are missing these lines from your profile, tab completion
# for `choco` will not function.
# See https://ch0.co/tab-completion for details.
$ChocolateyProfile = "$env:ChocolateyInstall\helpers\chocolateyProfile.psm1"
if (Test-Path($ChocolateyProfile)) {
  Import-Module "$ChocolateyProfile"
}

function hs {
    param(
        [Parameter(ValueFromRemainingArguments = $true)]
        [string[]] $Args
    )
    $query = ($Args -join ' ').Trim()
    if (-not $query) { Write-Host "Usage: hs <text to find in current session history>"; return }

    Write-Host "Searching current session history for: '$query'"
    Get-History |
        Select-Object -ExpandProperty CommandLine |
        Select-String -SimpleMatch -Pattern $query |
        ForEach-Object { $_.Line } |
        Sort-Object -Unique
}

function hf {
    param(
        [Parameter(ValueFromRemainingArguments = $true)]
        [string[]] $Args
    )
    $query = ($Args -join ' ').Trim()
    if (-not $query) { Write-Host "Usage: hf <text to find in full history file>"; return }

    $histPath = (Get-PSReadLineOption).HistorySavePath
    if (-not (Test-Path $histPath)) { Write-Warning "History file not found at $histPath"; return }

    Write-Host "Searching full history file: $histPath"
    Get-Content -Path $histPath -ErrorAction SilentlyContinue |
        Select-String -SimpleMatch -Pattern $query |
        Select-Object -ExpandProperty Line |
        Sort-Object -Unique |
        Out-Host -Paging   # like 'more'
}


function cc {
    claude --dangerously-skip-permissions @args
}

function acc {
    agency claude --dangerously-skip-permissions @args
}

# Machine-local profile (not synced via OneDrive)
$_local = "C:\Users\pjanowski\.ps_local_profile.ps1"
if (Test-Path $_local) { . $_local }
