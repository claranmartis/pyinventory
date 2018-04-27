from kivy.app import App
from kivy.graphics import Color, Rectangle
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.image import AsyncImage
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.screenmanager import ScreenManager, Screen

import pymysql
import datetime
import os
from backend import models
from backend.utils import messagebox


class AddEmployee(FloatLayout):
    title = 'KAKABOKA'
    manufacturer_filled = ""
    quantity_prefilled = 0

    def __init__(self):
        super(AddEmployee, self).__init__()
        try:
            
            root = self
            root.bind(size=self._update_rect, pos=self._update_rect)


            # Name label
            label_bar = Label(text='Employee Name',
                              color=(0, 0, 0, 0.25),
                              font_size=20,
                              pos_hint={'center_x': 0.175, 'center_y': 0.8})
            root.add_widget(label_bar)



            # text box for Name
            self.name = TextInput(multiline=False,
                                     pos_hint={'center_x': 0.5, 'center_y': 0.8},
                                     size_hint=(0.5, 0.075),
                                     on_text_validate=self.fetch)

            self.fetch_btn = Button(text="Fetch",
                                    pos_hint={"center_x": 0.84, 'center_y': 0.8},
                                    size_hint=(.15, .07),
                                    on_press=self.fetch
                                    )

            def on_text(instance, value):
                # use try to check if value in database
                self.employee = self.name.text

            self.name.bind(text=on_text)
            root.add_widget(self.name)
            root.add_widget(self.fetch_btn)
            

            # company name
            self.company = Button(text='KAKABOKA',
                                  color=(0, 0, 0, 1),
                                  background_color=(0, 0, 0, 0),
                                  font_size=30,
                                  size_hint=(.25, .07),
                                  pos_hint={'center_x': 0.12, 'center_y': 0.95})
            root.add_widget(self.company)

            # Done button
            donebtn = Button(text='Done',
                             size_hint=(0.2, 0.15),
                             pos_hint={'center_x': 0.5, 'center_y': 0.2})

            def callback2(instance):
                print("Callback 2")

            donebtn.bind(on_press=self.addItem)
            root.add_widget(donebtn)

            with root.canvas.before:
                base_folder = os.path.dirname(__file__)
                image_path = os.path.join(base_folder, 'background.png')
                self.rect = Rectangle(source=image_path, size=root.size, pos=root.pos)
                # return root
        except:
            messagebox(message="Category Not provided", title="Error!")

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def addItem(self, event):
        try:
            name = self.name.text

            if len(name) == 0:
                messagebox(title="Oops!", message="Please enter a Name")
                return

            item = models.Employee(name=name)
            saved = item.save(insert=True)
            
            if saved == 1:
                messagebox(title="Success", message="Name {} added successfully".format(name))
                self.name.text = ""                
            else:
                messagebox(title="Failed", message="Could not add {}".format(name))
                
        except ValueError:
            messagebox(title="Warning", message="Error")
        except pymysql.err.IntegrityError:
            self.addName_cascade()

    def addName_cascade(self):
        try:
            name = self.name.text
            item = models.Employee(name=name)
            saved = item.save(update=True)
            if saved == 1 or saved == 0:
                popup = Popup(title='Success',
                              content=Label(text="Name {} updated successfully".format(name)),
                              size_hint=(None, None), size=(400, 400))
                popup.open()
                self.name.text = ""
            else:
                messagebox(title="Failed", message="Name {} already exists".format(name))
        except ValueError:
            messagebox(title="Warning", message="Error")
        except AttributeError:
            messagebox(title="Oops!", message="Seems like the name is already present in the database.")

    def fetch(self, event):

        name = self.name.text
        if len(name) == 0:
            messagebox(title="Failed", message="Please enter a name to fetch details")
            return
        employee_db = models.Employee(name)
        record = employee_db.getEmployeeName_givenName(name)
        if record == []:
            messagebox(title="Failed", message="Name does not exist")
            return
        record = record[0]
        print(record)

        #self.id = record.id
        #self.name.text = record.name


class AddNameApp(App):
    def build(self):
        return AddName()


if __name__ == '__main__':
    AddNameApp().run()
