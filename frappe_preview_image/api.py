# frappe_preview_image/api.py

import frappe
from frappe.utils.file_manager import save_file

@frappe.whitelist()
def save_preview_image(project_id, thumbnail, configurator_project_name):
    """
    Saves a Base64 thumbnail as a File document and attaches it to a Configurator Project.
    This function is whitelisted to be called from server scripts.
    """
    if not thumbnail:
        frappe.log_error("No thumbnail provided.", "Preview Image Sync")
        return

    # Strip data URI prefix if present
    if thumbnail.startswith("data:image"):
        thumbnail = thumbnail.split(",", 1)[1]

    try:
        file_doc = save_file(
            fname=f"{project_id}_preview.png",
            content=thumbnail,
            dt="Configurator Project",
            dn=configurator_project_name,
            is_private=0,
            decode=True
        )

        frappe.db.set_value("Configurator Project", configurator_project_name, "attach_image", file_doc.file_url)
        return file_doc.file_url

    except Exception as e:
        frappe.log_error(f"Failed to create preview image for {project_id}: {e}", "Preview Image Sync")
        return None
