# log-ts-diff

Modify log lines to reflect time diffs rather than timestamps

# Synopsis

	log-snippet < LOG

# Description

`log-snippet` reads a log as standard input with time info at the beginning of
each line. As output, `log-snippet` prints the same log lines, but replaces
the time info with a duration between current line and previous line.

# Example

Take this `journald` log:

```
May 16 18:40:03 myhost kernel: firewallIN=enp34s0 OUT= MAC=00:11:22:33:44:55:66:77:88:99:aa:bb:cc:dd SRC=1.2.3.4 DST=1.2.3.4 LEN=44 TOS=0x00 PREC=0x00 TTL=241 ID=54321 PROTO=TCP SPT=55617 DPT=311 WINDOW=65535 RES=0x00 SYN UR>
May 16 18:40:14 myhost kernel: firewallIN=enp34s0 OUT= MAC=00:11:22:33:44:55:66:77:88:99:aa:bb:cc:dd SRC=1.2.3.4 DST=1.2.3.4 LEN=62 TOS=0x00 PREC=0x00 TTL=40 ID=61495 DF PROTO=UDP SPT=9191 DPT=8080 LEN=42 
May 16 18:40:32 myhost kernel: firewallIN=enp34s0 OUT= MAC=00:11:22:33:44:55:66:77:88:99:aa:bb:cc:dd SRC=1.2.3.4 DST=1.2.3.4 LEN=44 TOS=0x00 PREC=0x00 TTL=240 ID=49667 PROTO=TCP SPT=17379 DPT=3780 WINDOW=1024 RES=0x00 SYN UR>
May 16 18:40:37 myhost kernel: firewallIN=enp34s0 OUT= MAC=00:11:22:33:44:55:66:77:88:99:aa:bb:cc:dd SRC=1.2.3.4 DST=1.2.3.4 LEN=44 TOS=0x00 PREC=0x00 TTL=239 ID=28910 PROTO=TCP SPT=8080 DPT=32768 WINDOW=1024 RES=0x00 SYN UR>
May 16 18:40:40 myhost kernel: firewallIN=enp34s0 OUT= MAC=00:11:22:33:44:55:66:77:88:99:aa:bb:cc:dd SRC=1.2.3.4 DST=1.2.3.4 LEN=44 TOS=0x00 PREC=0x00 TTL=244 ID=39758 PROTO=TCP SPT=40835 DPT=4936 WINDOW=1024 RES=0x00 SYN URGP>
May 16 18:40:45 myhost kernel: firewallIN=enp34s0 OUT= MAC=00:11:22:33:44:55:66:77:88:99:aa:bb:cc:dd SRC=1.2.3.4 DST=1.2.3.4 LEN=44 TOS=0x00 PREC=0x00 TTL=33 ID=3916 PROTO=TCP SPT=16407 DPT=11258 WINDOW=1024 RES=0x00 SYN UR>
May 16 18:40:48 myhost vpn-user[2171]: [Foobar CA] Inactivity timeout (--ping-restart), restarting
May 16 18:40:48 myhost vpn-user[2171]: SIGUSR1[soft,ping-restart] received, process restarting
May 16 18:40:53 myhost vpn-user[2171]: TCP/UDP: Preserving recently used remote address: [AF_INET]1.2.3.4:1194
```

It's hard to see how much time elapsed between each line. Minutes? Seconds? Not even a second?

Process it with `log-ts-diff`:

```
May 16 18:40:03 myhost kernel: firewallIN=enp34s0 OUT= MAC=00:11:22:33:44:55:66:77:88:99:aa:bb:cc:dd SRC=1.2.3.4 DST=1.2.3.4 LEN=44 TOS=0x00 PREC=0x00 TTL=241 ID=54321 PROTO=TCP SPT=55617 DPT=311 WINDOW=65535 RES=0x00 SYN UR>
+11s myhost kernel: firewallIN=enp34s0 OUT= MAC=00:11:22:33:44:55:66:77:88:99:aa:bb:cc:dd SRC=1.2.3.4 DST=1.2.3.4 LEN=62 TOS=0x00 PREC=0x00 TTL=40 ID=61495 DF PROTO=UDP SPT=9191 DPT=8080 LEN=42
+18s myhost kernel: firewallIN=enp34s0 OUT= MAC=00:11:22:33:44:55:66:77:88:99:aa:bb:cc:dd SRC=1.2.3.4 DST=1.2.3.4 LEN=44 TOS=0x00 PREC=0x00 TTL=240 ID=49667 PROTO=TCP SPT=17379 DPT=3780 WINDOW=1024 RES=0x00 SYN UR>
+ 5s myhost kernel: firewallIN=enp34s0 OUT= MAC=00:11:22:33:44:55:66:77:88:99:aa:bb:cc:dd SRC=1.2.3.4 DST=1.2.3.4 LEN=44 TOS=0x00 PREC=0x00 TTL=239 ID=28910 PROTO=TCP SPT=8080 DPT=32768 WINDOW=1024 RES=0x00 SYN UR>
+ 3s myhost kernel: firewallIN=enp34s0 OUT= MAC=00:11:22:33:44:55:66:77:88:99:aa:bb:cc:dd SRC=1.2.3.4 DST=1.2.3.4 LEN=44 TOS=0x00 PREC=0x00 TTL=244 ID=39758 PROTO=TCP SPT=40835 DPT=4936 WINDOW=1024 RES=0x00 SYN URGP>
+ 5s myhost kernel: firewallIN=enp34s0 OUT= MAC=00:11:22:33:44:55:66:77:88:99:aa:bb:cc:dd SRC=1.2.3.4 DST=1.2.3.4 LEN=44 TOS=0x00 PREC=0x00 TTL=33 ID=3916 PROTO=TCP SPT=16407 DPT=11258 WINDOW=1024 RES=0x00 SYN UR>
+ 3s myhost vpn-user[2171]: [Foobar CA] Inactivity timeout (--ping-restart), restarting
+0 myhost vpn-user[2171]: SIGUSR1[soft,ping-restart] received, process restarting
+ 5s myhost vpn-user[2171]: TCP/UDP: Preserving recently used remote address: [AF_INET]1.2.3.4:1194
```

The first timestamp is untouched, but the next ones are replaced with the time between 2 lines.

# Requirements

`log-ts-diff` uses Python and `dateutil`.

# License

This is free software, distributed under the WTFPL 2.0.
