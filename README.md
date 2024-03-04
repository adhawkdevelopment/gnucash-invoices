This software was created by Kevin Hall/AdHawk Development and is offered under the terms of the GNU General Public License version 3 (GPL-3.0)

https://www.gnu.org/licenses/gpl-3.0-standalone.html


This software is installed on:
Ubuntu 22.04.4 LTS 64-bit
GNOME Version: 42.9
Windowing System: Wayland


NOTE: THIS SCRIPT COPIES THE GNUCASH DATABASE FILE (SQLITE3) TO /var/gnucash AND THE SOURCE CODE TO "/opt/gnucash-invoices"


In order to install and configure this software to your specific needs:

    GNUCASH INVOICE TOOL INSTALL
    1. Download and copy this folder to your computer
    2. Navigate to this folder in a terminal
    3. Execute "./INSTALL.sh", you will first create a ssh key, then you will be prompted to enter your password, no input is required for the rest of this install, this install will complete on its own
    4. You will need to place your GNUCash DB file (SQLITE3) in the /var/gnucash/ directory
    5. You will need to enter the full path of the GNUCash database file in /opt/gnucash-invoices/db/db_path
    6. You will need to edit the rsync command in local_archive.py to copy your database to the archive, and create a naming convention so that you do not overwrite files, I used the curredt date in YYYY-MM-DD format
    7. You will need to edit local_gnucash_archive with your username, this is the cron.d file that will execute every week to archive your database
    8. You will need to add company_logo.png to /opt/gnucash-invoices/pdf/ so that it prints on your invoice
    
    INVOICE TEMPLATE
    1. Edit /opt/gnucash-invoices/pdf/TERMS_SECTIONS.json with the terms that you want to have at the bottom of your invoices, work orders, and special orders.  You might want to even edit the invoice_template.html if you change the structure of the TERMS_SECTIONS.json file
    2. Edit the invoice_template html and css files to your liking if you please
    3. Edit /opt/gnucash-invoices/pdf/COMPANY_INFO.json with your company's info
    4. Add your company's logo to /opt/gnucash-invoices/pdf/company_logo.png
    5. Edit /opt/gnucash-invoices/pdf/

    GOOGLE WORKSPACES
    1. You need Google Workspaces for this tool to work, create a project on console.cloud.google.com
    2. Enable the GMail API
    3. Navigate to the APIs & Services -> Credentials
    4. Create a Service Account
    5. Create an OAuth 2.0 Client ID and download your service key
    6. Add your service-key.json file to /opt/gnucash-invoices/gmail/
    7. Edit the EMAIL_CONTENT variable in /opt/gnucash-invoices/gmail/__init__.py
    8. Edit the EMAIL_FROM variable in /opt/gnucash-invoices/gmail/__init__.py, note the EMAIL_FROM needs to be the same email address as the one linked to the Google Workspaces account that you used to create the service key
    
    NOTE, THE EMAIL ADDRESS USED TO SEND AN EMAIL TO IS LISTED IN THE CUSTOMER'S BILLING ADDRESS SECTION IN THE EDIT CUSTOMER MENU




-----INDEMNITY AGREEMENT-----
I am not responsible for your usage of this software, it works fine on my computer, if you use a different OS or have different versions of software or packages that is installed then this software might crash, if you make changes to this software and multiple emails are sent or emails are sent to the wrong address then not my problem, this software is offered as is.  If you use this software you are doing so at your own will and risk and thereby agree to hold me (Kevin Hall) harmelss for any damages as a result of using this software, and this includes corruption of your database as this software does perform sqlite3 database commands, this is why I back up my database frequently
