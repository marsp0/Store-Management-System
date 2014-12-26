#!usr/bin/python

#imports
import Tkinter as tk
import tkMessageBox as mb
import tkFileDialog as fd
import ttk as ttk
import decimal
import shelve
import time
import fpdf

class Product(object):
	''' Product object containing:
		-name 
		-price
		-idNumber
		-quantity
		-unit / measurement unit
		-case / how much of that unit is in 1 case  
		'''
	def __init__(self, name = '?',price = 0.00,vendor = '?',idNumber = 0, quantity = 0,unit = '', case = 0 ):
		self.name = name
		self._price = price
		self._id = idNumber
		self._quantity = quantity
		self.unit = unit
		self._case = case

	@property
	def price(self):
		return self._price

	@price.setter
	def price(self,value):
		self._price = value

	@property
	def idNumber(self):
		return self._id

	@idNumber.setter
	def idNumber(self,value):
		self._id = value

	@property
	def quantity(self):
		return self._quantity

	@quantity.setter
	def quantity(self, value):
		self._quantity = value

	@property
	def case(self):
		return self._case

	@case.setter
	def case(self,value):
		self._case = value

	def __str__(self):
		return '%s - %s' % (self.idNumber, self.name)

class Vendor(object):
	def __init__(self, name='?', address = '?', idNumber = None):
		self._name = name
		self._address = address
		self._id = idNumber

	@property
	def name(self):
		return self._name

	@name.setter
	def name(self, value):
		self._name = value

	@property
	def address(self):
		return self._address

	@address.setter
	def address(self,value):
		self._address = value

	@property
	def idNumber(self):
		return self._id

	def __str__(self):
		return '%s' % self.name

class Order(object):

	def __init__(self,idNumber = 0, vendor = '?', date = '',products = [],total = 0):
		self.id = idNumber
		self.vendor = vendor
		self.products = products
		self.date = date
		self.total = total

class Main(tk.Frame):

	def __init__(self,filename, parent = None, *args, **kwargs):
		#init the parent frame with the args passed to the constructor
		tk.Frame.__init__(self,	parent, *args, **kwargs)
		self.filename = filename
		self.startDatabase()

		#make the window not resizable and pack it
		self.master.minsize(width = 600, height=400)
		self.master.maxsize(width=600, height = 400)
		self.pack()

		#main display
		self.mainDisplay = tk.Frame(self)

		self.main()

		#PRODUCT VARS
		self.productDisplay = tk.Frame(self)
		self.addProductDisplay = tk.Frame(self)
		self.editProductDisplay =tk.Frame(self)
		self.viewDisplay = tk.Frame(self)
		self.deleteView = tk.Frame(self)
		self.queryProductID = tk.IntVar()
		self.productOptions = ('ID','Name','Price','Unit','Quantity','Case')
		self.productVars = dict([('id',tk.IntVar()),('name',tk.StringVar()),('price',tk.DoubleVar()),('unit',tk.StringVar()),('quantity',tk.IntVar()),('case',tk.IntVar())])


		#ORDER VARS
		self.orderDisplay = tk.Frame(self)
		self.addOrderDisplay = tk.Frame(self)
		self.viewOrderDisplay = tk.Frame(self)
		self.orderHistoryDisplay = tk.Frame(self)
		self.makeOrderDisplay = tk.Frame(self)
		self.OrderVars = dict([('vendor', tk.StringVar()),('id',tk.IntVar()),('date',tk.StringVar())])
		self.OrderOptions = ('id','vendor','products','date')
		self.viewOrderDate = tk.StringVar()
		self.viewOrderMode = tk.IntVar()


		self.vendorDisplay = tk.Frame(self)
		self.addVendorDisplay = tk.Frame(self)
		self.deleteVendorDisplay = tk.Frame(self)
		self.viewVendorDisplay = tk.Frame(self)
		self.viewVendorAll = tk.Frame(self)
		self.vendorVars = dict([('name',tk.StringVar()),('address',tk.StringVar()),('id',tk.IntVar())])
		self.vendorID = tk.IntVar()

		#REPORTS VARS
		self.reportsDisplay = tk.Frame(self)
		self.inventoryDisplay = tk.Frame(self)

	''' FUNTIONALITIES '''

	def startDatabase(self):
		database = shelve.open(self.filename)
		if database:
			self.products = database['products']
			self.orders = database['orders']
			self.vendors = database['vendors']
			self.makeOrders = database['makeOrders']
		else:
			self.products = {}
			self.orders = {}
			self.makeOrders = {}
			self.vendors = {}
		database.close()

	def quit(self):
		database = shelve.open(self.filename)
		database['products'] = self.products
		database['orders'] = self.orders
		database['vendors'] = self.vendors
		database['makeOrders'] = self.makeOrders
		database.close()
		self.master.destroy()

	def packer(self, unpacked, packed = None,third = None,option = None, orderID = None):
		unpacked.pack_forget()
		for child in unpacked.winfo_children():
			child.destroy()
		if packed:
			if orderID:
				packed(orderID)
			else:
				packed()
		if option:
			self.clearVars(option)

	def clearVars(self,option):
		if option == 1:
			for key in self.productVars:
				self.productVars[key].set('')
		if option == 2:
			for key in self.vendorVars:
				self.vendorVars[key].set('')
		if option == 3:
			for key in self.OrderVars:
				self.OrderVars[key].set('')

	def main(self):
		self.mainDisplay.pack()
		tk.Button(self.mainDisplay, text='Quit', command = self.quit).grid(row=0,column = 3)
		tk.Button(self.mainDisplay, text='Products', command = lambda: self.packer(self.mainDisplay, self.productView) ).grid(row=0,column = 0)
		tk.Button(self.mainDisplay, text='Orders', command = lambda : self.packer(self.mainDisplay,self.orderMain)).grid(row=0,column = 1)
		tk.Button(self.mainDisplay, text='Reports', command = lambda: self.packer(self.mainDisplay, self.mainReports) ).grid(row=0,column = 2)

	''' PRODUCTS '''

	def productView(self):
		self.productDisplay.pack()
		tk.Button(self.productDisplay, text='Add Product', command = lambda : self.packer(self.productDisplay, self.addProduct) ).grid(row=0,column = 0)
		tk.Button(self.productDisplay, text='Edit Product', command = lambda: self.packer(self.productDisplay, self.editProduct) ).grid(row=0,column = 1)
		tk.Button(self.productDisplay, text='Delete Product', command = lambda : self.packer(self.productDisplay,self.deleteProduct)  ).grid(row=0,column = 2)
		tk.Button(self.productDisplay, text='View Product', command = lambda: self.packer(self.productDisplay,self.viewProduct) ).grid(row=0,column = 3)
		tk.Button(self.productDisplay, text='Back', command = lambda : self.packer(self.productDisplay,self.main) ).grid(row=0,column = 4)

	def addProduct(self):
		self.addProductDisplay.pack()
		tk.Button(self.addProductDisplay, text='Save', command = self.saveProduct ).grid(row=len(self.productOptions),column = 1)
		tk.Button(self.addProductDisplay, text='Cancel', command = lambda : self.packer(self.addProductDisplay,self.productView) ).grid(row=len(self.productOptions),column = 0)
		for i in xrange(len(self.productOptions)):
			tk.Label(self.addProductDisplay, text = self.productOptions[i]).grid(row=i, column=0)
			tk.Entry(self.addProductDisplay, textvariable = self.productVars[self.productOptions[i].lower()]).grid(row=i,column = 1)

	def saveProduct(self):
		try:
			p = Product()
			p.name = self.productVars['name'].get()
			p.idNumber = self.productVars['id'].get()
			p.price = self.productVars['price'].get()
			p.quantity = self.productVars['quantity'].get()
			p.unit = self.productVars['unit'].get()
			p.case = self.productVars['case'].get()
			self.clearVars(1)
			if p.idNumber in self.products.keys():
				mb.showwarning('ID taken','There is a product with that ID')
				
			else:
				self.products[p.idNumber] = p
				self.packer(self.addProductDisplay,self.productView)
		except ValueError: 
			mb.showwarning('Error','Price,ID,Quantity and Units per Case have to be numbers')

	def editSave(self,product):
		product.name = self.productVars['name'].get()
		product.quantity = self.productVars['quantity'].get()
		product.price = self.productVars['price'].get()
		product.unit = self.productVars['unit'].get()
		product.case = self.productVars['case'].get()
		self.clearVars(1)
		self.packer(self.editProductDisplay, self.productView)


	def editProduct(self):
		self.editProductDisplay1 = tk.Frame(self.editProductDisplay)
		self.editProductDisplay2 = tk.Frame(self.editProductDisplay)
		self.editProductDisplay.pack()
		self.editProductDisplay1.pack()
		tk.Entry(self.editProductDisplay1,textvariable = self.queryProductID).grid(row=0,columnspan=2)
		tk.Button(self.editProductDisplay1, text='Search', command = self.searchID ).grid(row=1,column = 1)
		tk.Button(self.editProductDisplay1, text='Cancel', command = lambda : self.packer(self.editProductDisplay,self.productView,option = 1) ).grid(row=1,column = 0)

	def searchID(self):
		try:
			product = self.products[self.queryProductID.get()]
			self.editProductDisplay2.pack()
			self.productVars['name'].set(product.name)
			self.productVars['price'].set(product.price)
			self.productVars['quantity'].set(product.quantity)
			self.productVars['unit'].set(product.unit)
			self.productVars['case'].set(product.case)
			tk.Label(self.editProductDisplay2, text = 'Name').grid(row=1,column = 0)
			tk.Entry(self.editProductDisplay2, textvariable = self.productVars['name']).grid(row=1,column=1)
			tk.Label(self.editProductDisplay2, text = 'Price').grid(row=2,column = 0)
			tk.Entry(self.editProductDisplay2, textvariable = self.productVars['price']).grid(row=2,column=1)
			tk.Label(self.editProductDisplay2, text = 'Quantity').grid(row=3,column = 0)
			tk.Entry(self.editProductDisplay2, textvariable = self.productVars['quantity']).grid(row=3,column=1)
			tk.Label(self.editProductDisplay2, text = 'Unit').grid(row=4,column = 0)
			tk.Entry(self.editProductDisplay2, textvariable = self.productVars['unit']).grid(row=4,column=1)
			tk.Label(self.editProductDisplay2, text = 'Case').grid(row=5,column = 0)
			tk.Entry(self.editProductDisplay2, textvariable = self.productVars['case']).grid(row=5,column=1)
			tk.Button(self.editProductDisplay2, text='Save', command = lambda: self.editSave(product)).grid(row=6,columnspan=2)
		except KeyError:
			mb.showwarning('Not Found', 'No such product in the database')

	def viewProduct(self):
		self.viewDisplay2 = tk.Frame(self.viewDisplay)
		self.viewDisplay1 = tk.Frame(self.viewDisplay)
		self.viewDisplay.pack()
		self.viewDisplay1.pack()
		self.viewDisplay2.pack()
		self.queryProductID.set(0)
		self.idNumber = tk.Label(self.viewDisplay2, textvariable = self.productVars['id'],width = 5)
		self.name = tk.Label(self.viewDisplay2, textvariable = self.productVars['name'],width = 20)
		self.price = tk.Label(self.viewDisplay2,textvariable=self.productVars['price'],width = 15)
		self.unit = tk.Label(self.viewDisplay2,textvariable = self.productVars['unit'],width = 5)
		self.quantity = tk.Label(self.viewDisplay2,textvariable = self.productVars['quantity'],width = 15)
		self.case = tk.Label(self.viewDisplay2,textvariable=self.productVars['case'],width = 10)
		tk.Entry(self.viewDisplay1, textvariable = self.queryProductID).grid(row=0,columnspan=2)
		tk.Button(self.viewDisplay1,text = 'Search',command = self.searchViewProduct).grid(row=1,column=1)
		tk.Button(self.viewDisplay1,text= 'Cancel',command = lambda: self.packer(self.viewDisplay, self.productView, option=1)).grid(row=1,column=0)


	def searchViewProduct(self):
		try:
			product = self.products[self.queryProductID.get()]
			for i in xrange(len(self.productOptions)):
				tk.Label(self.viewDisplay2, text = self.productOptions[i]).grid(row=1,column=i)
			self.productVars['id'].set(product.idNumber)
			self.idNumber.grid(row=2,column=0)
			self.productVars['name'].set(product.name)
			self.name.grid(row=2,column=1)
			self.productVars['price'].set(product.price)
			self.price.grid(row=2,column=2)
			self.productVars['unit'].set(product.unit)
			self.unit.grid(row=2,column=3)
			self.productVars['quantity'].set(product.quantity)
			self.quantity.grid(row=2,column=4)
			self.productVars['case'].set(product.case)
			self.case.grid(row=2,column=5)
		except KeyError:
			mb.showwarning('Not Found', 'No such product in the database')


	def deleteProduct(self):
		self.deleteView.pack()
		self.queryProductID.set(0)
		tk.Entry(self.deleteView, textvariable = self.queryProductID).grid(row=0,columnspan=2)
		tk.Button(self.deleteView, text = 'Delete', command = lambda: self.deleteProductID(self.queryProductID.get())).grid(row=1,column=1)
		tk.Button(self.deleteView, text = 'Cancel',command = lambda: self.packer(self.deleteView, self.productView)).grid(row=1,column=0)

	def deleteProductID(self,key):
		try:
			del self.products[key]
			self.packer(self.deleteView, self.productView)
		except KeyError:
			mb.showwarning('Not Found', 'No such product in the database')


	''' ORDERS '''
	def orderMain(self):
		self.orderDisplay.pack()
		tk.Button(self.orderDisplay, text='Incoming Order', command = lambda : self.packer(self.orderDisplay, self.addOrder)).grid(row=0,column = 0)
		tk.Button(self.orderDisplay, text='View Order', command = lambda : self.packer(self.orderDisplay,self.viewOrder) ).grid(row=0,column = 1)
		tk.Button(self.orderDisplay,text = 'Outgoing Order',command = lambda: self.packer(self.orderDisplay,self.makeOrder)).grid(row=0,column = 2)
		tk.Button(self.orderDisplay, text='Order History', command = lambda : self.packer(self.orderDisplay,self.orderHistory) ).grid(row=0,column = 3)
		tk.Button(self.orderDisplay,text = 'Vendors',command = lambda: self.packer(self.orderDisplay,self.vendorShow)).grid(row=0,column=4)
		tk.Button(self.orderDisplay, text='Back', command = lambda : self.packer(self.orderDisplay,self.main) ).grid(row=0,column = 5)

	def addOrder(self):
		self.orderMiniDisplay = tk.Frame(self.addOrderDisplay)
		self.orderMiniDisplay2 = tk.Frame(self.addOrderDisplay)
		self.addOrderDisplay.pack()
		self.orderMiniDisplay.pack()
		self.orderProducts = []
		row = 2
		tk.Label(self.orderMiniDisplay, text = 'Vendor').grid(row=0,column = 1)
		tk.Entry(self.orderMiniDisplay, textvariable = self.OrderVars['vendor'],width = 10).grid(row=0,column=2)
		tk.Label(self.orderMiniDisplay, text = 'ID').grid(row=0,column = 3)
		tk.Entry(self.orderMiniDisplay, textvariable = self.OrderVars['id'],width = 10).grid(row=0,column = 4)
		tk.Label(self.orderMiniDisplay, text = 'Date').grid(row=0,column = 5)
		tk.Entry(self.orderMiniDisplay, textvariable = self.OrderVars['date'],width = 10).grid(row=0,column = 6)
		tk.Button(self.orderMiniDisplay,text = 'Save',command = self.saveOrder).grid(row=0,column=7)
		tk.Button(self.orderMiniDisplay,text = 'Cancel',command = lambda: self.packer(self.addOrderDisplay,self.orderMain)).grid(row=0,column=8)

		
		tk.Label(self.orderMiniDisplay2,text = 'ID').grid(row=1,column = 1)
		tk.Label(self.orderMiniDisplay2,text = 'Name',width = 40).grid(row=1,column = 2)
		tk.Label(self.orderMiniDisplay2,text = 'Price',width = 10).grid(row=1,column = 3)
		tk.Label(self.orderMiniDisplay2,text = 'Case').grid(row=1,column = 4)
		self.buildField(row)

	def buildField(self,row):
		idvar = tk.IntVar()
		qvar= tk.IntVar()
		self.orderProducts.append((idvar,qvar))
		self.orderMiniDisplay2.pack()
		self.mini_dict = {'name':tk.StringVar(), 'price':tk.StringVar()}
		tk.Entry(self.orderMiniDisplay2,textvariable = idvar,width = 5).grid(row= row,column = 1)
		tk.Label(self.orderMiniDisplay2, textvariable = self.mini_dict['name'],text = '').grid(row=row, column=2)
		tk.Label(self.orderMiniDisplay2,textvariable = self.mini_dict['price'],text = '').grid(row=row,column=3)
		tk.Entry(self.orderMiniDisplay2,textvariable = qvar,width = 5).grid(row=row,column=4)
		row += 1
		self.addbutton = tk.Button(self.orderMiniDisplay2,text = 'Add', command=lambda: self.orderSearchID(row,self.addbutton,1))
		self.addbutton.grid(row=row-1,column=6)

	def orderSearchID(self,row,addbutton,option):
		try:
			product = self.products[self.orderProducts[-1][0].get()]
			self.mini_dict['name'].set(product.name)
			self.mini_dict['price'].set(product.price)
			addbutton.destroy()
			if option == 1:
				self.buildField(row)
			else:
				self.makeBuildField(row)
		except KeyError:
			mb.showwarning('Invalid ID', 'The ID entered is invalid')

	def saveOrder(self):
		products = []
		total = 0
		for i in xrange(len(self.orderProducts)-1):
			product = self.products[self.orderProducts[i][0].get()]
			product.quantity += self.orderProducts[i][1].get()*product.case
			products.append((self.orderProducts[i][0].get(),product.price, self.orderProducts[i][1].get()))
		vendor = self.OrderVars['vendor'].get()
		idOrder = self.OrderVars['id'].get()
		date = self.OrderVars['date'].get()
		for (key,price,quant) in products:
			total += price*quant
		order = Order(idNumber = idOrder, vendor = vendor, date = date, products = products,total = total)
		self.orders[date] = order
		self.packer(self.addOrderDisplay, self.orderMain,option = 3)

	def viewOrder(self):
		self.viewOrderDisplay1 = tk.Frame(self.viewOrderDisplay)
		self.viewOrderDisplay3 = tk.Frame(self.viewOrderDisplay)
		self.viewOrderDisplay2 = tk.Frame(self.viewOrderDisplay)
		self.viewOrderDisplay.pack()
		self.viewOrderDisplay1.pack()
		tk.Entry(self.viewOrderDisplay1, textvariable = self.viewOrderDate).grid(row=0,columnspan=2)
		tk.Radiobutton(self.viewOrderDisplay1,text = 'Incoming', variable = self.viewOrderMode,value = 0).grid(row=1,column=0)
		tk.Radiobutton(self.viewOrderDisplay1,text = 'Outgoing', variable = self.viewOrderMode,value = 1).grid(row=1,column=1)
		tk.Button(self.viewOrderDisplay1, text = 'Cancel',command = lambda : self.packer(self.viewOrderDisplay,self.orderMain)).grid(row=2,column=0)
		tk.Button(self.viewOrderDisplay1,text = 'Search',command = self.viewOrderSearch).grid(row = 2,column = 1)

	def viewOrderSearch(self,orderID = None):
		try:
			if orderID:
				if self.viewOrderMode.get() == 0:
					order = self.orders[orderID]
				else:
					order = self.makeOrders[orderID]
				self.viewOrderDisplay.pack()
			else:
				if self.viewOrderMode.get() == 0:
					order = self.orders[self.viewOrderDate.get()]
				else:
					order = self.makeOrders[self.viewOrderDate.get()]
			try:
				if self.viewOrderDisplay2.winfo_children(): 
					for child in self.viewOrderDisplay2.winfo_children():
						child.destroy()
					for child in self.viewOrderDisplay3.winfo_children():
						child.destroy()
			except:
				self.viewOrderDisplay2 = tk.Frame(self.viewOrderDisplay)
				self.viewOrderDisplay3 = tk.Frame(self.viewOrderDisplay)
				tk.Button(self.viewOrderDisplay3, text = 'Back',command = lambda : self.packer(self.viewOrderDisplay, self.orderHistory)).grid(row=0,column=7)
			self.viewOrderDisplay3.pack()
			self.viewOrderDisplay2.pack()
			tk.Label(self.viewOrderDisplay3, text = 'ID: ').grid(row=0,column=1)
			tk.Label(self.viewOrderDisplay3,text = order.id).grid(row=0,column=2)
			tk.Label(self.viewOrderDisplay3, text = 'Vendor: ').grid(row=0,column=3)
			tk.Label(self.viewOrderDisplay3,text = order.vendor).grid(row=0,column=4)
			tk.Label(self.viewOrderDisplay3, text = 'Date: ').grid(row=0,column=5)
			tk.Label(self.viewOrderDisplay3,text = order.date).grid(row=0,column=6)
			for i in xrange(len(self.productOptions)):
				tk.Label(self.viewOrderDisplay2, text = self.productOptions[i]).grid(row=1, column = i)
			row = 2
			for (key,price,quant) in order.products:
				product = self.products[key]
				tk.Label(self.viewOrderDisplay2, text = product.idNumber,width = 5).grid(row=row, column=0)
				tk.Label(self.viewOrderDisplay2,text = product.name, width = 20).grid(row=row,column=1)
				tk.Label(self.viewOrderDisplay2,text = price,width = 15).grid(row=row,column=2)
				tk.Label(self.viewOrderDisplay2,text = product.unit,width = 5).grid(row=row,column=3)
				tk.Label(self.viewOrderDisplay2,text = quant,width = 15).grid(row=row,column=4)
				tk.Label(self.viewOrderDisplay2,text = product.case, width =10).grid(row=row,column=5)
				row += 1

		except KeyError:
			mb.showwarning('Not Found', 'The format of the date should be dd.mm.yyyy')

	def orderHistory(self):
		self.orderHistoryDisplay.pack()
		row = 1
		self.orderHistoryDisplay1 = tk.Frame(self.orderHistoryDisplay)
		self.orderHistoryDisplay2 = tk.Frame(self.orderHistoryDisplay)
		self.orderHistoryDisplay1.pack()
		self.orderHistoryDisplay2.pack()
		tk.Radiobutton(self.orderHistoryDisplay1,text = 'Incoming', variable = self.viewOrderMode,value = 0).grid(row=0,column=0)
		tk.Radiobutton(self.orderHistoryDisplay1,text = 'Outgoing', variable = self.viewOrderMode,value = 1).grid(row=0,column=1)
		tk.Button(self.orderHistoryDisplay1, text= 'Fetch',command = lambda : self.fetchHistory(row)).grid(row=1,column=1)
		tk.Button(self.orderHistoryDisplay1,text = 'Back',command = lambda : self.packer(self.orderHistoryDisplay, self.orderMain)).grid(row=1,column=0)

	def fetchHistory(self,row):
		if self.orderHistoryDisplay2.winfo_children():
			for child in self.orderHistoryDisplay2.winfo_children():
				child.destroy()
		tk.Label(self.orderHistoryDisplay2, text = 'ID',width = 15).grid(row=0,column=1)
		tk.Label(self.orderHistoryDisplay2, text = 'Vendor',width = 15).grid(row=0,column=2)
		tk.Label(self.orderHistoryDisplay2, text = 'Date',width = 15).grid(row=0,column=3)
		tk.Label(self.orderHistoryDisplay2,text = 'Total',width = 15).grid(row=0,column=4)
		if self.viewOrderMode.get() == 0:
			for order in self.orders:
				tk.Label(self.orderHistoryDisplay2, text = self.orders[order].id,width = 15).grid(row=row,column=1)
				tk.Label(self.orderHistoryDisplay2,text = self.orders[order].vendor,width = 15).grid(row=row,column=2)
				tk.Label(self.orderHistoryDisplay2,text = self.orders[order].date,width = 15).grid(row=row,column=3)
				tk.Label(self.orderHistoryDisplay2,text = self.orders[order].total,width = 15).grid(row=row,column=4)
				tk.Button(self.orderHistoryDisplay2,text ='View',command = lambda order = order: self.fetchOrder(order)).grid(row=row,column=5)
				row+=1
		else:
			for order in self.makeOrders:
				tk.Label(self.orderHistoryDisplay2, text = self.makeOrders[order].id,width = 15).grid(row=row,column=1)
				tk.Label(self.orderHistoryDisplay2,text = self.makeOrders[order].vendor,width = 15).grid(row=row,column=2)
				tk.Label(self.orderHistoryDisplay2,text = self.makeOrders[order].date,width = 15).grid(row=row,column=3)
				tk.Label(self.orderHistoryDisplay2,text = self.makeOrders[order].total,width = 15).grid(row=row,column=4)
				tk.Button(self.orderHistoryDisplay2,text ='View',command = lambda order = order: self.fetchOrder(order)).grid(row=row,column=5)
				tk.Button(self.orderHistoryDisplay2,text ='Export',command = lambda order = order: self.exportOrder(order)).grid(row=row,column=6)
				row+=1

	def exportOrder(self,order):
		order = self.makeOrders[order]
		filename = fd.asksaveasfilename()
		out = fpdf.FPDF(format='letter')
		out.add_page()
		out.set_font('Arial',size=10)
		out.cell(200,8,'Vendor: %s' % order.vendor,ln=1,align='C')
		out.cell(200,8,'Date: %s' % order.date,ln=1,align='C')
		for (key,price,quant) in order.products:
			product = self.products[key]
			out.cell(200,8,'ID: %5s Name: %10s Price: %5.2f Quantity: %10d' % (product.idNumber, product.name, price, quant),ln=1,align='C')
		out.output(filename)


	def fetchOrder(self,orderID):
		self.packer(self.orderHistoryDisplay, self.viewOrderSearch, orderID = orderID )

	def makeOrder(self):
		self.makeOrderDisplay.pack()
		self.makeOrderDisplay1 = tk.Frame(self.makeOrderDisplay)
		self.makeOrderDisplay2 = tk.Frame(self.makeOrderDisplay)
		self.makeOrderDisplay1.pack()
		self.orderProducts = []
		tk.Label(self.makeOrderDisplay1,text = 'Date').grid(row=0,column=0)
		tk.Entry(self.makeOrderDisplay1,textvariable = self.OrderVars['date']).grid(row=0,column=1)
		tk.Label(self.makeOrderDisplay1,text = 'Vendor').grid(row=0,column=2)
		tk.Entry(self.makeOrderDisplay1,textvariable = self.OrderVars['vendor']).grid(row=0,column=3)
		tk.Button(self.makeOrderDisplay1,text = 'Save',command = self.saveMakeOrder).grid(row=0,column=4)
		tk.Button(self.makeOrderDisplay1,text = 'Cancel',command = lambda : self.packer(self.makeOrderDisplay,self.orderMain)).grid(row=0,column=5)
		row = 2
		tk.Label(self.makeOrderDisplay2,text = 'ID',width = 5).grid(row=1,column = 1)
		tk.Label(self.makeOrderDisplay2,text = 'Name',width = 50).grid(row=1,column = 2)
		tk.Label(self.makeOrderDisplay2,text = 'Price',width = 10).grid(row=1,column = 3)
		tk.Label(self.makeOrderDisplay2,text = 'Case').grid(row=1,column = 4)
		self.makeBuildField(row)

	def makeBuildField(self,row):
		idvar = tk.IntVar()
		qvar= tk.IntVar()
		self.orderProducts.append((idvar,qvar))
		self.makeOrderDisplay2.pack()
		self.mini_dict = {'name':tk.StringVar(), 'price':tk.StringVar()}
		tk.Entry(self.makeOrderDisplay2,textvariable = idvar,width = 5).grid(row= row,column = 1)
		tk.Label(self.makeOrderDisplay2, textvariable = self.mini_dict['name'],text = '').grid(row=row, column=2)
		tk.Label(self.makeOrderDisplay2,textvariable = self.mini_dict['price'],text = '').grid(row=row,column=3)
		tk.Entry(self.makeOrderDisplay2,textvariable = qvar,width = 5).grid(row=row,column=4)
		row += 1
		self.addbutton1 = tk.Button(self.makeOrderDisplay2,text = 'Add', command=lambda: self.orderSearchID(row,self.addbutton1,2))
		self.addbutton1.grid(row=row-1,column=6)

	def saveMakeOrder(self):
		products = []
		total = 0
		for i in xrange(len(self.orderProducts)-1):
			product = self.products[self.orderProducts[i][0].get()]
			products.append((self.orderProducts[i][0].get(),product.price, self.orderProducts[i][1].get()))
		vendor = self.OrderVars['vendor'].get()
		date = self.OrderVars['date'].get()
		for (key,price,quant) in products:
			total += price*quant
		order = Order(vendor = vendor, date = date, products = products,total = total)
		self.makeOrders[date] = order
		self.packer(self.makeOrderDisplay, self.orderMain,option = 3)
		
		

	'''REPORTS'''

	def mainReports(self):
		self.reportsDisplay.pack()
		tk.Button(self.reportsDisplay, text='Iventory', command = lambda: self.packer(self.reportsDisplay,self.inventoryShow) ).grid(row=0,column = 0)
		tk.Button(self.reportsDisplay, text='Counting Inventory', command = self.exportCountingInventory ).grid(row=0,column = 1)
		tk.Button(self.reportsDisplay, text='Product History', command = lambda : mb.showwarning('Not Implemented','Service not implemented yet') ).grid(row=0,column = 2)
		tk.Button(self.reportsDisplay, text='Back', command = lambda : self.packer(self.reportsDisplay,self.main) ).grid(row=0,column = 3)

	def inventoryShow(self):
		self.inventoryDisplay.pack()
		column = 0
		row=2
		tk.Button(self.inventoryDisplay,text = 'Back',command = lambda : self.packer(self.inventoryDisplay,self.mainReports)).grid(row=0,column=0)
		tk.Button(self.inventoryDisplay,text = 'Export',command  = self.exportInventory).grid(row=0,column=1)
		for item in self.productOptions:
			tk.Label(self.inventoryDisplay, text = item).grid(row=1,column=column)
			column+=1
		for product in self.products.values():
			tk.Label(self.inventoryDisplay,text = product.idNumber,width = 5).grid(row=row,column=0)
			tk.Label(self.inventoryDisplay,text = product.name,width = 20).grid(row=row,column=1)
			tk.Label(self.inventoryDisplay,text = product.price,width = 15).grid(row=row,column=2)
			tk.Label(self.inventoryDisplay,text = product.unit,width = 5).grid(row=row,column = 3)
			tk.Label(self.inventoryDisplay,text = product.quantity,width =15).grid(row=row,column=4)
			tk.Label(self.inventoryDisplay,text = product.case,width = 10).grid(row=row,column=5)
			row+=1

	def exportInventory(self):
		out = fpdf.FPDF(format='Letter')
		filename = fd.asksaveasfilename(defaultextension = '.pdf')
		out.add_page()
		out.set_font('Arial',size=20)
		out.cell(200,10,'Inventory',ln=1,align='C')
		out.set_font('Arial',size=10)
		for product in self.products.values():
			out.cell(200,10,'ID: %5d Name: %10s Price: %5.2f Unit: %5s Quantity: %10d Case: %5d' % (product.idNumber, product.name, product.price, product.unit, product.quantity, product.case),ln=1,align='C')
		out.output(filename)

	def exportCountingInventory(self):
		out = fpdf.FPDF(format='Letter')
		filename = fd.asksaveasfilename(defaultextension = '.pdf')
		out.add_page()
		out.set_font('Arial',size=20)
		out.cell(200,10,'Counting Inventory',ln=1,align='C')
		out.set_font('Arial',size=10)
		for product in self.products.values():
			out.cell(200,10,'ID: %5d Name: %10s Cases: _________ Units: _________ ' % (product.idNumber, product.name),ln=1,align='C')
		out.output(filename)

	''' Vendors '''

	def vendorShow(self):
		self.vendorDisplay.pack()
		tk.Button(self.vendorDisplay, text = 'Add Vendor',command = lambda: self.packer(self.vendorDisplay, self.addVendor)).grid(row=0,column=0)
		tk.Button(self.vendorDisplay, text = 'Delete Vendor',command =lambda: self.packer(self.vendorDisplay, self.deleteVendor)).grid(row=0,column=1)
		tk.Button(self.vendorDisplay, text = 'View Vendor',command =lambda: self.packer(self.vendorDisplay, self.viewVendor)).grid(row=0,column=2)
		tk.Button(self.vendorDisplay, text = 'All Vendors',command = lambda: self.packer(self.vendorDisplay, self.allVendors)).grid(row=0,column=3)
		tk.Button(self.vendorDisplay, text = 'Back',command = lambda : self.packer(self.vendorDisplay,self.orderMain)).grid(row=0,column=4)
		#ttk.Combobox(self.vendorDisplay, values = self.vendors.values()).grid(row=0,columnspan=2)

	def addVendor(self):
		self.addVendorDisplay.pack()
		tk.Label(self.addVendorDisplay,text = 'Name').grid(row=0,column=0)
		tk.Entry(self.addVendorDisplay,textvariable = self.vendorVars['name']).grid(row=0,column=1)
		tk.Label(self.addVendorDisplay,text = 'Address').grid(row=1,column=0)
		tk.Entry(self.addVendorDisplay,textvariable = self.vendorVars['address']).grid(row=1,column=1)
		tk.Label(self.addVendorDisplay,text = 'ID').grid(row=2,column=0)
		tk.Entry(self.addVendorDisplay,textvariable = self.vendorVars['id']).grid(row=2,column=1)
		tk.Button(self.addVendorDisplay,text = 'Cancel',command = lambda: self.packer(self.addVendorDisplay,self.vendorShow)).grid(row=3,column=0)
		tk.Button(self.addVendorDisplay,text = 'Save',command =self.saveVendor).grid(row=3,column=1)

	def saveVendor(self):
		try:
			name = self.vendorVars['name'].get()
			address = self.vendorVars['address'].get()
			idd = self.vendorVars['id'].get()
			self.clearVars(2)
			if idd in self.vendors:
				mb.showwarning('ID already exists', 'The chosen id already exists')
			else:
				self.vendors[idd] = Vendor(name = name, address = address, idNumber = idd)
				self.packer(self.addVendorDisplay,self.vendorShow)
		except ValueError:
			mb.showwarning('Invalid ID','ID must be a number')
			

	def deleteVendor(self):
		self.deleteVendorDisplay.pack()
		tk.Entry(self.deleteVendorDisplay,textvariable = self.vendorID).grid(row=0,columnspan=2)
		tk.Button(self.deleteVendorDisplay,text = 'Back',command = lambda : self.packer(self.deleteVendorDisplay,self.vendorShow)).grid(row=1,column=0)
		tk.Button(self.deleteVendorDisplay,text = 'Delete',command = self.deleteVendorID).grid(row=1,column=1)
		''' i have to figure out what to do with remaining orders from deleted vendors'''

	def deleteVendorID(self):
		try:
			del self.vendors[self.vendorID.get()]
			self.packer(self.deleteVendorDisplay,self.vendorShow)
			self.vendorID.set('')
		except KeyError:
			mb.showwarning('Not Found', 'No vendor with that ID')


	def viewVendor(self):
		self.viewVendorDisplay1 = tk.Frame(self.viewVendorDisplay)
		self.viewVendorDisplay2 = tk.Frame(self.viewVendorDisplay)
		self.viewVendorDisplay.pack()
		self.viewVendorDisplay1.pack()
		tk.Entry(self.viewVendorDisplay1,textvariable = self.vendorID).grid(row=0,columnspan=2)
		tk.Button(self.viewVendorDisplay1,text = 'Back',command = lambda: self.packer(self.viewVendorDisplay,self.vendorShow)).grid(row=1,column=0)
		tk.Button(self.viewVendorDisplay1,text = 'Search',command = self.searchVendorID).grid(row=1,column=1)

	def searchVendorID(self):
		if self.viewVendorDisplay2.winfo_children():
			for child in self.viewVendorDisplay2.winfo_children():
				child.destroy()
		self.viewVendorDisplay2.pack()
		tk.Label(self.viewVendorDisplay2,text = 'ID',width = 5).grid(row=0,column=0)
		tk.Label(self.viewVendorDisplay2,text = 'Name',width = 15).grid(row=0,column=1)
		tk.Label(self.viewVendorDisplay2,text = 'Address',width = 20).grid(row=0,column=2)
		vendor = self.vendors[self.vendorID.get()]
		tk.Label(self.viewVendorDisplay2,text = vendor.idNumber).grid(row=1,column=0)
		tk.Label(self.viewVendorDisplay2,text = vendor.name).grid(row=1,column=1)
		tk.Label(self.viewVendorDisplay2,text = vendor.address).grid(row=1,column=2)
		

	def allVendors(self):
		self.viewVendorAll.pack()
		tk.Button(self.viewVendorAll,text = 'Back',command = lambda : self.packer(self.viewVendorAll,self.vendorShow)).grid(row=0,column=0)
		tk.Label(self.viewVendorAll,text = 'ID',width = 5).grid(row=1,column=0)
		tk.Label(self.viewVendorAll,text = 'Name',width = 15).grid(row=1,column=1)
		tk.Label(self.viewVendorAll,text = 'Address',width = 20).grid(row=1,column=2)
		row = 2
		for vendor in self.vendors:
			tk.Label(self.viewVendorAll,text = self.vendors[vendor].idNumber).grid(row=row,column=0)
			tk.Label(self.viewVendorAll,text = self.vendors[vendor].name).grid(row=row,column=1)
			tk.Label(self.viewVendorAll,text = self.vendors[vendor].address).grid(row=row,column=2)
			row+=1


if __name__=='__main__':
	p = Main('database')
	p.mainloop()