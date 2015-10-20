# pylxc
playing with python and linux containers.

### Instaling

```
# apt-get install lxd
# service lxd restart
```

### Add Images

```
# lxc remote add images images.linuxcontainers.org
# lxc image list images
```

### Launching 

```
# lxc launch images:ubuntu/trusty/amd64 test01
```

```
# lxc list
+--------+---------+------------+------+-----------+
|  NAME  |  STATE  |    IPV4    | IPV6 | EPHEMERAL |
+--------+---------+------------+------+-----------+
| test01 | RUNNING | 10.0.3.107 |      | NO        |
+--------+---------+------------+------+-----------+
```

### Launching

```
# lxc launch images:ubuntu/trusty/amd64 test02
```

```
# lxc list
+--------+---------+------------+------+-----------+
|  NAME  |  STATE  |    IPV4    | IPV6 | EPHEMERAL |
+--------+---------+------------+------+-----------+
| test01 | RUNNING | 10.0.3.107 |      | NO        |
| test02 | RUNNING | 10.0.3.46  |      | NO        |
+--------+---------+------------+------+-----------+
```

# Exec

```
# lxc exec test01 /bin/bash 

// look the PS1 have changed
root@test01:~# 
```

### File System

```
root@lorcan:/var/lib/lxd/lxc# ls
lxc-monitord.log  test01  test02
root@lorcan:/var/lib/lxd/lxc/test01# cd rootfs/
root@lorcan:/var/lib/lxd/lxc/test01/rootfs# ls
bin  boot  dev  etc  home  lib  lib64  media  mnt  opt  proc  root  run  sbin  srv  sys  tmp  usr  var
```


### Stopping

```
root@lorcan:/var/lib/lxd/lxc/test01/rootfs# lxc stop test01
```

### List

```
root@lorcan:/var/lib/lxd/lxc/test01/rootfs# lxc list
+--------+---------+-----------+------+-----------+
|  NAME  |  STATE  |   IPV4    | IPV6 | EPHEMERAL |
+--------+---------+-----------+------+-----------+
| test01 | STOPPED |           |      | NO        |
| test02 | RUNNING | 10.0.3.46 |      | NO        |
+--------+---------+-----------+------+-----------+
```

### Delete

```
root@lorcan:/var/lib/lxd/lxc/test01/rootfs# lxc delete test01
```

```
root@lorcan:/var/lib/lxd/lxc/test01/rootfs# lxc list
+--------+---------+-----------+------+-----------+
|  NAME  |  STATE  |   IPV4    | IPV6 | EPHEMERAL |
+--------+---------+-----------+------+-----------+
| test02 | RUNNING | 10.0.3.46 |      | NO        |
+--------+---------+-----------+------+-----------+
```
