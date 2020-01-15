from objc_util import ObjCClass, nsurl, ObjCInstance, uiimage_to_png, UIImage
from PIL import Image
import ui, dialogs, clipboard

LSApplicationWorkspace = ObjCClass('LSApplicationWorkspace')
workspace = LSApplicationWorkspace.defaultWorkspace()
LSApplicationProxy = ObjCClass('LSApplicationProxy')
	
class App (object):
	def __init__(self, app):
		try:
			app.applicationIdentifier()
		except AttributeError:
			raise AttributeError('{0} is not an app ObjC Class'.format(app))
		self.objc = app
	
	@property
	def name(self):
		return str(self.objc.localizedName())
		
	@property
	def nameForSort(self):
		return str(self.objc.localizedName()).lower()
		
	@property
	def appID(self):
		return str(self.objc.applicationIdentifier())
		
	@property
	def icon(self, scale=2.0, form=10):	
		i = UIImage._applicationIconImageForBundleIdentifier_format_scale_(self.appID, form, scale)
		o = ObjCInstance(i.akCGImage())
		img = UIImage.imageWithCGImage_(o)
		return uiimage_to_png(img)
		
	@property
	def schemes(self):
		"""Set's the info.plist for an app"""
		returns = []
		#return self.objc._infoDictionary().propertyList().objectForKey_('CFBundleURLTypes')[0].objectForKey_('CFBundleURLSchemes')[0]
		try:
			u = self.objc._infoDictionary().propertyList().objectForKey_('CFBundleURLTypes')
			for x in u:
				for y in x.objectForKey_('CFBundleURLSchemes'):
					if str(y) != 'prefs':
						returns += [str(y).lower()+'://']
			return returns
		except:
			return []
			
	def __str__(self):
		return self.name
		
	def __repr__(self):
		# return '<' + self.appID + '>'
		return self.name
		
class TableViewDelegate(object):
	def tableview_did_select(self, tableview, section):
		# Called when a row was selected.
		selected = self.selected_row[1]
		list = self.data_source.items[selected]['app'].schemes
		data = ui.ListDataSource(list)
		
		table_push = ui.TableView()
		table_push.name = self.data_source.items[selected]['app'].name
		table_push.data_source = data
		table_push.delegate = DetailTableViewDelegate
		self.navigation_view.push_view(table_push)
		self.reload()
		
class DetailTableViewDelegate(object):
	def tableview_did_select(self, tableview, section):
		# Called when a row was selected.
		selected = self.selected_row[1]
		item = self.data_source.items[selected]
		clipboard.set(item)
		dialogs.hud_alert(item+' Copied')
		self.reload()
	
def _urlHandle(url):
	if not isinstance(url, ObjCInstance):
		return nsurl(url)
	return url if url.isKindOfClass_(ObjCClass('NSURL')) else None
		
def getAppsOfUserOnly():
	results = []
	for app in workspace.applicationsOfType_(0):
		results += [App(app)]
	return results
	
def findApp(Sender):
	returns = []
	input = dialogs.input_alert('Input Keyword')
	for i in items:
		if i['title'].lower().find(input.lower()) != -1:
			returns += [i]
	table.data_source.items = returns
	
def refreshApp(Sender):
	table.data_source.items = items
	
if __name__ == '__main__':
	apps = getAppsOfUserOnly()
	list = sorted(apps, key = lambda x: x.nameForSort, reverse = False)
	items = []
	for i in list:
		items += [{'title': i.name, 'image': ui.Image.from_data(i.icon), 'app': i}]
	data = ui.ListDataSource(items)
	
	table = ui.TableView()
	table.name = 'All Apps'
	table.data_source = data
	table.right_button_items = [ui.ButtonItem(image=ui.Image.named('iob:ios7_refresh_empty_32'), action=refreshApp), ui.ButtonItem(image=ui.Image.named('iob:ios7_search_24'), action=findApp)]


	table.delegate = TableViewDelegate
		
	navigation = ui.NavigationView(table)
	navigation.name = 'URL Schemes Viewer'
	navigation.tint_color = 'black'
	navigation.present('fullscreen')
