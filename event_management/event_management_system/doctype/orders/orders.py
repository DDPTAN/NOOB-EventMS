# Copyright (c) 2024, Noob Team and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Orders(Document):
    def validate(self):
        self.calculate_total_price()

    def calculate_total_price(self):
        if self.events and self.total_ticket:
            event_price = frappe.db.get_value('Events', self.events, 'price')
            self.total_price = self.total_ticket * event_price

    def before_save(self):
        self.calculate_total_price()
