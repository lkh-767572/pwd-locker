from gui import Gui, Popup

if __name__ == "__main__":

	app = Gui("PWD-Locker")

	# Popup Error Window
	if app.ERROR == True:
		Popup(app.ERROR_TEXT)
		app.ERROR = False
