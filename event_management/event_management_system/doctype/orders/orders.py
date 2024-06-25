# Copyright (c) 2024, Noob Team and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document


class Orders(Document):
    def validate(self):
        self.check_ticket_availability()
    
    def before_submit(self):
        self.calculate_total_price()
        self.reduce_event_tickets()
    
    def before_cancel(self):
        self.return_event_tickets()

    def check_ticket_availability(self):
        if self.event_id and self.total_ticket:
            available_tickets = frappe.db.get_value('Events', self.event_id, 'number_of_tickets')
            # Cek apakah jumlah tiket yang diminta melebihi jumlah yang tersedia
            if self.total_ticket > available_tickets:
                frappe.throw(_("Not enough tickets available for the event. Only {0} tickets remaining.")
                             .format(available_tickets))

    def calculate_total_price(self):
        if self.event_id and self.total_ticket:
            event_price = frappe.db.get_value('Events', self.event_id, 'price')
            self.total_price = self.total_ticket * event_price
    
    def reduce_event_tickets(self):
        if self.event_id and self.total_ticket:
            event = frappe.get_doc('Events', self.event_id)
            # Kurangi jumlah tiket yang tersedia
            event.number_of_tickets -= self.total_ticket
            event.save()
    
    def return_event_tickets(self):
        if self.event_id and self.total_ticket:
            event = frappe.get_doc('Events', self.event_id)
            # Tambahkan kembali jumlah tiket yang tersedia
            event.number_of_tickets += self.total_ticket
            event.save()