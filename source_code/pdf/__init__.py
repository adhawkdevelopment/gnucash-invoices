import sqlite3
from jinja2 import Template
import weasyprint
import db
import json
from PyQt5.QtWidgets import QMessageBox



APP_FOLDER_PATH = '/opt/gnucash-invoices/'



def create_invoice(invoice_guid, type):
    COMPANY_INFO = {}
    try:
        with open(__path__[0] + '/COMPANY_INFO.json') as file:
            COMPANY_INFO = json.load(file)
    except Exception as e:
        print('pdf.create_invoice(invoice_guid, type) open company_info.json')
        print(type(e))
        print(e.args)
        print(e) 
        return None
    
    DOCUMENT_TYPE = get_document_types()[type]


    TERMS = createTerms(type)

    if TERMS == None:
        return None
    
    invoice = db.get_invoice_by_guid(invoice_guid)

    job = db.get_job_from_invoice(invoice)

    customer = db.get_customer_from_invoice(invoice)

    billterms = db.get_billing_terms_from_invoice(invoice)

    materials_entries = db.get_materials_from_invoice(invoice)

    labor_entries = db.get_labor_from_invoice(invoice)

    if len(materials_entries) == 0 and len(labor_entries) == 0:
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle('Alert')
        msg.setText("This invoice contains no materials or labor entries!")
        msg.setInformativeText("Please enter labor or materials in GNUCash before sending to customer")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec()
        return None
    
    taxtable = []
    if len(materials_entries) > 0:
        taxtable = db.get_taxtable_from_materials(materials_entries)

    totals = {
        'materials_total': 0.00,
        'labor_total': 0.00,
        'tax_percent': 0.00,
    }


    for entry in materials_entries:
        quantity = entry['quantity_num']/entry['quantity_denom']
        unit_price = entry['i_price_num']/entry['i_price_denom']
        totals['materials_total'] = totals['materials_total'] + quantity*unit_price
    for entry in labor_entries:
        quantity = entry['quantity_num']/entry['quantity_denom']
        unit_price = entry['i_price_num']/entry['i_price_denom']
        totals['labor_total'] = totals['labor_total'] + quantity*unit_price
    if len(taxtable) > 0:
        totals['tax_percent'] = taxtable[0]['amount_num']/taxtable[0]['amount_denom']
        
    with open(__path__[0] + '/invoice_template.html') as file_:
        template = Template(file_.read())
        image = __path__[0] + '/company_logo.png'
        html_invoice = template.render(invoice=invoice, billterms=billterms, materials_entries=materials_entries, labor_entries=labor_entries, totals=totals, job=job, customer=customer, COMPANY_INFO=COMPANY_INFO, DOCUMENT_TYPE=DOCUMENT_TYPE, TERMS=TERMS, image=image)
        with open(__path__[0] + '/invoice_template.css', 'r') as f:
            weasyprint.HTML(string=html_invoice).write_pdf(APP_FOLDER_PATH + 'temp/' + invoice['id'] + ' ' + DOCUMENT_TYPE + '.pdf', stylesheets=[weasyprint.CSS(string=f.read())])
            return True
    



def createTerms(type):
    try:
        with open(__path__[0] + '/TERMS_SECTIONS.json') as file:
            TERMS_SECTIONS = json.load(file)
            
            if type == 'INVOICE': 
                return TERMS_SECTIONS['HEADER'] + '<br><br>' + TERMS_SECTIONS['DISCLAIMER'] + '<br><br>' + TERMS_SECTIONS['ADDITIONAL_TERMS']
            elif type == 'WORKORDER': 
                return TERMS_SECTIONS['HEADER'] + '<br><br>' + TERMS_SECTIONS['DISCLAIMER'] + '<br><br>' + TERMS_SECTIONS['ADDITIONAL_TERMS'] + '  ' + TERMS_SECTIONS['ALTERATIONS']
            elif type == 'SPECIALORDER': 
                return TERMS_SECTIONS['SPECIAL_ORDER'] + '<br><br>' + TERMS_SECTIONS['HEADER'] + '<br><br>' + TERMS_SECTIONS['DISCLAIMER'] + '<br><br>' + TERMS_SECTIONS['ADDITIONAL_TERMS'] + '  ' + TERMS_SECTIONS['ALTERATIONS']
            else:
                return None
    except Exception as e:
        print('pdf.createTerms(type)')
        print(type(e))
        print(e.args)
        print(e) 
        return None
    

def get_document_types():
    DOCUMENT_TYPEs = {}
    try:
        with open(__path__[0] + '/DOCUMENT_TYPES.json') as file:
            DOCUMENT_TYPEs = json.load(file)
            return DOCUMENT_TYPEs
    except Exception as e:
        print('pdf.get_document_types()')
        print(type(e))
        print(e.args)
        print(e) 
        return None
