# frappe_preview_image/frappe_preview_image/frappe_preview_image.py

import frappe
from frappe.utils.file_manager import save_file


def on_after_save(doc, method):
    """
    After saving a Unity Project, get its thumbnail, create a File record,
    and attach it to the corresponding Configurator Project.
    """

    if not doc.thumbnail:
        return

    project_id = doc.name

    # Find the corresponding Configurator Project name
    cp_name = frappe.db.get_value("Configurator Project", {"project_id": project_id})
    if not cp_name:
        frappe.log_error(f"No Configurator Project found for Unity Project {project_id}", "Preview Image Sync")
        return

    thumb = doc.thumbnail
    # Strip data URI prefix if present
    if thumb.startswith("data:image"):
        thumb = thumb.split(",", 1)[1]

    # Save the PNG via save_file, attached to the Configurator Project
    try:
        file_doc = save_file(
            fname=f"{project_id}_preview.png",
            content=thumb,
            dt="Configurator Project",
            dn=cp_name
        )

        # Update the attach_image field in Configurator Project without triggering save hooks
        frappe.db.set_value("Configurator Project", cp_name, "attach_image", file_doc.file_url)

    except Exception as e:
        frappe.log_error(f"Failed to create preview image for {project_id}: {e}", "Preview Image Sync")
