from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QInputDialog
from PyQt5.QtGui import QIcon
import sys
import gui.Menu
import gui.Layout
import pdf
import db
import os
import gmail

APP_FOLDER_PATH = '/opt/gnucash-invoices/'
GUI_TITLE = 'GNUCash Invoice Tool'

class Window(QMainWindow):

    INVOICE = 'INVOICE'
    WORKORDER = 'WORKORDER'
    SPECIALORDER = 'SPECIALORDER'

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

       
        self.resize(800, 500)
        Layout.center(self)

        self.setWindowTitle(GUI_TITLE)
        self.setWindowIcon(QIcon('app_logo.png'))

        self.statusBar()
        self.statusBar().showMessage('Ready')
      
        Menu.config(self)
        Layout.listRecentInvoices(self)



        self.show()


    # menu actions
    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Confirmation', 'Do you want to quit?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()



    def loadInvoicesByDate(self):
        calendarDialog = Layout.CalendarDialog()
        if (calendarDialog.startDate != None) and (calendarDialog.endDate != None):
            Layout.listInvoicesByDate(self, calendarDialog.startDate, calendarDialog.endDate)
            return True
        else:
            return None


    def searchInvoices(self):
        invoice_id, submitted = QInputDialog.getText(self, "Invoice Search", "Search Invoice By ID")
        if submitted and invoice_id:
            Layout.listInvoicesByID(self, invoice_id)
            return True
        else:
            None


    def emailInvoice(self, event):
        button, parentLayout = self.selectableLayout.getSelectedRow()
        if button != None:
            for i in range(parentLayout.count()):
                if parentLayout.itemAt(i).layout() != None and parentLayout.itemAt(i).itemAt(0) != None:
                    if parentLayout.itemAt(i).itemAt(0).widget() == button:
                        reply = QMessageBox.question(self, 'Confirmation', 'Do you want to send email?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                        if reply == QMessageBox.Yes:                        
                            row = parentLayout.itemAt(i)
                            if row:
                                invoice_guid = row.itemAt(6).widget().text()
                                if invoice_guid:
                                    dialog = Layout.InvoiceTypeSelectionDialog()
                                    dialog.exec_()
                                    if dialog.selected_value != None:
                                        invoice = db.get_invoice_by_guid(invoice_guid)
                                        customer = db.get_customer_from_invoice(invoice)
                                        document_type = pdf.get_document_types()[dialog.selected_value]
                                        email_subject = invoice['id'] + ' ' + document_type
                                        filename = email_subject + '.pdf'
                                        filename_path = APP_FOLDER_PATH + 'temp/'
                                        if document_type != None:
                                            if customer['addr_email'] != '':
                                                created = pdf.create_invoice(invoice_guid, dialog.selected_value)
                                                if created == True:
                                                    gmail.sendMail(customer['addr_email'], email_subject, filename_path + filename)
                                                    os.remove(filename_path + filename)
                                                    msg = QMessageBox()
                                                    msg.setIcon(QMessageBox.Information)
                                                    msg.setWindowTitle('Success')
                                                    msg.setText("Email has been sent!")
                                                    msg.setStandardButtons(QMessageBox.Ok)
                                                    msg.exec()
                                                    return True
                                                else:
                                                    return None
                                            else:
                                                msg = QMessageBox()
                                                msg.setIcon(QMessageBox.Information)
                                                msg.setWindowTitle('Alert')
                                                msg.setText("This customer does not have an email associated with their account!")
                                                msg.setInformativeText("Please add an email in the Billing Address section of their profile in GNUCash")
                                                msg.setStandardButtons(QMessageBox.Ok)
                                                msg.exec()
                                                return None
                                        else:
                                            return None
                                    else:
                                        return None
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setWindowTitle('Alert')
            msg.setText("Invoice not found!")
            msg.setInformativeText("Internal error, have your developer investigate")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec()
            return None
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setWindowTitle('Alert')
            msg.setText("Invoice not selected!")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec()
            return None

    def chargeCard(self, event):
        return None


    def syncDB(self, event):
        return None


    def showPreview(self):
        button, parentLayout = self.selectableLayout.getSelectedRow()
        if button != None:
            for i in range(parentLayout.count()):
                if parentLayout.itemAt(i).layout() != None and parentLayout.itemAt(i).itemAt(0) != None:
                    if parentLayout.itemAt(i).itemAt(0).widget() == button:
                        row = parentLayout.itemAt(i)
                        if row:
                            invoice_id = row.itemAt(1).widget().text()
                            invoice_guid = row.itemAt(6).widget().text()
                            if invoice_guid:
                                dialog = Layout.InvoiceTypeSelectionDialog()
                                dialog.exec_()
                                filename = invoice_id + ' ' + pdf.DOCUMENT_TYPES[dialog.selected_value] + '.pdf'
                                if dialog.selected_value != None:
                                    pdf.create_invoice(invoice_guid, dialog.selected_value)
                                    os.system('evince ' + '"' + APP_FOLDER_PATH + 'temp/' + filename + '"')
                                    os.remove('"' + APP_FOLDER_PATH + 'temp/' + filename + '"')
                                    return True
                                else:
                                    return None

            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setWindowTitle('Alert')
            msg.setText("Invoice not found!")
            msg.setInformativeText("Internal error, have your developer investigate")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec()
            return None
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setWindowTitle('Alert')
            msg.setText("Invoice not selected!")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec()
            return None
    
    def deleteInvoice(self):    
        button, parentLayout = self.selectableLayout.getSelectedRow()
        if button != None:
            reply = QMessageBox.question(self, 'Message', 'DO YOU WANT TO DELETE THIS INVOICE?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                    invoice_guid = self.selectableLayout.deleteSelectedRow()
                    deleted = db.delete_invoice(invoice_guid)
                    if deleted == True:
                        return True
                    else:
                        return None
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setWindowTitle('Alert')
            msg.setText("Invoice not selected!")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec()
            return None
                
            
    

    # helper fxnw
    def invoiceTypeClick(self):
        return self.text()


    def toggleStatusBar(self, state):
            if state:
                self.statusBar().show()
            else:
                self.statusBar().hide()    



def create():
    app = QApplication(sys.argv)
    
    window =  Window()

    sys.exit(app.exec_())
    
