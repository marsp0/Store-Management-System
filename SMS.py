#!usr/bin/python

#imports
import Tkinter as tk
import logging
import tkMessageBox as mb
import tkFileDialog as fd
import ttk as ttk
import decimal
import datetime
import shelve
import time
import fpdf

class Product(object):
	''' Product object:

		PARAMS >
			- name - type(str)
			- price - type(float)
			- idNumber - type(int)
			- quantity - type(int)
			- unit / measurement unit - type(str)
			- case / how much of that unit is in 1 case - type(int)
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
		'''Vendor object:
		PARAMS>
			- name - type(str)
			- address - type(str)
			- idNumber - type(int)
		'''
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

	def __init__(self,date,idNumber = 0, vendor = '?',products = [],total = 0):
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

		self.logger = logging.getLogger('StoreMSystem')
		self.logger.setLevel(logging.DEBUG)
		handler = logging.FileHandler('Logging.log')
		formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
		handler.setFormatter(formatter)
		self.logger.addHandler(handler)
		self.logger.debug('Program Started')

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
		self.OrderVars = dict([('vendor', tk.StringVar()),('id',tk.IntVar()),('day',tk.IntVar()),('month',tk.IntVar()),('year',tk.IntVar())])
		self.OrderOptions = ('id','vendor','products','date')
		self.viewOrderDate = tk.StringVar()
		self.viewOrderMode = tk.IntVar()


		self.vendorDisplay = tk.Frame(self)
		self.addVendorDisplay = tk.Frame(self)
		self.deleteVendorDisplay = tk.Frame(self)
		self.viewVendorDisplay = tk.Frame(self)
		self.viewVendorAll = tk.Frame(self)
		self.vendorVars = dict([('name',tk.StringVar()),('address',tk.StringVar()),('id',tk.IntVar())])
		self.vendorID = tk.StringVar()
		self.vendor_vars = ['%s: %s' % (vendor.idNumber	, vendor.name) for vendor in self.vendors.values()]

		#REPORTS VARS
		self.reportsDisplay = tk.Frame(self)
		self.inventoryDisplay = tk.Frame(self)

	''' FUNTIONALITIES '''

	def startDatabase(self):
		''' init the database (shelve file) and assign the appropriate lists/dicts
			PARAMS>
				- self.products - contains the product objects - type(dict)
				- self.orders - contains the order objects - type(dict)
				- self.vendors - contains the order objects - type(dict)
				- self.makeOrders - contains the outgoing orders - type(dict)
				- self.recentProducts - list of 10 tuples containing the object id, object's name and the action that was performed (Add,Edit,Delete)
				- self.recentProductsAdd - list of 10 tuples containing object.id and object.name  of the objects that were added
				- self.recentProductsEdit - list of 10 tuples containing object.id and object.name  of the objects that were edited
				- self.recentProductsDelete - list of 10 tuples containing object.id and object.name  of the objects that were deleted
				- self.recentOrders - list of 10 tuples containing the orders.id, objects.date, object.vendor, object.total and the action performed (Incoming or Outgoing)
				- self.recentOrdersIncoming - list of 10 tuples containing the orders.id, objects.date, object.vendor, object.total
				- self.recentOrdersOutgoing - list of 10 tuples containing the orders.id, objects.date, object.vendor, object.total
				- self.recentVendors - list of 10 tuples containing the vendors id and name and the action that was performed (add,edit,delete)
				- self.recentVendorsAdd - list of 10 tuples containing the recently added vendor's name and id
				- self.recentVendorsEdit - list of 10 tuples containing the recently edited vendor's name and id
				- self.recentVendorsDelete - list of 10 tuples containing the recently deleted vendor's name and id
		'''
		database = shelve.open(self.filename)
		if database:
			self.products = database['products']
			self.orders = database['orders']
			self.vendors = database['vendors']
			self.makeOrders = database['makeOrders']

			self.recentProducts = database['recentProducts']
			self.recentProductsAdd = database['recentProductsAdd']
			self.recentProductsEdit = database['recentProductsEdit']
			self.recentProductsDelete = database['recentProductsDelete']

			self.recentOrders = database['recentOrders']
			self.recentOrdersIncoming = database['recentOrdersIncoming']
			self.recentOrdersOutgoing = database['recentOrdersOutgoing']

			self.recentVendors = database['recentVendors']
			self.recentVendorsAdd = database['recentVendorsAdd']
			self.recentVendorsEdit = database['recentVendorsEdit']
			self.recentVendorsDelete = database['recentVendorsDelete']
		else:
			self.products = {}
			self.orders = {}
			self.makeOrders = {}
			self.vendors = {}

			self.recentProducts = []
			self.recentProductsAdd = []
			self.recentProductsEdit = []
			self.recentProductsDelete = []

			self.recentOrders = []
			self.recentOrdersIncoming = []
			self.recentOrdersOutgoing = []

			self.recentVendors = []
			self.recentVendorsAdd = []
			self.recentVendorsEdit = []
			self.recentVendorsDelete = []

		database.close()

	def quit(self):
		''' saving to the shelve file, 
			PARAMS>
			see the startDatabase method for vars info

		'''
		database = shelve.open(self.filename)
		database['products'] = self.products
		database['orders'] = self.orders
		database['vendors'] = self.vendors
		database['makeOrders'] = self.makeOrders

		database['recentProducts'] = self.recentProducts
		database['recentProductsAdd'] = self.recentProductsAdd
		database['recentProductsEdit'] = self.recentProductsEdit
		database['recentProductsDelete'] = self.recentProductsDelete

		database['recentOrders'] = self.recentOrders
		database['recentOrdersIncoming'] = self.recentOrdersIncoming
		database['recentOrdersOutgoing'] = self.recentOrdersOutgoing
		
		database['recentVendors'] = self.recentVendors
		database['recentVendorsAdd'] = self.recentVendorsAdd
		database['recentVendorsEdit'] = self.recentVendorsEdit
		database['recentVendorsDelete'] = self.recentVendorsDelete

		database.close()
		self.logger.debug('Program quits')
		self.master.destroy()

	def packer(self, unpacked, packed = None,option = None, orderID = None):
		''' Useful tool for packing
			PARAMS>
				unpacked - frame object
				packed - method function 
				option - int representing which one of the vars dictionaries to clear  (1 - self.productVars, 2- self.vendorVars, 3 - self.OrderVars)
		'''
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
		''' clears the textvariables of the dict that corresponds to the option'''
		if option == 1:
			for key in self.productVars:
				self.productVars[key].set('')
		if option == 2:
			for key in self.vendorVars:
				self.vendorVars[key].set('')
		if option == 3:
			for key in self.OrderVars:
				self.OrderVars[key].set('')

	def checkRecent(self,globalSeq,localSeq,idNumber, option):
		''' checks and appends to the recent vars
			PARAMS>
				- globalSeq - one of (self.recentProducts, self.recentOrders, self.recentVendors)
				- localSeq - one of (self.recentProductsAdd,self.recentProductsDelete,self.recentProductsEdit,
										self.recentOrdersOutgoing,self.recentOrdersIncoming,self.recentVendorsAdd,
										self.recentVendorsEdit,self.recentVendorsDelete)

		'''
		if len(globalSeq) >= 10 and globalSeq:
			del globalSeq[0]
		if len(localSeq) >= 10 and localSeq:
			del localSeq[0]
		globalSeq.append((idNumber,option))
		localSeq.append(idNumber)

	def main(self):
		''' The main display contai various buttons and 3 frames for (self.recentProducts,self.recentVendors,self.recentOrders)

		'''
		self.mainDisplay.pack()
		self.mainDisplay1 = tk.Frame(self.mainDisplay)
		self.mainDisplay15 = tk.Frame(self.mainDisplay)
		self.mainDisplay2=tk.Frame(self.mainDisplay15,bd=1,relief='sunken')
		self.mainDisplay3=tk.Frame(self.mainDisplay15,bd=1,relief='sunken')
		self.mainDisplay4=tk.Frame(self.mainDisplay15,bd=1,relief='sunken')
		self.mainDisplay1.pack()
		self.mainDisplay15.pack()
		self.mainDisplay2.pack(side='left',anchor='n')
		self.mainDisplay3.pack(side='left',anchor='n')
		self.mainDisplay4.pack(side='left',anchor='n')
		tk.Button(self.mainDisplay1, text='Quit', command = self.quit).grid(row=0,column = 3)
		tk.Button(self.mainDisplay1, text='Products', command = lambda: self.packer(self.mainDisplay, self.productView) ).grid(row=0,column = 0)
		tk.Button(self.mainDisplay1, text='Orders', command = lambda : self.packer(self.mainDisplay,self.orderMain)).grid(row=0,column = 1)
		tk.Button(self.mainDisplay1, text='Reports', command = lambda: self.packer(self.mainDisplay, self.mainReports) ).grid(row=0,column = 2)

		tk.Label(self.mainDisplay2, text = 'Recent Products',font = '15',width = 26,bd=1,relief='raised').grid(row=0,column = 0,columnspan=3)
		tk.Label(self.mainDisplay2,text='ID',width = 5).grid(row=1,column=0)
		tk.Label(self.mainDisplay2,text='Name',width=10).grid(row=1,column=1)
		tk.Label(self.mainDisplay2,text = 'Actn',width = 5).grid(row=1,column=2)
		product_row = 2
		for product,option in self.recentProducts:
			tk.Label(self.mainDisplay2,text = product[0]).grid(row=product_row,column=0)
			tk.Label(self.mainDisplay2,text = product[1]).grid(row=product_row,column=1)
			tk.Label(self.mainDisplay2,text = option).grid(row=product_row,column=2)
			product_row+=1

		tk.Label(self.mainDisplay3, text = 'Recent Orders',font = '15',width = 30,bd=1,relief='raised').grid(row=0,column = 0,columnspan=3)
		tk.Label(self.mainDisplay3,text='ID',width=10).grid(row=1,column=0)
		tk.Label(self.mainDisplay3,text='Date',width=10).grid(row=1,column=1)
		tk.Label(self.mainDisplay3,text = 'Actn',width = 5).grid(row=1,column=2)
		order_row = 2

		for order,option in self.recentOrders:
			if option == 'I':
				tk.Label(self.mainDisplay3,text = order[1]).grid(row=order_row,column=1)
				tk.Label(self.mainDisplay3,text = order[0]).grid(row=order_row,column=0)
				tk.Label(self.mainDisplay3,text = option).grid(row=order_row,column=2)
			else:
				tk.Label(self.mainDisplay3,text = order[1]).grid(row=order_row,column=1)
				tk.Label(self.mainDisplay3,text = order[0]).grid(row=order_row,column=0)
				tk.Label(self.mainDisplay3,text = option).grid(row=order_row,column=2)
			order_row+=1

		tk.Label(self.mainDisplay4, text = 'Recent Vendors',font = '15',width = 26,bd=1,relief='raised').grid(row=0,column = 0,columnspan=3)
		tk.Label(self.mainDisplay4,text='ID',width=5).grid(row=1,column=0)
		tk.Label(self.mainDisplay4,text='Name',width=10).grid(row=1,column=1)
		tk.Label(self.mainDisplay4,text='Actn',width=5).grid(row=1,column=2)
		vendor_row = 2
		for vendor,option in self.recentVendors:
			tk.Label(self.mainDisplay4,text = vendor[0]).grid(row=vendor_row,column=0)
			tk.Label(self.mainDisplay4,text = vendor[1]).grid(row=vendor_row,column=1)
			tk.Label(self.mainDisplay4,text = option).grid(row=vendor_row,column=2)
			vendor_row+=1

	''' PRODUCTS '''

	def productView(self):
		self.productDisplay.pack()
		self.productDisplay1 = tk.Frame(self.productDisplay)
		self.productDisplay2 = tk.Frame(self.productDisplay)
		self.productDisplay1.pack(side='top')
		self.productDisplay2.pack(side='top')
		self.productDisplay3 = tk.Frame(self.productDisplay2,bd = 1,relief='sunken')
		self.productDisplay4 = tk.Frame(self.productDisplay2,bd = 1,relief='sunken')
		self.productDisplay5 = tk.Frame(self.productDisplay2,bd = 1,relief='sunken')
		self.productDisplay3.pack(side='left',anchor='n')
		self.productDisplay4.pack(side='left',anchor='n')
		self.productDisplay5.pack(side='left',anchor='n')
		tk.Button(self.productDisplay1, text='Add Product', command = lambda : self.packer(self.productDisplay, self.addProduct) ).grid(row=0,column = 0)
		tk.Button(self.productDisplay1, text='Edit Product', command = lambda: self.packer(self.productDisplay, self.editProduct) ).grid(row=0,column = 1)
		tk.Button(self.productDisplay1, text='Delete Product', command = lambda : self.packer(self.productDisplay,self.deleteProduct)  ).grid(row=0,column = 2)
		tk.Button(self.productDisplay1, text='View Product', command = lambda: self.packer(self.productDisplay,self.viewProduct) ).grid(row=0,column = 3)
		tk.Button(self.productDisplay1, text='Back', command = lambda : self.packer(self.productDisplay,self.main) ).grid(row=0,column = 4)

		tk.Label(self.productDisplay3,text = 'Added Products',relief='raised',width=25).grid(row=0,columnspan=2)
		tk.Label(self.productDisplay3,text = 'ID',width=5).grid(row=1,column=0)
		tk.Label(self.productDisplay3,text = 'Name').grid(row=1,column=1)
		added_row=2
		for product in self.recentProductsAdd:
			tk.Label(self.productDisplay3,text = product[0]).grid(row=added_row,column=0)
			tk.Label(self.productDisplay3,text = product[1]).grid(row=added_row,column=1)
			added_row+=1

		tk.Label(self.productDisplay4,text = 'Edited Products',relief='raised',width=25).grid(row=0,columnspan=2)
		tk.Label(self.productDisplay4,text = 'ID',width=5).grid(row=1,column=0)
		tk.Label(self.productDisplay4,text = 'Name').grid(row=1,column=1)
		edited_row = 2
		for product in self.recentProductsEdit:
			tk.Label(self.productDisplay4,text = product[0]).grid(row=edited_row,column=0)
			tk.Label(self.productDisplay4,text = product[1]).grid(row=edited_row,column=1)
			edited_row+=1

		tk.Label(self.productDisplay5,text = 'Deleted Products',relief='raised',width=25).grid(row=0,columnspan=2)
		tk.Label(self.productDisplay5,text = 'ID',width=5).grid(row=1,column=0)
		tk.Label(self.productDisplay5,text = 'Name').grid(row=1,column=1)
		deleted_row = 2
		for product in self.recentProductsDelete:
			tk.Label(self.productDisplay5,text = product[0]).grid(row=deleted_row,column=0)
			tk.Label(self.productDisplay5,text = product[1]).grid(row=deleted_row,column=1)
			deleted_row+=1

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
				self.checkRecent(self.recentProducts,self.recentProductsAdd,(p.idNumber,p.name),'A')
				self.logger.debug('Product created : ID - %s, Name - %s, Price - %s, Unit - %s, Case - %s '%(p.idNumber,p.name,p.price,p.unit,p.case))
				self.packer(self.addProductDisplay,self.productView)
		except ValueError: 
			mb.showwarning('Error','Price,ID,Quantity and Units per Case have to be numbers')

	def editSave(self,product):
		product.name = self.productVars['name'].get()
		product.quantity = self.productVars['quantity'].get()
		product.price = self.productVars['price'].get()
		product.unit = self.productVars['unit'].get()
		product.case = self.productVars['case'].get()
		self.logger.debug('Product Edited : ID - %s, Name - %s, Price - %s, Unit - %s, Case - %s '%(product.idNumber,product.name,product.price,product.unit,product.case))
		self.clearVars(1)
		self.checkRecent(self.recentProducts,self.recentProductsEdit,(product.idNumber,product.name), 'E')
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
		self.viewDisplay2 = tk.Frame(self.viewDisplay,bd=1,relief='sunken')
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
			tk.Label(self.viewDisplay2,text = 'ID', bd = 1, relief = 'raised',width=5).grid(row=1,column=0)
			tk.Label(self.viewDisplay2,text = 'Name', bd = 1, relief = 'raised',width=20).grid(row=1,column=1)
			tk.Label(self.viewDisplay2,text = 'Price', bd = 1, relief = 'raised',width=15).grid(row=1,column=2)
			tk.Label(self.viewDisplay2,text = 'Unit', bd = 1, relief = 'raised',width=5).grid(row=1,column=3)
			tk.Label(self.viewDisplay2,text = 'Quantity', bd = 1, relief = 'raised',width=15).grid(row=1,column=4)
			tk.Label(self.viewDisplay2,text = 'Case', bd = 1, relief = 'raised',width=10).grid(row=1,column=5)
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
			self.logger.debug('Viewing product with ID - %s'%product.idNumber)
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
			self.checkRecent(self.recentProducts,self.recentProductsDelete,(key,self.products[key].name),'D')
			p = self.products[key]
			self.logger.debug('Product deleted : ID - %s, Name - %s, Price - %s, Unit - %s, Case - %s '%(p.idNumber,p.name,p.price,p.unit,p.case))
			del self.products[key]
			self.packer(self.deleteView, self.productView)
		except KeyError:
			mb.showwarning('Not Found', 'No such product in the database')


	''' ORDERS '''
	def orderMain(self):
		self.orderDisplay.pack()
		self.orderDisplay1 = tk.Frame(self.orderDisplay)
		self.orderDisplay2 = tk.Frame(self.orderDisplay)
		self.orderDisplay1.pack(side='top')
		self.orderDisplay2.pack()
		self.orderDisplay3 = tk.Frame(self.orderDisplay2,bd=1,relief='sunken')
		self.orderDisplay4 = tk.Frame(self.orderDisplay2,bd=1,relief='sunken')
		self.orderDisplay5 = tk.Frame(self.orderDisplay2,bd=1,relief='sunken')
		self.orderDisplay3.pack(side='left',anchor='n')
		self.orderDisplay4.pack(side='left',anchor='n')
		self.orderDisplay5.pack(side='left',anchor='n')
		tk.Button(self.orderDisplay1, text='Incoming Order', command = lambda : self.packer(self.orderDisplay, self.addOrder)).grid(row=0,column = 0)
		tk.Button(self.orderDisplay1, text='View Order', command = lambda : self.packer(self.orderDisplay,self.viewOrder) ).grid(row=0,column = 1)
		tk.Button(self.orderDisplay1,text = 'Outgoing Order',command = lambda: self.packer(self.orderDisplay,self.makeOrder)).grid(row=0,column = 2)
		tk.Button(self.orderDisplay1, text='Order History', command = lambda : self.packer(self.orderDisplay,self.orderHistory) ).grid(row=0,column = 3)
		tk.Button(self.orderDisplay1,text = 'Vendors',command = lambda: self.packer(self.orderDisplay,self.vendorShow)).grid(row=0,column=4)
		tk.Button(self.orderDisplay1, text='Back', command = lambda : self.packer(self.orderDisplay,self.main) ).grid(row=0,column = 5)

		tk.Label(self.orderDisplay3,text = 'Recentrly Added Outgoing',width = 32,relief='raised').grid(row=0,columnspan=3)
		tk.Label(self.orderDisplay3,text = 'Date',width = 10).grid(row=1,column=0)
		tk.Label(self.orderDisplay3,text = 'Vendor',width = 15).grid(row=1,column=1)
		tk.Label(self.orderDisplay3,text = 'Total',width = 5).grid(row=1,column=2)
		outgoing_row=2
		for order in self.recentOrdersOutgoing:
			tk.Label(self.orderDisplay3,text= order[1]).grid(row=outgoing_row,column=0)
			tk.Label(self.orderDisplay3,text= order[2]).grid(row=outgoing_row,column=1)
			tk.Label(self.orderDisplay3,text= order[3]).grid(row=outgoing_row,column=2)

		tk.Label(self.orderDisplay4,text = 'Recentrly Added Incoming',width = 40,relief='raised').grid(row=0,columnspan=4)
		tk.Label(self.orderDisplay4,text = 'ID',width = 7).grid(row=1,column=0)
		tk.Label(self.orderDisplay4,text = 'Date',width = 10).grid(row=1,column=1)
		tk.Label(self.orderDisplay4,text = 'Vendor',width = 10).grid(row=1,column=2)
		tk.Label(self.orderDisplay4,text = 'Total',width = 5).grid(row=1,column=3)
		incoming_row=2
		for order in self.recentOrdersIncoming:
			tk.Label(self.orderDisplay4,text= order[0]).grid(row=outgoing_row,column=0)
			tk.Label(self.orderDisplay4,text= order[1]).grid(row=outgoing_row,column=1)
			tk.Label(self.orderDisplay4,text= order[2]).grid(row=outgoing_row,column=2)
			tk.Label(self.orderDisplay4,text= order[3]).grid(row=outgoing_row,column=3)

	def addOrder(self):
		self.orderMiniDisplay = tk.Frame(self.addOrderDisplay)
		self.orderMiniDisplay2 = tk.Frame(self.addOrderDisplay,bd=1,relief='sunken')
		self.addOrderDisplay.pack()
		self.orderMiniDisplay.pack()
		self.orderProducts = []
		row = 2
		tk.Label(self.orderMiniDisplay, text = 'Vendor').grid(row=0,column = 1)
		tk.Entry(self.orderMiniDisplay, textvariable = self.OrderVars['vendor'],width = 10).grid(row=0,column=2)
		tk.Label(self.orderMiniDisplay, text = 'ID').grid(row=0,column = 3)
		tk.Entry(self.orderMiniDisplay, textvariable = self.OrderVars['id'],width = 10).grid(row=0,column = 4)
		tk.Label(self.orderMiniDisplay, text = 'Date').grid(row=0,column = 5)
		tk.Entry(self.orderMiniDisplay, textvariable = self.OrderVars['day'],width = 3,text='Day').grid(row=0,column = 6)
		tk.Entry(self.orderMiniDisplay, textvariable = self.OrderVars['month'],width = 3,text='Month').grid(row=0,column = 7)
		tk.Entry(self.orderMiniDisplay, textvariable = self.OrderVars['year'],width = 6,text='Year').grid(row=0,column = 8)
		tk.Button(self.orderMiniDisplay,text = 'Save',command = self.saveOrder).grid(row=0,column=9)
		tk.Button(self.orderMiniDisplay,text = 'Cancel',command = lambda: self.packer(self.addOrderDisplay,self.orderMain)).grid(row=0,column=10)

		
		tk.Label(self.orderMiniDisplay2,text = 'ID',width=5,bd=1,relief='raised').grid(row=1,column = 1)
		tk.Label(self.orderMiniDisplay2,text = 'Name',width = 40,bd=1,relief='raised').grid(row=1,column = 2)
		tk.Label(self.orderMiniDisplay2,text = 'Price',width = 10,bd=1,relief='raised').grid(row=1,column = 3)
		tk.Label(self.orderMiniDisplay2,text = 'Case',width = 5,bd=1,relief='raised').grid(row=1,column = 4)
		self.buildField(row)

	def buildField(self,row):
		idvar = tk.IntVar()
		qvar= tk.IntVar()
		self.orderProducts.append((idvar,qvar))
		self.orderMiniDisplay2.pack()
		self.mini_dict = {'name':tk.StringVar(), 'price':tk.StringVar()}
		tk.Entry(self.orderMiniDisplay2,textvariable = idvar,width = 4).grid(row= row,column = 1)
		tk.Label(self.orderMiniDisplay2, textvariable = self.mini_dict['name'],text = '').grid(row=row, column=2)
		tk.Label(self.orderMiniDisplay2,textvariable = self.mini_dict['price'],text = '').grid(row=row,column=3)
		tk.Entry(self.orderMiniDisplay2,textvariable = qvar,width = 4).grid(row=row,column=4)
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
		date = datetime.date(self.OrderVars['year'].get(),self.OrderVars['month'].get(),self.OrderVars['day'].get())
		for (key,price,quant) in products:
			total += price*quant
		order = Order(date,idNumber = idOrder, vendor = vendor, products = products,total = total)
		self.orders[date] = order
		self.checkRecent(self.recentOrders,self.recentOrdersIncoming,(order.id,date,order.vendor,order.total),'I')
		self.logger.debug('Order Incoming : ID - %s, Date - %s, Vendor - %s, Products - %s, Total - %s'%(order.id,order.date,order.vendor,order.products,order.total))
		self.packer(self.addOrderDisplay, self.orderMain,option = 3)

	def viewOrder(self):
		self.viewOrderDisplay1 = tk.Frame(self.viewOrderDisplay)
		self.viewOrderDisplay3 = tk.Frame(self.viewOrderDisplay,bd=1,relief='sunken')
		self.viewOrderDisplay2 = tk.Frame(self.viewOrderDisplay,bd=1,relief='sunken')
		self.viewOrderDisplayDate = tk.Frame(self.viewOrderDisplay)
		self.viewOrderDisplay.pack()
		self.viewOrderDisplayDate.pack()
		self.viewOrderDisplay1.pack()
		tk.Label(self.viewOrderDisplayDate,text = 'Date').grid(row=0,column=0)
		tk.Entry(self.viewOrderDisplayDate, textvariable = self.OrderVars['day'],width = 3,text='Day').grid(row=0,column = 1)
		tk.Entry(self.viewOrderDisplayDate, textvariable = self.OrderVars['month'],width = 3,text='Month').grid(row=0,column = 2)
		tk.Entry(self.viewOrderDisplayDate, textvariable = self.OrderVars['year'],width = 6,text='Year').grid(row=0,column = 3)
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
				date_order = datetime.date(self.OrderVars['year'].get(),self.OrderVars['month'].get(),self.OrderVars['day'].get())
				if self.viewOrderMode.get() == 0:
					order = self.orders[date_order]
				else:
					order = self.makeOrders[date_order]
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
			self.clearVars(3)
			self.viewOrderDisplay3.pack()
			self.viewOrderDisplay2.pack()
			tk.Label(self.viewOrderDisplay3, text = 'ID:',width=5,bd=1,relief='raised').grid(row=0,column=1)
			tk.Label(self.viewOrderDisplay3,text = order.id,width = 11).grid(row=0,column=2)
			tk.Label(self.viewOrderDisplay3, text = 'Vendor:',width=10,bd=1,relief='raised').grid(row=0,column=3)
			tk.Label(self.viewOrderDisplay3,text = order.vendor,width = 20).grid(row=0,column=4)
			tk.Label(self.viewOrderDisplay3, text = 'Date: ',width=10,bd=1,relief='raised').grid(row=0,column=5)
			tk.Label(self.viewOrderDisplay3,text = order.date,width = 15).grid(row=0,column=6)

			tk.Label(self.viewOrderDisplay2, text = 'ID',width= 5,bd=1,relief='raised').grid(row=1, column = 0)
			tk.Label(self.viewOrderDisplay2, text = 'Name',width= 20,bd=1,relief='raised').grid(row=1, column = 1)
			tk.Label(self.viewOrderDisplay2, text = 'Price',width= 15,bd=1,relief='raised').grid(row=1, column = 2)
			tk.Label(self.viewOrderDisplay2, text = 'Unit',width= 5,bd=1,relief='raised').grid(row=1, column = 3)
			tk.Label(self.viewOrderDisplay2, text = 'Quantity',width= 15,bd=1,relief='raised').grid(row=1, column = 4)
			tk.Label(self.viewOrderDisplay2, text = 'Case',width= 10,bd=1,relief='raised').grid(row=1, column = 5)
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
			self.logger.debug('Viewing Order ID - %s and from %s'% (order.id,order.date))
		except KeyError:
			mb.showwarning('Not Found', 'Order Not Found!\nCheck the date again, it should be dd/mm/yyyy')
		except ValueError:
			mb.showwarning('Not Found', 'Incorrect date')

	def orderHistory(self):
		self.orderHistoryDisplay.pack()
		row = 1
		self.orderHistoryDisplay1 = tk.Frame(self.orderHistoryDisplay)
		self.orderHistoryDisplay2 = tk.Frame(self.orderHistoryDisplay,bd=1,relief='sunken')
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
		tk.Label(self.orderHistoryDisplay2, text = 'ID',width = 15,bd=1,relief='raised').grid(row=0,column=1)
		tk.Label(self.orderHistoryDisplay2, text = 'Vendor',width = 15,bd=1,relief='raised').grid(row=0,column=2)
		tk.Label(self.orderHistoryDisplay2, text = 'Date',width = 15,bd=1,relief='raised').grid(row=0,column=3)
		tk.Label(self.orderHistoryDisplay2,text = 'Total',width = 15,bd=1,relief='raised').grid(row=0,column=4)
		if self.viewOrderMode.get() == 0:
			for order in self.orders:
				tk.Label(self.orderHistoryDisplay2, text = self.orders[order].id,width = 15).grid(row=row,column=1)
				tk.Label(self.orderHistoryDisplay2,text = self.orders[order].vendor,width = 15).grid(row=row,column=2)
				tk.Label(self.orderHistoryDisplay2,text = self.orders[order].date,width = 15).grid(row=row,column=3)
				tk.Label(self.orderHistoryDisplay2,text = '%5.2f' % self.orders[order].total,width = 15).grid(row=row,column=4)
				tk.Button(self.orderHistoryDisplay2,text ='View',command = lambda order=order: self.fetchOrder(order)).grid(row=row,column=5)
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
		self.logger.debug('Viewing Order history')

	def exportOrder(self,order):
		order = self.makeOrders[order]
		filename = fd.asksaveasfilename()
		if filename:
			self.logger.debug('Exporting order ID - %s'%order.id)
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
		tk.Entry(self.makeOrderDisplay1, textvariable = self.OrderVars['day'],width = 3,text='Day').grid(row=0,column = 1)
		tk.Entry(self.makeOrderDisplay1, textvariable = self.OrderVars['month'],width = 3,text='Month').grid(row=0,column = 2)
		tk.Entry(self.makeOrderDisplay1, textvariable = self.OrderVars['year'],width = 6,text='Year').grid(row=0,column = 3)
		tk.Label(self.makeOrderDisplay1,text = 'Vendor').grid(row=0,column=4)
		tk.Entry(self.makeOrderDisplay1,textvariable = self.OrderVars['vendor']).grid(row=0,column=5)
		tk.Button(self.makeOrderDisplay1,text = 'Save',command = self.saveMakeOrder).grid(row=0,column=6)
		tk.Button(self.makeOrderDisplay1,text = 'Cancel',command = lambda : self.packer(self.makeOrderDisplay,self.orderMain)).grid(row=0,column=7)
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
		date = datetime.date(self.OrderVars['year'].get(),self.OrderVars['month'].get(),self.OrderVars['day'].get())
		for (key,price,quant) in products:
			total += price*quant
		order = Order(date,vendor = vendor, products = products,total = total)
		self.makeOrders[date] = order
		self.checkRecent(self.recentOrders,self.recentOrdersOutgoing,(order.id,date,order.vendor,order.total),'O')
		self.logger.debug('Order Outgoing : ID - %s, Date - %s, Vendor - %s, Products - %s, Total - %s'%(order.id,order.date,order.vendor,order.products,order.total))
		self.packer(self.makeOrderDisplay, self.orderMain,option = 3)
		
	'''REPORTS'''

	def mainReports(self):
		self.reportsDisplay.pack()
		tk.Button(self.reportsDisplay, text='Iventory', command = lambda: self.packer(self.reportsDisplay,self.inventoryShow) ).grid(row=0,column = 0)
		tk.Button(self.reportsDisplay, text='Counting Inventory', command = self.exportCountingInventory ).grid(row=0,column = 1)
		tk.Button(self.reportsDisplay, text='Product History', command = lambda : mb.showwarning('Not Implemented','Service not implemented yet') ).grid(row=0,column = 2)
		tk.Button(self.reportsDisplay, text='Back', command = lambda : self.packer(self.reportsDisplay,self.main) ).grid(row=0,column = 3)

	def inventoryShow(self):
		self.logger.debug('Viewing Inventory')
		self.inventoryDisplay.pack()
		self.inventoryDisplay1 = tk.Frame(self.inventoryDisplay)
		self.inventoryDisplay2 = tk.Frame(self.inventoryDisplay,bd=1,relief='sunken')
		self.inventoryDisplay1.pack()
		self.inventoryDisplay2.pack()
		row=2
		tk.Button(self.inventoryDisplay1,text = 'Back',command = lambda : self.packer(self.inventoryDisplay,self.mainReports)).grid(row=0,column=0)
		tk.Button(self.inventoryDisplay1,text = 'Export',command  = self.exportInventory).grid(row=0,column=1)
		tk.Label(self.inventoryDisplay2,text = 'ID',width = 5, bd = 1, relief='raised').grid(row=1,column=0)
		tk.Label(self.inventoryDisplay2,text = 'Name',width = 20, bd = 1, relief='raised').grid(row=1,column=1)
		tk.Label(self.inventoryDisplay2,text = 'Price',width = 15, bd = 1, relief='raised').grid(row=1,column=2)
		tk.Label(self.inventoryDisplay2,text = 'Unit',width = 5, bd = 1, relief='raised').grid(row=1,column=3)
		tk.Label(self.inventoryDisplay2,text = 'Quantity',width = 15, bd = 1, relief='raised').grid(row=1,column=4)
		tk.Label(self.inventoryDisplay2,text = 'Case',width = 10, bd = 1, relief='raised').grid(row=1,column=5)
		for product in self.products.values():
			tk.Label(self.inventoryDisplay2,text = product.idNumber,width = 5).grid(row=row,column=0)
			tk.Label(self.inventoryDisplay2,text = product.name,width = 20).grid(row=row,column=1)
			tk.Label(self.inventoryDisplay2,text = product.price,width = 15).grid(row=row,column=2)
			tk.Label(self.inventoryDisplay2,text = product.unit,width = 5).grid(row=row,column = 3)
			tk.Label(self.inventoryDisplay2,text = product.quantity,width =15).grid(row=row,column=4)
			tk.Label(self.inventoryDisplay2,text = product.case,width = 10).grid(row=row,column=5)
			row+=1

	def exportInventory(self):
		self.logger.debug('Exporting Inventory')
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
		filename = fd.asksaveasfilename(defaultextension = '.pdf')
		if filename:
			out = fpdf.FPDF(format='Letter')
			self.logger.debug('Exporting Counting Inventory')
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
		self.vendorDisplay1 = tk.Frame(self.vendorDisplay)
		self.vendorDisplay2 = tk.Frame(self.vendorDisplay)
		self.vendorDisplay1.pack(side='top')
		self.vendorDisplay2.pack(side='top')
		self.vendorDisplay3 = tk.Frame(self.vendorDisplay2,bd=1,relief='sunken')
		self.vendorDisplay4 = tk.Frame(self.vendorDisplay2,bd=1,relief='sunken')
		self.vendorDisplay5 = tk.Frame(self.vendorDisplay2,bd=1,relief='sunken')
		self.vendorDisplay3.pack(side='left',anchor='n')
		self.vendorDisplay4.pack(side='left',anchor='n')
		self.vendorDisplay5.pack(side='left',anchor='n')
		tk.Button(self.vendorDisplay1, text = 'Add Vendor',command = lambda: self.packer(self.vendorDisplay, self.addVendor)).grid(row=0,column=0)
		tk.Button(self.vendorDisplay1, text = 'Delete Vendor',command =lambda: self.packer(self.vendorDisplay, self.deleteVendor)).grid(row=0,column=1)
		tk.Button(self.vendorDisplay1, text = 'View Vendor',command =lambda: self.packer(self.vendorDisplay, self.viewVendor)).grid(row=0,column=2)
		tk.Button(self.vendorDisplay1, text = 'All Vendors',command = lambda: self.packer(self.vendorDisplay, self.allVendors)).grid(row=0,column=3)
		tk.Button(self.vendorDisplay1, text = 'Back',command = lambda : self.packer(self.vendorDisplay,self.orderMain)).grid(row=0,column=4)

		tk.Label(self.vendorDisplay3,text = 'Added Vendors',width = 26,relief='raised').grid(row=0,columnspan=2)
		tk.Label(self.vendorDisplay3,text='ID',width = 5).grid(row=1,column=0)
		tk.Label(self.vendorDisplay3,text='Name',width=18).grid(row=1,column=1)
		added_row = 2
		for vendor in self.recentVendorsAdd:
			tk.Label(self.vendorDisplay3,text = vendor[0]).grid(row=added_row,column=0)
			tk.Label(self.vendorDisplay3,text = vendor[1]).grid(row=added_row,column=1)
			added_row+=1

		tk.Label(self.vendorDisplay4,text = 'Edited Vendors',width = 26,relief='raised').grid(row=0,columnspan=2)
		tk.Label(self.vendorDisplay4,text='ID',width = 5).grid(row=1,column=0)
		tk.Label(self.vendorDisplay4,text='Name',width=18).grid(row=1,column=1)
		edited_row = 2
		for vendor in self.recentVendorsEdit:
			tk.Label(self.vendorDisplay4,text = vendor[0]).grid(row=edited_row,column=0)
			tk.Label(self.vendorDisplay4,text = vendor[1]).grid(row=edited_row,column=1)
			edited_row+=1

		tk.Label(self.vendorDisplay5,text = 'Deleted Vendors',width = 26,relief='raised').grid(row=0,columnspan=2)
		tk.Label(self.vendorDisplay5,text='ID',width = 5).grid(row=1,column=0)
		tk.Label(self.vendorDisplay5,text='Name',width=18).grid(row=1,column=1)
		deleted_row = 2
		for vendor in self.recentVendorsDelete:
			tk.Label(self.vendorDisplay5,text = vendor[0]).grid(row=deleted_row,column=0)
			tk.Label(self.vendorDisplay5,text = vendor[1]).grid(row=deleted_row,column=1)
			deleted_row+=1		

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
				self.checkRecent(self.recentVendors,self.recentVendorsAdd,(idd,self.vendors[idd].name),'A')
				self.vendor_vars.append(('%s: %s'% (self.vendors[idd].idNumber,self.vendors[idd].name)))
				self.packer(self.addVendorDisplay,self.vendorShow)
				self.logger.debug('Creating Vendor: ID - %s, Name - %s, Address - %s'%(idd,name,address))
		except ValueError:
			mb.showwarning('Invalid ID','ID must be a number')
			

	def deleteVendor(self):
		self.deleteVendorDisplay.pack()
		ttk.Combobox(self.deleteVendorDisplay,textvariable = self.vendorID, values = self.vendor_vars).grid(row=0,columnspan=2)
		tk.Button(self.deleteVendorDisplay,text = 'Back',command = lambda : self.packer(self.deleteVendorDisplay,self.vendorShow)).grid(row=1,column=0)
		tk.Button(self.deleteVendorDisplay,text = 'Delete',command = self.deleteVendorID).grid(row=1,column=1)
		''' i have to figure out what to do with remaining orders from deleted vendors'''

	def deleteVendorID(self):
		try:
			idd = int(self.vendorID.get().split(':')[0])
			print idd
			self.checkRecent(self.recentVendors,self.recentVendorsDelete,(idd,self.vendors[idd].name),'D')
			del self.vendors[idd]
			self.packer(self.deleteVendorDisplay,self.vendorShow)
			self.vendorID.set('')
			self.logger.debug('Deleting Vendor with ID - %s' % idd)
		except KeyError:
			mb.showwarning('Not Found', 'No vendor with that ID')


	def viewVendor(self):
		self.viewVendorDisplay1 = tk.Frame(self.viewVendorDisplay)
		self.viewVendorDisplay2 = tk.Frame(self.viewVendorDisplay)
		self.viewVendorDisplay.pack()
		self.viewVendorDisplay1.pack()
		ttk.Combobox(self.viewVendorDisplay1,textvariable = self.vendorID, values = self.vendor_vars).grid(row=0,columnspan=2)
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
		vendor = self.vendors[int(self.vendorID.get().split(':')[0])]
		tk.Label(self.viewVendorDisplay2,text = vendor.idNumber).grid(row=1,column=0)
		tk.Label(self.viewVendorDisplay2,text = vendor.name).grid(row=1,column=1)
		tk.Label(self.viewVendorDisplay2,text = vendor.address).grid(row=1,column=2)
		self.logger.debug('Viewing vendor with id %s' % vendor.idNumber)
		

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
		self.logger.debug('Viewing all vendors')


if __name__=='__main__':
	p = Main('database')
	p.mainloop()