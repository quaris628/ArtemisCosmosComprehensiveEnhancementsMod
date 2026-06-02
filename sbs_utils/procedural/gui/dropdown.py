from ...helpers import FrameContext
from ..style import apply_control_styles
from ...pages.layout.dropdown import Dropdown, DropdownPatched

def gui_drop_down(props, style=None, var=None, data=None):
    """ Draw a gui drop down list 

    Args:
        props (str): 
        style (style, optional): Style. Defaults to None.
        var (str, optional): Variable name to set the selection to. Defaults to None.
        data (object, optional): data to pass the handler. Defaults to None.

    Returns:
        layout object: The Layout object created
    """    
    page = FrameContext.page
    task = FrameContext.task
    if page is None:
        return None
    tag = page.get_tag()
    props = task.compile_and_format_string(props)
    layout_item = Dropdown(tag, props)
    layout_item.data = data
    if var is not None:
        layout_item.var_name = var
        layout_item.var_scope_id = task.get_id()
    apply_control_styles(".dropdown", style, layout_item, task)
    # Last in case tag changed in style
    page.add_content(layout_item, None)
    return layout_item


# https://github.com/artemis-sbs/LegendaryMissions/issues/568
# Caused lots of sync issues with the ship type editing dropdowns

# sbs_utils/procedural/gui/dropdown.py gui_drop_down()
def gui_dropdown_patched(values, value=None, style=None, var=None, data=None):
    """ Draw a gui drop down list 

    Args:
        values (list[str] | str): list of options, either as a list of
            strings or as a comma-delimited string
        value (str | None): Default first option in the list.
            What option starts as selected.
        style (style, optional): Style. Defaults to None.
        var (str, optional): Variable name to set the selection to. Defaults to None.
        data (object, optional): data to pass the handler. Defaults to None.

    Returns:
        layout object: The Layout object created
    """
    page = FrameContext.page
    task = FrameContext.task
    if page is None:
        return None
    tag = page.get_tag()
    layout_item = DropdownPatched(tag, values, value, style)
    layout_item.data = data # pylint: disable=attribute-defined-outside-init
    if var is not None:
        layout_item.var_name = var # pylint: disable=attribute-defined-outside-init
        layout_item.var_scope_id = task.get_id() # pylint: disable=attribute-defined-outside-init
    apply_control_styles(".dropdown", style, layout_item, task)
    # Last in case tag changed in style
    page.add_content(layout_item, None)
    return layout_item
