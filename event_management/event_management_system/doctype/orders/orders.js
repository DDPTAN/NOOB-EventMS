// Copyright (c) 2024, Noob Team and contributors
// For license information, please see license.txt

frappe.ui.form.on("Orders", {
	total_ticket: function (frm) {
		// Ambil nilai total_ticket
		let total_ticket = frm.doc.total_ticket;

		// Validasi agar total_ticket tidak boleh 0 atau kurang dari 0
		if (total_ticket < 1) {
			frappe.msgprint(__("Total ticket must be greater than 0"));
			frm.set_value("total_ticket", 1); // Set nilai total_ticket ke 1
		} else {
			// Ambil harga tiket dari event yang terkait
			if (frm.doc.event_id) {
				frappe.call({
					method: "frappe.client.get_value",
					args: {
						doctype: "Events",
						filters: { name: frm.doc.event_id },
						fieldname: "price",
					},
					callback: function (r) {
						if (r.message) {
							let price_per_ticket = r.message.price;
							let total_price = frm.doc.total_ticket * price_per_ticket;
							frm.set_value("total_price", total_price);
						}
					},
				});
			}
		}
	},

	refresh: function (frm) {
		if (!frm.doc.user_id) {
			frm.set_value("user_id", frappe.session.user);
		}

		if(!frm.is_new()) {
			frm.disable_save();
			frm.set_df_property("event_id", "read_only", 1);
			frm.set_df_property("total_ticket", "read_only", 1);

			if (frm.doc.status !== "Cancelled") {
				frm.add_custom_button(__("Cancel"), function () {
					// Tampilkan konfirmasi sebelum menjalankan fungsi cancel
					frappe.confirm(__("Are you sure you want to cancel this order?"), function () {
						frm.call({
							doc: frm.doc,
							method: "return_event_tickets",
							args: {
								order_id: frm.doc.name,
							},
							freeze: true,
							freeze_message: __("Cancelling order..."),
							callback: function (response) {
								if (response.message === "success") {
									// Ubah status menjadi Cancelled setelah fungsi sukses
									frm.set_value("status", "Cancelled");
									frm.save();
								} else {
									frappe.msgprint(__("Failed to cancel this order."));
								}
							},
						});
					});
				}).addClass("btn-danger");
			}
		}
	},
});
