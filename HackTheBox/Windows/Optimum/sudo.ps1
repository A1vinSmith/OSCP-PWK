$pw = ConvertTo-SecureString 'CanChange-Expi-Req' -AsPlainText -Force
$pp = New-Object System.Management.Automation.PSCredential("OPTIMUM\Administrator", $pw)
Start-Process powershell -Credential $pp -ArgumentList '-noprofile -command &{Start-Process C:\Users\kostas\Desktop\nc.bat -verb Runas}'