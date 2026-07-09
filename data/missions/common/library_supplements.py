from sbs_utils.helpers import FrameContext

def get_current_task():
    return FrameContext.task

def set_widget_list(console, widgets):
    FrameContext.page.set_widget_list(console, widgets)

# https://github.com/artemis-sbs/LegendaryMissions/issues/564
# This music_base_folder setting is practically never respected in vanilla
def get_full_music_file_path(name):
    music_base_folder = FrameContext.context.sbs.get_preference_string("music_base_folder")
    return f"music/{music_base_folder}/{name}"
