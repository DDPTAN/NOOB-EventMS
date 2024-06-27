# Copyright (c) 2024, Noob Team and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document


class Orders(Document):
    def validate(self):
        self.check_ticket_availability()
    
    def before_save(self):
        if self.is_new():
            self.calculate_total_price()
            self.reduce_event_tickets()

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
    
    @frappe.whitelist()
    def return_event_tickets(order_id):
        order = frappe.get_doc('Orders', order_id)
        if order.event_id and order.total_ticket:
            event = frappe.get_doc('Events', order.event_id)
            # Tambahkan kembali jumlah tiket yang tersedia
            event.number_of_tickets += order.total_ticket
            event.save()
            # Kembalikan pesan sukses
            return "success"
        else:
            # Kembalikan pesan error jika tidak berhasil
            return "failed"