app_description = "Unity Project"
app_email = "guenther.eder@indigitalform.com"
app_license = "mit"
app_name = "frappe_preview_image"
app_publisher = "In Digital Form GmbH"
app_title = "Unity Project"


doc_events = {
    "Unity Project": {
        "after_save": "frappe_preview_image.frappe_preview_image.on_after_save"
    }
}