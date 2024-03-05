ssh-keygen

echo "Enter Your Password, you will need sudo priviledges"
read -s pass
echo $pass | sudo -S apt-get update
echo $pass | sudo -S apt-get install -y python3=3.10.6-1~22.04
echo $pass | sudo -S apt-get install -y python3-pip=22.0.2+dfsg-1ubuntu0.4
echo $pass | sudo -S apt-get install -y python3-venv==3.10.6-1~22.04
echo $pass | sudo -S apt-get install -y libdbd-sqlite3=0.9.0-10
echo $pass | sudo -S apt-get install -y gnucash=1:4.8-1build2
echo $pass | sudo -S apt-get install -y rsync=3.2.7-0ubuntu0.22.04.2
unset pass


echo "What is the name of the database you will be using? NOTE: DO NOT INCLUDE '.gnucash' at the end"
read dbName
sudo mkdir -p /var/gnucash/archive/log
sudo mv ./local_archive.py /var/gnucash/
crontab crontab_entry

sudo chown -R $USER:$USER /var/gnucash

sudo mv ./gnucash-invoices.desktop /usr/share/applications/

sudo mkdir /opt/gnucash-invoices
sudo cp -r ./source_code/* /opt/gnucash-invoices/
sudo chown -R $USER:$USER /opt/gnucash-invoices/




python3 -m venv /opt/gnucash-invoices/.venv
source /opt/gnucash-invoices/.venv/bin/activate
pip3 install jinja2==3.1.3
pip3 install weasyprint==52.5
pip3 install google-api-python-client==2.120.0
pip3 install PyQt5==5.15.10
deactivate


