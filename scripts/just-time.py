import obspython as obs
from datetime import datetime

source_time = ""
enabled = False

# ------------------------------------------------------------

def update_text():
	global source_time
	global enabled

	src_time = obs.obs_get_source_by_name(source_time)

	if source_time is not None:
		try:
			current = datetime.now().strftime('%H:%M:%S')
			settings = obs.obs_data_create()
			obs.obs_data_set_string(settings, "text", current)
			obs.obs_source_update(src_time, settings)
			obs.obs_data_release(settings)
		except Exception as err:
			obs.script_log(obs.LOG_WARNING, "Error: " + err)
			obs.remove_current_callback()

		obs.obs_source_release(src_time)

def refresh_pressed(props, prop):
	update_text()

# ------------------------------------------------------------

def script_description():
	return \
        """
        <h2>just current time</h2>
		select text source, enable. time.
        """

def script_update(settings):
	global source_time
	global enabled

	source_time = obs.obs_data_get_string(settings, "source_time")
	enabled    		= obs.obs_data_get_bool(settings, "enabled")

	obs.timer_remove(update_text)

	if source_time != "" and enabled:
		obs.timer_add(update_text, 1000)

def script_properties():
	props = obs.obs_properties_create()

	obs.obs_properties_add_bool(props, "enabled", "Enable")
	p = obs.obs_properties_add_list(props, "source_time", "Text Source Time", obs.OBS_COMBO_TYPE_EDITABLE, obs.OBS_COMBO_FORMAT_STRING)
	
	sources = obs.obs_enum_sources()
	if sources is not None:
		for source in sources:
			source_id = obs.obs_source_get_unversioned_id(source)
			if source_id == "text_gdiplus" or source_id == "text_ft2_source":
				name = obs.obs_source_get_name(source)
				obs.obs_property_list_add_string(p, name, name)
		obs.source_list_release(sources)

	obs.obs_properties_add_button(props, "button", "Refresh", refresh_pressed)
	return props
