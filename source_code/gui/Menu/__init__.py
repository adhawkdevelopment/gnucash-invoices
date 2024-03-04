from PyQt5.QtWidgets import QAction, qApp




def config(self):


    menubar = self.menuBar()

    ## create file menu
    # exit
    exitAct = QAction('Exit', self)
    exitAct.setShortcut('Ctrl+Q')
    exitAct.setStatusTip('Exit Application')
    exitAct.triggered.connect(qApp.quit)

    # create menu and add actions
    fileMenu = menubar.addMenu('File')
    fileMenu.addAction(exitAct)


    ## create invoice menu
    # load invoice date range
    loadAct = QAction('Load Invoices', self)
    loadAct.setStatusTip('Load Invoices Within Date Range')
    loadAct.triggered.connect(self.loadInvoicesByDate)

    # search invoice id
    searchAct = QAction('Search Invoice', self)
    searchAct.setStatusTip('Search For Invoice By ID')
    searchAct.triggered.connect(self.searchInvoices)

    # show invoice details
    showAct = QAction('Show Preview', self)
    showAct.setStatusTip('Show Print Preview of Invoice')
    showAct.triggered.connect(self.showPreview)

    # email invoice to address on file
    emailAct = QAction('Email Invoice', self)
    emailAct.setStatusTip('Email Invoice To Client')
    emailAct.triggered.connect(self.emailInvoice)

    # delete invoice
    deleteAct = QAction('Delete Invoice', self)
    deleteAct.setStatusTip('Delete Invoice From Database')
    deleteAct.triggered.connect(self.deleteInvoice)


    # create menu and add actions
    invoiceMenu = menubar.addMenu('Invoice')
    invoiceMenu.addAction(loadAct)
    invoiceMenu.addAction(searchAct)
    invoiceMenu.addAction(showAct)
    invoiceMenu.addAction(emailAct)
    invoiceMenu.addAction(deleteAct)

    
    ## create view menu
    # toggle status bar
    viewStatAct = QAction('View Statusbar', self, checkable=True)
    viewStatAct.setStatusTip('View Statusbar')
    viewStatAct.setChecked(True)
    # requires toggleStatusBar to be defined in parent __init__.py file
    viewStatAct.triggered.connect(self.toggleStatusBar)

    # create menu and add actions
    viewMenu = menubar.addMenu('View')
    viewMenu.addAction(viewStatAct)


