import sqlite3
import random
import string


OWNER_TYPE_CUSTOMER = 2
OWNER_TYPE_JOB = 3
OWNER_TYPE_VENDOR = 4






def get_db_path():
    filepath = ''
    with open(__path__[0] + '/db_path', 'r') as file:
        filepath = file.read().split('\n')[0]
    file.close()
    return filepath



def create_dict_from_resp(resp):
    struct = []
    values = resp.fetchall()
    for i in range(0, len(values)):
        temp = {}
        for j in range(0, len(values[i])):
            temp[resp.description[j][0]] = values[i][j]
        struct.append(temp)
    return struct



def get_all_customers():
    conn=sqlite3.connect(get_db_path())
    cur = conn.cursor()

    resp=cur.execute("select * from customers")
    invoices = create_dict_from_resp(resp)

    conn.close()

    return invoices

def get_all_invoices():
    conn=sqlite3.connect(get_db_path())
    cur = conn.cursor()

    resp=cur.execute("select * from invoices")
    invoices = create_dict_from_resp(resp)

    conn.close()

    return invoices



def get_all_lots():
    conn=sqlite3.connect(get_db_path())
    cur = conn.cursor()

    resp=cur.execute("select * from lots")
    lots = create_dict_from_resp(resp)

    conn.close()

    return lots

def get_all_slots():
    conn=sqlite3.connect(get_db_path())
    cur = conn.cursor()

    resp=cur.execute("select * from slots")
    slots = create_dict_from_resp(resp)

    conn.close()

    return slots



def get_all_splits():
    conn=sqlite3.connect(get_db_path())
    cur = conn.cursor()

    resp=cur.execute("select * from splits")
    splits = create_dict_from_resp(resp)

    conn.close()

    return splits

def get_all_entries():
    conn=sqlite3.connect(get_db_path())
    cur = conn.cursor()

    resp=cur.execute("select * from entries")
    entries = create_dict_from_resp(resp)

    conn.close()

    return entries

def get_all_transactions():
    conn=sqlite3.connect(get_db_path())
    cur = conn.cursor()

    resp=cur.execute("select * from transactions")
    transactions = create_dict_from_resp(resp)

    conn.close()

    return transactions

def get_all_invoices():
    conn=sqlite3.connect(get_db_path())
    cur = conn.cursor()

    resp=cur.execute("select * from invoices order by date_opened")
    invoices = create_dict_from_resp(resp)

    conn.close()

    return invoices
    

def get_recent_invoices():
    conn=sqlite3.connect(get_db_path())
    cur = conn.cursor()

    resp=cur.execute("select * from invoices order by date_opened desc limit 30")
    invoices = create_dict_from_resp(resp)

    conn.close()

    return invoices




def get_invoice_by_guid(invoice_guid):
    conn=sqlite3.connect(get_db_path())
    cur = conn.cursor()

    resp=cur.execute("select * from invoices where guid = '" + invoice_guid + "' order by date_opened")

    invoice = create_dict_from_resp(resp)
    
    conn.close()

    if len(invoice) > 0:
        return invoice[0]
    else:
        return None

    

    
def get_invoices_by_id(invoice_id):
    conn=sqlite3.connect(get_db_path())
    cur = conn.cursor()

    resp=cur.execute("select * from invoices where id = '" + invoice_id + "' order by date_opened")
    
    invoices = create_dict_from_resp(resp)

    conn.close()

    return invoices

    


def get_invoices_within_date_range(startDate, endDate):
    conn=sqlite3.connect(get_db_path())
    cur = conn.cursor()
    
    resp=cur.execute("select * from invoices where date_opened >= '" + startDate + "' and date_opened <= '" + endDate + "' order by date_opened")
    invoices = create_dict_from_resp(resp)

    conn.close()
    return invoices

    



def get_job_from_invoice(invoice):
    conn=sqlite3.connect(get_db_path())
    cur = conn.cursor()
    
    resp=cur.execute("select * from jobs where guid = '" + invoice['owner_guid'] + "'")
    job = create_dict_from_resp(resp)

    conn.close()
    
    if len(job) > 0:
        return job[0]
    else:
        return None

    


def get_job_name_array_from_job(job):
    if job != None:
        job_name = job['name'].split(',')
        job_name[-2] = ''.join(job_name[-2:])
        job_name.pop(-1)
        return job_name
    return None



def get_job_name_string_from_array(job_array):
    job = ''
    for line in job_array:
        job = job + line
    return job



def get_billing_terms_from_invoice(invoice):
    conn=sqlite3.connect(get_db_path())
    cur = conn.cursor()
    if invoice['terms'] != None:
        resp=cur.execute("select * from billterms where guid = '" + invoice['terms'] + "'")
        billing_terms = create_dict_from_resp(resp)

        conn.close()

        if len(billing_terms) > 0:
            return billing_terms[0]
        else:
            return None
    else:
        return None



def get_customer_from_invoice(invoice):
    conn=sqlite3.connect(get_db_path())
    cur = conn.cursor()
    
    resp=cur.execute("select * from jobs where guid = '" + invoice['owner_guid'] + "'")
    job = create_dict_from_resp(resp)
    if len(job) > 0:
        job = job[0]

    if int(invoice['owner_type']) == OWNER_TYPE_CUSTOMER:
        resp=cur.execute("select * from customers where guid = '" + invoice['owner_guid'] + "'")
        customer = create_dict_from_resp(resp)[0]
    elif int(invoice['owner_type']) == OWNER_TYPE_JOB:
        resp=cur.execute("select * from customers where guid = '" + job['owner_guid'] + "'")
        customer = create_dict_from_resp(resp)[0]
    
    conn.close()
    return customer

    
    


def get_materials_from_invoice(invoice):
    conn=sqlite3.connect(get_db_path())
    cur = conn.cursor()
    
    resp=cur.execute("select * from entries where action = 'Material' and invoice = '" + invoice['guid'] + "'")
    materials_entries = create_dict_from_resp(resp)

    conn.close()

    return materials_entries
    


def get_taxtable_from_materials(materials_entries):
    conn=sqlite3.connect(get_db_path())
    cur = conn.cursor()
    
    resp=cur.execute("select * from taxtable_entries where taxtable = '" + materials_entries[0]['i_taxtable'] + "'")
    taxtable = create_dict_from_resp(resp)

    conn.close()

    return taxtable
    


def get_labor_from_invoice(invoice):
    conn=sqlite3.connect(get_db_path())
    cur = conn.cursor()
    
    resp=cur.execute("select * from entries where action = 'Hours' and invoice = '" + invoice['guid'] + "'")
    labor_entries = create_dict_from_resp(resp)

    conn.close()

    return labor_entries

    

def delete_invoice(invoice_guid):
    conn=sqlite3.connect(get_db_path())
    cur = conn.cursor()


    # lots
    resp=cur.execute("select post_lot from invoices where guid = '" + invoice_guid + "'")
    invoice_post_lot = resp.fetchall()
    if len(invoice_post_lot) > 0:
        invoice_post_lot=invoice_post_lot[0][0]
        
        if invoice_post_lot != None:
            resp=cur.execute("select guid from lots where guid = '" + invoice_post_lot + "'")
            lot_guids = resp.fetchall()
            for l_guid in lot_guids:
                if l_guid[0] != None:
                    resp=cur.execute("select * from splits where lot_guid = '" + l_guid[0] + "'")
                    splits_guids = resp.fetchall()
                    for sp_guid in splits_guids:
                        if sp_guid[0] != None:
                            cur.execute("delete from slots where guid_val = '" + sp_guid[0] + "' or obj_guid = '" + sp_guid[0] + "'")
                            cur.execute("delete from splits where guid = '" + sp_guid[0] + "'")
                    cur.execute("delete from slots where guid_val = '" + l_guid[0] + "' or obj_guid = '" + l_guid[0] + "'")
                    cur.execute("delete from lots where guid = '" + l_guid[0] + "'")

    # transactions
    resp=cur.execute("select post_txn from invoices where guid = '" + invoice_guid + "'")
    invoice_post_txn = resp.fetchall()
    if len(invoice_post_txn) > 0:
        invoice_post_txn = invoice_post_txn[0][0]
        if invoice_post_txn != None:
            resp=cur.execute("select guid from transactions where guid = '" + invoice_post_txn + "'")
            transaction_guids = resp.fetchall()
            for tx_guid in transaction_guids:
                if tx_guid[0] != None:
                    # splits
                    resp=cur.execute("select guid from splits where tx_guid = '" + tx_guid[0] + "'")
                    splits_guids = resp.fetchall()
                    for sp_guid in splits_guids:
                        if sp_guid[0] != None:
                            cur.execute("delete from slots where guid_val = '" + sp_guid[0] + "' or obj_guid = '" + sp_guid[0] + "'")
                            cur.execute("delete from splits where guid = '" + sp_guid[0] + "'")
                    cur.execute("delete from slots where guid_val = '" + tx_guid[0] + "' or obj_guid = '" + tx_guid[0] + "'")
                    cur.execute("delete from transactions where guid = '" + tx_guid[0] + "'")

    # entries
    resp=cur.execute("select guid from entries where invoice = '" + invoice_guid + "'")
    entry_guids = resp.fetchall()
    for en_guid in entry_guids:
        if en_guid[0] != None:
            cur.execute("delete from slots where guid_val = '" + en_guid[0] + "' or obj_guid = '" + en_guid[0] + "'")
            cur.execute("delete from entries where guid = '" + en_guid[0] + "'")
            cur.execute("delete from entries where invoice = 'None'")

    # invoices
    cur.execute("delete from invoices where guid = '" + invoice_guid + "'")
    cur.execute("delete from slots where guid_val = '" + invoice_guid + "' or obj_guid = '" + invoice_guid + "'")
    
    conn.commit()
    conn.close()
    return True



