import frappe
from frappe import auth
from frappe import _

@frappe.whitelist( allow_guest=True )
def login(email, password):
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
def get_events():
    try:
        events = frappe.get_all('Events', fields=[ 'name',
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


@frappe.whitelist(allow_guest=True)
def get_event_by_id(id=None):
    try:
        # Retrieve the id parameter from the URL
        if not id:
            id = frappe.form_dict.id

        if not id:
            frappe.response["message"] = {
                "success_key": 0,
                "message": "Event ID is required"
            }
            return

        event = frappe.get_doc('Events', id)
        event_data = {
            'event_title': event.event_title,
            'organized_by': event.organized_by,
            'starts_on': event.starts_on,
            'ends_on': event.ends_on,
            'address_line_1': event.address_line_1,
            'city': event.city,
            'province': event.province,
            'location': event.location,
            'price': event.price,
            'number_of_tickets': event.number_of_tickets,
            'status': event.status,
            'image': event.image,
            'description': event.description,
            'published': event.published
        }

        frappe.response["message"] = {
            "success_key": 1,
            "message": "Event detail fetched successfully",
            "data": event_data
        }
    except Exception as e:
        frappe.response["message"] = {
            "success_key": 0,
            "message": f"An error occurred: {str(e)}"
        }

@frappe.whitelist()
def create_order(event_id, total_ticket):
    try:
        event = frappe.get_doc('Events', event_id)
        event_title = event.event_title
        available_tickets = event.number_of_tickets
        if total_ticket > available_tickets:
            frappe.local.response["http_status_code"] = 400
            frappe.throw(_("Not enough tickets available for the event. Only {0} tickets remaining.")
                         .format(available_tickets))
        event_price = event.price

        order = frappe.new_doc('Orders')
        order.user_id = frappe.session.user
        order.event_id = event_id
        order.event_title = event_title
        order.total_ticket = total_ticket
        order.total_price = total_ticket * event_price
        order.status = "Confirmed"
        order.insert()

        event.reload()
        event.number_of_tickets -= total_ticket

        frappe.response["message"] = {
            "success_key": 1,
            "message": "Order created successfully",
            "data": order,
        }
    except Exception as e:
        frappe.response["message"] = {
            "success_key": 0,
            "message": f"Failed to create order: {str(e)}"
        }


@frappe.whitelist()
def get_orders_by_user():
    try:
        user = frappe.session.user

        orders = frappe.get_all('Orders', filters={'user_id': user}, fields=[
            'name', 'user_id', 'event_id', 'event_title', 'total_ticket', 'total_price', 'status'
        ])

        frappe.response["message"] = {
            "success_key": 1,
            "message": "Orders fetched successfully",
            "data": orders
        }
    except Exception as e:
        frappe.response["message"] = {
            "success_key": 0,
            "message": f"An error occurred: {str(e)}"
        }

@frappe.whitelist()
def cancel_order(order_id):
    try:
        order = frappe.get_doc('Orders', order_id)

        if order.status == "Cancelled":
            frappe.response["message"] = {
                "success_key": 0,
                "message": "Order has already been cancelled",
            }
            return

        order.status = "Cancelled"
        order.save()

        event = frappe.get_doc('Events', order.event_id)
        event.number_of_tickets += order.total_ticket
        event.save()

        frappe.response["message"] = {
            "success_key": 1,
            "message": "Order cancelled successfully",
        }
    except Exception as e:
        frappe.response["message"] = {
            "success_key": 0,
            "message": f"Failed to cancel order: {str(e)}"
        }