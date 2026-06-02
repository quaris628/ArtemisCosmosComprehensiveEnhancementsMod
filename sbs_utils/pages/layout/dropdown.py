from .column import Column
from ...helpers import FrameContext


class Dropdown(Column):
    def __init__(self, tag, props) -> None:
        super().__init__()
        self.values = props
        self.tag = tag
        #TODO: Prase out default ?
        self._value = ""
        
    def _present(self, event):
        ctx = FrameContext.context
        ctx.sbs.send_gui_dropdown(event.client_id, self.region_tag,
            self.tag, self.values,
            self.bounds.left, self.bounds.top, self.bounds.right, self.bounds.bottom)
        
    def on_message(self, event):
        if event.sub_tag == self.tag:
            self.value = event.value_tag
        super().on_message(event)

    def update(self, props):
        self.props = props

    @property
    def value(self):
        return self._value
       
    @value.setter
    def value(self, v):
        self._value= v
        self.update_variable()


# https://github.com/artemis-sbs/LegendaryMissions/issues/568
# Caused lots of sync issues with the ship type editing dropdowns

class DropdownPatched(Column):
    def __init__(self, tag, values, value=None, style=None):
        super().__init__()
        
        self.tag = tag
        
        if isinstance(values, str):
            self._values_as_list = values.split(",")
            self._values_as_csv = values
        else: # list
            self._values_as_list = values
            self._values_as_csv = ",".join(values)
        
        if value is None:
            if len(self._values_as_list) > 0:
                self._selected_value = self._values_as_list[0]
            else:
                self._selected_value = ""
        else:
            self._selected_value = value
        
        if style is None or len(style) == 0:
            self._style = ""
        elif style[-1] != ";": # see issue #99
            self._style = f"{style};"
        else:
            self._style = style
        
        self._props_cache = self._get_props_string()
    
    @property
    def values_as_list(self):
        return self._values_as_list
    
    @values_as_list.setter
    def values_as_list(self, val):
        self._values_as_list = val
        self._values_as_csv = ",".join(val)
        self._default_selected_value()
        self._update_props_cache()
        # mark dirty?
    
    @property
    def values_as_csv(self):
        return self._values_as_csv
    
    @values_as_csv.setter
    def values_as_csv(self, val):
        self._values_as_list = val.split(",")
        self._values_as_csv = val
        self._default_selected_value()
        self._update_props_cache()
        # mark dirty?
    
    def _default_selected_value(self):
        if self._selected_value in self._values_as_list:
            return
        if len(self._values_as_list) > 0:
            self._selected_value = self._values_as_list[0]
        else:
            self._selected_value = ""
        self._update_props_cache()
    
    @property
    def value(self):
        return self._selected_value
    
    @value.setter
    def value(self, val):
        self._update_selected_value(val)
        # mark dirty?
    
    # for behavior shared between being triggered programatically
    # and triggered by a gui click
    def _update_selected_value(self, val):
        if self._selected_value == val:
            return
        if val not in self._values_as_list:
            if len(self._selected_value) == 0:
                return
            val = ""
        self._selected_value = val
        self._update_props_cache()
        self.update_variable()
    
    def update_style(self, val):
        if self._style == val:
            return
        if val is None or len(val) == 0:
            self._style = ""
        elif val[-1] != ";":
            # https://github.com/artemis-sbs/LegendaryMissions/issues/99
            # creating an intermediate string value adds a small performance cost
            # but hopefully this correction won't be needed very often
            self._style = f"{val};"
        else:
            self._style = val
        self._update_props_cache()
        # mark dirty?
    
    def _update_props_cache(self):
        self._props_cache = self._get_props_string()
    
    def _get_props_string(self):
        return f"$text:{self._selected_value};list:{self._values_as_csv};{self._style}"
    
    def _present(self, event):
        FrameContext.context.sbs.send_gui_dropdown(event.client_id, self.region_tag, self.tag, self._props_cache, self.bounds.left, self.bounds.top, self.bounds.right, self.bounds.bottom)
        
    def on_message(self, event):
        if event.sub_tag == self.tag:
            self._update_selected_value(event.value_tag)
        super().on_message(event)
