#!/bin/bash
# One-time, run on the host: opens MariaDB on the VM's libvirt address for the
# portal and creates portal@192.168.122.1 (SELECT, INSERT on account.account
# only). Restarts MariaDB, so the game servers are stopped and started around it.
# The password comes from /root/.metin2/portal-db.pw and never leaves the machines.
set -euo pipefail
VM="ssh -i /root/.ssh/metin2_vm -o BatchMode=yes root@192.168.122.10"
PW=$(cat /root/.metin2/portal-db.pw)

$VM 'umask 077; cat > /tmp/portal_user.sql' <<EOF
CREATE USER IF NOT EXISTS 'portal'@'192.168.122.1' IDENTIFIED BY '$PW';
ALTER USER 'portal'@'192.168.122.1' IDENTIFIED BY '$PW';
GRANT SELECT, INSERT ON account.account TO 'portal'@'192.168.122.1';
FLUSH PRIVILEGES;
EOF

$VM 'sh -s' <<'EOF'
set -e
C=/usr/local/etc/mysql/conf.d/zz-metin2.cnf
mysql < /tmp/portal_user.sql
rm -f /tmp/portal_user.sql
mysql -N -e "SHOW GRANTS FOR 'portal'@'192.168.122.1'" | sed -E "s/PASSWORD '[^']*'/PASSWORD '<hash>'/"
[ -f $C.bak-portal ] || cp -p $C $C.bak-portal
sed -i '' 's/^bind-address = 127.0.0.1$/bind-address = 127.0.0.1,192.168.122.10/' $C
grep bind-address $C
service metin2 stop
if ! service mysql-server restart; then
    echo "MARIADB RESTART FAILED - restoring the old config"
    cp -p $C.bak-portal $C
    service mysql-server restart
fi
sockstat -4l | grep mariadbd
service metin2 start
sleep 8
service metin2 status
EOF

docker exec -w /app m2web-portal node --input-type=module -e '
import { createConnection } from "mysql2/promise";
const e = process.env;
const c = await createConnection({ host: e.DB_HOST, user: e.DB_USER, password: e.DB_PASSWORD, database: e.DB_NAME });
await c.query("SELECT COUNT(*) FROM account");
await c.end();' && echo PORTAL_DB_OK
