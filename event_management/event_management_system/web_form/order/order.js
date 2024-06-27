frappe.ready(function () {
	// bind events here
	if (frappe.session.user === "Guest") {
		window.location.href = "/login";
	}

	frappe.web_form.after_save = () => {
		// Redirect to login page after saving the form
		window.location.href = "/admin/order";
	};

	frappe.web_form.on("event_id", (field, value) => {
		// Ambil nilai event_id yang dipilih
		let event_id = value;

		if (event_id) {
			// Mengambil title dari event yang dipilih
			frappe.call({
				method: "frappe.client.get_value",
				args: {
					doctype: "Events",
					filters: { name: event_id },
					fieldname: "event_title",
				},
				callback: function (r) {
					if (r.message) {
						// Set nilai event_title ke hasil yang didapat dari server
						let event_title = r.message.event_title;
						frappe.web_form.set_value("event_title", event_title);
					} else {
						// Jika tidak ada data, reset nilai event_title
						frappe.web_form.set_value("event_title", "");
					}
				},
			});
		} else {
			// Jika event_id kosong, reset nilai event_title
			frappe.web_form.set_value("event_title", "");
		}
	});

	frappe.web_form.on("total_ticket", (field, value) => {
		// Ambil nilai total_ticket
		let total_ticket = value;

		// Validasi agar total_ticket tidak boleh kurang dari 1
		if (total_ticket < 1) {
			frappe.msgprint(__("Total ticket must be greater than 0"));
			frappe.web_form.set_value("total_ticket", 1); // Set nilai total_ticket ke 1
		} else {
			// Jika ada event_id yang terkait, ambil harga tiket dari event tersebut
			let event_id = frappe.web_form.get_value("event_id");
			if (event_id) {
				frappe.call({
					method: "frappe.client.get_value",
					args: {
						doctype: "Events",
						filters: { name: event_id },
						fieldname: "price",
					},
					callback: function (r) {
						if (r.message) {
							let price_per_ticket = r.message.price;
							let total_price = total_ticket * price_per_ticket;
							// Set nilai total_price ke hasil perhitungan
							frappe.web_form.set_value("total_price", total_price);
						}
					},
				});
			}
		}
	});

	frappe.web_form.after_load = () => {
		// If the form is not new
		if (!frappe.web_form.is_new) {
			// Check if status is not "Cancelled"
			if (frappe.web_form.doc.status !== "Cancelled") {
				const headerContainer = $(".web-form-header .title").first().parent();
				// Add a custom Cancel button with a confirmation dialog
				$("<button/>", {
					text: "Cancel", // Button text
					class: "btn btn-danger", // Button classes for styling
					click: function () {
						// Confirmation dialog before cancelling
						frappe.confirm(
							__("Are you sure you want to cancel this order?"),
							function () {
								frappe.call({
									method: "event_management.event_management_system.doctype.orders.orders.return_event_tickets",
									args: {
										order_id: frappe.web_form.doc.name,
									},
									freeze: true,
									freeze_message: __("Cancelling order..."),
									callback: function (response) {
										if (response.message === "success") {
											// Update the status to "Cancelled" and save the form
											frappe.web_form.set_value("status", "Cancelled");
											frappe.web_form.save();
										} else {
											frappe.msgprint(__("Failed to cancel this order."));
										}
									},
								});
							}
						);
					},
				}).appendTo(headerContainer);

				headerContainer.css({
					display: "flex",
					justifyContent: "space-between",
					alignItems: "center",
				});
			}
		}
	};

	// Manually trigger the after_load if necessary
	if (typeof frappe.web_form.after_load === "function") {
		frappe.web_form.after_load();
	}
});
