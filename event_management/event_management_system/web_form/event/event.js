frappe.ready(function() {
    // bind events here
    frappe.ui.form.on('Event', {
        starts_on: function(frm) {
            // Ambil nilai tanggal starts_on
            let starts_on = frm.doc.starts_on;
            let tomorrow = frappe.datetime.add_days(frappe.datetime.nowdate(), 1);

            // Validasi apakah starts_on tanggal ke depan
            if (starts_on && frappe.datetime.get_diff(starts_on, tomorrow) < 0) {
                frappe.msgprint(__("Start date must be tomorrow or later."));
                frm.set_value("starts_on", null); // Reset nilai starts_on ke null
            }
        },

        ends_on: function(frm) {
            frm.trigger('validate_dates');
        },

        validate_dates: function(frm) {
            let starts_on = frm.doc.starts_on;
            let ends_on = frm.doc.ends_on;
            
            //Validasi tanggal ends_on harus setelah starts_on
            if (starts_on && ends_on && frappe.datetime.get_diff(ends_on, starts_on) < 0) {
                frappe.msgprint(__("End date cannot be before start date"));
                frm.set_value("ends_on", null); // Reset nilai ends_on ke null
            }
        },

        number_of_tickets: function (frm) {
            // Ambil nilai number_of_tickets
            let tickets = frm.doc.number_of_tickets;

            // Validasi number_of_tickets agar tidak bisa negatif
            if (tickets < 0) {
                frappe.msgprint(__("Number of tickets must be greater than or equal to 0"));
                frm.set_value("number_of_tickets", 0);
            }

            // Set status berdasarkan nilai number_of_tickets
            if (tickets === 0) {
                frm.set_value("status", "Sold Out");
            } else {
                frm.set_value("status", "Available");
            }
        },

        price: function (frm) {
            let price = frm.doc.price;

            // Validasi harga tiket agar tidak bisa negatif
            if (price < 1) {
                frappe.msgprint(__("Price must be greater than 0"));
                frm.set_value("price", 1);
            }
        }
    });
});
