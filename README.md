Deploy
------
Use following example script from outside of this folder:

    mkdir -p pi_build;./pi_server/build_pyz.sh pi_build/pi_server.pyz;darkhttpd pi_build --pidfile pi_httpd.pid --daemon;ssh robin@192.168.1.69 'wget 192.168.1.4:8080/pi_server.pyz;sudo mv /home/robin/pi_server.pyz /srv/;sudo systemctl restart pi_server';kill `cat pi_httpd.pid`
