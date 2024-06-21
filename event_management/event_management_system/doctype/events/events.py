# Copyright (c) 2024, Noob Team and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document


class Events(Document):
	def validate(self):
		self.location = f"{self.address_line_1}, {self.city}, {self.province}"

		if self.number_of_tickets < 0:
			frappe.throw(_("Number of tickets must be greater than or equal to 0"))
		
		if self.price < 1:
			frappe.throw(_("Price must be greater than 0"))
    
	def before_save(self):
		if self.number_of_tickets == 0:
			self.status = 'Sold Out'
		else:
			self.status = 'Available'
