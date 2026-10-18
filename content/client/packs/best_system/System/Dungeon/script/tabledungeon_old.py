if __USE_DYNAMIC_MODULE__:
	import pyapi

app = __import__(pyapi.GetModuleName("app"))

import uiScriptLocale
import item
import grp

SIZE_WIDTH = 532
SIZE_HEIGHT = 480+7
RUTA_IMGS = "System/Dungeon/design/"

window = {
	"name" : "table_dungeon_windows",

	"x" : (SCREEN_WIDTH -SIZE_WIDTH) / 2,
	"y" : (SCREEN_HEIGHT - SIZE_HEIGHT) / 2,

	"style" : ("movable", "float",),

	"width" : SIZE_WIDTH,
	"height" : SIZE_HEIGHT,

	"children" :
	(
		{
			"name" : "board",
			"type" : "board",

			"x" : 0,
			"y" : 0,

			"width" : SIZE_WIDTH,
			"height" :SIZE_HEIGHT,
		
			"children" :
			(
				## Title
				{
					"name" : "TitleBar",
					"type" : "titlebar",

					"x" : 6,
					"y" : 6,

					"width" : SIZE_WIDTH-12,
					"color" : "yellow",

					"children" :
					(
						{ "name":"TitleName", "type":"text", "x":SIZE_WIDTH/2, "y":3, "text" : "Panel de Mazmorras", "text_horizontal_align":"center" },
					),
				},

				{

					"name" : "banner_dungeon",
					"type" : "image",

					"x" : 10,
					"y" : 30,

					"image" : RUTA_IMGS+"razador_1.tga",
				},

				{

					"name" : "thinboard_elements_dungeon",
					"type" : "image",

					"x" : 10,
					"y" : 98,

					"image" : RUTA_IMGS+"marco_dungeons.tga"
					#"width" : 295,
					#"height" :SIZE_HEIGHT-110,
				},

				{
					"name" : "scrollbar_elements",
					"type" : "scrollbar",

					"x" : 305+5,
					"y" : 100,

					"size" : SIZE_HEIGHT-110,
				},
				{

					"name" : "thinboard_info_dungeon",
					"type" : "thinboard_circle",

					"x" : 320+10,
					"y" : 98,

					"width" : 202-10,
					"height" :SIZE_HEIGHT-109,

					"children":
					(
						{
							"name": "decoration_title",
							"type": "image",
							"x": 7-5,
							"y": 2,
							"image" : RUTA_IMGS+"barra_titulos.tga",

							"children":
							(
								{
									"name": "name_boss",
									"type": "text",
									"x": 90,
									"y": 6,
									"color": 0xffE3BB72,
									"text_horizontal_align":"center",
									"text": "Informacion Mazmorra",
								},
							),
						},

						##Type Info
						{
							"name" 	: "bar_type",
							"type"	: "bar",
							"x" : 1,
							"y" : 45,
							"width" : 199-9,
							"height": 20,
							"color": grp.GenerateColor(1.0, 1.0, 1.0, 0.2),
							"children":
							(
								{
									"name" : "title_type",
									"type" : "text",
									"x" : 8,
									"y" : 2,
									"text": "Tipo:",
								},

								{
									"name" : "value_type",
									"type" : "text",
									"x" : 40+8,
									"y" : 2,
									"text_horizontal_align":"left",
									"text": "Privada / Grupo",
								},
							),
						},

						##Level Info
						{
							"name" 	: "bar_lvl",
							"type"	: "bar",
							"x" : 1,
							"y" : 45+21,
							"width" : 199-9,
							"height": 20,
							"color": grp.GenerateColor(0.0, 0.0, 0.0, 1.0),
							"children":
							(
								{
									"name" : "title_lvl",
									"type" : "text",
									"x" : 8,
									"y" : 2,
									"text": "Nivel limite:",
								},
								{
									"name" : "value_lvl",
									"type" : "text",
									"x" : 40+22+15,
									"y" : 2,
									"text_horizontal_align":"left",
									"text": "90 - 120",
								},
							),
						},

						##Party Members Info
						{
							"name" 	: "bar_party_member",
							"type"	: "bar",
							"x" : 1,
							"y" : 45+(21*2),
							"width" : 199-9,
							"height": 20,
							"color": grp.GenerateColor(1.0, 1.0, 1.0, 0.2),
							"children":
							(
								{
									"name" : "title_party_member",
									"type" : "text",
									"x" : 8,
									"y" : 2,
									"text": "Limte grupal:",
								},
								{
									"name" : "value_party_member",
									"type" : "text",
									"x" : 40+43+19,
									"y" : 2,
									"text_horizontal_align":"left",
									"text": "1 - 7",
								},
							),
						},

						##Respawn Info
						{
							"name" 	: "bar_respawn",
							"type"	: "bar",
							"x" : 1,
							"y" : 45+(21*3),
							"width" : 199-9,
							"height": 20,
							"color": grp.GenerateColor(0.0, 0.0, 0.0, 1.0),
							"children":
							(
								{
									"name" : "title_respawn",
									"type" : "text",
									"x" : 8,
									"y" : 2,
									"text": "Respawn:",
								},
								{
									"name" : "value_respawn",
									"type" : "text",
									"x" : 40+16+14,
									"y" : 2,
									"text_horizontal_align":"left",
									"text": "1 Hour",
								},
							),
						},
						
						##Time Room Info
						{
							"name" 	: "bar_time_room",
							"type"	: "bar",
							"x" : 1,
							"y" : 45+(21*4),
							"width" : 199-9,
							"height": 20,
							"color": grp.GenerateColor(1.0, 1.0, 1.0, 0.2),
							"children":
							(
								{
									"name" : "title_time_room",
									"type" : "text",
									"x" : 8,
									"y" : 2,
									"text": "Tiempo max:",
								},
								{
									"name" : "value_time_room",
									"type" : "text",
									"x" : 40+29+17,
									"y" : 2,
									"text_horizontal_align":"left",
									"text": "1 Hour",
								},
							),
						},


						##Entrance Info
						{
							"name" 	: "bar_entrance",
							"type"	: "bar",
							"x" : 1,
							"y" : 45+(21*5),
							"width" : 199-9,
							"height": 20,
							"color": grp.GenerateColor(0.0, 0.0, 0.0, 1.0),
							"children":
							(
								{
									"name" : "title_entrance",
									"type" : "text",
									"x" : 8,
									"y" : 2,
									"text": "Lugar:",
								},
								{
									"name" : "value_entrance",
									"type" : "text",
									"x" : 40+18+8,
									"y" : 2,
									"text_horizontal_align":"left",
									"text": "Fire Land",
								},
							),
						},

						##Resistance Info
						{
							"name" 	: "bar_resistance",
							"type"	: "bar",
							"x" : 1,
							"y" : 45+(21*6),
							"width" : 199-9,
							"height": 20,
							"color": grp.GenerateColor(1.0, 1.0, 1.0, 0.2),
							"children":
							(
								{
									"name" : "title_resistance",
									"type" : "text",
									"x" : 8,
									"y" : 2,
									"text": "Defensa:",
								},
								{
									"name" : "value_resistance",
									"type" : "text",
									"x" : 40+24+13,
									"y" : 2,
									"text_horizontal_align":"left",
									"text": "Fire Monster",
								},
							),
						},


						##Force Info
						{
							"name" 	: "bar_force",
							"type"	: "bar",
							"x" : 1,
							"y" : 45+(21*7),
							"width" : 199-9,
							"height": 20,
							"color": grp.GenerateColor(0.0, 0.0, 0.0, 1.0),
							"children":
							(
								{
									"name" : "title_force",
									"type" : "text",
									"x" : 8,
									"y" : 2,
									"text": "Fuerza:",
								},
								{
									"name" : "value_force",
									"type" : "text",
									"x" : 40+7+6,
									"y" : 2,
									"text_horizontal_align":"left",
									"text": "Fire Monster",
								},
							),
						},


						{
							"name": "info_extra_title",
							"type": "image",
							"x" : 2,
							"y" : 45+(21*9),
							"image" : RUTA_IMGS+"barra_titulos.tga",

							"children":
							(
								{
									"name": "info_extra",
									"type": "text",
									"x": 90,
									"y": 6,
									"color": 0xffE3BB72,
									"text_horizontal_align":"center",
									"text": "Informacion extra",
								},
							),
						},

						##Total Finish Info
						{
							"name" 	: "bar_total_finish",
							"type"	: "bar",
							"x" : 1,
							"y" : 45+(21*11),
							"width" : 199-9,
							"height": 20,
							"color": grp.GenerateColor(1.0, 1.0, 1.0, 0.2),
							"children":
							(
								{
									"name" : "title_total_finish",
									"type" : "text",
									"x" : 8,
									"y" : 2,
									"text": "Total realizado:",
								},
								{
									"name" : "value_total_finish",
									"type" : "text",
									"x" : 40+40+20,
									"y" : 2,
									"text_horizontal_align":"left",
									"text": "20",
								},
							),
						},


						##Time Finish Info
						{
							"name" 	: "bar_time_finish",
							"type"	: "bar",
							"x" : 1,
							"y" : 45+(21*12),
							"width" : 199-9,
							"height": 20,
							"color": grp.GenerateColor(0.0, 0.0, 0.0, 1.0),
							"children":
							(
								{
									"name" : "title_time_finish",
									"type" : "text",
									"x" : 8,
									"y" : 2,
									"text": "Record:",
								},
								{
									"name" : "value_time_finish",
									"type" : "text",
									"x" : 40+32+23,
									"y" : 2,
									"text_horizontal_align":"left",
									"text": "1h 10m 20s",
								},
							),
						},


						{
							"name" : "teleport",
							"type" : "button",

							"x" : 12,
							"y" : 329+15,

							"text" : "TELEPORT",

							"default_image" : "d:/ymir work/ui/public/large_button_01.sub",
							"over_image" : "d:/ymir work/ui/public/large_button_02.sub",
							"down_image" : "d:/ymir work/ui/public/large_button_03.sub",
						},


						{"name": "item_slot_img","type": "image","x" : 145,"y" : 320+15,"image" : "d:/ymir work/ui/public/Slot_Base.sub"},	


						{
							"name": "item_slot",
							"type": "slot",
							"x" : 145,
							"y" : 320+15,
							"slot" : ({"index":0, "x":0, "y":0, "width":32, "height":32},),
							"width": 32,
							"height": 32,
						},

					),
				},
			),
		},
	),
}

