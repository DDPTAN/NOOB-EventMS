frappe.ready(function () {
	// Check if the user is logged in using frappe.session.user
	if (frappe.session.user !== "Guest") {
		// If the user is logged in (not Guest), redirect to the dashboard
		window.location.href = "/dashboard";
	} else {
		// Bind events here
		frappe.web_form.after_save = () => {
			// Redirect to login page after saving the form
			let user_email = frappe.web_form.get_value("email");
			frappe.call({
                method: "frappe.client.set_value",
                args: {
                    doctype: "User",
                    fieldname: "user_type",
                    value: "Website User",
                    filters: {
                        "email": user_email
                    }
                },
                callback: function(r) {
                    if(!r.exc) {
                        console.log("User Type set to Website User for " + user_email);
                    } else {
                        console.error("Failed to set User Type for " + user_email);
                    }
                }
            });
			window.location.href = "/login";
		};
	}
});
