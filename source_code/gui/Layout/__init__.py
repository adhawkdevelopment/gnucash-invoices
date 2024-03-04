from PyQt5.QtWidgets import QDesktopWidget, QWidget, QFrame, QLabel, QVBoxLayout, QHBoxLayout, QScrollArea, QPushButton, QDialog, QCalendarWidget, QMessageBox
from PyQt5.QtCore import Qt, QDate

import db
from datetime import date, timedelta


def listInvoicesByDate(self, startDate, endDate):
    invoices = db.get_invoices_within_date_range(startDate, endDate)
    self.selectableLayout = SelectableVBoxLayout(invoices)
    scroll = CustomScrollArea()
    scroll.setWidget(self.selectableLayout)
    self.setCentralWidget(scroll)


def listInvoicesByID(self, invoice_id):
    invoices = db.get_invoices_by_id(invoice_id)
    self.selectableLayout = SelectableVBoxLayout(invoices)
    scroll = CustomScrollArea()
    scroll.setWidget(self.selectableLayout)
    self.setCentralWidget(scroll)


def listRecentInvoices(self):
    invoices = db.get_recent_invoices()
    self.selectableLayout = SelectableVBoxLayout(invoices)
    scroll = CustomScrollArea()
    scroll.setWidget(self.selectableLayout)
    self.setCentralWidget(scroll)
    

def center(self):
    qr = self.frameGeometry()
    cp = QDesktopWidget().availableGeometry().center()
    qr.moveCenter(cp)
    self.move(qr.topLeft())




class SelectableVBoxLayout(QWidget):
    def __init__(self, invoices):
        super().__init__()

        # Initialize the layout
        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)

        row = QHBoxLayout()

        selected_label = QLabel('')
        selected_label.setFixedWidth(30)


        invoice_num_label = QLabel('Invoice #', self)
        invoice_num_label.setFixedWidth(120)


        date_created_label = QLabel('Date Created', self)
        date_created_label.setFixedWidth(100)


        date_posted_label = QLabel('Date Posted', self)
        date_posted_label.setFixedWidth(100)

        customer_label = QLabel('Company', self)
        customer_label.setFixedWidth(300)

        job_label = QLabel('Job', self)
        job_label.setFixedWidth(400)

        guid_label = QLabel('Invoice GUID', self)
        guid_label.setFixedWidth(300)

        row.addWidget(selected_label)
        row.addWidget(invoice_num_label)
        row.addWidget(date_created_label)
        row.addWidget(date_posted_label)
        row.addWidget(customer_label)
        row.addWidget(job_label)
        row.addWidget(guid_label)
        
        row.setAlignment(Qt.AlignLeft)

        self.layout.addLayout(row)
        

        self.buttons = []
        self.frames = []

        # Add buttons
        if invoices == None:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setWindowTitle('Alert')
            msg.setText("No invoices in range!")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec()
            return None
        elif len(invoices) == 0:
            deviding_line = QFrame()
            deviding_line.setFrameShape(QFrame.HLine)
            self.layout.addWidget(deviding_line)
        else:
            for i in range(0, len(invoices)):
                invoice = invoices[i]

                row = QHBoxLayout()

                invoice_id = QLabel(invoice['id'])
                invoice_id.setFixedWidth(120)
                invoice_date_created = QLabel(invoice['date_opened'].split(' ')[0])
                invoice_date_created.setFixedWidth(100)

                date_posted = ''
                if invoice['date_posted'] != None:
                    date_posted = invoice['date_posted'].split(' ')[0]
                
                invoice_date_posted = QLabel(date_posted)
                invoice_date_posted.setFixedWidth(100)

                customer = QLabel(db.get_customer_from_invoice(invoice)['name'])
                customer.setFixedWidth(300)
                
                job = QLabel('')

                job_in_invoice = db.get_job_from_invoice(invoice)
                if job_in_invoice != None:
                    job = QLabel(job_in_invoice['name'])

                job.setFixedWidth(400)

                invoice_guid = QLabel(invoice['guid'])
                invoice_guid.setFixedWidth(300)

                button = QPushButton(f"")
                button.setCheckable(True)  # Make buttons selectable
                button.setMaximumWidth(30)
                self.buttons.append(button)

                
                
                row.addWidget(button)

                row.addWidget(invoice_id)
                row.addWidget(invoice_date_created)
                row.addWidget(invoice_date_posted)
                row.addWidget(customer)
                row.addWidget(job)
                row.addWidget(invoice_guid)

                row.setAlignment(Qt.AlignLeft)
                
                deviding_line = QFrame()
                deviding_line.setFrameShape(QFrame.HLine)
                self.frames.append(deviding_line)
                self.layout.addWidget(deviding_line)
                self.layout.addLayout(row)

            # Connect button signals
            for button in self.buttons:
                button.toggled.connect(self.onButtonToggled)


    def onButtonToggled(self, checked):
        sender = self.sender()
        if checked:
            sender.setText('✓')
            # Deselect other buttons
            for button in self.buttons:
                if button != sender:
                    button.setChecked(False)
                    button.setText('')
        else:
            sender.setText('')


    def getSelectedRow(self):
        for button in self.buttons:
            if button.isChecked():
                parentLayout = button.parentWidget().layout
                return button, parentLayout
        return None, None
    
    
    def deleteSelectedRow(self):
        invoice_guid = ''
        for i, button in enumerate(self.buttons):
            if button.isChecked():
                # Remove the corresponding row and button
                frame = self.layout.itemAt(i*2 + 1)  # Skip the first row (labels)
                item = self.layout.itemAt(i*2 + 2)  # Skip the first row (labels)
                if frame is not None:
                    if frame.widget() is not None:
                        INVOICE_GUID_INDEX = 6
                        invoice_guid = item.layout().itemAt(INVOICE_GUID_INDEX).widget().text()
                        for j in range(item.layout().count()):
                            item.layout().itemAt(j).widget().deleteLater()
                            
                        self.layout.removeItem(item)
                        self.layout.removeItem(frame)
                        button.deleteLater()
                        frame.widget().deleteLater()
                        self.buttons.pop(i)
                        self.frames.pop(i)
                return invoice_guid
        return None
    
        

class CalendarDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.startDate = None
        self.endDate = None

        self.setWindowTitle("Select Date Range")
        self.layout = QVBoxLayout()

        today = str(date.today()).split('-')
        tomorrow = str(date.today()+ timedelta(1)).split('-')

        startLabel = QLabel('Start Date')
        startLabel.setGeometry(0, 0, 900, 50)
        startLabel.setAlignment(Qt.AlignCenter)

        startCalendar = QCalendarWidget(self)
        startCalendar.setGeometry(0, 50, 900, 600)
        startCalendar.setSelectedDate(QDate(int(today[0]), int(today[1]), int(today[2])))
        
        endLabel = QLabel('End Date')
        endLabel.setGeometry(920, 0, 900, 50)
        endLabel.setAlignment(Qt.AlignCenter)
        endCalendar = QCalendarWidget(self)
        endCalendar.setGeometry(920, 50, 900, 600)
        endCalendar.setSelectedDate(QDate(int(tomorrow[0]), int(tomorrow[1]), int(tomorrow[2])))
        
        btn = QPushButton(self)
        btn.setText("Submit")
        btn.move(920, 600)
        btn.clicked.connect(self.submitclose)

        self.layout.addWidget(startLabel)
        self.layout.addWidget(startCalendar)
        self.layout.addWidget(endLabel)
        self.layout.addWidget(endCalendar)
        self.layout.addWidget(btn)
        self.setLayout(self.layout)

        self.exec()

    def submitclose(self):
        self.startDate = self.layout.itemAt(1).widget().selectedDate().toString('yyyy-MM-dd')
        self.endDate = self.layout.itemAt(3).widget().selectedDate().toString('yyyy-MM-dd')
        self.accept()




class InvoiceTypeSelectionDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.selected_value = None

        self.initUI()

    def initUI(self):

        self.setWindowTitle('Document Type Selection')
        layout = QHBoxLayout()

        button1 = QPushButton("Invoice", self)
        button1.clicked.connect(lambda: self.setAndClose("INVOICE"))
        layout.addWidget(button1)

        button1 = QPushButton("Work Order", self)
        button1.clicked.connect(lambda: self.setAndClose("WORKORDER"))
        layout.addWidget(button1)

        button1 = QPushButton("Special Order", self)
        button1.clicked.connect(lambda: self.setAndClose("SPECIALORDER"))
        layout.addWidget(button1)

        self.setLayout(layout)

    def setAndClose(self, value):
            self.selected_value = value
            self.accept()




class CustomScrollArea(QScrollArea):
    def __init__(self):
            super().__init__() 
            self.setGeometry(0,0, 200, 400)
            self.setWidgetResizable(False)
            self.setAlignment(Qt.AlignTop)
