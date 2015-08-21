#!/bin/sh

# Encode Nginx proxy server setup.
# Assumes ssl.tgz present containing SSL certs / keys.

# Use the nginx/stable ppa as we want the current nginx.
apt-get install software-properties-common
add-apt-repository -y ppa:nginx/stable
apt-get update
apt-get install -y curl dnsmasq nginx-full ntp unattended-upgrades update-notifier-common

# Enable automatic security updates. This does not cover nginx as it is from a ppa.
cat <<'EOF' > /etc/apt/apt.conf.d/20auto-upgrades
APT::Periodic::Update-Package-Lists "1";
APT::Periodic::Unattended-Upgrade "1";
EOF

# Quoting 'EOF' prevents $variable substitution
cat <<'EOF' > /etc/apt/apt.conf.d/50unattended-upgrades
Unattended-Upgrade::Allowed-Origins {
    "${distro_id} ${distro_codename}-security";
};
Unattended-Upgrade::Automatic-Reboot "true";
EOF

mkdir -p /etc/nginx/ssl
tar -zxf ssl.tgz --directory /etc/nginx/ssl
# Generate a new (takes a few minutes.)
openssl dhparam 2048 -out /etc/nginx/ssl/dhparam.pem
chmod 600 /etc/nginx/ssl/dhparam.pem

cat <<'EOF' > /etc/nginx/nginx.conf
user www-data;
worker_processes  auto;
worker_rlimit_nofile 8192;
events {
    worker_connections  2048;
}
http {
    # Use upstream to support keepalive
    upstream test {
        server v30-test.instance.encodedcc.org;
        keepalive 30;
    }
    upstream production {
        server v30.production.encodedcc.org;
        keepalive 30;
    }

    resolver 127.0.0.1;
    resolver_timeout 5s;
    include  mime.types;
    client_max_body_size 500m;
    default_type  application/octet-stream;
    keepalive_timeout  65;
    proxy_buffers 8 16k;
    proxy_send_timeout    5m;
    proxy_read_timeout    5m;
    send_timeout    5m;

    merge_slashes off;

    # https://wiki.mozilla.org/Security/Server_Side_TLS
    ssl_session_timeout 1d;
    ssl_session_cache shared:SSL:50m;

    # Diffie-Hellman parameter for DHE ciphersuites, recommended 2048 bits
    ssl_dhparam /etc/nginx/ssl/dhparam.pem;

    # intermediate configuration. tweak to your needs.
    ssl_protocols TLSv1 TLSv1.1 TLSv1.2;
    ssl_ciphers 'ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-AES256-GCM-SHA384:DHE-RSA-AES128-GCM-SHA256:DHE-DSS-AES128-GCM-SHA256:kEDH+AESGCM:ECDHE-RSA-AES128-SHA256:ECDHE-ECDSA-AES128-SHA256:ECDHE-RSA-AES128-SHA:ECDHE-ECDSA-AES128-SHA:ECDHE-RSA-AES256-SHA384:ECDHE-ECDSA-AES256-SHA384:ECDHE-RSA-AES256-SHA:ECDHE-ECDSA-AES256-SHA:DHE-RSA-AES128-SHA256:DHE-RSA-AES128-SHA:DHE-DSS-AES128-SHA256:DHE-RSA-AES256-SHA256:DHE-DSS-AES256-SHA:DHE-RSA-AES256-SHA:AES128-GCM-SHA256:AES256-GCM-SHA384:AES128-SHA256:AES256-SHA256:AES128-SHA:AES256-SHA:AES:CAMELLIA:DES-CBC3-SHA:!aNULL:!eNULL:!EXPORT:!DES:!RC4:!MD5:!PSK:!aECDH:!EDH-DSS-DES-CBC3-SHA:!EDH-RSA-DES-CBC3-SHA:!KRB5-DES-CBC3-SHA';
    ssl_prefer_server_ciphers on;

    # OCSP Stapling ---
    # fetch OCSP records from URL in ssl_certificate and cache them
    ssl_stapling on;
    ssl_stapling_verify on;

    server {
        listen 80;
        location / {
            if ($request_method !~ ^(GET)|(HEAD)$) {
                return 405;
            }
            return  301  https://$host$request_uri;
        }
    }

    server {
        listen 171.67.205.78:443 ssl spdy;
        server_name ~^(?<servername>[^.]+)\.demo\.encodedcc\.org$;
        ssl_certificate         /etc/nginx/ssl/demo.encodedcc.org/server.chained.pem;
        ssl_certificate_key     /etc/nginx/ssl/demo.encodedcc.org/server.key;
        ssl_trusted_certificate /etc/nginx/ssl/demo.encodedcc.org/ca.chained.pem;
        add_header Strict-Transport-Security max-age=15768000;  # 6 months
        location / {
            # Normalize duplicate slashes
            if ($request ~ ^(GET|HEAD)\s([^?]*)//(.*)\sHTTP/[0-9.]+$) {
                return 301 $2/$3;
            }
            proxy_set_header  Host  $host;
            proxy_set_header  X-Forwarded-For    $proxy_add_x_forwarded_for;
            proxy_set_header  X-Forwarded-Proto  $scheme;
            proxy_pass  http://$servername.instance.encodedcc.org;
            proxy_http_version  1.1;
            proxy_set_header  Connection  "";
        }
        location ~ ^/_proxy/(.*)$ {
            internal;
            proxy_buffering off;
            proxy_pass $1$is_args$args;
        }
    }

    server {
        listen 171.67.205.78:443 ssl spdy;
        server_name test.encodedcc.org;
        ssl_certificate         /etc/nginx/ssl/encodedcc.org/server.chained.pem;
        ssl_certificate_key     /etc/nginx/ssl/encodedcc.org/server.key;
        ssl_trusted_certificate /etc/nginx/ssl/encodedcc.org/ca.chained.pem;
        add_header Strict-Transport-Security max-age=15768000;  # 6 months
        location / {
            # Normalize duplicate slashes
            if ($request ~ ^(GET|HEAD)\s([^?]*)//(.*)\sHTTP/[0-9.]+$) {
                return 301 $2/$3;
            }
            proxy_set_header  Host  $host;
            proxy_set_header  X-Forwarded-For    $proxy_add_x_forwarded_for;
            proxy_set_header  X-Forwarded-Proto  $scheme;
            proxy_pass  http://test;
            proxy_http_version  1.1;
            proxy_set_header  Connection  "";
        }
        location ~ ^/_proxy/(.*)$ {
            internal;
            proxy_buffering off;
            proxy_pass $1$is_args$args;
        }
    }

    server {
        listen 171.67.205.70:443 ssl spdy;
        server_name www.encodeproject.org;
        ssl_certificate         /etc/nginx/ssl/encodeproject.org/server.chained.pem;
        ssl_certificate_key     /etc/nginx/ssl/encodeproject.org/server.key;
        ssl_trusted_certificate /etc/nginx/ssl/encodeproject.org/ca.chained.pem;
        add_header Strict-Transport-Security max-age=15768000;  # 6 months
        location / {
            # Normalize duplicate slashes
            if ($request ~ ^(GET|HEAD)\s([^?]*)//(.*)\sHTTP/[0-9.]+$) {
                return 301 $2/$3;
            }
            proxy_set_header  Host  $host;
            proxy_set_header  X-Forwarded-For    $proxy_add_x_forwarded_for;
            proxy_set_header  X-Forwarded-Proto  $scheme;
            proxy_pass  http://production;
            proxy_http_version  1.1;
            proxy_set_header  Connection  "";
        }
        location ~ ^/_proxy/(.*)$ {
            internal;
            proxy_buffering off;
            proxy_pass $1$is_args$args;
        }
    }

    server {
        listen 171.67.205.70:443 ssl spdy;
        server_name download.encodeproject.org;
        ssl_certificate         /etc/nginx/ssl/encodeproject.org/server.chained.pem;
        ssl_certificate_key     /etc/nginx/ssl/encodeproject.org/server.key;
        ssl_trusted_certificate /etc/nginx/ssl/encodeproject.org/ca.chained.pem;
        location = /robots.txt {
            add_header Content-Type text/plain;
            return 200 'User-agent: *\nDisallow: /\n';
        }
        location ~ ^/(https?://(encode-files|encoded-files-dev)\.s3\.amazonaws\.com(:80|:443)?/.*)$ {
            proxy_buffering off;
            proxy_pass $1$is_args$args;
        }
    }

}
EOF

service nginx restart
