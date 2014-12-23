#!usr/bin/python

#imports
import Tkinter as tk
import tkMessageBox as mb
import decimal
import shelve

class Product(object):
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
	def nam (self, value):
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

		#keeping track of total products in the system
		self.totalProducts = 0

		#main display
		self.mainDisplay = tk.Frame(self)
		self.mainDisplay.pack()

		#main display buttons
		tk.Button(self.mainDisplay, text='Quit', command = self.quit).grid(row=0,column = 3)
		tk.Button(self.mainDisplay, text='Products', command = lambda : self.packer(self.mainDisplay, self.productDisplay) ).grid(row=0,column = 0)
		tk.Button(self.mainDisplay, text='Orders', command = lambda : self.packer(self.mainDisplay, self.orderDisplay) ).grid(row=0,column = 1)
		tk.Button(self.mainDisplay, text='Reports', command = lambda: self.packer(self.mainDisplay, self.reportsDisplay) ).grid(row=0,column = 2)

		#PRODUCT VARS
		self.productDisplay = tk.Frame(self)
		self.addProductDisplay = tk.Frame(self)
		self.editProductDisplay =tk.Frame(self)
		self.editProductDisplay1 = tk.Frame(self.editProductDisplay)
		self.editProductDisplay2 = tk.Frame(self.editProductDisplay)
		self.viewDisplay = tk.Frame(self)
		self.viewDisplay2 = tk.Frame(self)
		self.deleteView = tk.Frame(self)
		self.queryProductID = tk.IntVar()
		self.productOptions = ('ID','Name','Price','Unit','Quantity','Case')
		self.productVars = dict([('id',tk.IntVar()),('name',tk.StringVar()),('price',tk.DoubleVar()),('unit',tk.StringVar()),('quantity',tk.IntVar()),('case',tk.IntVar())])

		#PRODUCTS BUTTONS
		tk.Button(self.productDisplay, text='Add Product', command = self.addProduct ).grid(row=0,column = 0)
		tk.Button(self.productDisplay, text='Edit Product', command = self.editProduct ).grid(row=0,column = 1)
		tk.Button(self.productDisplay, text='Delete Product', command = self.deleteProduct ).grid(row=0,column = 2)
		tk.Button(self.productDisplay, text='View Product', command = self.viewProduct ).grid(row=0,column = 3)
		tk.Button(self.productDisplay, text='Back', command = lambda : self.packer(self.productDisplay,self.mainDisplay) ).grid(row=0,column = 4)

		#ORDER VARS
		self.orderDisplay = tk.Frame(self)
		self.addOrderDisplay = tk.Frame(self)
		self.orderMiniDisplay = tk.Frame(self.addOrderDisplay)
		self.orderMiniDisplay2 = tk.Frame(self.addOrderDisplay)
		self.viewOrderDisplay = tk.Frame(self)
		self.viewOrderDisplay1 = tk.Frame(self.viewOrderDisplay)
		self.viewOrderDisplay3 = tk.Frame(self.viewOrderDisplay)
		self.viewOrderDisplay2 = tk.Frame(self.viewOrderDisplay)
		self.orderHistoryDisplay = tk.Frame(self)
		self.OrderVars = dict([('vendor', tk.StringVar()),('id',tk.StringVar()),('date',tk.StringVar())])
		self.OrderOptions = ('id','vendor','products','date')
		self.orderID = tk.IntVar()

		#ORDER BUTTONS
		tk.Button(self.orderDisplay, text='Add Order', command = self.addOrder ).grid(row=0,column = 0)
		tk.Button(self.orderDisplay, text='View Order', command = self.viewOrder ).grid(row=0,column = 1)
		tk.Button(self.orderDisplay, text='Order History', command = self.orderHistory ).grid(row=0,column = 2)
		tk.Button(self.orderDisplay, text='Back', command = lambda : self.packer(self.orderDisplay,self.mainDisplay) ).grid(row=0,column = 3)

		#REPORTS VARS
		self.reportsDisplay = tk.Frame(self)
		self.inventoryDisplay = tk.Frame(self)

		#REPORTS BUTTONS
		tk.Button(self.reportsDisplay, text='Iventory', command = self.inventoryShow ).grid(row=0,column = 0)
		tk.Button(self.reportsDisplay, text='Product History', command = lambda : mb.showwarning('Not Implemented','Service not implemented yet') ).grid(row=0,column = 1)
		tk.Button(self.reportsDisplay, text='Back', command = lambda : self.packer(self.reportsDisplay,self.mainDisplay) ).grid(row=0,column = 2)

	''' FUNTIONALITIES '''

	def startDatabase(self):
		database = shelve.open(self.filename)
		if database:
			self.products = database['products']
			self.orders = database['orders']
		else:
			self.products = {}
			self.orders = {}
		database.close()

	def quit(self):
		database = shelve.open(self.filename)
		database['products'] = self.products
		database['orders'] = self.orders
		database.close()
		self.master.destroy()

	def packer(self, unpacked, packed,third = None,option = None):
		unpacked.pack_forget()
		packed.pack()
		if third:
			third.pack_forget()
		if option:
			self.clearVars()

	def clearVars(self):
		for key in self.productVars:
			self.productVars[key].set('')

	''' PRODUCTS '''

	def addProduct(self):
		self.packer(self.productDisplay,self.addProductDisplay)
		tk.Button(self.addProductDisplay, text='Save', command = self.saveProduct ).grid(row=len(self.productOptions),column = 1)
		tk.Button(self.addProductDisplay, text='Cancel', command = lambda : self.packer(self.addProductDisplay,self.productDisplay) ).grid(row=len(self.productOptions),column = 0)
		for i in xrange(len(self.productOptions)):
			tk.Label(self.addProductDisplay, text = self.productOptions[i]).grid(row=i, column=0)
			tk.Entry(self.addProductDisplay, textvariable = self.productVars[self.productOptions[i].lower()]).grid(row=i,column = 1)

	def saveProduct(self):
		self.totalProducts +=1
		try:
			p = Product()
			p.name = self.productVars['name'].get()
			p.idNumber = self.productVars['id'].get()
			p.price = self.productVars['price'].get()
			p.quantity = self.productVars['quantity'].get()
			p.unit = self.productVars['unit'].get()
			p.case = self.productVars['case'].get()
			self.clearVars()
			if p.idNumber in self.products.keys():
				mb.showwarning('ID taken','There is a product with that ID')
				
			else:
				self.products[p.idNumber] = p
				self.packer(self.addProductDisplay,self.productDisplay)
		except ValueError: 
			mb.showwarning('Error','Price,ID,Quantity and Units per Case have to be numbers')

	def editSave(self,product):
		product.name = self.productVars['name'].get()
		product.quantity = self.productVars['quantity'].get()
		product.price = self.productVars['price'].get()
		product.unit = self.productVars['unit'].get()
		product.case = self.productVars['case'].get()
		self.clearVars()
		self.editProductDisplay2.pack_forget()


	def editProduct(self):
		self.packer(self.productDisplay, self.editProductDisplay)
		self.editProductDisplay1.pack()
		tk.Entry(self.editProductDisplay1,textvariable = self.queryProductID).grid(row=0,columnspan=2)
		tk.Button(self.editProductDisplay1, text='Search', command = self.searchID ).grid(row=1,column = 1)
		tk.Button(self.editProductDisplay1, text='Cancel', command = lambda : self.packer(self.editProductDisplay,self.productDisplay,self.editProductDisplay2,1) ).grid(row=1,column = 0)

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
		self.packer(self.productDisplay,self.viewDisplay)
		self.queryProductID.set(0)
		self.viewDisplay2.pack()
		self.idNumber = tk.Label(self.viewDisplay2, textvariable = self.productVars['id'],width = 5)
		self.name = tk.Label(self.viewDisplay2, textvariable = self.productVars['name'],width = 20)
		self.price = tk.Label(self.viewDisplay2,textvariable=self.productVars['price'],width = 15)
		self.unit = tk.Label(self.viewDisplay2,textvariable = self.productVars['unit'],width = 5)
		self.quantity = tk.Label(self.viewDisplay2,textvariable = self.productVars['quantity'],width = 15)
		self.case = tk.Label(self.viewDisplay2,textvariable=self.productVars['case'],width = 10)
		tk.Entry(self.viewDisplay, textvariable = self.queryProductID).grid(row=0,columnspan=2)
		tk.Button(self.viewDisplay,text = 'Search',command = self.searchViewProduct).grid(row=1,column=1)
		tk.Button(self.viewDisplay,text= 'Cancel',command = lambda: self.packer(self.viewDisplay, self.productDisplay, self.viewDisplay2, 1)).grid(row=1,column=0)

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
		self.packer(self.productDisplay, self.deleteView)
		self.queryProductID.set(0)
		tk.Entry(self.deleteView, textvariable = self.queryProductID).grid(row=0,columnspan=2)
		tk.Button(self.deleteView, text = 'Delete', command = lambda: self.deleteProductID(self.queryProductID.get())).grid(row=1,column=1)
		tk.Button(self.deleteView, text = 'Cancel',command = lambda: self.packer(self.deleteView, self.productDisplay)).grid(row=1,column=0)

	def deleteProductID(self,key):
		try:
			del self.products[key]
			self.packer(self.deleteView, self.productDisplay)
		except KeyError:
			mb.showwarning('Not Found', 'No such product in the database')


	''' ORDERS '''

	def addOrder(self):
		self.packer(self.orderDisplay, self.addOrderDisplay)
		
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
		tk.Button(self.orderMiniDisplay,text = 'Cancel',command = lambda: self.packer(self.addOrderDisplay,self.orderDisplay)).grid(row=0,column=8)

		
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
		self.addbutton = tk.Button(self.orderMiniDisplay2,text = 'Add', command=lambda: self.orderSearchID(row,self.addbutton))
		self.addbutton.grid(row=row-1,column=6)

	def orderSearchID(self,row,addbutton):
		try:
			product = self.products[self.orderProducts[-1][0].get()]
			self.mini_dict['name'].set(product.name)
			self.mini_dict['price'].set(product.price)
			addbutton.grid_forget()
			self.buildField(row)
		except KeyError:
			mb.showwarning('Invalid ID', 'The ID entered is invalid')

	def saveOrder(self):
		products = []
		total = 0
		for i in xrange(len(self.orderProducts)-1):
			product = self.products[self.orderProducts[i][0].get()]
			product.quantity += self.orderProducts[i][1].get()*product.case
			products.append((self.orderProducts[i][0].get(), self.orderProducts[i][1].get()))
		vendor = self.OrderVars['vendor'].get()
		idOrder = self.OrderVars['id'].get()
		date = self.OrderVars['date'].get()
		for (key,quant) in products:
			product = self.products[key]
			total += product.price*quant
		order = Order(idNumber = idOrder, vendor = vendor, date = date, products = products,total = total)
		self.orders[date] = order
		if self.orderMiniDisplay2.winfo_children():
			for child in self.orderMiniDisplay2.winfo_children():
				child.destroy()
		self.packer(self.addOrderDisplay, self.orderDisplay)

	def viewOrder(self):
		
		self.packer(self.orderDisplay, self.viewOrderDisplay)
		self.viewOrderID = tk.StringVar()
		
		self.viewOrderDisplay1.pack()
		tk.Entry(self.viewOrderDisplay1, textvariable = self.viewOrderID).grid(row=0,columnspan=2)
		tk.Button(self.viewOrderDisplay1, text = 'Cancel',command = lambda : self.packer(self.viewOrderDisplay,self.orderDisplay)).grid(row=1,column=0)
		tk.Button(self.viewOrderDisplay1,text = 'Search',command = self.viewOrderSearch).grid(row = 1,column = 1)

	def viewOrderSearch(self,orderID = None):
		try:
			if orderID:
				order = self.orders[orderID]
			else:
				order = self.orders[self.viewOrderID.get()]
			if self.viewOrderDisplay2.winfo_children(): 
				for child in self.viewOrderDisplay2.winfo_children():
					child.destroy()
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
			for (key,quant) in order.products:
				product = self.products[key]
				tk.Label(self.viewOrderDisplay2, text = product.idNumber,width = 5).grid(row=row, column=0)
				tk.Label(self.viewOrderDisplay2,text = product.name, width = 20).grid(row=row,column=1)
				tk.Label(self.viewOrderDisplay2,text = product.price,width = 15).grid(row=row,column=2)
				tk.Label(self.viewOrderDisplay2,text = product.unit,width = 5).grid(row=row,column=3)
				tk.Label(self.viewOrderDisplay2,text = quant,width = 15).grid(row=row,column=4)
				tk.Label(self.viewOrderDisplay2,text = product.case, width =10).grid(row=row,column=5)
				row += 1

		except KeyError:
			mb.showwarning('Not Found', 'The format of the date should be dd.mm.yyyy')

	def orderHistory(self):
		self.packer(self.orderDisplay, self.orderHistoryDisplay)
		row = 1
		tk.Label(self.orderHistoryDisplay, text = 'ID',width = 15).grid(row=0,column=1)
		tk.Label(self.orderHistoryDisplay, text = 'Vendor',width = 15).grid(row=0,column=2)
		tk.Label(self.orderHistoryDisplay, text = 'Date',width = 15).grid(row=0,column=3)
		tk.Label(self.orderHistoryDisplay,text = 'Total',width = 15).grid(row=0,column=4)
		for order in self.orders:
			tk.Label(self.orderHistoryDisplay, text = self.orders[order].id).grid(row=row,column=1)
			tk.Label(self.orderHistoryDisplay,text = self.orders[order].vendor).grid(row=row,column=2)
			tk.Label(self.orderHistoryDisplay,text = self.orders[order].date).grid(row=row,column=3)
			tk.Label(self.orderHistoryDisplay,text = self.orders[order].total).grid(row=row,column=4)
			tk.Button(self.orderHistoryDisplay,text ='View',command = lambda order = order: self.fetchOrder(order)).grid(row=row,column=5)
			row+=1

	def fetchOrder(self,orderID):
		self.packer(self.orderHistoryDisplay, self.viewOrderDisplay)
		self.viewOrderSearch(orderID)

	'''REPORTS'''

	def inventoryShow(self):
		self.packer(self.reportsDisplay,self.inventoryDisplay)
		column = 0
		row=2
		tk.Button(self.inventoryDisplay,text = 'Back',command = lambda : self.packer(self.inventoryDisplay,self.reportsDisplay)).grid(row=0,column=0)
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

	

if __name__=='__main__':
	p = Main('database')
	p.mainloop()