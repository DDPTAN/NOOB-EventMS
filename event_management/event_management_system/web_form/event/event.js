frappe.ready(function () {
	// Bind events to fields in Web Form using frappe.web_form.on

	frappe.web_form.after_save = () => {
		// Redirect to login page after saving the form
		window.location.href = "/admin/event";
	};

	frappe.web_form.on("starts_on", (field, value) => {
		// Ambil nilai tanggal starts_on
		let starts_on = value;
		let tomorrow = frappe.datetime.add_days(frappe.datetime.nowdate(), 1);

		// Validasi apakah starts_on adalah tanggal masa depan
		if (starts_on && frappe.datetime.get_diff(starts_on, tomorrow) < 0) {
			frappe.msgprint(__("Start date must be tomorrow or later."));
			frappe.web_form.set_value("starts_on", null); // Reset nilai starts_on ke null
		}
	});

	frappe.web_form.on("ends_on", (field, value) => {
		validate_dates();
	});

	function validate_dates() {
		let starts_on = frappe.web_form.get_value("starts_on");
		let ends_on = frappe.web_form.get_value("ends_on");

		// Validasi tanggal ends_on harus setelah starts_on
		if (starts_on && ends_on && frappe.datetime.get_diff(ends_on, starts_on) < 0) {
			frappe.msgprint(__("End date cannot be before start date"));
			frappe.web_form.set_value("ends_on", null); // Reset nilai ends_on ke null
		}
	}

	frappe.web_form.on("number_of_tickets", (field, value) => {
		// Ambil nilai number_of_tickets
		let tickets = value;

		// Validasi number_of_tickets agar tidak bisa negatif
		if (tickets < 0) {
			frappe.msgprint(__("Number of tickets must be greater than or equal to 0"));
			frappe.web_form.set_value("number_of_tickets", 0);
		}

		// Set status berdasarkan nilai number_of_tickets
		let status = tickets === 0 ? "Sold Out" : "Available";
		frappe.web_form.set_value("status", status);
	});

	frappe.web_form.on("price", (field, value) => {
		let price = value;

		// Validasi harga tiket agar tidak bisa negatif
		if (price < 1) {
			frappe.msgprint(__("Price must be greater than 0"));
			frappe.web_form.set_value("price", 1);
		}
	});
});
