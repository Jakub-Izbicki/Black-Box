import kivy
kivy.require('1.9.1')

from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Label
from kivy.uix.listview import ListItemButton, ListView
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.adapters.dictadapter import DictAdapter


import sqlite3
import re

from TreeStructureModule import Tree_Structure
from DBToolsModule import DBTools

Builder.load_string("""
[CustomListItem@SelectableView+BoxLayout]:
    size_hint_y: None
    height: '50dp'
    BoxLayout:
        orientation: 'vertical'
        ListItemLabel:
            text: ctx.file_name_text
            font_size: '30sp'
            is_selected: ctx.is_selected
        ListItemLabel:
            text: ctx.file_path_text
    Button:
        size_hint_x: None
        width: '100dp'
        text: 'Backup'
    Button:
        size_hint_x: None
        width: '100dp'
        text: 'Remove'

""")

class StudentListButton(ListItemButton):
    pass

class MainLayout(BoxLayout):
    first_txt_input = ObjectProperty()
    last_txt_input = ObjectProperty()
    student_list = ObjectProperty()

    def __init__(self, **kwargs):
        super(MainLayout, self).__init__(**kwargs)

        dbConn = sqlite3.connect(DBTools.itemsDBName)
        dbTools = DBTools(dbConn)
        items_list = dbTools.selectAllItemsDb(dbConn)

        list_item_args_converter = \
            lambda row_index, rec: {'file_name_text': rec['file_name_text'],
                                    'file_path_text': rec['file_path_text'],
                                    'is_selected': rec['is_selected'],
                                    'size_hint_y': None,
                                    'height': 25}
        integers_dict = \
            {str(i): {'file_name_text': i[0], 'is_selected': False, 'file_path_text': i[1]} for i in items_list}


        dict_adapter = DictAdapter(sorted_keys=[str(i) for i in range(len(items_list))],
                                   data=integers_dict,
                                   args_converter=list_item_args_converter,
                                   template='CustomListItem')

        list_view = ListView(adapter=dict_adapter)
        self.add_widget(list_view)

        list_view.adapter.data.extend([{str(i): {'file_name_text': i[0], 'is_selected': False, 'file_path_text': i[1]})

    def submit_student(self):
        new_name = self.first_txt_input.text + ' ' + self.last_txt_input.text
        self.student_list.adapter.data.extend([new_name])
        self.student_list._trigger_reset_populate()


    def delete_student(self):
        if self.student_list.adapter.selection:
            selection = self.student_list.adapter.selection[0].text
            self.student_list.adapter.data.remove(selection)
            self.student_list._trigger_reset_populate()

    def replace_student(self):
        if self.student_list.adapter.selection:
            selection = self.student_list.adapter.selection[0].text
            self.student_list.adapter.data.remove(selection)
            new_name = self.first_txt_input.text + ' ' + self.last_txt_input.text
            self.student_list.adapter.data.extend([new_name])
            self.student_list._trigger_reset_populate()

    def on_file_drop(self, file_path):


        file_path = unicode(file_path, 'utf8')
        item_name = re.findall(r'[^\\]+$', file_path)

        tree_structure = Tree_Structure.generateTreeStructure(file_path)

        dbConn = sqlite3.connect(DBTools.itemsDBName)
        dbTools = DBTools(dbConn)

        # TODO: see if item is a dir or a file
        # TODO: if directory, convert tree structure into BLOB

        dbTools.insertItem(dbConn, item_name[0], file_path, tree_structure)

        dbConn.close()


    def initDB(self):
        dbConn = sqlite3.connect(DBTools.itemsDBName)
        dbTools = DBTools(dbConn)
        dbConn.close()

    def resetDB(self):
        dbConn = sqlite3.connect(DBTools.itemsDBName)
        dbTools = DBTools(dbConn)
        dbTools.resetDB(dbConn)
        dbConn.close()

    def printDB(self):
        dbConn = sqlite3.connect(DBTools.itemsDBName)
        dbTools = DBTools(dbConn)
        dbTools.printItems(dbConn)
        dbConn.close()







class MainScreenApp(App):

    def build(self):
        Window.bind(on_dropfile=MainLayout.on_file_drop)
        return MainLayout()

helloKivy = MainScreenApp()
helloKivy.run()

