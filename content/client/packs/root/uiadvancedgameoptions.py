if __USE_DYNAMIC_MODULE__:
	import pyapi

player = __import__(pyapi.GetModuleName("player"))
net = __import__(pyapi.GetModuleName("net"))
pack = __import__(pyapi.GetModuleName("pack"))
app = __import__(pyapi.GetModuleName("app"))

#static
import ui, constInfo, uiSelectMusic, musicInfo, localeInfo, uiScriptLocale

# dynamic
import dbg, chat, wndMgr, systemSetting, snd, background
import time
MUSIC_FILENAME_MAX_LEN = 25
blockMode = 0
IMG_DIR = "d:/ymir work/ui/game/advanced_game_options/"
TEXT_MAIN_COLOR = "|cffcab5a4"

# If you add a new category, you need to add a new dictionary entry to the option_data list and 
# create a new game_option_*.py file in the uiscript/advanced_game_options folder
# The dictionary entry should have the following structure:
# {
#	 "category": "Category Name",
#	 "subcategories": []
# }
# The "category" key should contain the name of the category
# The "subcategories" are self added by the GetTitleTextLines function and should be left empty
# Add a 16x16 icon to the category_icons folder with the same name as the category in lowercase

option_data = [
    {
        "category": "Arayüz", # uiscript/advanced_game_options/game_option_0.py
        "subcategories": []
    },
    {
        "category": "Oyun", # uiscript/advanced_game_options/game_option_1.py
        "subcategories": []
    },
    {
        "category": "Çevre", # uiscript/advanced_game_options/game_option_2.py
        "subcategories": []
    },
    {
        "category": "Ses", # uiscript/advanced_game_options/game_option_3.py
        "subcategories": []
    },
    {
        "category": "Grafik", # uiscript/advanced_game_options/game_option_4.py
        "subcategories": []
    },
    {
        "category": "Toplama", # uiscript/advanced_game_options/game_option_5.py
        "subcategories": []
    }
]

class AdvancedGameOptionsWindow(ui.BoardWithTitleBar):
	def __del__(self):
		ui.BoardWithTitleBar.__del__(self)
	def Destroy(self):
		self.pvpModeButtonDict={}
		self.blockButtonList=[]
		self.viewChatButtonList = []
		self.nameColorModeButtonList = []
		self.viewTargetBoardButtonList=[]
		self.alwaysShowNameButtonList=[]
		self.showDamageButtonList=[]
		self.showsalesTextButtonList=[]
		self.showsalesTextButtonList=[]
		self.cameraModeButtonList=[]
		self.fogModeButtonList = []
		self.nightModeButtonList = []
		self.snowModeButtonList = []
		self.snowTextureModeButtonList = []
		self.nameOutlineModeButtonList = []
		self.enbModeButtonList = []
		self.effectLevelButtonList = []
		self.effectLevel = 0
		self.effectLevelApplyButton = None
		self.privateShopLevelButtonList = []
		self.privateShopLevel = 0
		self.privateShopLevelApplyButton = None
		self.dropItemLevelButtonList = []
		self.dropItemLevel = 0
		self.dropItemLevelApplyButton = None
		self.petStatusButtonList = []
		self.npcNameStatusButtonList = []
		self.showMobLevelButtonList = []
		self.showMobAIFlagButtonList = []
		self.fovController = None
		self.fovResetButton = None
		self.stoneScaleController = None
		self.stoneScaleResetButton = None
		self.mainPickModeButtonList = []
		self.mainPickUPButtonList = []
		self.pickupPremiumStatusText = None
		self.scrollbar_is_show = False

		self.ctrlSoundVolume = None
		self.ctrlMusicVolume = None
		self.selectMusicFile = None
		self.selectMusicButton = None
		self.musicListDlg = None

		for j in xrange(10):
			for x in xrange(10):
				if self.children.has_key("optionWindow%d"%(j)):
					window = self.children["optionWindow%d"%(j)]
					if window:
						window.Hide()
						window.scrollBar = None
						window.ClearDictionary()
						window.Destroy()
		self.children = {}
		self.Hide()

	def __init__(self):
		ui.BoardWithTitleBar.__init__(self)
		self.children = {}
		self.Destroy()
		self.scrollbar_is_show = False
		self.__LoadWindow()
		self.SetTitleName(uiScriptLocale.GAMEOPTION_TITLE)
		self.last_update_time = time.time()
		self.animation_interval = 0.01  # Adjust this value to control the speed
		self.text_directions = {}  # Dictionary t0 track the direction of each text line
		self.original_texts = {}  # Dictionary t0 store the original text
		self.expected_ending_texts = {}  # Dictionary t0 store the expected ending text
		self.default_texts = {}  # Dictionary t0 store the default text
		self.text_iteration = {}  # Dictionary t0 store the length of the text
		self.text_length = {}

		self.text_nr_of_letters_hidden = {}
		self.text_nr_of_letters_revealed = {}



	def __LoadWindow(self):
		self.AddFlag("movable")
		self.AddFlag("attach")

		bg = ui.ImageBox()
		bg.SetParent(self)
		bg.AddFlag("attach")
		bg.SetPosition(10, 33)
		bg.LoadImage(IMG_DIR + "background.png")
		bg.Show()
		self.children["bg"] = bg		

		categoryScrollBoard = ui.Window()
		categoryScrollBoard.SetParent(self)
		categoryScrollBoard.SetPosition(10, 33)
		categoryScrollBoard.SetSize(218, 406)
		categoryScrollBoard.Show()
		self.children["categoryScrollBoard"] = categoryScrollBoard

		searchBoard = ui.Window()
		searchBoard.SetParent(self)
		searchBoard.SetPosition(10, 33)
		searchBoard.SetSize(218, 36)
		searchBoard.Show()
		self.children["searchBoard"] = searchBoard			

		self.search_bg = ui.ImageBox()
		self.search_bg.SetParent(self.children["searchBoard"])
		self.search_bg.SetPosition(5, 5)
		self.search_bg.LoadImage(IMG_DIR + "search_bg.png")
		self.search_bg.Show()		

		self.searchButton = ui.Button()
		self.searchButton.SetParent(self.search_bg)
		self.searchButton.SetUpVisual(IMG_DIR + "btn_search_1.png")
		self.searchButton.SetOverVisual(IMG_DIR + "btn_search_2.png")
		self.searchButton.SetDownVisual(IMG_DIR + "btn_search_3.png")
		self.searchButton.SetPosition(self.search_bg.GetWidth()- self.searchButton.GetWidth()+3, -2)
		self.searchButton.SAFE_SetEvent(self.StartSearch)
		self.searchButton.Show()

		self.CancelSearchButton = ui.Button()
		self.CancelSearchButton.SetParent(self.search_bg)
		self.CancelSearchButton.SetUpVisual(IMG_DIR + "search_btn_x_0.png")
		self.CancelSearchButton.SetOverVisual(IMG_DIR + "search_btn_x_1.png")
		self.CancelSearchButton.SetDownVisual(IMG_DIR + "search_btn_x_2.png")
		self.CancelSearchButton.SetPosition(self.search_bg.GetWidth()-56, self.search_bg.GetHeight() / 2 - self.search_bg.GetHeight() / 2 + 2)
		self.CancelSearchButton.SAFE_SetEvent(self.OnPressNameEscapeKey)
		self.CancelSearchButton.Hide()			

		self.searchEdit = ui.EditLine()
		self.searchEdit.SetParent(self.search_bg)
		self.searchEdit.SetMax(50)
		self.searchEdit.SetSize(self.search_bg.GetWidth() - self.searchButton.GetWidth() - self.CancelSearchButton.GetWidth() - 10, 15)
		self.searchEdit.SetPosition(10, self.search_bg.GetHeight() / 2 - 15 / 2)
		#self.searchEdit.SetOverlayText("Search..")
		self.searchEdit.SetLimitWidth(self.searchEdit.GetWidth())
		self.searchEdit.SetEscapeEvent(ui.__mem_func__(self.OnPressNameEscapeKey))
		#self.searchEdit.SetUpdateEvent(ui.__mem_func__(self.ShowHideCancelSearchButton))
		self.searchEdit.SetReturnEvent(ui.__mem_func__(self.StartSearch))
		self.searchEdit.SetOutline()
		self.searchEdit.Show()	

		self.children["filteringEnabled"] = False

		self.scrollBar2 = ScrollBarNew()
		self.scrollBar2.SetParent(self.children["categoryScrollBoard"])
		self.scrollBar2.SetPosition(207, self.search_bg.GetHeight() + 10)
		self.scrollBar2.SetScrollBarSize(bg.GetHeight()-self.search_bg.GetHeight() - 14)
		self.scrollBar2.SetScrollEvent(self.OnScroll)
		self.scrollBar2.Show()
		self.children["categoryScrollBoard"].OnMouseWheel = ui.__mem_func__(self.OnMouseWheelCategories)

		self.categoryButtons = []

		self.GetTitleTextLines()

		# Icon mapping: Türkçe kategori isimleri -> Ýngilizce icon dosya isimleri
		icon_mapping = {
			"Arayüz": "interface",
			"Oyun": "game",
			"Çevre": "environment",
			"Ses": "sound",
			"Grafik": "graphics",
			"Toplama": "pickup"
		}

		for optionIndex, category_data in enumerate(option_data):
			key = category_data["category"]
			icon_name = icon_mapping.get(key, key.lower())

			categoryButton = ui.Button()
			categoryButton.SetParent(self.children["categoryScrollBoard"])
			categoryButton.SetUpVisual(IMG_DIR + "btn_cat_1.png")
			categoryButton.SetOverVisual(IMG_DIR + "btn_cat_2.png")
			categoryButton.SetDownVisual(IMG_DIR + "btn_cat_3.png")
			categoryButton.SetPosition(5, self.search_bg.GetHeight() + 10 + (optionIndex * (categoryButton.GetHeight() + 5)))
			categoryButton.SetTextAlignLeft(TEXT_MAIN_COLOR+key, 50)
			if categoryButton.ButtonText:
				categoryButton.ButtonText.SetPosition(50, categoryButton.GetHeight()/2)
			categoryButton.SAFE_SetEvent(self.ClickCategory, optionIndex)

			category_icon = ui.Button()
			category_icon.SetParent(categoryButton)
			category_icon.SetUpVisual(IMG_DIR + "category_icons/" + icon_name + ".png")
			category_icon.SetOverVisual(IMG_DIR + "category_icons/" + icon_name + ".png")
			category_icon.SetDownVisual(IMG_DIR + "category_icons/" + icon_name + ".png")
			category_icon.SetPosition(0, 0)
			category_icon.SAFE_SetEvent(self.ClickCategory, optionIndex)
			category_icon.Show()

			expand_icon = ui.Button()
			expand_icon.SetParent(categoryButton)
			expand_icon.SetUpVisual(IMG_DIR + "arrow_up.png")
			expand_icon.SetOverVisual(IMG_DIR + "arrow_up.png")
			expand_icon.SetDownVisual(IMG_DIR + "arrow_up.png")			
			expand_icon.SetPosition(categoryButton.GetWidth() - 25, categoryButton.GetHeight()/2-expand_icon.GetHeight()/2)
			expand_icon.SAFE_SetEvent(self.ClickCategory, optionIndex)
			expand_icon.Show()
			

			categoryButton.Show()
			self.children["titleBtn%d" % optionIndex] = categoryButton
			self.children["category_icon%d" % optionIndex] = category_icon
			self.children["expand_icon%d" % optionIndex] = expand_icon
			self.categoryButtons.append(categoryButton)

			self.children["is_expanded%d" % optionIndex] = False

			for categoryIndex, keyEx in enumerate(category_data["subcategories"]):
				subcategoryButton = ui.Button()
				subcategoryButton.SetParent(self.children["categoryScrollBoard"])
				subcategoryButton.SetUpVisual(IMG_DIR + "subcat_1.png")
				subcategoryButton.SetOverVisual(IMG_DIR + "subcat_2.png")
				subcategoryButton.SetDownVisual(IMG_DIR + "subcat_3.png")
				subcategoryButton.SetPosition(5, 10 + categoryButton.GetHeight() + (categoryIndex * (subcategoryButton.GetHeight())))
				subcategoryButton.SAFE_SetEvent(self.ClickSubcategory, optionIndex, categoryIndex)
				subcategoryButton.SetTextAlignLeft(TEXT_MAIN_COLOR+keyEx, 13)
				if subcategoryButton.ButtonText:
					subcategoryButton.ButtonText.SetPosition(35, subcategoryButton.GetHeight()/2)
				subcategoryButton.Hide()
				self.children["subcategoryButton%d%d" % (optionIndex, categoryIndex)] = subcategoryButton

				optionWindow = self.CreateOptionWindow(bg, optionIndex)
				self.children["optionWindow%d" % (optionIndex)] = optionWindow

			# Subcategories bos olsa bile (yeni kategori / game_option_X.py yok) optionWindow olustur - donmayi onler
			if not self.children.has_key("optionWindow%d" % (optionIndex)):
				optionWindow = self.CreateOptionWindow(bg, optionIndex)
				self.children["optionWindow%d" % (optionIndex)] = optionWindow

			if not self.children.has_key("optionWindow%d" % (optionIndex)):
				optionWindow = self.CreateOptionWindow(bg, optionIndex)
				self.children["optionWindow%d" % (optionIndex)] = optionWindow

		self.ClickCategory(0)
		self.scrollBar2.SetPos(0)
		self.SetSize(bg.GetWidth() + 21, bg.GetHeight() + 44)
		self.SetCenterPosition()
		self.UpdateScrollBar()

	def ShowHideCancelSearchButton(self):
		if not self.searchEdit:
			return

		if self.searchEdit.GetText() == "":
			self.CancelSearchButton.Hide()
		else:
			self.CancelSearchButton.Show()

	def OnPressNameEscapeKey(self):
		if not self.searchEdit:
			return
		
		if not self.searchEdit.IsShowCursor() or self.searchEdit.GetText() == "":
			self.OnPressEscapeKey()
		else:
			self.searchEdit.SetText("")
			self.ShowHideCancelSearchButton()

	def StartSearch(self):
		searchText = self.searchEdit.GetText()
		self.children["filteringEnabled"] = True
		elements = {}
		scriptWindow = ui.ScriptWindow()
		scriptWindow.SetParent(self.children["bg"])
		pyScrLoader = ui.PythonScriptLoader()
		
		windowHeight = 0

		for categoryIndex, category_data in enumerate(option_data):
			fileName = "UIScript/advanced_game_options/game_option_filter.py"
			self.children["optionWindow%d" % (categoryIndex)].Hide()
			
			yPos = 5					
			if pack.Exist(fileName):
				pyScrLoader.LoadScriptFile(scriptWindow, fileName)
				scriptChildrens = scriptWindow.Children
				elementDictionary = scriptWindow.ElementDictionary
				self.children["filteredWindow"] = scriptWindow				
				scriptWindow.Show()
				for optionParent in scriptChildrens:
					temp_height = 0
					found = False
					for component in optionParent.Children:
						if not isinstance(component, ui.ExpandedImageBox) and not isinstance(component, ui.ImageBox) and not isinstance(component, ui.SliderBar_AdvancedGameOptions) and not isinstance(component, ui.SliderBar):
							if searchText.lower() in component.GetText().lower():
								found = True
						elif isinstance(component, ui.ExpandedImageBox):
							for child2 in component.Children:
								if searchText.lower() in child2.GetText().lower():
									found = True								
					if not found:
						optionParent.Hide()
					else:
						optionParent.SetPosition(0, yPos)
						yPos += optionParent.GetHeight()
						temp_height += optionParent.GetHeight()
					windowHeight = yPos

		self.LoadCategoryOptions(scriptWindow, 0)
		self.children["filterWindow"] = scriptWindow
		
		if windowHeight > 0:
			self.children["filteredWindowHeight"] = windowHeight
			scrollBar = ScrollBarNew()
			scrollBar.SetParent(scriptWindow)
			scrollBar.SetPosition(scriptWindow.GetWidth()-scrollBar.GetWidth()-3,3)
			scrollBar.SetScrollBarSize(scriptWindow.GetHeight()-6)
			scrollBar.Hide()
			scrollBar.SetScrollEvent(ui.__mem_func__(self.UpdateScrollBar))
			scriptWindow.scrollBar = scrollBar
			scriptWindow.OnMouseWheel = ui.__mem_func__(self.OnMouseWheel)

			scriptChildrens = scriptWindow.Children
			for child in scriptChildrens:
				(_x,_y) = child.GetLocalPosition()
				child.SetPosition(_x,_y, True)

			scriptWindow.Show()
		else:
			scriptWindow.scrollBar = None

		self.UpdateScrollBar()

	def Open(self):
		self.RefreshBlock()
		self.Show()
	def OnPressEscapeKey(self):
		self.Hide()
		return True
	def __ClickRadioButton(self, buttonList, buttonIndex):
		try:
			if not buttonList or not isinstance(buttonList, (list, tuple)):
				return
			if buttonIndex < 0 or buttonIndex >= len(buttonList):
				return
			btn = buttonList[buttonIndex]
			if btn is None:
				return
			for eachButton in buttonList:
				if eachButton:
					eachButton.SetUp()
			btn.Down()
		except Exception, e:
			dbg.TraceError("__ClickRadioButton: %s" % str(e))

	def IsCanContinue(self, dictKey):
		if dictKey == "index":
			return True
		return False

	def GetTitleTextLines(self):
		title_text_lines = []
		scriptWindow = ui.ScriptWindow()
		scriptWindow.SetParent(self)
		title_text_lines_with_y = []
		for category_data in option_data:
			category_data["subcategories"] = [] 
		for categoryIndex, category_data in enumerate(option_data):
			fileName = "UIScript/advanced_game_options/game_option_%d.py" % (categoryIndex)
			
			pyScrLoader = ui.PythonScriptLoader()
			if pack.Exist(fileName):
				# Her kategori için script window'u temizle (duplicate önlemek için)
				scriptWindow.ClearDictionary()
				pyScrLoader.LoadScriptFile(scriptWindow, fileName)
				elementDictionary = scriptWindow.ElementDictionary
				seen_titles_in_category = []  # Bu kategori için görülen title'larý takip et
				for childName, child in elementDictionary.items():
					if childName.startswith("title_"):
						child_y = child.GetGlobalPosition()[1] - scriptWindow.GetGlobalPosition()[1]
						# ExpandedImageBox tipindeki elementler için içlerindeki text elementini bul
						text_value = ""
						if isinstance(child, ui.ExpandedImageBox):
							# ExpandedImageBox içindeki text elementini bul
							for textChild in child.Children:
								if isinstance(textChild, ui.TextLine):
									text_value = textChild.GetText()
									break
						else:
							# Normal text elementleri için
							try:
								text_value = child.GetText()
							except:
								text_value = ""
						
						if text_value:
							# Duplicate kontrolü: Ayný kategori içinde ayný text deðeri daha önce eklenmiþse ekleme
							if text_value not in seen_titles_in_category:
								seen_titles_in_category.append(text_value)
								title_text_lines_with_y.append([categoryIndex, text_value, child_y])

		title_text_lines_with_y.sort(key=lambda x: (x[0],x[2]))
		for child in title_text_lines_with_y:
			option_data[child[0]]["subcategories"].append(child[1])

	def ClickCategory(self, optionType):
		is_expanded = self.children["is_expanded%d" % optionType]
		self.children["is_expanded%d" % optionType] = not is_expanded
		is_expanded = not is_expanded

		for j in xrange(len(option_data)):
			if self.children.has_key("titleBtn%d" % j):
				categoryBtn = self.children["titleBtn%d" % j]
				expand_icon = self.children["expand_icon%d" % j]
				if j == optionType:
					if is_expanded:
						categoryBtn.SetUpVisual(IMG_DIR + "btn_cat_3.png")
						categoryBtn.SetOverVisual(IMG_DIR + "btn_cat_3.png")
						categoryBtn.SetDownVisual(IMG_DIR + "btn_cat_3.png")
						expand_icon.SetUpVisual(IMG_DIR + "arrow_down.png")
						expand_icon.SetOverVisual(IMG_DIR + "arrow_down.png")
						expand_icon.SetDownVisual(IMG_DIR + "arrow_down.png")		

					else:
						categoryBtn.SetUpVisual(IMG_DIR + "btn_cat_1.png")
						categoryBtn.SetOverVisual(IMG_DIR + "btn_cat_2.png")
						categoryBtn.SetDownVisual(IMG_DIR + "btn_cat_3.png")
						expand_icon.SetUpVisual(IMG_DIR + "arrow_up.png")
						expand_icon.SetOverVisual(IMG_DIR + "arrow_up.png")
						expand_icon.SetDownVisual(IMG_DIR + "arrow_up.png")		

		for j in xrange(10):
			if self.children.has_key("subcategoryButton%d%d" % (optionType, j)):
				subcategoryButton = self.children["subcategoryButton%d%d" % (optionType, j)]
				if is_expanded:
					subcategoryButton.Hide()
				else:
					subcategoryButton.Show()

		if is_expanded:
			self.ClickSubcategory(optionType, 0)
		self.RepositionCategoryButtons()
		self.OnScroll()

	def ClickSubcategory(self, optionType, categoryType):
		try:
			if optionType < 0 or optionType >= len(option_data):
				return
		except:
			pass
		try:
			if self.children.has_key("filteringEnabled"):
				self.children["filteringEnabled"] = False
				if self.children.has_key("filterWindow"):
					self.children["filterWindow"].Hide()
			if self.children.has_key("optionType"):
				if self.children["optionType"] != optionType:
					self.scrollbar_is_show = False
			for j in xrange(len(option_data)):
					if self.children.has_key("optionWindow%d" % (j)):
						self.children["optionWindow%d" % (j)].Hide()

			for j in xrange(len(option_data)):
				for x in xrange(10):
					if self.children.has_key("subcategoryButton%d%d" % (j, x)):
						subcategoryBtn = self.children["subcategoryButton%d%d" % (j, x)]
						if j == optionType and x == categoryType:
							subcategoryBtn.SetUpVisual(IMG_DIR + "subcat_3.png")
							subcategoryBtn.SetOverVisual(IMG_DIR + "subcat_3.png")
							subcategoryBtn.SetDownVisual(IMG_DIR + "subcat_3.png")
							subcategoryBtn.Down()
						else:
							subcategoryBtn.SetUpVisual(IMG_DIR + "subcat_1.png")
							subcategoryBtn.SetOverVisual(IMG_DIR + "subcat_2.png")
							subcategoryBtn.SetDownVisual(IMG_DIR + "subcat_3.png")
							subcategoryBtn.SetUp()

			self.children["optionType"] = optionType
			self.children["categoryType"] = categoryType
			key = "optionWindow%d" % (optionType)
			if not self.children.has_key(key):
				self.children[key] = self.CreateOptionWindow(self.children["bg"], optionType)
			if self.children.has_key(key):
				self.LoadCategoryOptions(self.children[key], optionType)
				self.children[key].Show()
				if optionType == 5:
					self.RefreshPickUP()

			self.UpdateScrollBar()
			subcategories = option_data[optionType]["subcategories"]
			if categoryType < len(subcategories):
				self.GoToSubcategory(subcategories[categoryType])
		except Exception, e:
			dbg.TraceError("ClickSubcategory optionType=%s categoryType=%s: %s" % (optionType, categoryType, str(e)))


	def RepositionCategoryButtons(self):
		yPos = self.search_bg.GetHeight() + 10
		for i in xrange(len(option_data)):
			if self.children.has_key("titleBtn%d" % i):
				categoryButton = self.children["titleBtn%d" % i]
				categoryButton.SetPosition(5, yPos)
				yPos += categoryButton.GetHeight()+5

				if self.children.has_key("is_expanded%d" % i):
					is_expanded = self.children["is_expanded%d" % i]
					if is_expanded:
						for j in xrange(10):
							if self.children.has_key("subcategoryButton%d%d" % (i, j)):
								subcategoryButton = self.children["subcategoryButton%d%d" % (i, j)]
								subcategoryButton.SetPosition(5, yPos-5)
								subcategoryButton.Show()
								yPos += subcategoryButton.GetHeight()
							else:
								break
					else:
						for j in xrange(10):
							if self.children.has_key("subcategoryButton%d%d" % (i, j)):
								subcategoryButton = self.children["subcategoryButton%d%d" % (i, j)]
								subcategoryButton.Hide()

		totalHeight = yPos
		visibleHeight = self.children["bg"].GetHeight()
		if totalHeight > visibleHeight:
			self.scrollBar2.SetMiddleBarSize(float(visibleHeight) / float(totalHeight))
			self.scrollBar2.Show()
			self.scrollBar2.OnMouseLeftButtonDown()
		else:
			self.scrollBar2.SetPos(0)
			self.OnScroll()
			self.scrollBar2.Hide()
		self.UpdateCategoryRenderingRect()	

	def CalculateTotalHeight(self):
		yPos = self.search_bg.GetHeight() + 10
		for i in xrange(len(option_data)):
			if self.children.has_key("titleBtn%d" % i):
				categoryButton = self.children["titleBtn%d" % i]
				yPos += categoryButton.GetHeight()+5

				if self.children.has_key("is_expanded%d" % i):
					is_expanded = self.children["is_expanded%d" % i]
					if is_expanded:
						for j in xrange(10):
							if self.children.has_key("subcategoryButton%d%d" % (i, j)):
								subcategoryButton = self.children["subcategoryButton%d%d" % (i, j)]
								yPos += subcategoryButton.GetHeight()
							else:
								break
		return yPos

	def OnScroll(self):
		pos = self.scrollBar2.GetPos()
		totalHeight = self.CalculateTotalHeight()
		visibleHeight = self.children["bg"].GetHeight()
		scrollHeight = totalHeight - visibleHeight

		yPos = self.search_bg.GetHeight() + 10 - int(pos * scrollHeight)
		for i in xrange(len(option_data)):
			if self.children.has_key("titleBtn%d" % i):
				categoryButton = self.children["titleBtn%d" % i]
				categoryButton.SetPosition(5, yPos)
				yPos += categoryButton.GetHeight() + 5

				if self.children.has_key("is_expanded%d" % i):
					is_expanded = self.children["is_expanded%d" % i]
					if is_expanded:
						for j in xrange(10):
							if self.children.has_key("subcategoryButton%d%d" % (i, j)):
								subcategoryButton = self.children["subcategoryButton%d%d" % (i, j)]
								subcategoryButton.SetPosition(5, yPos-5)
								subcategoryButton.Show()
								yPos += subcategoryButton.GetHeight()
							else:
								break
					else:
						for j in xrange(10):
							if self.children.has_key("subcategoryButton%d%d" % (i, j)):
								subcategoryButton = self.children["subcategoryButton%d%d" % (i, j)]
								subcategoryButton.Hide()

		self.UpdateCategoryRenderingRect()	
	def UpdateCategoryRenderingRect(self):
		visibleHeight = self.children["bg"].GetHeight() - 4- (self.search_bg.GetHeight() + 10)
		for i in xrange(len(option_data)):
			if self.children.has_key("titleBtn%d" % i):
				categoryButton = self.children["titleBtn%d" % i]
				categoryButtonHeight = categoryButton.GetHeight()
				(categoryButtonX, categoryButtonY) = categoryButton.GetLocalPosition()
				categoryButtonY -= self.search_bg.GetHeight() + 10 
				if categoryButtonY < 0:
					categoryButton.SetRenderingRect(0, ui.calculateRect(categoryButtonHeight - abs(categoryButtonY), categoryButtonHeight), 0, 0)
				elif categoryButtonY + categoryButtonHeight > visibleHeight:
					calculate = (visibleHeight - categoryButtonY) - categoryButtonHeight
					if calculate == 0:
						return
					f = ui.calculateRect(categoryButtonHeight - abs(calculate), categoryButtonHeight)
					categoryButton.SetRenderingRect(0, 0, 0, f)
				else:
					categoryButton.SetRenderingRect(0, 0, 0, 0)

				if categoryButtonY < -15 or categoryButtonY + categoryButtonHeight > visibleHeight + 13:
					categoryButton.ButtonText.Hide()
				else:
					categoryButton.ButtonText.Show()

				category_icon = self.children["category_icon%d" % i]
				category_iconHeight = category_icon.GetHeight()
				category_iconY = categoryButtonY + categoryButtonHeight / 2 - category_iconHeight / 2
				if category_iconY < 0:
					category_icon.SetRenderingRect(0, ui.calculateRect(category_iconHeight - abs(category_iconY), category_iconHeight), 0, 0)
				elif category_iconY + category_iconHeight > visibleHeight:
					calculate = (visibleHeight - category_iconY) - category_iconHeight
					if calculate == 0:
						return
					f = ui.calculateRect(category_iconHeight - abs(calculate), category_iconHeight)
					category_icon.SetRenderingRect(0, 0, 0, f)
				else:
					category_icon.SetRenderingRect(0, 0, 0, 0)

				expand_icon = self.children["expand_icon%d" % i]
				expand_iconHeight = expand_icon.GetHeight()
				expand_iconY = categoryButtonY + categoryButtonHeight / 2 - expand_iconHeight / 2
				if expand_iconY < 0:
					expand_icon.SetRenderingRect(0, ui.calculateRect(expand_iconHeight - abs(expand_iconY), expand_iconHeight), 0, 0)
				elif expand_iconY + expand_iconHeight > visibleHeight:
					calculate = (visibleHeight - expand_iconY) - expand_iconHeight
					if calculate == 0:
						return
					f = ui.calculateRect(expand_iconHeight - abs(calculate), expand_iconHeight)
					expand_icon.SetRenderingRect(0, 0, 0, f)
				else:
					expand_icon.SetRenderingRect(0, 0, 0, 0)

				if self.children.has_key("is_expanded%d" % i):
					is_expanded = self.children["is_expanded%d" % i]
					if is_expanded:
						for j in xrange(10):
							if self.children.has_key("subcategoryButton%d%d" % (i, j)):
								subcategoryButton = self.children["subcategoryButton%d%d" % (i, j)]
								subcategoryButtonHeight = subcategoryButton.GetHeight()
								(subcategoryButtonX, subcategoryButtonY) = subcategoryButton.GetLocalPosition()
								subcategoryButtonY -= self.search_bg.GetHeight() + 10  
								if subcategoryButtonY < 0:
									subcategoryButton.SetRenderingRect(0, ui.calculateRect(subcategoryButtonHeight - abs(subcategoryButtonY), subcategoryButtonHeight), 0, 0)
								elif subcategoryButtonY + subcategoryButtonHeight > visibleHeight:
									calculate = (visibleHeight - subcategoryButtonY) - subcategoryButtonHeight
									if calculate == 0:
										return
									f = ui.calculateRect(subcategoryButtonHeight - abs(calculate), subcategoryButtonHeight)
									subcategoryButton.SetRenderingRect(0, 0, 0, f)
								else:
									subcategoryButton.SetRenderingRect(0, 0, 0, 0)

								if subcategoryButtonY < -10 or subcategoryButtonY + subcategoryButtonHeight > visibleHeight + 8:
									subcategoryButton.ButtonText.Hide()
								else:
									subcategoryButton.ButtonText.Show()									

	# Dont Touch #						
	def OnUpdate(self):
		current_time = time.time()

		self.last_update_time = current_time

		# ENABLE_AUTOMATIC_PICK_UP_SYSTEM için premium status text'ini güncelle
		if app.ENABLE_AUTOMATIC_PICK_UP_SYSTEM:
			if self.pickupPremiumStatusText:
				try:
					if hasattr(constInfo, 'PREMIUMMODE') and len(constInfo.PREMIUMMODE) >= 2:
						if constInfo.PREMIUMMODE[0] == True or constInfo.PREMIUMMODE[0] == 1:
							remainingTime = constInfo.PREMIUMMODE[1] - app.GetGlobalTimeStamp()
							if remainingTime > 0:
								m, s = divmod(remainingTime, 60)
								h, m = divmod(m, 60)
								d, h = divmod(h, 24)
								if d > 0:
									timeStr = "%dd %dh %dm %ds" % (d, h, m, s)
								elif h > 0:
									timeStr = "%dh %dm %ds" % (h, m, s)
								elif m > 0:
									timeStr = "%dm %ds" % (m, s)
								else:
									timeStr = "%ds" % (s)
								self.pickupPremiumStatusText.SetText(uiScriptLocale.AUTO_PICKUP_PREMIUM_STATUS_ON % timeStr)
				except:
					pass

		window = self.GetCurrentWindow()
		if window == None:
			return
		scriptChildrens = window.Children
		if len(scriptChildrens) == 0:
			return

		elementDictionary = window.ElementDictionary
		for childName, child in elementDictionary.items():
			(_x, _y) = child.GetGlobalPosition()
			childHeight = child.GetHeight()
			textLines = []
			if isinstance(child, ui.TextLine):
				textLines.append(child)

			for childItem in textLines:
				text = childItem.GetText()
				if text is None or len(text) == 0:
					continue
				if childItem.GetTextSize()[0] > 250 and text.endswith("..") == False:
					if childItem not in self.original_texts:
						self.original_texts[childItem] = text
						self.text_iteration[childItem] = len(text)
						self.text_length[childItem] = len(text)

					if childItem not in self.default_texts:
						while childItem.GetTextSize()[0] > 250 and len(text) > 0:
							text = text[:-1]
							childItem.SetText(text)
						if childItem not in self.text_nr_of_letters_hidden:
							self.text_nr_of_letters_hidden[childItem] = len(self.original_texts[childItem]) - len(text)
						self.default_texts[childItem] = text
						self.text_iteration[childItem] = len(text)
						text = self.default_texts[childItem][:-2] + ".."
						childItem.SetText(text)							

				xMouse, yMouse = wndMgr.GetMousePosition()
				x, y = childItem.GetGlobalPosition()
				is_hovered = (
					xMouse >= x and
					xMouse < x + childItem.GetTextSize()[0] and
					yMouse >= y and
					yMouse < y + childItem.GetTextSize()[1]
				)

				if is_hovered:
					if childItem.GetText().endswith(".."):
						text = childItem.SetText(self.default_texts[childItem])
						self.text_iteration[childItem] = len(self.default_texts[childItem])
						self.text_nr_of_letters_hidden[childItem] = len(self.original_texts[childItem]) - len(self.default_texts[childItem])
						self.text_nr_of_letters_revealed[childItem] = 0

					if text is None or len(text) == 0:
						continue
					if len(text) > 2 and childItem in self.original_texts:
						if childItem not in self.text_directions:
							self.text_directions[childItem] = "forward"

						if self.text_directions[childItem] == "backward":
							self.text_directions[childItem] = "forward"

						if self.text_directions[childItem] == "forward":
							if self.text_iteration[childItem] < len(self.original_texts[childItem]):
								expected_next_letter = self.original_texts[childItem][self.text_iteration[childItem]]
								self.text_iteration[childItem] += 1
								new_text = text[1:] + expected_next_letter

								childItem.SetText(new_text)
								if childItem.GetTextSize()[0] > 250:
									new_text = new_text[:-1]
									self.text_iteration[childItem] -= 1
									childItem.SetText(new_text)

								if childItem.GetTextSize()[0] < 250-5:
									childItem.SetText(new_text)									

								if childItem not in self.text_nr_of_letters_revealed:
									self.text_nr_of_letters_revealed[childItem] = 1
								else:
									self.text_nr_of_letters_revealed[childItem] += 1
				else:
					if childItem in self.text_directions and self.text_directions[childItem] == "forward":
						self.text_directions[childItem] = "backward"
					elif childItem in self.text_directions and self.text_directions[childItem] == "backward":
						if childItem in self.default_texts:
							text = childItem.GetText()
							prev_char_index = self.text_nr_of_letters_revealed.get(childItem, 0) - 1
							self.text_iteration[childItem] -= 1

							if prev_char_index >= 0:
								new_text = self.original_texts[childItem][prev_char_index] + text[:-1]
								childItem.SetText(new_text)
								self.text_nr_of_letters_revealed[childItem] = prev_char_index
								while childItem.GetTextSize()[0] > 250:
									new_text = new_text[:-1]
									self.text_iteration[childItem] -= 1
									childItem.SetText(new_text)
								while childItem.GetTextSize()[0] < 250 - 5 and prev_char_index > 0:
									prev_char_index -= 1
									new_text = self.original_texts[childItem][prev_char_index] + new_text
									childItem.SetText(new_text)
									self.text_nr_of_letters_revealed[childItem] = prev_char_index								
							else:
								self.text_directions[childItem] = "forward"
								childItem.SetText(self.default_texts[childItem])
								self.text_iteration[childItem] = len(self.default_texts[childItem])
								self.text_nr_of_letters_hidden[childItem] = len(self.original_texts[childItem]) - len(self.default_texts[childItem])
								self.text_nr_of_letters_revealed[childItem] = 0
								text = self.default_texts[childItem][:-2] + ".."
								childItem.SetText(text)
	# Dont Touch #		

	def CreateOptionWindow(self, windowBG, optionIndex):
		scriptWindow = ui.ScriptWindow()
		scriptWindow.SetParent(windowBG)
		try:
			fileName = "UIScript/advanced_game_options/game_option_%d.py"%(optionIndex)
			pyScrLoader = ui.PythonScriptLoader()
			if pack.Exist(fileName):
				pyScrLoader.LoadScriptFile(scriptWindow, fileName)
				self.LoadCategoryOptions(scriptWindow, optionIndex)
			else:
				dbg.TraceError("[AdvancedGameOptions]Can't find script window for categoryIndex: %d"%(optionIndex))
		except Exception, msg:
			dbg.TraceError("AdvancedGameOptions.LoadScript - %s" % (msg))
		if scriptWindow.GetWidth() > 0:

			scrollBar = ScrollBarNew()
			scrollBar.SetParent(scriptWindow)
			scrollBar.SetPosition(scriptWindow.GetWidth()-scrollBar.GetWidth()-3,3)
			scrollBar.SetScrollBarSize(scriptWindow.GetHeight()-6)
			scrollBar.Hide()
			scrollBar.SetScrollEvent(ui.__mem_func__(self.UpdateScrollBar))
			scriptWindow.scrollBar = scrollBar
			scriptWindow.OnMouseWheel = ui.__mem_func__(self.OnMouseWheel)

			scriptChildrens = scriptWindow.Children
			for child in scriptChildrens:
				(_x,_y) = child.GetLocalPosition()
				child.SetPosition(_x,_y, True)

			scriptWindow.Show()
		else:
			scriptWindow.scrollBar = None
		
		return scriptWindow

	def LoadCategoryOptions(self, scriptWindow, optionIndex):
		try:
			# Button text pozisyonlarýný ayarla (sadece bir kez)
			if not hasattr(scriptWindow, '_text_positions_adjusted'):
				self.__AdjustButtonTextPositionsOnce(scriptWindow)
				scriptWindow._text_positions_adjusted = True
			
			GetObject = scriptWindow.GetChild
			# Iç içe elemanlar için (Arayüz): ElementDictionary ile bul
			elementDict = getattr(scriptWindow, "ElementDictionary", None)
			def getOpt(name):
				if elementDict:
					w = elementDict.get(name)
					if w:
						return w
				return GetObject(name)

			if optionIndex == 0 or self.children["filteringEnabled"]:#Interface-Options
					self.viewTargetBoardButtonList = []
					self.viewChatButtonList = []
					self.showDamageButtonList = []
					self.showsalesTextButtonList = []

					# Hedef Tahtasý
					target_board_view = getOpt("target_board_view")
					target_board_no_view = getOpt("target_board_no_view")
					if target_board_view and target_board_no_view:
						self.viewTargetBoardButtonList.append(target_board_view)
						self.viewTargetBoardButtonList[0].SAFE_SetEvent(self.__SetTargetBoardViewMode)
						self.viewTargetBoardButtonList.append(target_board_no_view)
						self.viewTargetBoardButtonList[1].SAFE_SetEvent(self.__SetTargetBoardViewMode)
						self.RefreshTargetBoard()

					# Sohbet Satýrý (Gözle Göster)
					view_chat_off_button = getOpt("view_chat_off_button")
					if view_chat_off_button:
						self.viewChatButtonList = view_chat_off_button
						view_chat_off_button.SetToggleUpEvent(self.__OnClickViewChat)
						view_chat_off_button.SetToggleDownEvent(self.__OnClickViewChat)
						self.RefreshViewChat()

					# Önemli Bilgiler (Show Damage)
					show_damage_on_button = getOpt("show_damage_on_button")
					if show_damage_on_button:
						self.showDamageButtonList = show_damage_on_button
						show_damage_on_button.SetToggleUpEvent(self.__OnClickShowDamage)
						show_damage_on_button.SetToggleDownEvent(self.__OnClickShowDamage)
						self.RefreshShowDamage()

					# Market Ýsmi
					try:
						salestext_window = getOpt("salestext_window")
						if salestext_window:
							salestext_on_button = salestext_window.GetChild("salestext_on_button") or getOpt("salestext_on_button")
							salestext_off_button = salestext_window.GetChild("salestext_off_button") or getOpt("salestext_off_button")
						else:
							salestext_on_button = getOpt("salestext_on_button")
							salestext_off_button = getOpt("salestext_off_button")
					except:
						salestext_on_button = None
						salestext_off_button = None
					
					if salestext_on_button and salestext_off_button and salestext_on_button is not salestext_off_button:
						self.showsalesTextButtonList.append(salestext_on_button)
						self.showsalesTextButtonList.append(salestext_off_button)
						self.showsalesTextButtonList[0].SetToggleUpEvent(self.__OnClickSalesTextGizle)
						self.showsalesTextButtonList[0].SetToggleDownEvent(self.__OnClickSalesTextGizle)
						self.showsalesTextButtonList[1].SetToggleUpEvent(self.__OnClickSalesTextGoster)
						self.showsalesTextButtonList[1].SetToggleDownEvent(self.__OnClickSalesTextGoster)
						self.RefreshShowSalesText()

			if optionIndex == 1 or self.children["filteringEnabled"]:#Game-Options
					self.pvpModeButtonDict={}
					self.blockButtonList=[]
					self.nameColorModeButtonList = []
					self.alwaysShowNameButtonList=[]
					self.showsalesTextButtonList=[]

					self.pvpModeButtonDict[player.PK_MODE_PEACE] = GetObject("pvp_peace")
					self.pvpModeButtonDict[player.PK_MODE_PEACE].SAFE_SetEvent(self.__OnClickPvPModePeaceButton)
					self.pvpModeButtonDict[player.PK_MODE_REVENGE] = GetObject("pvp_revenge")
					self.pvpModeButtonDict[player.PK_MODE_REVENGE].SAFE_SetEvent(self.__OnClickPvPModeRevengeButton)
					self.pvpModeButtonDict[player.PK_MODE_GUILD] = GetObject("pvp_guild")
					self.pvpModeButtonDict[player.PK_MODE_GUILD].SAFE_SetEvent(self.__OnClickPvPModeGuildButton)
					self.pvpModeButtonDict[player.PK_MODE_FREE] = GetObject("pvp_free")
					self.pvpModeButtonDict[player.PK_MODE_FREE].SAFE_SetEvent(self.__OnClickPvPModeFreeButton)
					self.__SetPeacePKMode()

					block_exchange_button = GetObject("block_exchange_button")
					block_exchange_button.SetToggleUpEvent(self.__OnClickBlockExchangeButton)
					block_exchange_button.SetToggleDownEvent(self.__OnClickBlockExchangeButton)
					self.blockButtonList.append(block_exchange_button)

					block_party_button = GetObject("block_party_button")
					block_party_button.SetToggleUpEvent(self.__OnClickBlockPartyButton)
					block_party_button.SetToggleDownEvent(self.__OnClickBlockPartyButton)
					self.blockButtonList.append(block_party_button)

					block_guild_button = GetObject("block_guild_button")
					block_guild_button.SetToggleUpEvent(self.__OnClickBlockGuildButton)
					block_guild_button.SetToggleDownEvent(self.__OnClickBlockGuildButton)
					self.blockButtonList.append(block_guild_button)

					block_whisper_button = GetObject("block_whisper_button")
					block_whisper_button.SetToggleUpEvent(self.__OnClickBlockWhisperButton)
					block_whisper_button.SetToggleDownEvent(self.__OnClickBlockWhisperButton)
					self.blockButtonList.append(block_whisper_button)

					block_friend_button = GetObject("block_friend_button")
					block_friend_button.SetToggleUpEvent(self.__OnClickBlockFriendButton)
					block_friend_button.SetToggleDownEvent(self.__OnClickBlockFriendButton)
					self.blockButtonList.append(block_friend_button)

					block_party_request_button = GetObject("block_party_request_button")
					block_party_request_button.SetToggleUpEvent(self.__OnClickBlockPartyRequest)
					block_party_request_button.SetToggleDownEvent(self.__OnClickBlockPartyRequest)
					self.blockButtonList.append(block_party_request_button)

					try:
						block_warp_request_button = elementDict.get("block_warp_request_button") if elementDict else None
						if block_warp_request_button:
							block_warp_request_button.SetToggleUpEvent(self.__OnClickBlockWarpRequest)
							block_warp_request_button.SetToggleDownEvent(self.__OnClickBlockWarpRequest)
							self.blockButtonList.append(block_warp_request_button)
					except Exception:
						pass
					self.RefreshBlock()

					self.alwaysShowNameButtonList.append(GetObject("always_show_name_on_button"))
					self.alwaysShowNameButtonList[0].SAFE_SetEvent(self.__OnClickAlwaysShowName)
					self.alwaysShowNameButtonList.append(GetObject("always_show_name_off_button"))
					self.alwaysShowNameButtonList[1].SAFE_SetEvent(self.__OnClickAlwaysShowName)
					self.RefreshAlwaysShowName()

					self.nameColorModeButtonList.append(GetObject("name_color_normal"))
					self.nameColorModeButtonList[0].SAFE_SetEvent(self.__OnClickNameColorMode)
					self.nameColorModeButtonList.append(GetObject("name_color_empire"))
					self.nameColorModeButtonList[1].SAFE_SetEvent(self.__OnClickNameColorMode)
					self.RefreshNameColor()

					self.nameOutlineModeButtonList = []
					name_outline_on = GetObject("name_outline_on")
					name_outline_off = GetObject("name_outline_off")
					if name_outline_on and name_outline_off:
						self.nameOutlineModeButtonList.append(name_outline_on)
						self.nameOutlineModeButtonList[0].SAFE_SetEvent(self.__OnClickNameOutlineMode)
					self.nameOutlineModeButtonList.append(name_outline_off)
					self.nameOutlineModeButtonList[1].SAFE_SetEvent(self.__OnClickNameOutlineMode)
					self.RefreshNameOutline()
			if optionIndex == 2 or self.children["filteringEnabled"]:#Environment-Options

					self.cameraModeButtonList=[]
					self.fogModeButtonList = []
					self.nightModeButtonList = []
					self.snowModeButtonList = []
					self.snowTextureModeButtonList = []

					self.cameraModeButtonList.append(GetObject("camera_short"))
					self.cameraModeButtonList[0].SAFE_SetEvent(self.__OnClickCameraMode)
					self.cameraModeButtonList.append(GetObject("camera_long"))
					self.cameraModeButtonList[1].SAFE_SetEvent(self.__OnClickCameraMode)
					self.RefreshCameraMode()

					self.fogModeButtonList.append(GetObject("fog_level0"))
					self.fogModeButtonList[0].SAFE_SetEvent(self.__OnClickFog, 0)
					self.fogModeButtonList.append(GetObject("fog_level1"))
					self.fogModeButtonList[1].SAFE_SetEvent(self.__OnClickFog, 1)
					self.fogModeButtonList.append(GetObject("fog_level2"))
					self.fogModeButtonList[2].SAFE_SetEvent(self.__OnClickFog, 2)
					self.RefreshFog()

					night_mode_on = GetObject("night_mode_on")
					night_mode_off = GetObject("night_mode_off")
					if night_mode_on and night_mode_off:
						self.nightModeButtonList.append(night_mode_on)
						self.nightModeButtonList[0].SAFE_SetEvent(self.__OnClickNightMode)
						self.nightModeButtonList.append(night_mode_off)
						self.nightModeButtonList[1].SAFE_SetEvent(self.__OnClickNightMode)
						self.RefreshNightMode()

					snow_mode_on = GetObject("snow_mode_on")
					snow_mode_off = GetObject("snow_mode_off")
					if snow_mode_on and snow_mode_off:
						self.snowModeButtonList.append(snow_mode_on)
						self.snowModeButtonList[0].SAFE_SetEvent(self.__OnClickSnowMode)
						self.snowModeButtonList.append(snow_mode_off)
						self.snowModeButtonList[1].SAFE_SetEvent(self.__OnClickSnowMode)
						self.RefreshSnowMode()

					snow_texture_mode_on = GetObject("snow_texture_mode_on")
					snow_texture_mode_off = GetObject("snow_texture_mode_off")
					if snow_texture_mode_on and snow_texture_mode_off:
						self.snowTextureModeButtonList.append(snow_texture_mode_on)
						self.snowTextureModeButtonList[0].SAFE_SetEvent(self.__OnClickSnowTextureMode)
						self.snowTextureModeButtonList.append(snow_texture_mode_off)
						self.snowTextureModeButtonList[1].SAFE_SetEvent(self.__OnClickSnowTextureMode)
						self.RefreshSnowTextureMode()

			if optionIndex == 3 or self.children["filteringEnabled"]:#Sound-Options

					self.ctrlSoundVolume = None
					self.ctrlMusicVolume = None
					self.selectMusicFile = None
					self.selectMusicButton = None
					self.musicListDlg = None

					ctrlSoundVolume = GetObject("sound_volume_controller")
					ctrlSoundVolume.SetSliderPos(float(systemSetting.GetSoundVolume()) / 5.0)
					ctrlSoundVolume.SetEvent(ui.__mem_func__(self.OnChangeSoundVolume))
					self.ctrlSoundVolume = ctrlSoundVolume

					ctrlMusicVolume = GetObject("music_volume_controller")
					ctrlMusicVolume.SetSliderPos(float(systemSetting.GetMusicVolume()))
					ctrlMusicVolume.SetEvent(ui.__mem_func__(self.OnChangeMusicVolume))
					self.ctrlMusicVolume = ctrlMusicVolume
					self.selectMusicButton = GetObject("bgm_button")
					self.selectMusicButton.SetToggleDownEvent(self.__OnClickChangeMusicButton)
					self.selectMusicFile = GetObject("bgm_file")

			if optionIndex == 4 or self.children["filteringEnabled"]:#Graphics-Options
					self.enbModeButtonList = []
					self.effectLevelButtonList = []
					self.privateShopLevelButtonList = []
					self.dropItemLevelButtonList = []
					self.petStatusButtonList = []
					self.npcNameStatusButtonList = []
					self.showMobLevelButtonList = []
					self.showMobAIFlagButtonList = []
					
					# ENB Mode
					enbMode_on = GetObject("enbMode_on")
					enbMode_off = GetObject("enbMode_off")
					if enbMode_on and enbMode_off:
						self.enbModeButtonList.append(enbMode_on)
						self.enbModeButtonList[0].SAFE_SetEvent(self.__OnClickENBMode)
						self.enbModeButtonList.append(enbMode_off)
						self.enbModeButtonList[1].SAFE_SetEvent(self.__OnClickENBMode)
						self.RefreshENBMode()
					
					# Effect Level - sadece RadioButton ise event bagla (yanlis tip cokmeyi onler)
					for i in xrange(1, 6):
						effectBtn = GetObject("effect_level%d" % i)
						if effectBtn and isinstance(effectBtn, ui.RadioButton):
							self.effectLevelButtonList.append(effectBtn)
							self.effectLevelButtonList[-1].SAFE_SetEvent(self.__OnClickEffectLevel, len(self.effectLevelButtonList)-1)
					if len(self.effectLevelButtonList) > 0:
						self.RefreshEffectLevel()
					
					# Effect Apply Button
					effectApplyBtn = GetObject("effect_apply")
					if effectApplyBtn:
						self.effectLevelApplyButton = effectApplyBtn
						effectApplyBtn.SAFE_SetEvent(self.__OnClickEffectApplyButton)
					
					# Private Shop Level - sadece RadioButton ise event bagla
					for i in xrange(1, 6):
						shopBtn = GetObject("privateShop_level%d" % i)
						if shopBtn and isinstance(shopBtn, ui.RadioButton):
							self.privateShopLevelButtonList.append(shopBtn)
							self.privateShopLevelButtonList[-1].SAFE_SetEvent(self.__OnClickPrivateShopLevel, len(self.privateShopLevelButtonList)-1)
					if len(self.privateShopLevelButtonList) > 0:
						self.RefreshPrivateShopLevel()
					
					# Private Shop Apply Button
					privateShopApplyBtn = GetObject("privateShop_apply")
					if privateShopApplyBtn:
						self.privateShopLevelApplyButton = privateShopApplyBtn
						privateShopApplyBtn.SAFE_SetEvent(self.__OnClickPrivateShopApplyButton)
					
					# Drop Item Level
					for i in xrange(1, 6):
						dropBtn = GetObject("dropItem_level%d" % i)
						if dropBtn:
							self.dropItemLevelButtonList.append(dropBtn)
							self.dropItemLevelButtonList[i-1].SAFE_SetEvent(self.__OnClickDropItemLevel, i-1)
					self.RefreshDropItemLevel()
					
					# Drop Item Apply Button
					dropItemApplyBtn = GetObject("dropItem_apply")
					if dropItemApplyBtn:
						self.dropItemLevelApplyButton = dropItemApplyBtn
						dropItemApplyBtn.SAFE_SetEvent(self.__OnClickDropItemApplyButton)
					
					# Pet Status
					pet_on = GetObject("pet_on")
					pet_off = GetObject("pet_off")
					if pet_on and pet_off:
						self.petStatusButtonList.append(pet_on)
						self.petStatusButtonList[0].SAFE_SetEvent(self.__OnClickPetStatus)
						self.petStatusButtonList.append(pet_off)
						self.petStatusButtonList[1].SAFE_SetEvent(self.__OnClickPetStatus)
						self.RefreshPetStatus()
					
					# NPC Name Status
					npcName_on = GetObject("npcName_on")
					npcName_off = GetObject("npcName_off")
					if npcName_on and npcName_off:
						self.npcNameStatusButtonList.append(npcName_on)
						self.npcNameStatusButtonList[0].SAFE_SetEvent(self.__OnClickNpcNameStatus)
						self.npcNameStatusButtonList.append(npcName_off)
						self.npcNameStatusButtonList[1].SAFE_SetEvent(self.__OnClickNpcNameStatus)
						self.RefreshNpcNameStatus()
					
					# Show Mob Level
					showMobLevelBtn = GetObject("show_mob_level_button")
					if showMobLevelBtn:
						self.showMobLevelButtonList = showMobLevelBtn
						showMobLevelBtn.SetToggleUpEvent(self.__OnClickShowMobLevel)
						showMobLevelBtn.SetToggleDownEvent(self.__OnClickShowMobLevel)
						self.RefreshShowMobLevel()
					
					# Show Mob AI Flag
					showMobAIFlagBtn = GetObject("show_mob_AI_flag_button")
					if showMobAIFlagBtn:
						self.showMobAIFlagButtonList = showMobAIFlagBtn
						showMobAIFlagBtn.SetToggleUpEvent(self.__OnClickShowMobAIFlag)
						showMobAIFlagBtn.SetToggleDownEvent(self.__OnClickShowMobAIFlag)
						self.RefreshShowMobAIFlag()
					
					# FOV Controller (if exists)
					try:
						fovController = GetObject("fov_controller")
						if fovController:
							self.fovController = fovController
							fovController.SetEvent(ui.__mem_func__(self.OnChangeFOV))
							if hasattr(systemSetting, 'GetFOV'):
								if hasattr(app, 'MAX_CAMERA_PERSPECTIVE'):
									fovController.SetSliderPos(float(systemSetting.GetFOV()) / float(app.MAX_CAMERA_PERSPECTIVE))
								else:
									fovController.SetSliderPos(float(systemSetting.GetFOV()) / 100.0)
						
						fovResetBtn = GetObject("fov_reset_button")
						if fovResetBtn:
							self.fovResetButton = fovResetBtn
							fovResetBtn.SAFE_SetEvent(self.OnClickFOVReset)
					except:
						pass
					
					# Stone Scale Controller (if exists)
					try:
						stoneScaleController = GetObject("stone_scale_controller")
						if stoneScaleController:
							self.stoneScaleController = stoneScaleController
							stoneScaleController.SetEvent(ui.__mem_func__(self.OnChangeStoneScale))
							if hasattr(systemSetting, 'GetStoneScale'):
								stoneScaleValue = systemSetting.GetStoneScale()
								stoneScaleController.SetSliderPos(float(stoneScaleValue))
						
						stoneScaleResetBtn = GetObject("stone_scale_reset_button")
						if stoneScaleResetBtn:
							self.stoneScaleResetButton = stoneScaleResetBtn
							stoneScaleResetBtn.SAFE_SetEvent(self.OnClickStoneScaleReset)
					except:
						pass

			if optionIndex == 5 or self.children["filteringEnabled"]:#Pickup-Options
					self.mainPickModeButtonList = []
					self.mainPickUPButtonList = []

					# Premium status text (nested in pickup_premimum_image)
					try:
						pickupPremiumImage = GetObject("pickup_premimum_image")
						if pickupPremiumImage:
							pickupPremiumStatusText = pickupPremiumImage.GetChild("pickup_premium_status_text")
							if pickupPremiumStatusText:
								self.pickupPremiumStatusText = pickupPremiumStatusText
								pickupPremiumStatusText.Show()  # Text'i göster
								# Baþlangýç deðerini ayarla
								import uiScriptLocale
								pickupPremiumStatusText.SetText(uiScriptLocale.AUTO_PICKUP_PREMIUM_STATUS_OFF)
					except Exception, e:
						try:
							# Fallback: try direct GetObject
							pickupPremiumStatusText = GetObject("pickup_premium_status_text")
							if pickupPremiumStatusText:
								self.pickupPremiumStatusText = pickupPremiumStatusText
								pickupPremiumStatusText.Show()  # Text'i göster
								import uiScriptLocale
								pickupPremiumStatusText.SetText(uiScriptLocale.AUTO_PICKUP_PREMIUM_STATUS_OFF)
						except:
							pass

					# Pickup activate/deactivate buttons (toggle buttons - mutually exclusive)
					try:
						pick_up_button_activate = GetObject("pick_up_button_activate")
						if pick_up_button_activate:
							# Aktif butonuna týklandýðýnda (eski sistem gibi - her iki event de ayný handler'ý çaðýrýr)
							pick_up_button_activate.SetToggleUpEvent(self.__OnClickPickupModeButton)
							pick_up_button_activate.SetToggleDownEvent(self.__OnClickPickupModeButton)
							pick_up_button_activate.Show()
							self.mainPickModeButtonList.append(pick_up_button_activate)

						pick_up_button_deactivate = GetObject("pick_up_button_deactivate")
						if pick_up_button_deactivate:
							# Devre Dýþý butonuna týklandýðýnda (eski sistem gibi - her iki event de ayný handler'ý çaðýrýr)
							pick_up_button_deactivate.SetToggleUpEvent(self.__OnClickPickupModeButton)
							pick_up_button_deactivate.SetToggleDownEvent(self.__OnClickPickupModeButton)
							pick_up_button_deactivate.Show()
							self.mainPickModeButtonList.append(pick_up_button_deactivate)
					except:
						pass

					# Pickup filter buttons
					pickup_filter_child_names = [
						"pick_up_weapons",
						"pick_up_armors",
						"pick_up_shield",
						"pick_up_helmets",
						"pick_up_bracelets",
						"pick_up_necklace",
						"pick_up_earrings",
						"pick_up_shoes",
						"pick_up_others",
						"pick_up_yang",
						"pick_up_chests"
					]

					try:
						import constInfo
						i = 1
						for names in pickup_filter_child_names:
							objectPointer = GetObject(names)
							if objectPointer:
								objectPointer.SetToggleUpEvent(lambda type = 1 << i, ignore = False : self.__OnClickPickupIgnoreButton(type, ignore))
								objectPointer.SetToggleDownEvent(lambda type = 1 << i, ignore = True : self.__OnClickPickupIgnoreButton(type, ignore))
								objectPointer.Show()  # Checkbox'ý göster
								self.mainPickUPButtonList.append(objectPointer)
								i += 1
					except:
						pass

					self.RefreshPickUP()
		except Exception, msg:
			dbg.TraceError("LoadCategoryOptions : %s" % (msg))

	def __AdjustButtonTextPositionsOnce(self, scriptWindow):
		"""Radio button ve toggle button'larýn text pozisyonlarýný bir kez ayarla"""
		try:
			def adjustButtonRecursive(element):
				"""Recursive olarak tüm elementleri tarar ve button text pozisyonlarýný ayarlar"""
				if isinstance(element, ui.RadioButton) or isinstance(element, ui.ToggleButton):
					if element.ButtonText:
						# Mevcut pozisyonu al
						currentX, currentY = element.ButtonText.GetLocalPosition()
						# Radio button için 15 pixel, toggle button için 25 pixel saða kaydýr
						if isinstance(element, ui.RadioButton):
							newX = currentX + 1  # Orijinal 25'ten 40'a çýkarmak için +15
						else:  # ToggleButton
							newX = currentX + 1  # Orijinal 45'ten 70'e çýkarmak için +25
						element.ButtonText.SetPosition(newX, currentY)
				
				# Children'larý recursive olarak kontrol et
				if hasattr(element, 'Children'):
					for child in element.Children:
						adjustButtonRecursive(child)
			
			# Script window'un tüm elementlerini tarayarak button'larý bul
			elementDictionary = scriptWindow.ElementDictionary
			for childName, child in elementDictionary.items():
				adjustButtonRecursive(child)
			
			# Script window'un direkt children'larýný da kontrol et
			if hasattr(scriptWindow, 'Children'):
				for child in scriptWindow.Children:
					adjustButtonRecursive(child)
		except Exception, msg:
			dbg.TraceError("__AdjustButtonTextPositionsOnce : %s" % (msg))

	# Dont Touch #
	def GetCurrentWindow(self):
		if self.children.has_key("optionType"):
			optionType = self.children["optionType"]
			if self.children.has_key("filteringEnabled"):
				if self.children["filteringEnabled"]:
					return self.children["filteredWindow"]
				else:
					if self.children.has_key("optionWindow%d"%(optionType)):
						return self.children["optionWindow%d"%(optionType)]
		return None
	def GetCurrentScrollBar(self):
		window = self.GetCurrentWindow()
		if window != None:
			return window.scrollBar
		return None
	def OnMouseWheel(self, nLen):
		scrollBar = self.GetCurrentScrollBar()
		if scrollBar:
			if scrollBar.IsShow():
				if nLen > 0:
					scrollBar.OnUp()
				else:
					scrollBar.OnDown()
				return True
		return False

	def OnMouseWheelCategories(self, nLen):
		scrollBar = self.scrollBar2
		if scrollBar:
			if scrollBar.IsShow():
				if nLen > 0:
					scrollBar.OnUp()
				else:
					scrollBar.OnDown()
				return True
		return False		

	def GoToSubcategory(self, subcategoryName):
		if not self.scrollbar_is_show:
			return
		window = self.GetCurrentWindow()
		if window is None:
			return

		scrollBar = window.scrollBar
		if scrollBar is None:
			return

		scriptChildrens = window.Children
		if len(scriptChildrens) == 0:
			return
		elementDictionary = window.ElementDictionary
		scrollStep = 0.3 
		maxScroll = 1.0   
		minScroll = 0.0  

		for childName, child in elementDictionary.items():
			if childName.startswith("title_"):
				# ExpandedImageBox tipindeki elementler için içlerindeki text elementini bul
				text_value = ""
				if isinstance(child, ui.ExpandedImageBox):
					for textChild in child.Children:
						if isinstance(textChild, ui.TextLine):
							text_value = textChild.GetText()
							break
				else:
					try:
						text_value = child.GetText()
					except:
						text_value = ""
				
				if text_value == subcategoryName:
					maxIter = 100
					iterCount = 0
					while iterCount < maxIter:
						iterCount += 1
						try:
							child_y = child.GetGlobalPosition()[1] - window.GetGlobalPosition()[1]
						except Exception:
							break
						if child_y > 10:
							currentScroll = scrollBar.GetPos()
							newScroll = min(currentScroll + scrollStep, maxScroll)
							if newScroll == currentScroll:
								break
							scrollBar.SetPos(newScroll)
							self.UpdateScrollBar()
						elif child_y < 8:
							currentScroll = scrollBar.GetPos()
							newScroll = min(currentScroll - scrollStep, minScroll)
							if newScroll == currentScroll:
								break
							scrollBar.SetPos(newScroll)
							self.UpdateScrollBar()
						else:
							break

	def UpdateScrollBar(self):
		window = self.GetCurrentWindow()
		if window == None:
			return
		scrollBar = window.scrollBar
		if scrollBar == None:
			return
		scriptChildrens = window.Children
		if len(scriptChildrens) == 0:
			return

		windowHeight = window.GetHeight()

		screenSize = 0
		for child in scriptChildrens:
			try:
				exPos = getattr(child, 'exPos', None)
				if exPos is None:
					(_x, _y) = child.GetLocalPosition()
					childHeight = _y + child.GetHeight()
				else:
					childHeight = exPos[1] + child.GetHeight()
			except Exception:
				childHeight = child.GetHeight()
			if childHeight > screenSize:
				screenSize=childHeight

		if self.children.has_key("filteringEnabled"):
			if self.children["filteringEnabled"]:
				if self.children.has_key("filteredWindowHeight"):
					screenSize = self.children["filteredWindowHeight"]

		if screenSize > windowHeight:
			scrollLen = screenSize-windowHeight
			basePos = int(scrollBar.GetPos()*scrollLen)
			for child in scriptChildrens:
				try:
					exPos = getattr(child, 'exPos', None)
					if exPos is not None:
						(_x,_y) = exPos
					else:
						(_x,_y) = child.GetLocalPosition()
					child.SetPosition(_x,_y-basePos)
				except Exception:
					pass

			scrollBar.SetMiddleBarSize(float(windowHeight-(self.search_bg.GetHeight() + 10))/float(screenSize))
			scrollBar.Show()
			self.scrollbar_is_show = True
		else:
			scrollBar.Hide()
			self.scrollbar_is_show = False

		_wy = window.GetGlobalPosition()[1]
		elementDictionary = window.ElementDictionary
		for childName, child in elementDictionary.items():
			try:
				(_x,_y) = child.GetGlobalPosition()
				childHeight = child.GetHeight()
			except Exception:
				continue
			textLines = []
			images = []
			if isinstance(child, ui.ExpandedImageBox):
				images.append(child)
			elif isinstance(child, ui.TextLine):
				textLines.append(child)
			elif isinstance(child, ui.ToggleButton) or isinstance(child, ui.RadioButton) or isinstance(child, ui.Button):
				if child.ButtonText != None:
					textLines.append(child.ButtonText)
				images.append(child)
			elif isinstance(child, ui.SliderBar):
				if child.backGroundImage != None:
					images.append(child.backGroundImage)
				if child.cursor != None:
					images.append(child.cursor)
			elif isinstance(child, ui.SliderBar_AdvancedGameOptions):
				if child.backGroundImage != None:
					images.append(child.backGroundImage)
				if child.cursor != None:
					images.append(child.cursor)			
				if child.percentage != None:
					textLines.append(child.percentage)		

			for childItem in textLines:
				if _y < _wy:
					if childItem.IsShow():
						childItem.Hide()
				elif _y > (_wy+windowHeight-20):
					if childItem.IsShow():
						childItem.Hide()
				else:
					if not childItem.IsShow():
						childItem.Show()

			for childItem in images:
				if _y < _wy:
					childItem.SetRenderingRect(0,ui.calculateRect(childHeight-abs(_y-_wy),childHeight),0,0)
				elif _y+childHeight > (_wy+windowHeight-4):
					calculate = (_wy+windowHeight-4) - (_y+childHeight)
					if calculate == 0:
						return
					f = ui.calculateRect(childHeight-abs(calculate),childHeight)
					childItem.SetRenderingRect(0,0,0,f)
				else:
					childItem.SetRenderingRect(0,0,0,0)
	# Dont Touch #

	# PvP - Mode
	def __SetPeacePKMode(self):
		self.__SetPKMode(player.PK_MODE_PEACE)
	def __SetPKMode(self, mode):
		for btn in self.pvpModeButtonDict.values():
			btn.SetUp()
		if self.pvpModeButtonDict.has_key(mode):
			self.pvpModeButtonDict[mode].Down()
	def __CheckPvPProtectedLevelPlayer(self):
		if player.GetStatus(player.LEVEL)<constInfo.PVPMODE_PROTECTED_LEVEL:
			self.__SetPeacePKMode()
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.OPTION_PVPMODE_PROTECT % (constInfo.PVPMODE_PROTECTED_LEVEL))
			return True
		return False
	def __RefreshPVPButtonList(self):
		self.__SetPKMode(player.GetPKMode())
	def __OnClickPvPModePeaceButton(self):
		if self.__CheckPvPProtectedLevelPlayer():
			return
		self.__RefreshPVPButtonList()
		if constInfo.PVPMODE_ENABLE:
			net.SendChatPacket("/pkmode 0", chat.CHAT_TYPE_TALKING)
		else:
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.OPTION_PVPMODE_NOT_SUPPORT)
	def __OnClickPvPModeRevengeButton(self):
		if self.__CheckPvPProtectedLevelPlayer():
			return
		self.__RefreshPVPButtonList()
		if constInfo.PVPMODE_ENABLE:
			net.SendChatPacket("/pkmode 1", chat.CHAT_TYPE_TALKING)
		else:
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.OPTION_PVPMODE_NOT_SUPPORT)
	def __OnClickPvPModeFreeButton(self):
		if self.__CheckPvPProtectedLevelPlayer():
			return
		self.__RefreshPVPButtonList()
		if constInfo.PVPMODE_ENABLE:
			net.SendChatPacket("/pkmode 2", chat.CHAT_TYPE_TALKING)
		else:
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.OPTION_PVPMODE_NOT_SUPPORT)
	def __OnClickPvPModeGuildButton(self):
		if self.__CheckPvPProtectedLevelPlayer():
			return
		self.__RefreshPVPButtonList()
		if 0 == player.GetGuildID():
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.OPTION_PVPMODE_CANNOT_SET_GUILD_MODE)
			return
		if constInfo.PVPMODE_ENABLE:
			net.SendChatPacket("/pkmode 4", chat.CHAT_TYPE_TALKING)
		else:
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.OPTION_PVPMODE_NOT_SUPPORT)
	def OnChangePKMode(self):
		self.__RefreshPVPButtonList()
	# PvP - Mode

	# Block - Mode
	def RefreshBlock(self):
		global blockMode
		for i in xrange(len(self.blockButtonList)):
			if 0 != (blockMode & (1 << i)):
				self.blockButtonList[i].Down()
			else:
				self.blockButtonList[i].SetUp()
	def OnBlockMode(self, mode):
		global blockMode
		blockMode = mode
		self.RefreshBlock()
	def __OnClickBlockExchangeButton(self):
		self.RefreshBlock()
		global blockMode
		net.SendChatPacket("/setblockmode " + str(blockMode ^ player.BLOCK_EXCHANGE))

	def __OnClickBlockPartyButton(self):
		self.RefreshBlock()
		global blockMode
		net.SendChatPacket("/setblockmode " + str(blockMode ^ player.BLOCK_PARTY))
	def __OnClickBlockGuildButton(self):
		self.RefreshBlock()
		global blockMode
		net.SendChatPacket("/setblockmode " + str(blockMode ^ player.BLOCK_GUILD))
	def __OnClickBlockWhisperButton(self):
		self.RefreshBlock()
		global blockMode
		net.SendChatPacket("/setblockmode " + str(blockMode ^ player.BLOCK_WHISPER))
	def __OnClickBlockFriendButton(self):
		self.RefreshBlock()
		global blockMode
		net.SendChatPacket("/setblockmode " + str(blockMode ^ player.BLOCK_FRIEND))
	def __OnClickBlockPartyRequest(self):
		self.RefreshBlock()
		global blockMode
		net.SendChatPacket("/setblockmode " + str(blockMode ^ player.BLOCK_PARTY_REQUEST))
	def __OnClickBlockWarpRequest(self):
		self.RefreshBlock()
		global blockMode
		# BLOCK_WARP_REQUEST kullanýlýyor
		if hasattr(player, 'BLOCK_WARP_REQUEST'):
			net.SendChatPacket("/setblockmode " + str(blockMode ^ player.BLOCK_WARP_REQUEST))
		elif hasattr(player, 'BLOCK_WARP'):
			net.SendChatPacket("/setblockmode " + str(blockMode ^ player.BLOCK_WARP))
	# Block - Mode

	# Chat - Mode
	def RefreshViewChat(self):
		if not systemSetting.IsViewChat():
			self.viewChatButtonList.Down()
			self.viewChatButtonList.SetUp()
		else:
			self.viewChatButtonList.SetUp()
			self.viewChatButtonList.Down()
	def __OnClickViewChat(self):
		systemSetting.SetViewChatFlag(not systemSetting.IsViewChat())
		self.RefreshViewChat()
	# Chat - Mode

	# Name Color - Mode
	def __OnClickNameColorMode(self):
		constInfo.SET_CHRNAME_COLOR_INDEX(not constInfo.GET_CHRNAME_COLOR_INDEX())
		self.RefreshNameColor()
	def RefreshNameColor(self):
		index = constInfo.GET_CHRNAME_COLOR_INDEX()
		self.nameColorModeButtonList[index].Down()
		self.nameColorModeButtonList[not index].SetUp()
	# Name Color - Mode

	# Target Board - Mode
	def RefreshTargetBoard(self):
		index = constInfo.GET_VIEW_OTHER_EMPIRE_PLAYER_TARGET_BOARD()
		self.viewTargetBoardButtonList[index].Down()
		self.viewTargetBoardButtonList[not index].SetUp()
	def __SetTargetBoardViewMode(self):
		constInfo.SET_VIEW_OTHER_EMPIRE_PLAYER_TARGET_BOARD(not constInfo.GET_VIEW_OTHER_EMPIRE_PLAYER_TARGET_BOARD())
		self.RefreshTargetBoard()
	# Target Board - Mode

	# Show Always Name - Mode
	def RefreshAlwaysShowName(self):
		if len(self.alwaysShowNameButtonList) >= 2:
			if hasattr(systemSetting, 'IsAlwaysShowName'):
				# 0 = Her zaman (ON), 1 = Sinirli (OFF)
				index = 0 if systemSetting.IsAlwaysShowName() else 1
				self.alwaysShowNameButtonList[index].Down()
				self.alwaysShowNameButtonList[1 - index].SetUp()
	def __OnClickAlwaysShowName(self):
		if hasattr(systemSetting, 'SetAlwaysShowNameFlag'):
			systemSetting.SetAlwaysShowNameFlag(not systemSetting.IsAlwaysShowName())
			self.RefreshAlwaysShowName()
	# Show Always Name - Mode

	# Name Outline - Mode
	def RefreshNameOutline(self):
		if len(self.nameOutlineModeButtonList) >= 2:
			if hasattr(systemSetting, 'IsShowOutline'):
				index = 1 if systemSetting.IsShowOutline() else 0
				self.nameOutlineModeButtonList[index].Down()
				self.nameOutlineModeButtonList[not index].SetUp()
	def __OnClickNameOutlineMode(self):
		if hasattr(systemSetting, 'SetShowOutlineFlag') and hasattr(systemSetting, 'IsShowOutline'):
			systemSetting.SetShowOutlineFlag(not systemSetting.IsShowOutline())
			self.RefreshNameOutline()
	# Name Outline - Mode

	# Show Damage - Mode
	def RefreshShowDamage(self):
		if systemSetting.IsShowDamage():
			self.showDamageButtonList.Down()
			self.showDamageButtonList.SetUp()
		else:
			self.showDamageButtonList.SetUp()
			self.showDamageButtonList.Down()		
	def __OnClickShowDamage(self):
		systemSetting.SetShowDamageFlag(not systemSetting.IsShowDamage())
		self.RefreshShowDamage()
	# Show Damage - Mode

	# Sales Text - Mode: Gizle=0, Goster=1; tek secim, C++ 0/1
	def __OnClickSalesTextGizle(self):
		if hasattr(systemSetting, 'SetShowSalesTextFlag'):
			systemSetting.SetShowSalesTextFlag(0)
		self.__ClickRadioButton(self.showsalesTextButtonList, 0)
		try:
			import uiPrivateShopBuilder
			uiPrivateShopBuilder.UpdateADBoard()
		except:
			pass
		try:
			import uiOfflineShopBuilder
			uiOfflineShopBuilder.UpdateADBoard()
		except:
			pass
	def __OnClickSalesTextGoster(self):
		if hasattr(systemSetting, 'SetShowSalesTextFlag'):
			systemSetting.SetShowSalesTextFlag(1)
		self.__ClickRadioButton(self.showsalesTextButtonList, 1)
		try:
			import uiPrivateShopBuilder
			uiPrivateShopBuilder.UpdateADBoard()
		except:
			pass
		try:
			import uiOfflineShopBuilder
			uiOfflineShopBuilder.UpdateADBoard()
		except:
			pass
	def RefreshShowSalesText(self):
		if len(self.showsalesTextButtonList) >= 2 and hasattr(systemSetting, 'IsShowSalesText'):
			index = 1 if systemSetting.IsShowSalesText() else 0
			self.__ClickRadioButton(self.showsalesTextButtonList, index)
	# Sales Text - Mode


	# Sound - Mode
	def OnChangeSoundVolume(self):
		pos = self.ctrlSoundVolume.GetSliderPos()
		snd.SetSoundVolumef(pos)
		systemSetting.SetSoundVolumef(pos)
	# Sound - Mode

	# Music - Mode
	def OnChangeMusicVolume(self):
		pos = self.ctrlMusicVolume.GetSliderPos()
		snd.SetMusicVolume(pos * net.GetFieldMusicVolume())
		systemSetting.SetMusicVolume(pos)
	def __OnChangeMusic(self, fileName):
		self.selectMusicFile.SetText(fileName[:MUSIC_FILENAME_MAX_LEN])
		if musicInfo.fieldMusic != "":
			snd.FadeOutMusic("BGM/"+ musicInfo.fieldMusic)
		if fileName==uiSelectMusic.DEFAULT_THEMA:
			musicInfo.fieldMusic=musicInfo.METIN2THEMA
		else:
			musicInfo.fieldMusic=fileName
		musicInfo.SaveLastPlayFieldMusic()
		if musicInfo.fieldMusic != "":
			snd.FadeInMusic("BGM/" + musicInfo.fieldMusic)
	def __OnClickChangeMusicButton(self):
		self.selectMusicButton.SetUp()
		if not self.musicListDlg:
			self.musicListDlg=uiSelectMusic.FileListDialog()
			self.musicListDlg.SAFE_SetSelectEvent(self.__OnChangeMusic)
		self.musicListDlg.Open()
	# Music - Mode

	# Camera - Mode
	def RefreshCameraMode(self):
		index = constInfo.GET_CAMERA_MAX_DISTANCE_INDEX()
		self.cameraModeButtonList[index].Down()
		self.cameraModeButtonList[not index].SetUp()
	def __OnClickCameraMode(self):
		constInfo.SET_CAMERA_MAX_DISTANCE_INDEX(not constInfo.GET_CAMERA_MAX_DISTANCE_INDEX())
		self.RefreshCameraMode()
	# Camera - Mode

	# Fog - Mode
	def RefreshFog(self):
		self.__ClickRadioButton(self.fogModeButtonList, constInfo.GET_FOG_LEVEL_INDEX())
	def __OnClickFog(self, index):
		constInfo.SET_FOG_LEVEL_INDEX(index)
		self.RefreshFog()
	# Fog - Mode

	# Night Mode - Mode
	def RefreshNightMode(self):
		if len(self.nightModeButtonList) >= 2:
			if hasattr(systemSetting, 'GetNightModeOption'):
				# nightModeButtonList[0] = night_mode_on (ON), nightModeButtonList[1] = night_mode_off (OFF)
				# True = ON (index 0), False = OFF (index 1)
				nightModeValue = systemSetting.GetNightModeOption()
				index = 0 if nightModeValue else 1
				self.nightModeButtonList[index].Down()
				self.nightModeButtonList[1 - index].SetUp()
				# Apply the visual effect by calling background module
				if hasattr(background, 'SetNightModeOption'):
					background.SetNightModeOption(nightModeValue)
	def __OnClickNightMode(self):
		if hasattr(systemSetting, 'SetNightModeOption') and hasattr(systemSetting, 'GetNightModeOption'):
			# Toggle the night mode option
			newValue = not systemSetting.GetNightModeOption()
			systemSetting.SetNightModeOption(newValue)
			# Apply the visual effect by calling background module
			if hasattr(background, 'SetNightModeOption'):
				background.SetNightModeOption(newValue)
			self.RefreshNightMode()
	# Night Mode - Mode

	# Snow Mode - Mode
	def RefreshSnowMode(self):
		if len(self.snowModeButtonList) >= 2:
			if hasattr(systemSetting, 'GetSnowModeOption'):
				# snowModeButtonList[0] = snow_mode_on (ON), snowModeButtonList[1] = snow_mode_off (OFF)
				# True = ON (index 0), False = OFF (index 1)
				index = 0 if systemSetting.GetSnowModeOption() else 1
				self.snowModeButtonList[index].Down()
				self.snowModeButtonList[1 - index].SetUp()
	def __OnClickSnowMode(self):
		if hasattr(systemSetting, 'SetSnowModeOption') and hasattr(systemSetting, 'GetSnowModeOption'):
			# Toggle the snow mode option
			systemSetting.SetSnowModeOption(not systemSetting.GetSnowModeOption())
			self.RefreshSnowMode()
	# Snow Mode - Mode

	# Snow Texture Mode - Mode
	def RefreshSnowTextureMode(self):
		if len(self.snowTextureModeButtonList) >= 2:
			if hasattr(systemSetting, 'GetSnowTextureModeOption'):
				# snowTextureModeButtonList[0] = snow_texture_mode_on (ON), snowTextureModeButtonList[1] = snow_texture_mode_off (OFF)
				# True = ON (index 0), False = OFF (index 1)
				index = 0 if systemSetting.GetSnowTextureModeOption() else 1
				self.snowTextureModeButtonList[index].Down()
				self.snowTextureModeButtonList[1 - index].SetUp()
	def __OnClickSnowTextureMode(self):
		if hasattr(systemSetting, 'SetSnowTextureModeOption') and hasattr(systemSetting, 'GetSnowTextureModeOption'):
			# Toggle the snow texture mode option
			systemSetting.SetSnowTextureModeOption(not systemSetting.GetSnowTextureModeOption())
			self.RefreshSnowTextureMode()
	# Snow Texture Mode - Mode

	# ENB Mode - Mode
	def RefreshENBMode(self):
		if len(self.enbModeButtonList) >= 2:
			if hasattr(systemSetting, 'IsENBModeStatus'):
				index = 1 if systemSetting.IsENBModeStatus() else 0
				self.enbModeButtonList[index].Down()
				self.enbModeButtonList[not index].SetUp()
	def __OnClickENBMode(self):
		if hasattr(systemSetting, 'SetENBModeStatusFlag') and hasattr(systemSetting, 'IsENBModeStatus'):
			systemSetting.SetENBModeStatusFlag(not systemSetting.IsENBModeStatus())
			self.RefreshENBMode()
	# ENB Mode - Mode

	# Effect Level - Mode
	def RefreshEffectLevel(self):
		if len(self.effectLevelButtonList) >= 5:
			if hasattr(systemSetting, 'GetEffectLevel'):
				level = systemSetting.GetEffectLevel()
				if level >= 1 and level <= 5:
					self.effectLevel = level - 1
					self.__ClickRadioButton(self.effectLevelButtonList, level - 1)
	def __OnClickEffectLevel(self, index):
		if not self.effectLevelButtonList or index < 0 or index >= len(self.effectLevelButtonList):
			return
		self.effectLevel = index
		self.__ClickRadioButton(self.effectLevelButtonList, index)
	def __OnClickEffectApplyButton(self):
		if hasattr(systemSetting, 'SetEffectLevel'):
			systemSetting.SetEffectLevel(self.effectLevel + 1)
			self.RefreshEffectLevel()
	# Effect Level - Mode

	# Private Shop Level - Mode
	def RefreshPrivateShopLevel(self):
		if len(self.privateShopLevelButtonList) >= 5:
			if hasattr(systemSetting, 'GetPrivateShopLevel'):
				level = systemSetting.GetPrivateShopLevel()
				if level >= 1 and level <= 5:
					self.privateShopLevel = level - 1
					self.__ClickRadioButton(self.privateShopLevelButtonList, level - 1)
	def __OnClickPrivateShopLevel(self, index):
		if not self.privateShopLevelButtonList or index < 0 or index >= len(self.privateShopLevelButtonList):
			return
		self.privateShopLevel = index
		self.__ClickRadioButton(self.privateShopLevelButtonList, index)
	def __OnClickPrivateShopApplyButton(self):
		if hasattr(systemSetting, 'SetPrivateShopLevel'):
			systemSetting.SetPrivateShopLevel(self.privateShopLevel + 1)
			self.RefreshPrivateShopLevel()
	# Private Shop Level - Mode

	# Drop Item Level - Mode
	def RefreshDropItemLevel(self):
		if len(self.dropItemLevelButtonList) >= 5:
			if hasattr(systemSetting, 'GetDropItemLevel'):
				level = systemSetting.GetDropItemLevel()
				if level >= 1 and level <= 5:
					self.dropItemLevel = level - 1
					self.__ClickRadioButton(self.dropItemLevelButtonList, level - 1)
	def __OnClickDropItemLevel(self, index):
		self.dropItemLevel = index
		self.__ClickRadioButton(self.dropItemLevelButtonList, index)
	def __OnClickDropItemApplyButton(self):
		if hasattr(systemSetting, 'SetDropItemLevel'):
			systemSetting.SetDropItemLevel(self.dropItemLevel + 1)
			self.RefreshDropItemLevel()
	# Drop Item Level - Mode

	# Pet Status - Mode
	def RefreshPetStatus(self):
		if len(self.petStatusButtonList) >= 2:
			if hasattr(systemSetting, 'IsPetStatus'):
				index = 1 if systemSetting.IsPetStatus() else 0
				self.petStatusButtonList[index].Down()
				self.petStatusButtonList[not index].SetUp()
	def __OnClickPetStatus(self):
		if hasattr(systemSetting, 'SetPetStatusFlag') and hasattr(systemSetting, 'IsPetStatus'):
			systemSetting.SetPetStatusFlag(not systemSetting.IsPetStatus())
			self.RefreshPetStatus()
	# Pet Status - Mode

	# NPC Name Status - Mode
	def RefreshNpcNameStatus(self):
		if len(self.npcNameStatusButtonList) >= 2:
			if hasattr(systemSetting, 'IsNpcNameStatus'):
				index = 1 if systemSetting.IsNpcNameStatus() else 0
				self.npcNameStatusButtonList[index].Down()
				self.npcNameStatusButtonList[not index].SetUp()
	def __OnClickNpcNameStatus(self):
		if hasattr(systemSetting, 'SetNpcNameStatusFlag') and hasattr(systemSetting, 'IsNpcNameStatus'):
			systemSetting.SetNpcNameStatusFlag(not systemSetting.IsNpcNameStatus())
			self.RefreshNpcNameStatus()
	# NPC Name Status - Mode

	# Show Mob Level - Mode
	def RefreshShowMobLevel(self):
		if self.showMobLevelButtonList:
			if hasattr(systemSetting, 'IsShowMobLevel'):
				if systemSetting.IsShowMobLevel():
					self.showMobLevelButtonList.Down()
					self.showMobLevelButtonList.SetUp()
				else:
					self.showMobLevelButtonList.SetUp()
					self.showMobLevelButtonList.Down()
	def __OnClickShowMobLevel(self):
		if hasattr(systemSetting, 'SetShowMobLevel') and hasattr(systemSetting, 'IsShowMobLevel'):
			systemSetting.SetShowMobLevel(not systemSetting.IsShowMobLevel())
			self.RefreshShowMobLevel()
	# Show Mob Level - Mode

	# Show Mob AI Flag - Mode
	def RefreshShowMobAIFlag(self):
		if self.showMobAIFlagButtonList:
			if hasattr(systemSetting, 'IsShowMobAIFlag'):
				if systemSetting.IsShowMobAIFlag():
					self.showMobAIFlagButtonList.Down()
					self.showMobAIFlagButtonList.SetUp()
				else:
					self.showMobAIFlagButtonList.SetUp()
					self.showMobAIFlagButtonList.Down()
	def __OnClickShowMobAIFlag(self):
		if hasattr(systemSetting, 'SetShowMobAIFlag') and hasattr(systemSetting, 'IsShowMobAIFlag'):
			systemSetting.SetShowMobAIFlag(not systemSetting.IsShowMobAIFlag())
			self.RefreshShowMobAIFlag()
	# Show Mob AI Flag - Mode

	# FOV Controller - Mode
	def OnChangeFOV(self):
		if self.fovController:
			pos = self.fovController.GetSliderPos()
			if hasattr(app, 'MAX_CAMERA_PERSPECTIVE'):
				fovValue = pos * float(app.MAX_CAMERA_PERSPECTIVE)
			else:
				fovValue = int(pos * 100.0)
			if hasattr(systemSetting, 'SetFOV'):
				systemSetting.SetFOV(fovValue)
	def OnClickFOVReset(self):
		if hasattr(systemSetting, 'SetFOV'):
			if hasattr(app, 'DEFAULT_CAMERA_PERSPECTIVE'):
				defaultFOV = float(app.DEFAULT_CAMERA_PERSPECTIVE)
			else:
				defaultFOV = 90.0
			systemSetting.SetFOV(defaultFOV)
			if self.fovController:
				if hasattr(app, 'MAX_CAMERA_PERSPECTIVE'):
					self.fovController.SetSliderPos(defaultFOV / float(app.MAX_CAMERA_PERSPECTIVE))
				else:
					self.fovController.SetSliderPos(defaultFOV / 100.0)
	# FOV Controller - Mode

	# Stone Scale Controller - Mode
	def OnChangeStoneScale(self):
		if self.stoneScaleController:
			value = self.stoneScaleController.GetSliderPos()
			if hasattr(systemSetting, 'SetStoneScale'):
				systemSetting.SetStoneScale(value)
			# Görsel olarak uygula
			try:
				import background
				if hasattr(background, 'ApplyStoneScale'):
					background.ApplyStoneScale(value)
			except:
				pass
	def OnClickStoneScaleReset(self):
		if hasattr(systemSetting, 'SetStoneScale'):
			systemSetting.SetStoneScale(0)  # Default scale (eski sistemde 0)
			if self.stoneScaleController:
				self.stoneScaleController.SetSliderPos(0)
			# Görsel olarak uygula
			try:
				import background
				if hasattr(background, 'ApplyStoneScale'):
					background.ApplyStoneScale(0)
			except:
				pass
	# Stone Scale Controller - Mode

	# Pickup - Mode
	def __SendPickupModeCommand(self):
		try:
			import constInfo
			net.SendChatPacket("/setpickupmode %d" % (constInfo.PICKUPMODE))
		except:
			pass

	def __OnClickPickupModeButton(self):
		"""Eski sistem gibi - sadece PICKUPMODE'u toggle et ve RefreshPickUP'ý çaðýr"""
		try:
			import constInfo
			# PICKUPMODE'u toggle et
			if 0 != (constInfo.PICKUPMODE & (1 << 0)):
				constInfo.PICKUPMODE -= (1 << 0)
			else:
				constInfo.PICKUPMODE |= (1 << 0)
			
			self.__SendPickupModeCommand()
			# RefreshPickUP'ý çaðýr - button durumlarý ve premium status text'i güncellenecek
			self.RefreshPickUP()
		except Exception, e:
			import dbg
			dbg.TraceError("__OnClickPickupModeButton error: %s" % str(e))

	def OnChangePickUPMode(self):
		"""Server'dan gelen PickUPMode komutu için çaðrýlýr"""
		self.RefreshPickUP()

	def __OnClickPickupIgnoreButton(self, type, ignore):
		try:
			import constInfo
			if ignore:
				constInfo.PICKUPMODE += type
			else:
				constInfo.PICKUPMODE -= type
			self.__SendPickupModeCommand()
			self.RefreshPickUP()
		except:
			pass

	def RefreshPickUP(self):
		try:
			import constInfo
			# Premium status text'i tekrar yükle (eðer henüz yüklenmemiþse)
			if not self.pickupPremiumStatusText:
				try:
					# optionWindow5'i al
					if self.children.has_key("optionWindow5"):
						optionWindow = self.children["optionWindow5"]
						GetObject = optionWindow.GetChild
						pickupPremiumImage = GetObject("pickup_premimum_image")
						if pickupPremiumImage:
							pickupPremiumStatusText = pickupPremiumImage.GetChild("pickup_premium_status_text")
							if pickupPremiumStatusText:
								self.pickupPremiumStatusText = pickupPremiumStatusText
				except:
					pass

			if len(self.mainPickModeButtonList) >= 2:
				# Aktif butonu (index 0) ve Devre Dýþý butonu (index 1)
				if 0 != (constInfo.PICKUPMODE & (1 << 0)):
					# Aktif durumda
					self.mainPickModeButtonList[0].Down()  # Aktif butonu aktif
					self.mainPickModeButtonList[1].SetUp()  # Devre Dýþý butonu pasif
				else:
					# Devre Dýþý durumda
					self.mainPickModeButtonList[0].SetUp()  # Aktif butonu pasif
					self.mainPickModeButtonList[1].Down()  # Devre Dýþý butonu aktif

			for i in xrange(1, 12):
				if i-1 < len(self.mainPickUPButtonList):
					if 0 != (constInfo.PICKUPMODE & (1 << i)):
						self.mainPickUPButtonList[i-1].Down()
					else:
						self.mainPickUPButtonList[i-1].SetUp()

			if self.pickupPremiumStatusText:
				try:
					import app
					import uiScriptLocale
					# Eski sistem gibi - sadece PREMIUMMODE kontrolü yap
					if hasattr(constInfo, 'PREMIUMMODE') and len(constInfo.PREMIUMMODE) >= 2:
						if constInfo.PREMIUMMODE[0] == False or constInfo.PREMIUMMODE[0] == 0:
							self.pickupPremiumStatusText.SetText(uiScriptLocale.AUTO_PICKUP_PREMIUM_STATUS_OFF)
						else:
							# Premium aktif - kalan süreyi göster
							remainingTime = constInfo.PREMIUMMODE[1] - app.GetGlobalTimeStamp()
							if remainingTime > 0:
								m, s = divmod(remainingTime, 60)
								h, m = divmod(m, 60)
								d, h = divmod(h, 24)
								if d > 0:
									timeStr = "%dd %dh %dm %ds" % (d, h, m, s)
								elif h > 0:
									timeStr = "%dh %dm %ds" % (h, m, s)
								elif m > 0:
									timeStr = "%dm %ds" % (m, s)
								else:
									timeStr = "%ds" % (s)
								self.pickupPremiumStatusText.SetText(uiScriptLocale.AUTO_PICKUP_PREMIUM_STATUS_ON % timeStr)
							else:
								# Premium süresi dolmuþ
								self.pickupPremiumStatusText.SetText(uiScriptLocale.AUTO_PICKUP_PREMIUM_STATUS_OFF)
					else:
						# PREMIUMMODE yok - Devre Dýþý göster
						self.pickupPremiumStatusText.SetText(uiScriptLocale.AUTO_PICKUP_PREMIUM_STATUS_OFF)
					self.pickupPremiumStatusText.Show()
				except Exception, e:
					try:
						# Fallback: Devre Dýþý göster
						import uiScriptLocale
						self.pickupPremiumStatusText.SetText(uiScriptLocale.AUTO_PICKUP_PREMIUM_STATUS_OFF)
						self.pickupPremiumStatusText.Show()
					except:
						pass
			else:
				# Eðer text henüz yüklenmemiþse, tekrar yüklemeyi dene
				try:
					if self.children.has_key("optionWindow5"):
						optionWindow = self.children["optionWindow5"]
						GetObject = optionWindow.GetChild
						pickupPremiumImage = GetObject("pickup_premimum_image")
						if pickupPremiumImage:
							pickupPremiumStatusText = pickupPremiumImage.GetChild("pickup_premium_status_text")
							if pickupPremiumStatusText:
								self.pickupPremiumStatusText = pickupPremiumStatusText
								import uiScriptLocale
								pickupPremiumStatusText.SetText(uiScriptLocale.AUTO_PICKUP_PREMIUM_STATUS_OFF)
								pickupPremiumStatusText.Show()
				except:
					pass
		except:
			pass
	# Pickup - Mode

class ScrollBarNew(ui.Window):
	SCROLLBAR_WIDTH = 7
	SCROLL_BTN_XDIST = 1
	SCROLL_BTN_YDIST = 1
	class MiddleBar(ui.DragButton):
		def __init__(self):
			ui.DragButton.__init__(self)
			self.AddFlag("movable")
			self.SetWindowName("scrollbar_middlebar")
		def MakeImage(self):
			top = ui.ExpandedImageBox()
			top.SetParent(self)
			top.LoadImage(IMG_DIR+"scrollbar/scrollbar_top.tga")
			top.AddFlag("not_pick")
			top.Show()
			topScale = ui.ExpandedImageBox()
			topScale.SetParent(self)
			topScale.SetPosition(0, top.GetHeight())
			topScale.LoadImage(IMG_DIR+"scrollbar/scrollbar_scale.tga")
			topScale.AddFlag("not_pick")
			topScale.Show()
			bottom = ui.ExpandedImageBox()
			bottom.SetParent(self)
			bottom.LoadImage(IMG_DIR+"scrollbar/scrollbar_bottom.tga")
			bottom.AddFlag("not_pick")
			bottom.Show()
			bottomScale = ui.ExpandedImageBox()
			bottomScale.SetParent(self)
			bottomScale.LoadImage(IMG_DIR+"scrollbar/scrollbar_scale.tga")
			bottomScale.AddFlag("not_pick")
			bottomScale.Show()
			middle = ui.ExpandedImageBox()
			middle.SetParent(self)
			middle.LoadImage(IMG_DIR+"scrollbar/scrollbar_mid.tga")
			middle.AddFlag("not_pick")
			middle.Show()
			self.top = top
			self.topScale = topScale
			self.bottom = bottom
			self.bottomScale = bottomScale
			self.middle = middle
		def SetSize(self, height):
			minHeight = self.top.GetHeight() + self.bottom.GetHeight() + self.middle.GetHeight()
			height = max(minHeight, height)
			ui.DragButton.SetSize(self, 10, height)
			scale = (height - minHeight) / 2 
			extraScale = 0
			if (height - minHeight) % 2 == 1:
				extraScale = 1
			self.topScale.SetRenderingRect(0, 0, 0, scale - 1)
			self.middle.SetPosition(0, self.top.GetHeight() + scale)
			self.bottomScale.SetPosition(0, self.middle.GetBottom())
			self.bottomScale.SetRenderingRect(0, 0, 0, scale - 1 + extraScale)
			self.bottom.SetPosition(0, height - self.bottom.GetHeight())
	def __init__(self):
		ui.Window.__init__(self)
		self.pageSize = 1
		self.curPos = 0.0
		self.eventScroll = None
		self.eventArgs = None
		self.lockFlag = False
		self.CreateScrollBar()
		self.SetScrollBarSize(0)
		self.scrollStep = 0.4
		self.SetWindowName("NONAME_ScrollBar")
	def __del__(self):
		ui.Window.__del__(self)
	def CreateScrollBar(self):
		topImage = ui.ExpandedImageBox()
		topImage.SetParent(self)
		topImage.AddFlag("not_pick")
		topImage.LoadImage(IMG_DIR+"scrollbar/scroll_top.tga")
		topImage.Show()
		bottomImage = ui.ExpandedImageBox()
		bottomImage.SetParent(self)
		bottomImage.AddFlag("not_pick")
		bottomImage.LoadImage(IMG_DIR+"scrollbar/scroll_bottom.tga")
		bottomImage.Show()
		middleImage = ui.ExpandedImageBox()
		middleImage.SetParent(self)
		middleImage.AddFlag("not_pick")
		middleImage.SetPosition(0, topImage.GetHeight())
		middleImage.LoadImage(IMG_DIR+"scrollbar/scroll_mid.tga")
		middleImage.Show()
		self.topImage = topImage
		self.bottomImage = bottomImage
		self.middleImage = middleImage
		middleBar = self.MiddleBar()
		middleBar.SetParent(self)
		middleBar.SetMoveEvent(ui.__mem_func__(self.OnMove))
		middleBar.Show()
		middleBar.MakeImage()
		middleBar.SetSize(12)
		self.middleBar = middleBar
	def Destroy(self):
		self.eventScroll = None
		self.eventArgs = None
	def SetScrollEvent(self, event, *args):
		self.eventScroll = event
		self.eventArgs = args
	def SetMiddleBarSize(self, pageScale):
		self.middleBar.SetSize(int(pageScale * float(self.GetHeight() - (self.SCROLL_BTN_YDIST*2))))
		realHeight = self.GetHeight() - (self.SCROLL_BTN_YDIST*2) - self.middleBar.GetHeight()
		self.pageSize = realHeight

	def SetScrollBarSize(self, height):
		self.SetSize(self.SCROLLBAR_WIDTH, height)
		self.pageSize = height - self.SCROLL_BTN_YDIST*2 - self.middleBar.GetHeight()
		middleImageScale = float((height - self.SCROLL_BTN_YDIST*2) - self.middleImage.GetHeight()) / float(self.middleImage.GetHeight())
		self.middleImage.SetRenderingRect(0, 0, 0, middleImageScale)
		self.bottomImage.SetPosition(0, height - self.bottomImage.GetHeight())
		self.middleBar.SetRestrictMovementArea(self.SCROLL_BTN_XDIST, self.SCROLL_BTN_YDIST, \
			self.middleBar.GetWidth(), height - self.SCROLL_BTN_YDIST * 2)
		self.middleBar.SetPosition(self.SCROLL_BTN_XDIST, self.SCROLL_BTN_YDIST)
	def SetScrollStep(self, step):
		self.scrollStep = step
	def OnUp(self):
		self.SetPos(self.curPos-self.scrollStep)
	def OnDown(self):
		self.SetPos(self.curPos+self.scrollStep)
	def GetScrollStep(self):
		return self.scrollStep
	def GetPos(self):
		return self.curPos
	def OnUp(self):
		self.SetPos(self.curPos-self.scrollStep)
	def OnDown(self):
		self.SetPos(self.curPos+self.scrollStep)
	def SetPos(self, pos, moveEvent = True):
		pos = max(0.0, pos)
		pos = min(1.0, pos)
		newPos = float(self.pageSize) * pos
		self.middleBar.SetPosition(self.SCROLL_BTN_XDIST, int(newPos) + self.SCROLL_BTN_YDIST)
		if moveEvent == True:
			self.OnMove()
	def OnMove(self):
		if self.lockFlag:
			return
		if 0 == self.pageSize:
			return
		(xLocal, yLocal) = self.middleBar.GetLocalPosition()
		self.curPos = float(yLocal - self.SCROLL_BTN_YDIST) / float(self.pageSize)
		if self.eventScroll:
			apply(self.eventScroll, self.eventArgs)
	def OnMouseLeftButtonDown(self):
		(xMouseLocalPosition, yMouseLocalPosition) = self.GetMouseLocalPosition()
		newPos = float(yMouseLocalPosition) / float(self.GetHeight())
		self.SetPos(newPos)
	def LockScroll(self):
		self.lockFlag = True
	def UnlockScroll(self):
		self.lockFlag = False
