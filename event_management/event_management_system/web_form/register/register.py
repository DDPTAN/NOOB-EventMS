import frappe

def add_event_participant_role(doc, method):
    try:
        # Periksa apakah pengguna adalah Website User
        if doc.user_type == "Website User":
            # Tambahkan peran 'Event Participant'
            role = "Event Participant"
            # Periksa apakah role "event Participant" belum ada
            # List comprehension '[r.role for r in doc.get("roles", [])]' untuk membuat daftar nama-nama role.
            if role not in [r.role for r in doc.get("roles", [])]:
                doc.append("roles", {"role": role})
                doc.save()
    except Exception as e:
        frappe.log_error(message=str(e), title="Failed to add 'Event Participant' role to user")

def get_context(context):
	# do your magic here
	pass
