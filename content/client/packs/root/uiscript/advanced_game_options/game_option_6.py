import uiScriptLocale

IMG_DIR = "d:/ymir work/ui/game/advanced_game_options/"
TITLE_IMAGE_TEXT_X = 5
TITLE_IMAGE_TEXT_Y = 4
SMALL_OPTION_HEIGHT = 65

window = {
	"name": "GameOptionDialog",
	"style": (),
	"x": 222,
	"y": 1,
	"width": 371,
	"height": 404,
	"children": (
		{
			"name": "efekler_section",
			"type": "window",
			"x": 0,
			"y": 5,
			"width": 304,
			"height": SMALL_OPTION_HEIGHT,
			"children": (
				{
					"name": "title_efekler",
					"type": "expanded_image",
					"x": 5,
					"y": 0,
					"image": IMG_DIR + "option_title.png",
					"children": (
						{
							"name": "title_efekler_text",
							"type": "text",
							"x": TITLE_IMAGE_TEXT_X,
							"y": TITLE_IMAGE_TEXT_Y,
							"text_horizontal_align": "left",
							"text": "Efekler",
						},
					),
				},
			),
		},
	),
}
