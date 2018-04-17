# -*- coding: UTF-8 -*-
import gtk
from os import listdir
from tempfile import mkstemp
from shutil import move
from os import remove, close
import gtk.gtkgl
from subprocess import call


class FileIO():
    """A static class used for simplifying file IO operations"""

    @staticmethod
    def replace(file_path, pattern, subst):
        """Replaces a single line in a file"""

        fh, abs_path = mkstemp()
        with open(abs_path, 'w') as new_file:
            with open(file_path) as old_file:
                for line in old_file:
                    new_file.write(line.replace(pattern, subst))
        close(fh)
        remove(file_path)
        move(abs_path, file_path)


class FontFetcher:
    """A static class used for accessing fonts"""

    @staticmethod
    def fetchAllFonts():
        """Gets every usable font on the system"""

        FONT_PATH = "/usr/share/fonts/TTF"
        fonts = listdir(FONT_PATH)
        for f in fonts:
            if not f.lower().endswith('.ttf'):
                fonts.remove(f)
        return fonts


class MainWindow:
    def __init__(self):
        # Create window, set its properties and connect signals
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.connect("delete_event", self.delete_event)
        self.window.connect("destroy", self.destroy)
        self.window.set_title("BlenderTextGenerator")
        self.window.set_border_width(10)

        # Create a hBox which would allow parallel using of settings
        # and openGL view
        self.hBox = gtk.HBox(True, 5)
        self.window.add(self.hBox)

        # Create a vBox to hold all of the settings' controls
        self.vBox = gtk.VBox(True, 5)
        self.hBox.add(self.vBox)

        # Create textbox
        self.textEditFrame = gtk.Frame("Enter Text:")
        self.textEditEntry = gtk.Entry(16)
        self.textEditFrame.add(self.textEditEntry)

        # Create a font selector
        self.fontSelectFrame = gtk.Frame("Select Font:")
        self.fontSelectComboBox = gtk.combo_box_new_text()
        for f in FontFetcher.fetchAllFonts():
            self.fontSelectComboBox.append_text(f)
        self.fontSelectFrame.add(self.fontSelectComboBox)

        # Create a hBox to hold the number settings
        self.numberValuesHBox = gtk.HBox(True, 5)

        # Create an entry for the text height setting
        self.textHeightFrame = gtk.Frame("Height")
        self.textHeightEntry = gtk.Entry(4)
        self.textHeightFrame.add(self.textHeightEntry)

        # Create an entry for the base height setting
        self.baseHeightFrame = gtk.Frame("Base Height")
        self.baseHeightEntry = gtk.Entry(4)
        self.baseHeightFrame.add(self.baseHeightEntry)

        # Create an entry for the base height setting
        self.paddingFrame = gtk.Frame("Padding")
        self.paddingEntry = gtk.Entry(4)
        self.paddingFrame.add(self.paddingEntry)

        # Add all of the number entries to the numberValuesHBox
        self.numberValuesHBox.pack_start(self.textHeightFrame)
        self.numberValuesHBox.add(self.baseHeightFrame)
        self.numberValuesHBox.add(self.paddingFrame)

        # Create a button for creating the model and connect the signal
        self.createButton = gtk.Button("Create")
        self.createButton.connect("clicked", self.createModel)

        # Fill the vBox with the settings
        self.vBox.pack_start(self.textEditFrame)
        self.vBox.add(self.fontSelectFrame)
        self.vBox.add(self.numberValuesHBox)
        self.vBox.add(self.createButton)

        # Show all elements
        self.hBox.show()
        self.vBox.show()
        self.textEditFrame.show()
        self.textEditEntry.show()
        # TODO: self.fontSelectFrame.show()
        self.fontSelectComboBox.show()
        self.numberValuesHBox.show()
        self.textHeightFrame.show()
        self.textHeightEntry.show()
        self.baseHeightFrame.show()
        self.baseHeightEntry.show()
        self.paddingFrame.show()
        self.paddingEntry.show()
        self.createButton.show()
        self.window.show()

    def main(self):
        gtk.main()

    def delete_event(self, widget, event, data=None):
        return False

    def destroy(self, widget, data=None):
        gtk.main_quit()

    def createModel(self, widget, data=None):
        try:
            float(self.textHeightEntry.get_text())
            float(self.baseHeightEntry.get_text())
            float(self.paddingEntry.get_text())

            call(['blender', '-b', '-P', 'BlenderSup.py', '--',
                  '-t', self.textEditEntry.get_text(),
                  '-e', self.textHeightEntry.get_text(),
                  '-b', self.baseHeightEntry.get_text(),
                  '-p', self.paddingEntry.get_text()])
        except ValueError:
            message = gtk.MessageDialog(parent=None,
                                        flags=0,
                                        type=gtk.MESSAGE_WARNING,
                                        buttons=gtk.BUTTONS_OK,
                                        message_format=None)
            message.set_markup('Invalid values entered')
            message.run()
            message.destroy()


if __name__ == "__main__":
    mainWindow = MainWindow()
    mainWindow.main()
