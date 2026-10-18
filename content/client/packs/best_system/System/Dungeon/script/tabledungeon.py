if __USE_DYNAMIC_MODULE__:
	import pyapi

app = __import__(pyapi.GetModuleName("app"))

import uiScriptLocale
import item
import grp
import localeInfo
SIZE_WIDTH = 532+128
SIZE_HEIGHT = 380+80
X_POSITION_INFO = 15
Y_POSITION_INFO = 105


RUTA_IMGS = "System/Dungeon/new_dungeon/"

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
						{ "name":"TitleName", "type":"text", "x":125, "y":3, "text" : localeInfo.TITLE_DUNGEON_INFO, "text_horizontal_align":"center" },
					),
				},

				{
					"name": "ImgBase",
					"type": "image",
					"x": 15,
					"y": 36,
					"image": RUTA_IMGS+"base_mazmorras.tga",
				},

				{
					"name" : "scrollbar_elements",
					"type" : "scrollbar",

					"x" : 256,
					"y" : 38,

					"size" : SIZE_HEIGHT-55,
				},

				{
					"name": "ImgInfo1",
					"type": "image",
					"x": 270,
					"y": 36,
					"image": RUTA_IMGS+"base_info.tga",

					"children":
					(
						{
							"name": "img_banner",
							"type": "image",
							"x": 3,
							"y": -56,
							"image": RUTA_IMGS+"duratus.tga",
						},

						{
							"name" : "windows_info",
							"type" : "window",
							"x"	   : 0,
							"y"	   : 0,
							"width" : 374,
							"height": 326,
							"children":
							(


								{
									"name": "img_slot",
									"type": "image",
									"x": 270,
									"y": 15,
									"image": RUTA_IMGS+"item_slot.tga",

									"children":
									(
										{
											"name": "item_slot",
											"type": "slot",
											"x" : 7,
											"y" : 7,
											"slot" : ({"index":0, "x":0, "y":0, "width":32, "height":32},),
											"width": 32,
											"height": 32,
										},

										{
											"name" : "text_slot",
											"type" : "text",
											"x" : -16,
											"y" : 45,
											"text": localeInfo.TITLE_DUNGEON_INFO_ITEM,
										},
									),
								},

								{
									"name" : "bar_info_1",
									"type" : "image",
									"x": X_POSITION_INFO-12,
									"y": Y_POSITION_INFO-20,
									"image": RUTA_IMGS+"barra_titulos.tga",
									"children":
									(
										{
											"name": "title_icon_1",
											"type": "image",
											"x": 10,
											"y": 2,
											"image": RUTA_IMGS+"title_icon.tga",
											"children":
											(
												{	
													"name" : "title_name_1",
													"type" : "text",
													"x" : 33,
													"y" : 1,
													"color": 0xffe4cd9f,
													"text": "Þeytan Kulesi",
												},
											),
										},
									),
								},

								{
									"name" : "border_info_0",
									"type" : "image",
									"x": X_POSITION_INFO-12,
									"y": Y_POSITION_INFO+20,
									"image": RUTA_IMGS+"borde_info.tga",
								},

								{
									"name" : "border_info_1",
									"type" : "image",
									"x": X_POSITION_INFO-12,
									"y": Y_POSITION_INFO+(20*3),
									"image": RUTA_IMGS+"borde_info.tga",
								},

								{
									"name" : "title_lvl",
									"type" : "text",
									"x" : X_POSITION_INFO,
									"y" : Y_POSITION_INFO+3 ,
									"text": "Seviye Sýnýrý: %d - %d"%(0,0),
								},

								{
									"name" : "title_entrance",
									"type" : "text",
									"x" : X_POSITION_INFO,
									"y" : Y_POSITION_INFO+20+3,
									"text": "Konum: %s"%("None"),
								},

								{
									"name" : "title_party_member",
									"type" : "text",
									"x" : X_POSITION_INFO,
									"y" : Y_POSITION_INFO+(20*2)+3,
									"text": "Grup Sýnýrý: %d - %d"%(0,0),
								},
								{
									"name" : "title_respawn",
									"type" : "text",
									"x" : X_POSITION_INFO,
									"y" : Y_POSITION_INFO+(20*3)+3,
									"text": "Bekleme Süresi: %d Dakika"%(0),
								},

								{
									"name" : "title_difficulty",
									"type" : "start_dungeon",
									"x" : X_POSITION_INFO+170,
									"y" : Y_POSITION_INFO+3,
								},

								{
									"name" : "title_force",
									"type" : "text",
									"x" : X_POSITION_INFO+170,
									"y" : Y_POSITION_INFO+20+3,
									"text": "Güç: Canavar / Ölümsüz",
								},

								{
									"name" : "title_resistance",
									"type" : "text",
									"x" : X_POSITION_INFO+170,
									"y" : Y_POSITION_INFO+(20*2)+3,
									"text": "Savunma: Savunma / Hp",
								},
								{
									"name" : "title_time_room",
									"type" : "text",
									"x" : X_POSITION_INFO+170,
									"y" : Y_POSITION_INFO+(20*3)+3,
									"text": "Süre Sýnýrý: 40 Dakika",
								},


								{
									"name" : "bar_info_2",
									"type" : "image",
									"x": X_POSITION_INFO-12,
									"y": Y_POSITION_INFO+(20*5),
									"image": RUTA_IMGS+"barra_titulos.tga",
									"children":
									(
										{
											"name": "title_icon_2",
											"type": "image",
											"x": 10,
											"y": 2,
											"image": RUTA_IMGS+"title_icon.tga",
											"children":
											(
												{	
													"name" : "title_name_2",
													"type" : "text",
													"x" : 33,
													"y" : 1,
													"color": 0xffe4cd9f,
													"text": "Kiþisel Bilgiler",
												},
											),
										},
									),
								},

								{
									"name" : "border_info_2",
									"type" : "image",
									"x": X_POSITION_INFO-12,
									"y": Y_POSITION_INFO+(20*7),
									"image": RUTA_IMGS+"borde_info.tga",
								},


								{
									"name" : "title_total_finish",
									"type" : "text",
									"x" : X_POSITION_INFO,
									"y" : Y_POSITION_INFO+(20*6)+3,
									"text": "Gerçekleþtirilen Sayý: 1.000",
								},

								{
									"name" : "title_damage_done",
									"type" : "text",
									"x" : X_POSITION_INFO,
									"y" : Y_POSITION_INFO+(20*7)+3,
									"text": "Gerçekleþen Hasar: 701.000",
								},


								{
									"name" : "title_time_finish",
									"type" : "text",
									"x" : X_POSITION_INFO+170,
									"y" : Y_POSITION_INFO+(20*6)+3,
									"text": "Kayýt: 00:20:30 ",
								},


								{
									"name" : "title_damage_received",
									"type" : "text",
									"x" : X_POSITION_INFO+170,
									"y" : Y_POSITION_INFO+(20*7)+3,
									"text": "Alýnan Hasar: 701.000",
								},
							),
						},

						{
							"name" : "windows_misiones",
							"type" : "window",
							"x"	   : 0,
							"y"	   : 306,
							"width" : 374,
							"height": 105,
							"children":
							(
								{
									"name" : "bar_info_3",
									"type" : "image",
									"x": X_POSITION_INFO-12,
									"y": 20,
									"image": RUTA_IMGS+"barra_titulos.tga",
									"children":
									(
										{
											"name": "title_icon_3",
											"type": "image",
											"x": 10,
											"y": 2,
											"image": RUTA_IMGS+"icon.tga",
											"children":
											(
												{	
													"name" : "title_name_3",
													"type" : "text",
													"x" : 33,
													"y" : 1,
													"color": 0xffe4cd9f,
													"text": "Anahtar Alma Görevi",
												},
											),
										},
									),
								},
								{
									"name" : "name_item_mision",
									"type" : "text",
									"x" : X_POSITION_INFO,
									"y" : (Y_POSITION_INFO-64)+3 ,
									"text": "Anahtar: None",
								},

								{
									"name" : "border_info_3",
									"type" : "image",
									"x": X_POSITION_INFO-12,
									"y": (Y_POSITION_INFO-64)+20,
									"image": RUTA_IMGS+"slot_info.tga",
								},

								{
									"name" : "level_mision",
									"type" : "text",
									"x" : X_POSITION_INFO,
									"y" : (Y_POSITION_INFO-64)+20+3 ,
									"text": "Minimum Seviye: 1",
								},

								{
									"name" : "time_mision",
									"type" : "text",
									"x" : X_POSITION_INFO,
									"y" : (Y_POSITION_INFO-64)+(20*2)+3 ,
									"text": "Süre Sýnýrý: Sýnýrsýz",
								},


								{
									"name" : "img_slot_mision",
									"type" : "image",
									"x": X_POSITION_INFO+202,
									"y": (Y_POSITION_INFO-64)+4,
									"image": RUTA_IMGS+"slot_mision.tga",
									"children":
									(

										{
											"name" : "icon_check",
											"type" : "image",
											"x": -3,
											"y": -3,
											"image": RUTA_IMGS+"check.tga",
										},

										{	
											"name" : "name_mob_mision",
											"type" : "text",
											"x" : 75,
											"y" : 6,
											"text": "Yeni Okçu",
											"text_horizontal_align": "center",
										},
										

										{	
											"name" : "count_mision",
											"type" : "text",
											"x" : 75,
											"y" : 6+23,
											"text": "0/300",
											"text_horizontal_align": "center",
										},

										{
											"name" : "empezar_mision",
											"type" : "button",

											"x" : 9,
											"y" : 6+20,


											"default_image" : RUTA_IMGS+"boton_aceptar_mision1.tga",
											"over_image" : RUTA_IMGS+"boton_aceptar_mision2.tga",
											"down_image" :RUTA_IMGS+ "boton_aceptar_mision3.tga",

											"children":
											(
												{	
													"name" : "title_name_e",
													"type" : "text",
													"x" : 33,
													"y" : 3,
													"text": "Görevi Baþlat",
												},
											),
										},

										{
											"name" : "recibir_mision",
											"type" : "button",

											"x" : 9,
											"y" : 6+20,

											"default_image" : RUTA_IMGS+"recoger_llave1.tga",
											"over_image" : RUTA_IMGS+"recoger_llave2.tga",
											"down_image" :RUTA_IMGS+ "recoger_llave3.tga",

											"children":
											(
												{	
													"name" : "title_name_r",
													"type" : "text",
													"x" : 33,
													"y" : 3,
													"text": "Anahtarý Al",
												},
											),

										},

									),
								},
							),

						},

						{
							"name" : "windows_ranking",
							"type" : "window",
							"x"	   : 0,
							"y"	   : 0,
							"width" : 374,
							"height": 326,
							"children":
							(

								{
									"name": "title_top_1_rankings",
									"type": "image",
									"x": 240,
									"y": 15,
									"image": RUTA_IMGS+"top1_icon.tga",
									"children":
									(
										{	
											"name" : "title_top_1_ranking",
											"type" : "text",
											"x" : 30,
											"y" : 2,
											"color": 0xffe4cd9f,
											"text": "Top 1:",
										},
									),
								},

								{	
									"name" : "name_top_ranking",
									"type" : "text",
									"x" : 272,
									"y" : 33,
									"color": 0xffe4cd9f,
									"text": "Dünya Adresi",
									"text_horizontal_align": "center",
								},

								{	
									"name" : "extra_top_ranking",
									"type" : "text",
									"x" : 272,
									"y" : 33+12,
									"color": 0xffe4cd9f,
									"text": "Dünya Adresi",
									"text_horizontal_align": "center",
								},


								{
									"name" : "bar_info_top_ranking",
									"type" : "image",
									"x": X_POSITION_INFO-12,
									"y": Y_POSITION_INFO-20,
									"image": RUTA_IMGS+"barra_titulos.tga",
									"children":
									(
										{
											"name": "number_icon_ranking",
											"type": "image",
											"x": 25,
											"y": 1,
											"image": RUTA_IMGS+"no_icon.tga",
										},

										{
											"name": "name_icon_ranking",
											"type": "image",
											"x": 100,
											"y": 3,
											"image": RUTA_IMGS+"name_icon.tga",
											"children":
											(
												{	
													"name" : "name_text_ranking",
													"type" : "text",
													"x" : 33,
													"y" : 0,
													"color": 0xffe4cd9f,
													"text": "Oyuncu Adý",
												},
											),
										},


										{
											"name": "extra_icon_ranking",
											"type": "image",
											"x": 110+140,
											"y": 3,
											"image": RUTA_IMGS+"info_icon.tga",
											"children":
											(
												{	
													"name" : "extra_text_ranking",
													"type" : "text",
													"x" : 29,
													"y" : 0,
													"color": 0xffe4cd9f,
													"text": "Gerçekleþtirilen Süre",
												},
											),
										},
									),
								},
							),
						},

						{
							"name" : "button_ranking_time",
							"type" : "radio_button",

							"x" : 20+45,
							"y" : 287,

							"tooltip_text": "Sýralama Süresi",

							"default_image" : RUTA_IMGS+"time_1.tga",
							"over_image" : RUTA_IMGS+"time_2.tga",
							"down_image" :RUTA_IMGS+ "time_3.tga",
						},

						{
							"name" : "button_ranking_kills",
							"type" : "radio_button",

							"x" : 20+45+62,
							"y" : 287,

							"tooltip_text": "Sýralama Öldürmeleri",

							"default_image" : RUTA_IMGS+"kills_1.tga",
							"over_image" : RUTA_IMGS+"kills_2.tga",
							"down_image" :RUTA_IMGS+ "kills_3.tga",
						},

						{
							"name" : "button_ranking_danger",
							"type" : "radio_button",

							"x" : 20+45+(62*2),
							"y" : 287,


							"tooltip_text": "Sýralama Hasarý",

							"default_image" : RUTA_IMGS+"top_1.tga",
							"over_image" : RUTA_IMGS+"top_2.tga",
							"down_image" :RUTA_IMGS+ "top_3.tga",
						},


						{
							"name" : "button_info",
							"type" : "radio_button",

							"x" : 10,
							"y" : 287,

							"tooltip_text": "Bilgi",


							"default_image" : RUTA_IMGS+"info_1.tga",
							"over_image" : 	RUTA_IMGS+"info_2.tga",
							"down_image" : 	RUTA_IMGS+"info_3.tga",
						},

						{
							"name" : "teleport",
							"type" : "button",

							"x" : 270,
							"y" : 287,

							"tooltip_text": "Iþýnlanma",

							"default_image" : RUTA_IMGS+"teleport_1.tga",
							"over_image" : RUTA_IMGS+"teleport_2.tga",
							"down_image" :RUTA_IMGS+ "teleport_3.tga",
						},

					),
				},
			),
		},
	),
}

