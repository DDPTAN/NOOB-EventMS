import frappe

def get_context(context):
    # Dapatkan path URL saat ini
    current_url = frappe.local.request.path
    # Dapatkan user dan roles
    user = frappe.session.user
    
	# Periksa user type
    user_type = frappe.get_value("User", user, "user_type")
    
	# Periksa jika role adalah Event Participant
    if "/admin/event" in current_url or "/admin/order" in current_url:
        # Jika user adalah 'Website User', redirect ke dashboard
        if user_type == "Website User":
            frappe.local.flags.redirect_location = "/dashboard"
            raise frappe.Redirect
        
	# Periksa use belum login
    if "Guest" in user:
        frappe.local.flags.redirect_location = f"/login"
        raise frappe.Redirect
    pass

