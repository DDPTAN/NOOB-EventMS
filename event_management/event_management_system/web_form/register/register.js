frappe.ready(function () {
	// Check if the user is logged in using frappe.session.user
	if (frappe.session.user !== "Guest") {
		// If the user is logged in (not Guest), redirect to the dashboard
		window.location.href = "/dashboard";
	} else {
		// Bind events here
		frappe.web_form.after_save = () => {
			// Redirect to login page after saving the form
			window.location.href = "/login";
		};
	}
});
