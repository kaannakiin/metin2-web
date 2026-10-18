if __USE_DYNAMIC_MODULE__:
	import pyapi

app = __import__(pyapi.GetModuleName("app"))

ROOT = "d:/ymir work/ui/minimap/"
PATCH_IMG = "d_ranking_gremios/"
ROOT2 = "d:/ymir work/ui/game/minimapa/"

import localeInfo


window = {
	"name" : "MiniMap",

	"x" : SCREEN_WIDTH - 136,
	"y" : 0,

	"width" : 136,
	"height" : 137,

	"children" :
	[
		## OpenWindow
		{
			"name" : "OpenWindow",
			"type" : "window",

			"x" : 0,
			"y" : 0,

			"width" : 136,
			"height" : 137,

			"children" :
			[
				{
					"name" : "OpenWindowBGI",
					"type" : "image",
					"x" : 0,
					"y" : 0,
					"image" : ROOT + "minimap.sub",
				},
				## MiniMapWindow
				{
					"name" : "MiniMapWindow",
					"type" : "window",

					"x" : 4,
					"y" : 5,

					"width" : 128,
					"height" : 128,
				},
				## ScaleUpButton
				{
					"name" : "ScaleUpButton",
					"type" : "button",

					"x" : 101,
					"y" : 116,

					"default_image" : ROOT + "minimap_scaleup_default.sub",
					"over_image" : ROOT + "minimap_scaleup_over.sub",
					"down_image" : ROOT + "minimap_scaleup_down.sub",
				},
				## ScaleDownButton
				{
					"name" : "ScaleDownButton",
					"type" : "button",

					"x" : 115,
					"y" : 103,

					"default_image" : ROOT + "minimap_scaledown_default.sub",
					"over_image" : ROOT + "minimap_scaledown_over.sub",
					"down_image" : ROOT + "minimap_scaledown_down.sub",
				},
				## MiniMapHideButton
				{
					"name" : "MiniMapHideButton",
					"type" : "button",

					"x" : 111,
					"y" : 6,

					"default_image" : ROOT + "minimap_close_default.sub",
					"over_image" : ROOT + "minimap_close_over.sub",
					"down_image" : ROOT + "minimap_close_down.sub",
				},
				## AtlasShowButton
				{
					"name" : "AtlasShowButton",
					"type" : "button",

					"x" : 12,
					"y" : 12,

					"default_image" : ROOT + "atlas_open_default.sub",
					"over_image" : ROOT + "atlas_open_over.sub",
					"down_image" : ROOT + "atlas_open_down.sub",
				},

				## ServerInfo
				{
					"name" : "ServerInfo",
					"type" : "text",
					
					"text_horizontal_align" : "center",

					"outline" : 1,

					"x" : 70,
					"y" : 160,

					"text" : "",
				},
				## PositionInfo
				{
					"name" : "PositionInfo",
					"type" : "text",
					
					"text_horizontal_align" : "center",

					"outline" : 1,

					"x" : 70,
					"y" : 170,

					"text" : "",
				},

				## ObserverCount
				{
					"name" : "ObserverCount",
					"type" : "text",

					"text_horizontal_align" : "center",

					"outline" : 1,

					"x" : 70,
					"y" : 190,

					"text" : "",
				},

				## FPSInfo
				{
					"name" : "FPSInfo",
					"type" : "text",
					
					"text_horizontal_align" : "center",

					"outline" : 1,

					"x" : -25,
					"y" : 15,

					"text" : "",
				},

			],
		},
		{
			"name" : "CloseWindow",
			"type" : "window",

			"x" : 0,
			"y" : 0,

			"width" : 132,
			"height" : 48,

			"children" :
			[
				## ShowButton
				{
					"name" : "MiniMapShowButton",
					"type" : "button",

					"x" : 100,
					"y" : 4,

					"default_image" : ROOT + "minimap_open_default.sub",
					"over_image" : ROOT + "minimap_open_default.sub",
					"down_image" : ROOT + "minimap_open_default.sub",
				},
			],
		},
		## ENABLE_ZODIAC_MISSION
		 {
		 	"name" : "bead",
			 "type" :"button",

			 "x" : 15,
			 "y" : 0,

			 "default_image" : "d:/ymir work/ui/game/12zi/bead/bead_default.sub",
			 "over_image" : "d:/ymir work/ui/game/12zi/bead/bead_down.sub",
			 "down_image" : "d:/ymir work/ui/game/12zi/bead/bead_over.sub",
		 },

		 {
		 	"name" : "beadInfo",
			 "type" : "text",

			 "x" : 27,
			 "y" : 7,

			 "text":"0",
		 },
		## ENABLE_ZODIAC_MISSION
	],
}

window["x"] = window["x"] - 15
window["width"] = window["width"] + 15
window["children"][0]["width"] = window["children"][0]["width"] + 15
window["children"][1]["width"] = window["children"][1]["width"] + 15

for idx in range(len(window["children"][0]["children"])):
	window["children"][0]["children"][idx]["x"] = window["children"][0]["children"][idx]["x"] + 15

window["children"][1]["children"][0]["x"] = window["children"][1]["children"][0]["x"] + 15
window["children"][1]["children"][0]["y"] = 2

window["children"][0]["children"][5]["x"] = 0
window["children"][0]["children"][5]["y"] = 57
window["children"][0]["children"] = window["children"][0]["children"] + [
			{
				"name" : "battlepass",
				"type" : "button",

				"x" : 3,
				"y" : 80,

				"default_image" : ROOT + "battlepass_open_default.tga",
				"over_image" : ROOT + "battlepass_open_over.tga",
				"down_image" : ROOT + "battlepass_open_down.tga",
			},]

if app.ENABLE_BIOLOGIST_SYSTEM:
	window["children"][0]["children"] = window["children"][0]["children"] + [
					{
						"name" : "BiologistButton",
						"type" : "button",

						"x" : 17,
						"y" : 102,

						"default_image" : ROOT + "biolog_button_down.png",
						"over_image" : ROOT + "biolog_button_normal.png",
						"down_image" : ROOT + "biolog_button_over.png",
					},]

if app.__DUNGEON_INFO__:
	window["children"][0]["children"] = window["children"][0]["children"] + [
					## DungeonSystemButton
					{
						"name" : "DungeonSystemButton",
						"type" : "button",

						"x" : 35,
						"y" : 117,

						"default_image" : ROOT + "dungeon_button_down.png",
						"over_image" : ROOT + "dungeon_button_normal.png",
						"down_image" : ROOT + "dungeon_button_over.png",
					},]

window["children"][0]["children"] = window["children"][0]["children"] + [
				## OpenRewardWindow
				{
					"name" : "OpenRewardWindow",
					"type" : "button",

					"x" : 48,
					"y" : 127,

					"default_image" : ROOT + "ranking_button_down.png",
					"over_image" : ROOT + "ranking_button_normal.png",
					"down_image" : ROOT + "ranking_button_over.png",
				},]

# OpenRewardWindow button'unun x pozisyonuna +15 ekle (loop'tan sonra eklendiði için)
for idx in range(len(window["children"][0]["children"])):
	if window["children"][0]["children"][idx].get("name") == "OpenRewardWindow":
		window["children"][0]["children"][idx]["x"] = window["children"][0]["children"][idx]["x"] + 15
		break

#if app.ENABLE_RANKING:
#	window["children"][0]["children"] = window["children"][0]["children"] + [
#					{
#						"name" : "OpenRewardWindow",
#						"type" : "button",
#
#						"x" : 60,
#						"y" : 125,

#						"default_image" : ROOT + "btn_ranking_normal.tga",
#						"over_image" : ROOT + "btn_ranking_hover.tga",
#						"down_image" : ROOT + "btn_ranking_down.tga",
#					},]

if app.ENABLE_OFFLINESHOP_SEARCH_SYSTEM:
	window["children"][0]["children"] = window["children"][0]["children"] + [
					{
						"name" : "PortableSearchButton",
						"type" : "button",

						"x" : 90,
						"y" : 125,

						"default_image" : ROOT + "shop_button_down.png",
						"over_image" : ROOT + "shop_button_norm.png",
						"down_image" : ROOT + "shop_button_over.png",
					},]
