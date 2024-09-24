Deploy
------
Use following script from outside of this folder:

    ./pi_server/build_pyz.sh pi_server.pyz;scp pi_server.pyz robin@192.168.1.69:~;ssh robin@192.168.1.69 'sudo mv /home/robin/pi_server.pyz /srv/;sudo systemctl restart pi_server'
