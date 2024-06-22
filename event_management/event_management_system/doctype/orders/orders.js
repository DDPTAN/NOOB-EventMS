// Copyright (c) 2024, Noob Team and contributors
// For license information, please see license.txt

frappe.ui.form.on("Orders", {
	// total_ticket: function (frm) {
	// 	// Ambil nilai total_ticket
	// 	let total_ticket = frm.doc.total_ticket;

	// 	// Validasi agar total_ticket tidak boleh 0 atau kurang dari 0
	// 	if (total_ticket <= 0) {
	// 		frappe.msgprint(__("Total ticket must be greater than 0"));
	// 		frm.set_value("total_ticket", 1); // Set nilai total_ticket ke 1 atau nilai lain yang valid
	// 	} else {
	// 		// Ambil harga tiket dari event yang terkait
	// 		if (frm.doc.events) {
	// 			frappe.call({
	// 				method: "frappe.client.get_value",
	// 				args: {
	// 					doctype: "Events",
	// 					filters: { name: frm.doc.events },
	// 					fieldname: "price",
	// 				},
	// 				callback: function (r) {
	// 					if (r.message) {
	// 						let price_per_ticket = r.message.price;
	// 						let total_price = frm.doc.total_ticket * price_per_ticket;
	// 						frm.set_value("total_price", total_price);
	// 					}
	// 				},
	// 			});
	// 		}
	// 	}
	// },

	total_ticket: function (frm) {
		let TotalTicket = frm.doc.total_ticket;

		// Validasi harga tiket agar tidak bisa negatif
		if (TotalTicket < 1) {
			frappe.msgprint(__("Total ticket must be greater than 0"));
			frm.set_value("total_ticket", 1);
		}
	},
});
