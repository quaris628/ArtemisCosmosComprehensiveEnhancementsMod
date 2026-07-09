from sbs_utils.procedural.execution import get_variable, set_variable

# ----- setter/getter wrappers -----

def _get_document_back_button_label():
    return get_variable(_DOCUMENT_BACK_BUTTON_LABEL_VAR_NAME)

def set_document_back_button_label(back_label):
    set_variable(_DOCUMENT_BACK_BUTTON_LABEL_VAR_NAME, back_label)

_DOCUMENT_BACK_BUTTON_LABEL_VAR_NAME = "_document_back_button_label"
