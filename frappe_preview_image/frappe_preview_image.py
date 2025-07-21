# frappe_preview_image/frappe_preview_image/frappe_preview_image.py

import frappe
import json
from frappe.utils.file_manager import save_file


def on_after_save(doc, method):
    """
    After saving a Configurator Project, parse its stored JSON to extract a Base64 thumbnail,
    create a File record, and update the preview_image field with the file URL.
    """
    # 1) Parse the ConfiguratorProject's project_data JSON
    # data = json.loads(doc.project_data or "{}")
    # thumb = data.get("thumbnail")
    thumb = doc.thumbnail
    if not thumb:
        return

    # 2) Strip data URI prefix if present
    if thumb.startswith("data:image"):
        thumb = thumb.split(",", 1)[1]

    # 3) Save the PNG via save_file (decodes Base64)
    filedoc = save_file(
        f"{doc.project_id}_preview.png",
        thumb,
        "Configurator Project",
        doc.name,
        is_private=0,
        decode=True
    )

    # 4) Update the preview_image field with the file URL
    frappe.db.set_value(
        "Configurator Project",
        doc.name,
        "preview_image",
        filedoc.file_url,
        update_modified=False
    )
