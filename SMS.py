#!usr/bin/python

#imports

import logging
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

class SMS(object):

	def __init__(self,filename):

		self.filename = filename
		self.startDatabase()

		self.vendor_vars = ['%s: %s' % (vendor.idNumber	, vendor.name) for vendor in self.vendors.values()]

		self.logger = logging.getLogger('StoreMSystem')
		self.logger.setLevel(logging.DEBUG)
		handler = logging.FileHandler('Logging.log')
		formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
		handler.setFormatter(formatter)
		self.logger.addHandler(handler)
		self.logger.debug('Program Started')

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

	def stopDatabase(self):
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

	def updateRecentLists(self,globalSeq,localSeq,idNumber, option):
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

	'''PRODUCTS ''' 

	def getProduct(self,key):
		return self.products[key]

	def getProducts(self):
		return self.products.keys()

	def getRecentProducts(self):
		return self.recentProducts

	def getRecentProductsAdd(self):
		return self.recentProductsAdd

	def getRecentProductsEdit(self):
		return self.recentProductsEdit

	def getRecentProductsDelete(self):
		return self.recentProductsDelete

	def createProduct(self,infoDict):
		product = Product()
		product.name = infoDict['name']
		product.idNumber = infoDict['id']
		product.price = infoDict['price']
		product.unit = infoDict['unit']
		product.quantity = infoDict['quantity']
		product.case = infoDict['case']
		if product.idNumber in self.products:
			raise KeyError
		else:
			self.products[product.idNumber] = product
			self.updateRecentLists(self.recentProducts,self.recentProductsAdd,(product.idNumber,product.name),'A')
			self.logger.debug('Product created : ID - %s, Name - %s, Price - %s, Unit - %s, Case - %s '%(product.idNumber,product.name,product.price,product.unit,product.case))

	def editProductSave(self,infoDict):
		self.products[infoDict['id']].name = infoDict['name']
		self.products[infoDict['id']].price = infoDict['price']
		self.products[infoDict['id']].unit = infoDict['unit']
		self.products[infoDict['id']].quantity = infoDict['quantity']
		self.products[infoDict['id']].case = infoDict['case']
		self.logger.debug('Product Edited : ID - %s, Name - %s, Price - %s, Unit - %s, Case - %s '%(self.products[infoDict['id']].idNumber,self.products[infoDict['id']].name,self.products[infoDict['id']].price,self.products[infoDict['id']].unit,self.products[infoDict['id']].case))
		self.updateRecentLists(self.recentProducts,self.recentProductsEdit,(self.products[infoDict['id']].idNumber,self.products[infoDict['id']].name), 'E')

	def deleteProduct(self,key):
		self.updateRecentLists(self.recentProducts,self.recentProductsDelete,(key,self.products[key].name),'D')
		p = self.products[key]
		self.logger.debug('Product deleted : ID - %s, Name - %s, Price - %s, Unit - %s, Case - %s '%(p.idNumber,p.name,p.price,p.unit,p.case))
		del self.products[key]

	''' ORDERS '''

	def getMakeOrders(self):
		return self.makeOrders.keys()

	def getOrders(self):
		return self.orders.keys()

	def getRecentOrders(self):
		return self.recentOrders

	def getRecentOrdersOutgoing(self):
		return self.recentOrdersOutgoing

	def getRecentOrdersIncoming(self):
		return self.recentOrdersIncoming

	def saveOrder(self,idOrder,date,vendor_id,products,option):
		total = 0
		for (key,price,quant) in products:
			total += price*quant
		order = Order(date,idNumber = idOrder, vendor = self.vendors[vendor_id], products = products,total = total)
		if option == 1:
			self.orders[date] = order
			self.updateRecentLists(self.recentOrders,self.recentOrdersIncoming,(order.id,date,order.vendor,order.total),'I')
			self.logger.debug('Order Incoming : ID - %s, Date - %s, Vendor - %s, Products - %s, Total - %s'%(order.id,order.date,order.vendor,order.products,order.total))
		elif option == 2:
			self.makeOrders[date] = order
			self.updateRecentLists(self.recentOrders,self.recentOrdersOutgoing,(order.id,date,order.vendor,order.total),'O')
			self.logger.debug('Order Outgoing : ID - %s, Date - %s, Vendor - %s, Products - %s, Total - %s'%(order.id,order.date,order.vendor,order.products,order.total))

	def getOrder(self,viewOrderMode,orderID):
		if viewOrderMode == 0:
			order = self.orders[orderID]
		elif  viewOrderMode == 1:
			order = self.makeOrders[orderID]
		self.logger.debug('Viewing Order ID - %s and from %s'% (order.id,order.date))
		return order

	def getOrderHistory(self,option):
		if option == 0:
			return self.orders.values()
		elif option == 1:
			return self.makeOrders.values()

	def exportOrder(self,orderDate,filename):
		order = self.makeOrders[orderDate]
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

	def exportInventory(self,filename,counting = None):
		out = fpdf.FPDF(format='Letter')
		out.add_page()
		out.set_font('Arial',size=20)
		out.cell(200,10,'Inventory',ln=1,align='C')
		out.set_font('Arial',size=10)
		if counting :
			self.logger.debug('Exporting Counting Inventory')
			for product in self.products.values():
				out.cell(200,10,'ID: %5d Name: %10s Cases: _________ Units: _________ ' % (product.idNumber, product.name),ln=1,align='C')
		else:
			self.logger.debug('Exporting Inventory')
			for product in self.products.values():
				out.cell(200,10,'ID: %5d Name: %10s Price: %5.2f Unit: %5s Quantity: %10d Case: %5d' % (product.idNumber, product.name, product.price, product.unit, product.quantity, product.case),ln=1,align='C')
		out.output(filename)

	'''VENDORS'''

	def getVendorVars(self):
		return self.vendor_vars

	def getVendors(self):
		return self.vendors.keys()

	def getVendor(self,key):
		return self.vendors[key]

	def getRecentVendors(self):
		return self.recentVendors

	def getRecentVendorsAdd(self):
		return self.recentVendorsAdd

	def getRecentVendorsEdit(self):
		return self.recentVendorsEdit

	def getRecentVendorsDelete(self):
		return self.recentVendorsDelete

	def saveVendor(self,infoDict):
		if infoDict['id'] in self.vendors.keys():
			raise KeyError
		else:
			self.vendors[infoDict['id']] = Vendor(name = infoDict['name'], address = infoDict['address'], idNumber = infoDict['id'])
			self.updateRecentLists(self.recentVendors,self.recentVendorsAdd,(infoDict['id'],infoDict['name']),'A')
			self.vendor_vars.append(('%s: %s'% (infoDict['id'],infoDict['name'])))
			self.logger.debug('Creating Vendor: ID - %s, Name - %s, Address - %s'%(infoDict['id'],infoDict['name'],infoDict['address']))

	def deleteVendor(self,key):
		self.updateRecentLists(self.recentVendors,self.recentVendorsDelete,(key,self.vendors[key].name),'D')
		for to_del in xrange(len(self.vendor_vars)):
			if int(self.vendor_vars[to_del].split(':')[0]) == key:
				del self.vendor_vars[to_del]
		del self.vendors[key]
		self.logger.debug('Deleting Vendor with ID - %s' % key)

