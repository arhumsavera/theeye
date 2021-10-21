# these can be refactored and improved later
# but provide a way we can have variable validations
def validate_page_interaction_pageview(data):
    required = {"host", "path"}
    return set(data.keys()) == required


def validate_page_interaction_cta_click(data):
    required = {"host", "path", "element"}
    return set(data.keys()) == required


def validate_form_interaction_submit(data):
    required = {"host", "path", "form"}
    return set(data.keys()) == required


payload_validation_dict = {
    "page interaction_pageview": validate_page_interaction_pageview,
    "page interaction_cta click": validate_page_interaction_cta_click,
    "form interaction_submit": validate_form_interaction_submit,
}
