import os


GNUCASH_ARCHIVE_FILEPATH = '/var/gnucash/archive/'
if __name__ == "__main__":
    list = os.listdir(GNUCASH_ARCHIVE_FILEPATH)
    list.sort()
    while len(list) > 8:
        os.remove(GNUCASH_ARCHIVE_FILEPATH + list[0])
    os.system("rsync -r /var/gnucash/<YOUR_DB_NAME> /var/gnucash/archive/<YOUR_ARCHIVED_DB_NAME>")
