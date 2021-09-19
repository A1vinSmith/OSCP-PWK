### SPIKE scripting
```
❯ generic_send_tcp
argc=1
Usage: ./generic_send_tcp host port spike_script SKIPVAR SKIPSTR
./generic_send_tcp 192.168.1.100 701 something.spk 0 0
```

### Strings
The string commands provide a way of adding ASCII character data into your SPIKES. Also included within the string commands is the s_string_variable command, one of the most important commands within SPIKE as it actually allows you to add fuzz strings to your SPIKE.
```
s_readline(); //print received line from server
s_string_variable("COMMAND "); //send fuzzed string
s_string_variable("0");
```
```
    s_string(“string”); // simply prints the string “string” as part of your “SPIKE”
    s_string_repeat(“string”,200); // repeats the string “string” 200 times
    s_string_variable(“string”); // inserts a fuzzed string into your “SPIKE”. The string “string” will be used for the first iteration of this variable, as well as for any SPIKES where other s_string_variables are being iterated
```
