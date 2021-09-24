# for i in `seq 1 100`; do echo $i; done
for i in `seq 0 100`; do echo $i >> num.txt; done

for i in {0..255}; do echo $i >> num2.txt; done

# Alternatives
# /usr/share/wordlists/seclists/Fuzzing/
