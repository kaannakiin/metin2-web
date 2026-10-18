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

RADIO_BUTTON_TEXT_X = 15
TOGGLE_BUTTON_TEXT_X = 35

SMALL_OPTION_HEIGHT = 65
NORMAL_OPTION_HEIGHT = 80
SLIDER_OPTION_HEIGHT = 65

PRIMARY_COLOR = 0xffd0c2b7
SECONDARY_COLOR = 0xff9f9892

window = {
	"name" : "GameOptionDialog",
	"style" : (),
	"x" : 222,
	"y" :1,
	"width" : 371,
	"height" : 404,
	"children" :
	(
		{
			"name" : "pickup_premium_info_window",
			"type" : "window",
			"x" : 0,
			"y" : 5,
			"width":304,
			"height":85,
			"children":
			(
				{
					"name" : "pickup_premimum_image",
					"type" : "image",
					"x" : 5,
					"y" : 0,
					"image" : "d:/ymir work/ui/game/option/info_bg.tga",
					"children":
					(
						{
							"name" : "pickup_premium_status",
							"type" : "text",
							"x" : 60,
							"y" : 6,
							"text" : uiScriptLocale.AUTO_PICKUP_PREMIUM_STATUS,
							"fontname" : "Verdana:17",
							"color" : 0xFFC1C1C1,
							"outline" : 1,
						},
						{
							"name" : "pickup_premium_status_text",
							"type" : "text",
							"x" : 112,
							"y" : 6,
							"text" : "",
							"fontname" : "Verdana:17",
							"color" : 0xFFC1C1C1,
							"outline" : 1,
						},
						{
							"name" : "pickup_premium_info",
							"type" : "text",
							"x" : 60,
							"y" : 28,
							"text" : uiScriptLocale.AUTO_PICKUP_PREMIUM_INFO,
							"fontname" : "Verdana:13",
							"color" : 0xFFFFA900,
							"outline" : 1,
						},
						{
							"name" : "pickup_premium_info_benefit_1",
							"type" : "text",
							"x" : 60,
							"y" : 43,
							"text" : uiScriptLocale.AUTO_PICKUP_PREMIUM_INFO_BENEFIT_1,
							"fontname" : "Verdana:12",
							"color" : 0xFFC1C1C1,
							"outline" : 1,
						},
						{
							"name" : "pickup_premium_info_benefit_2",
							"type" : "text",
							"x" : 60,
							"y" : 56,
							"text" : uiScriptLocale.AUTO_PICKUP_PREMIUM_INFO_BENEFIT_2,
							"fontname" : "Verdana:12",
							"color" : 0xFFC1C1C1,
							"outline" : 1,
						},
					),
				},
			),
		},
		{
			"name" : "pickup_activate_window",
			"type" : "window",
			"x" : 0,
			"y" : 95,
			"width":304,
			"height":SMALL_OPTION_HEIGHT,
			"children":
			(
				{
					"name" : "pickup_title_img",
					"type" : "expanded_image",
					"x" : 5,
					"y" : 0,
					"image" : IMG_DIR+"option_title.png",
					"children":
					(
						{
							"name" : "title_pickup",
							"type" : "text",
							"x" : TITLE_IMAGE_TEXT_X,
							"y" : TITLE_IMAGE_TEXT_Y,
							"text_horizontal_align":"left",
							"text" : uiScriptLocale.AUTO_PICKUP_PREMIUM_TITLE,
						},
					),
				},
				{
					"name" : "pick_up_button_activate",
					"type" : "toggle_button",
					"x" : OPTION_START_X+TOGGLE_BUTTON_RANGE_X*0,
					"y" : 33,
					"text" : uiScriptLocale.AUTO_PICKUP_PREMIUM_ENABLED,
					"text_x" : TOGGLE_BUTTON_TEXT_X,
					"default_image" : IMG_DIR + "toggle_unselected.png",
					"over_image" : IMG_DIR + "toggle_unselected.png",
					"down_image" : IMG_DIR + "toggle_selected.png",
				},
				{
					"name" : "pick_up_button_deactivate",
					"type" : "toggle_button",
					"x" : OPTION_START_X+TOGGLE_BUTTON_RANGE_X*1,
					"y" : 33,
					"text" : uiScriptLocale.AUTO_PICKUP_PREMIUM_DISABLED,
					"text_x" : TOGGLE_BUTTON_TEXT_X,
					"default_image" : IMG_DIR + "toggle_unselected.png",
					"over_image" : IMG_DIR + "toggle_unselected.png",
					"down_image" : IMG_DIR + "toggle_selected.png",
				},
			),
		},
		{
			"name" : "pickup_filter_window",
			"type" : "window",
			"x" : 0,
			"y" : 95+SMALL_OPTION_HEIGHT,
			"width":304,
			"height":SMALL_OPTION_HEIGHT*3,
			"children":
			(
				{
					"name" : "pickup_filtre_title_img",
					"type" : "expanded_image",
					"x" : 5,
					"y" : 0,
					"image" : IMG_DIR+"option_title.png",
					"children":
					(
						{
							"name" : "title_pickup_filter",
							"type" : "text",
							"x" : TITLE_IMAGE_TEXT_X,
							"y" : TITLE_IMAGE_TEXT_Y,
							"text_horizontal_align":"left",
							"text" : uiScriptLocale.AUTO_PICKUP_PREMIUM_FILTER,
						},
					),
				},
				{
					"name" : "pick_up_weapons",
					"type" : "toggle_button",
					"x" : OPTION_START_X,
					"y" : 33,
					"text" : uiScriptLocale.AUTO_PICKUP_PREMIUM_FILTER_WEAPONS,
					"text_x" : TOGGLE_BUTTON_TEXT_X,
					"default_image" : IMG_DIR + "toggle_unselected.png",
					"over_image" : IMG_DIR + "toggle_unselected.png",
					"down_image" : IMG_DIR + "toggle_selected.png",
				},
				{
					"name" : "pick_up_armors",
					"type" : "toggle_button",
					"x" : OPTION_START_X+TOGGLE_BUTTON_RANGE_X+10,
					"y" : 33,
					"text" : uiScriptLocale.AUTO_PICKUP_PREMIUM_FILTER_ARMOR,
					"text_x" : TOGGLE_BUTTON_TEXT_X,
					"default_image" : IMG_DIR + "toggle_unselected.png",
					"over_image" : IMG_DIR + "toggle_unselected.png",
					"down_image" : IMG_DIR + "toggle_selected.png",
				},
				{
					"name" : "pick_up_shield",
					"type" : "toggle_button",
					"x" : OPTION_START_X+(TOGGLE_BUTTON_RANGE_X+10)*2,
					"y" : 33,
					"text" : uiScriptLocale.AUTO_PICKUP_PREMIUM_FILTER_SHIELD,
					"text_x" : TOGGLE_BUTTON_TEXT_X,
					"default_image" : IMG_DIR + "toggle_unselected.png",
					"over_image" : IMG_DIR + "toggle_unselected.png",
					"down_image" : IMG_DIR + "toggle_selected.png",
				},
				{
					"name" : "pick_up_helmets",
					"type" : "toggle_button",
					"x" : OPTION_START_X,
					"y" : 33+BUTTON_NEXT_Y,
					"text" : uiScriptLocale.AUTO_PICKUP_PREMIUM_FILTER_HELMET,
					"text_x" : TOGGLE_BUTTON_TEXT_X,
					"default_image" : IMG_DIR + "toggle_unselected.png",
					"over_image" : IMG_DIR + "toggle_unselected.png",
					"down_image" : IMG_DIR + "toggle_selected.png",
				},
				{
					"name" : "pick_up_bracelets",
					"type" : "toggle_button",
					"x" : OPTION_START_X+TOGGLE_BUTTON_RANGE_X+10,
					"y" : 33+BUTTON_NEXT_Y,
					"text" : uiScriptLocale.AUTO_PICKUP_PREMIUM_FILTER_BRACELET,
					"text_x" : TOGGLE_BUTTON_TEXT_X,
					"default_image" : IMG_DIR + "toggle_unselected.png",
					"over_image" : IMG_DIR + "toggle_unselected.png",
					"down_image" : IMG_DIR + "toggle_selected.png",
				},
				{
					"name" : "pick_up_necklace",
					"type" : "toggle_button",
					"x" : OPTION_START_X+(TOGGLE_BUTTON_RANGE_X+10)*2,
					"y" : 33+BUTTON_NEXT_Y,
					"text" : uiScriptLocale.AUTO_PICKUP_PREMIUM_FILTER_NECKLACE,
					"text_x" : TOGGLE_BUTTON_TEXT_X,
					"default_image" : IMG_DIR + "toggle_unselected.png",
					"over_image" : IMG_DIR + "toggle_unselected.png",
					"down_image" : IMG_DIR + "toggle_selected.png",
				},
				{
					"name" : "pick_up_earrings",
					"type" : "toggle_button",
					"x" : OPTION_START_X,
					"y" : 33+BUTTON_NEXT_Y*2,
					"text" : uiScriptLocale.AUTO_PICKUP_PREMIUM_FILTER_EARRINGS,
					"text_x" : TOGGLE_BUTTON_TEXT_X,
					"default_image" : IMG_DIR + "toggle_unselected.png",
					"over_image" : IMG_DIR + "toggle_unselected.png",
					"down_image" : IMG_DIR + "toggle_selected.png",
				},
				{
					"name" : "pick_up_shoes",
					"type" : "toggle_button",
					"x" : OPTION_START_X+TOGGLE_BUTTON_RANGE_X+10,
					"y" : 33+BUTTON_NEXT_Y*2,
					"text" : uiScriptLocale.AUTO_PICKUP_PREMIUM_FILTER_SHOES,
					"text_x" : TOGGLE_BUTTON_TEXT_X,
					"default_image" : IMG_DIR + "toggle_unselected.png",
					"over_image" : IMG_DIR + "toggle_unselected.png",
					"down_image" : IMG_DIR + "toggle_selected.png",
				},
				{
					"name" : "pick_up_yang",
					"type" : "toggle_button",
					"x" : OPTION_START_X+(TOGGLE_BUTTON_RANGE_X+10)*2,
					"y" : 33+BUTTON_NEXT_Y*2,
					"text" : uiScriptLocale.AUTO_PICKUP_PREMIUM_FILTER_YANG,
					"text_x" : TOGGLE_BUTTON_TEXT_X,
					"default_image" : IMG_DIR + "toggle_unselected.png",
					"over_image" : IMG_DIR + "toggle_unselected.png",
					"down_image" : IMG_DIR + "toggle_selected.png",
				},
				{
					"name" : "pick_up_chests",
					"type" : "toggle_button",
					"x" : OPTION_START_X,
					"y" : 33+BUTTON_NEXT_Y*3,
					"text" : uiScriptLocale.AUTO_PICKUP_PREMIUM_FILTER_CHESTS,
					"text_x" : TOGGLE_BUTTON_TEXT_X,
					"default_image" : IMG_DIR + "toggle_unselected.png",
					"over_image" : IMG_DIR + "toggle_unselected.png",
					"down_image" : IMG_DIR + "toggle_selected.png",
				},
				{
					"name" : "pick_up_others",
					"type" : "toggle_button",
					"x" : OPTION_START_X+TOGGLE_BUTTON_RANGE_X+10,
					"y" : 33+BUTTON_NEXT_Y*3,
					"text" : uiScriptLocale.AUTO_PICKUP_PREMIUM_FILTER_OTHERS,
					"text_x" : TOGGLE_BUTTON_TEXT_X,
					"default_image" : IMG_DIR + "toggle_unselected.png",
					"over_image" : IMG_DIR + "toggle_unselected.png",
					"down_image" : IMG_DIR + "toggle_selected.png",
				},
			),
		},
	),
}

