import frappe
from frappe import auth

@frappe.whitelist( allow_guest=True )
def getUser(email, password):
    try:
        login_manager = frappe.auth.LoginManager()
        login_manager.authenticate(user=email, pwd=password)
        login_manager.post_login()
    except frappe.exceptions.AuthenticationError:
        frappe.clear_messages()
        frappe.local.response["message"] = {
            "success_key":0,
            "message":"Authentication Error!"
        }

        return

    api_generate = generate_keys(frappe.session.user)
    user = frappe.get_doc('User', frappe.session.user)

    frappe.response["message"] = {
        "success_key":1,
        "message":"Authentication success",
        "sid":frappe.session.sid,
        "api_key":user.api_key,
        "api_secret":api_generate,
        "username":user.username,
        "email":user.email
    }



def generate_keys(user):
    user_details = frappe.get_doc('User', user)
    api_secret = frappe.generate_hash(length=15)

    if not user_details.api_key:
        api_key = frappe.generate_hash(length=15)
        user_details.api_key = api_key

    user_details.api_secret = api_secret
    user_details.save()

    return api_secret

@frappe.whitelist(allow_guest=True)
def getEvents():
    try:
        events = frappe.get_all('Events', fields=[
            'event_title', 'organized_by', 'starts_on', 'ends_on', 'address_line_1', 'city', 'province', 
            'location', 'price', 'number_of_tickets', 'status', 'image', 'description', 'published'
        ])
        
        frappe.response["message"] = {
            "success_key": 1,
            "message": "Events fetched successfully",
            "data": events
        }
    except Exception as e:
        frappe.response["message"] = {
            "success_key": 0,
            "message": f"An error occurred: {str(e)}"
        }