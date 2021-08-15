### Kind of interesting. You need to google about PBX/FreePBX
PBX https://support.skype.com/en/faq/FA10315/what-is-a-sip-enabled-pbx
https://github.com/EnableSecurity/sipvicious

### Try to find out the SIP extension number
```
svwar -m INVITE -e100-300 10.10.10.7
```
1. Try smaller range(e.g. -e100-500)
```
-e RANGE, --extensions=RANGE
                        specify an extension or extension range  example: -e
                        100-999,1000-1500,9999
```

2. Try other options (-m INVITE/OPTIONS)