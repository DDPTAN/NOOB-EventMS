import frappe

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

def get_context(context):
	# do your magic here
	pass
