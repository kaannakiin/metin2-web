import uiScriptLocale

IMG_DIR = "d:/ymir work/ui/game/advanced_game_options/"

TITLE_IMAGE_TEXT_X = 5
TITLE_IMAGE_TEXT_Y = 4

OPTION_START_X = 17
SLIDER_POSITION_X = 50

SLIDER_START_Y = 40
BUTTON_START_Y = 33
BUTTON_NEXT_Y = 20

RADIO_BUTTON_RANGE_X = 80
TOGGLE_BUTTON_RANGE_X = 65

RADIO_BUTTON_TEXT_X = 25
TOGGLE_BUTTON_TEXT_X = 45

SMALL_OPTION_HEIGHT = 65
NORMAL_OPTION_HEIGHT = 80
SLIDER_OPTION_HEIGHT = 65

PRIMARY_COLOR = 0xffd0c2b7
SECONDARY_COLOR = 0xff9f9892

window = {
	"name" : "GameOptionDialog",
	# Dont touch these lines!
	"style" : (),
	"x" : 222,
	"y" :1,
	"width" : 371,
	"height" : 404,
	# Dont touch these lines!
	"children" :
	(
		{
			"name" : "camera_mode_window",
			"type" : "window",
			"x" : 0,
			"y" : 5,
			"width":304,
			"height":SMALL_OPTION_HEIGHT,
			"children":
			(
				{
					"name" : "camera_mode_title_img",
					"type" : "expanded_image",
					"x" : 5,
					"y" : 0,
					"image" : IMG_DIR+"option_title.png",
					"children":
					(
						{
							"name" : "title_camera_mode",
							"type" : "text",
							"x" : TITLE_IMAGE_TEXT_X,
							"y" : TITLE_IMAGE_TEXT_Y,
							"text_horizontal_align":"left",
							"text" : uiScriptLocale.OPTION_CAMERA_DISTANCE,
						},
					),
				},
				{
					"name" : "camera_short",
					"type" : "radio_button",
					"x" : OPTION_START_X+RADIO_BUTTON_RANGE_X*0,
					"y" : 33,
					"text" : uiScriptLocale.OPTION_CAMERA_DISTANCE_SHORT,
					"text_x" : RADIO_BUTTON_TEXT_X,
					"default_image" : IMG_DIR + "radio_unselected.png",
					"over_image" : IMG_DIR + "radio_unselected.png",
					"down_image" : IMG_DIR + "radio_selected.png",
				},
				{
					"name" : "camera_long",
					"type" : "radio_button",
					"x" : OPTION_START_X+RADIO_BUTTON_RANGE_X*1,
					"y" : 33,
					"text" : uiScriptLocale.OPTION_CAMERA_DISTANCE_LONG,
					"text_x" : RADIO_BUTTON_TEXT_X,
					"default_image" : IMG_DIR + "radio_unselected.png",
					"over_image" : IMG_DIR + "radio_unselected.png",
					"down_image" : IMG_DIR + "radio_selected.png",
				},
			),
		},
		{
			"name" : "fog_mode_window",
			"type" : "window",
			"x" : 0,
			"y" : SMALL_OPTION_HEIGHT+5,
			"width":304,
			"height":SMALL_OPTION_HEIGHT,
			"children":
			(
				{
					"name" : "fog_mode_title_img",
					"type" : "expanded_image",
					"x" : 5,
					"y" : 0,
					"image" : IMG_DIR+"option_title.png",
					"children":
					(
						{
							"name" : "title_fog_mode",
							"type" : "text",
							"x" : TITLE_IMAGE_TEXT_X,
							"y" : TITLE_IMAGE_TEXT_Y,
							"text_horizontal_align":"left",
							"text" : uiScriptLocale.OPTION_FOG,
						},
					),
				},
				{
					"name" : "fog_level0",
					"type" : "radio_button",
					"x" : OPTION_START_X+RADIO_BUTTON_RANGE_X*0,
					"y" : 33,
					"text" : uiScriptLocale.OPTION_FOG_DENSE,
					"text_x" : RADIO_BUTTON_TEXT_X,
					"default_image" : IMG_DIR + "radio_unselected.png",
					"over_image" : IMG_DIR + "radio_unselected.png",
					"down_image" : IMG_DIR + "radio_selected.png",
				},
				{
					"name" : "fog_level1",
					"type" : "radio_button",
					"x" : OPTION_START_X+RADIO_BUTTON_RANGE_X*1,
					"y" : 33,
					"text" : uiScriptLocale.OPTION_FOG_MIDDLE,
					"text_x" : RADIO_BUTTON_TEXT_X,
					"default_image" : IMG_DIR + "radio_unselected.png",
					"over_image" : IMG_DIR + "radio_unselected.png",
					"down_image" : IMG_DIR + "radio_selected.png",
				},
				{
					"name" : "fog_level2",
					"type" : "radio_button",
					"x" : OPTION_START_X+RADIO_BUTTON_RANGE_X*2,
					"y" : 33,
					"text" : uiScriptLocale.OPTION_FOG_LIGHT,
					"text_x" : RADIO_BUTTON_TEXT_X,
					"default_image" : IMG_DIR + "radio_unselected.png",
					"over_image" : IMG_DIR + "radio_unselected.png",
					"down_image" : IMG_DIR + "radio_selected.png",
				},
			),
		},
		{
			"name" : "night_mode_window",
			"type" : "window",
			"x" : 0,
			"y" : SMALL_OPTION_HEIGHT*2+5,
			"width":304,
			"height":SMALL_OPTION_HEIGHT,
			"children":
			(
				{
					"name" : "night_mode_title_img",
					"type" : "expanded_image",
					"x" : 5,
					"y" : 0,
					"image" : IMG_DIR+"option_title.png",
					"children":
					(
						{
							"name" : "title_night_mode",
							"type" : "text",
							"x" : TITLE_IMAGE_TEXT_X,
							"y" : TITLE_IMAGE_TEXT_Y,
							"text_horizontal_align":"left",
							"text" : uiScriptLocale.OPTION_NIGHT_MODE,
						},
					),
				},
				{
					"name" : "night_mode_on",
					"type" : "radio_button",
					"x" : OPTION_START_X+RADIO_BUTTON_RANGE_X*0,
					"y" : 33,
					"text" : uiScriptLocale.OPTION_NIGHT_MODE_ON,
					"text_x" : RADIO_BUTTON_TEXT_X,
					"default_image" : IMG_DIR + "radio_unselected.png",
					"over_image" : IMG_DIR + "radio_unselected.png",
					"down_image" : IMG_DIR + "radio_selected.png",
				},
				{
					"name" : "night_mode_off",
					"type" : "radio_button",
					"x" : OPTION_START_X+RADIO_BUTTON_RANGE_X*1,
					"y" : 33,
					"text" : uiScriptLocale.OPTION_NIGHT_MODE_OFF,
					"text_x" : RADIO_BUTTON_TEXT_X,
					"default_image" : IMG_DIR + "radio_unselected.png",
					"over_image" : IMG_DIR + "radio_unselected.png",
					"down_image" : IMG_DIR + "radio_selected.png",
				},
			),
		},
		{
			"name" : "snow_mode_window",
			"type" : "window",
			"x" : 0,
			"y" : SMALL_OPTION_HEIGHT*3+5,
			"width":304,
			"height":SMALL_OPTION_HEIGHT,
			"children":
			(
				{
					"name" : "snow_mode_title_img",
					"type" : "expanded_image",
					"x" : 5,
					"y" : 0,
					"image" : IMG_DIR+"option_title.png",
					"children":
					(
						{
							"name" : "title_snow_mode",
							"type" : "text",
							"x" : TITLE_IMAGE_TEXT_X,
							"y" : TITLE_IMAGE_TEXT_Y,
							"text_horizontal_align":"left",
							"text" : uiScriptLocale.OPTION_SNOW_MODE,
						},
					),
				},
				{
					"name" : "snow_mode_on",
					"type" : "radio_button",
					"x" : OPTION_START_X+RADIO_BUTTON_RANGE_X*0,
					"y" : 33,
					"text" : uiScriptLocale.OPTION_SNOW_MODE_ON,
					"text_x" : RADIO_BUTTON_TEXT_X,
					"default_image" : IMG_DIR + "radio_unselected.png",
					"over_image" : IMG_DIR + "radio_unselected.png",
					"down_image" : IMG_DIR + "radio_selected.png",
				},
				{
					"name" : "snow_mode_off",
					"type" : "radio_button",
					"x" : OPTION_START_X+RADIO_BUTTON_RANGE_X*1,
					"y" : 33,
					"text" : uiScriptLocale.OPTION_SNOW_MODE_OFF,
					"text_x" : RADIO_BUTTON_TEXT_X,
					"default_image" : IMG_DIR + "radio_unselected.png",
					"over_image" : IMG_DIR + "radio_unselected.png",
					"down_image" : IMG_DIR + "radio_selected.png",
				},
			),
		},
		{
			"name" : "snow_texture_mode_window",
			"type" : "window",
			"x" : 0,
			"y" : SMALL_OPTION_HEIGHT*4+5,
			"width":304,
			"height":SMALL_OPTION_HEIGHT,
			"children":
			(
				{
					"name" : "snow_texture_mode_title_img",
					"type" : "expanded_image",
					"x" : 5,
					"y" : 0,
					"image" : IMG_DIR+"option_title.png",
					"children":
					(
						{
							"name" : "title_snow_texture_mode",
							"type" : "text",
							"x" : TITLE_IMAGE_TEXT_X,
							"y" : TITLE_IMAGE_TEXT_Y,
							"text_horizontal_align":"left",
							"text" : uiScriptLocale.OPTION_SNOW_TEXTURE_MODE,
						},
					),
				},
				{
					"name" : "snow_texture_mode_on",
					"type" : "radio_button",
					"x" : OPTION_START_X+RADIO_BUTTON_RANGE_X*0,
					"y" : 33,
					"text" : uiScriptLocale.OPTION_SNOW_TEXTURE_MODE_ON,
					"text_x" : RADIO_BUTTON_TEXT_X,
					"default_image" : IMG_DIR + "radio_unselected.png",
					"over_image" : IMG_DIR + "radio_unselected.png",
					"down_image" : IMG_DIR + "radio_selected.png",
				},
				{
					"name" : "snow_texture_mode_off",
					"type" : "radio_button",
					"x" : OPTION_START_X+RADIO_BUTTON_RANGE_X*1,
					"y" : 33,
					"text" : uiScriptLocale.OPTION_SNOW_TEXTURE_MODE_OFF,
					"text_x" : RADIO_BUTTON_TEXT_X,
					"default_image" : IMG_DIR + "radio_unselected.png",
					"over_image" : IMG_DIR + "radio_unselected.png",
					"down_image" : IMG_DIR + "radio_selected.png",
				},
			),
		},
	),
}