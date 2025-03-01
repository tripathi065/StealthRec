from main import main
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.core.window import Window
from kivymd.app import MDApp
from kivymd.uix.snackbar import Snackbar
from kivy.properties import StringProperty

KV = """
ScreenManager:
    EntryScreen:
    ProfileScreen:
    RecordingScreen:

<EntryScreen>:
    name: "entry"

    FloatLayout:
        Image:
            source: "background.png"  # Background only for the Entry Screen
            allow_stretch: True
            keep_ratio: False
            size_hint: 1, 1
            pos_hint: {"center_x": 0.5, "center_y": 0.5}

        MDRaisedButton:
            text: "Get Started"
            size_hint: None, None
            size: dp(150), dp(50)
            pos_hint: {"center_x": 0.5, "center_y": 0.35}  
            md_bg_color: 1, 0.3, 0, 1  # Orange button
            on_release: app.root.current = "profile"

<ProfileScreen>:
    name: "profile"

    BoxLayout:
        orientation: "vertical"
        padding: dp(20)
        spacing: dp(20)
        size_hint: 0.85, None
        height: dp(400)
        pos_hint: {"center_x": 0.5, "center_y": 0.5}  # CENTERED

        MDLabel:
            text: "Setup Your Profile"
            theme_text_color: "Primary"
            halign: "center"
            font_style: "H5"
            size_hint_y: None
            height: dp(40)

        MDTextField:
            id: activation_word
            hint_text: "Enter Start Code Word"
            icon_right: "key"
            mode: "rectangle"

        MDTextField:
            id: deactivation_word
            hint_text: "Enter End Code Word"
            icon_right: "lock"
            mode: "rectangle"

        MDTextField:
            id: emergency_contact
            hint_text: "Enter Emergency Number"
            icon_right: "phone"
            input_filter: "int"
            mode: "rectangle"

        MDRaisedButton:
            text: "Save Profile"
            size_hint: None, None
            size: dp(160), dp(50)
            pos_hint: {"center_x": 0.5}
            md_bg_color: 1, 0.3, 0, 1  
            on_release: root.save_profile(activation_word.text, deactivation_word.text, emergency_contact.text)

        MDRaisedButton:
            text: "Back"
            size_hint: None, None
            size: dp(120), dp(40)
            pos_hint: {"center_x": 0.5}
            md_bg_color: 0.2, 0.2, 0.2, 1  
            on_release: app.root.current = "entry"

<RecordingScreen>:
    name: "recording"

    BoxLayout:
        orientation: "vertical"
        padding: dp(20)
        spacing: dp(20)
        size_hint: 0.85, None
        height: dp(400)
        pos_hint: {"center_x": 0.5, "center_y": 0.5}

        MDLabel:
            text: "Recording Status"
            theme_text_color: "Primary"
            halign: "center"
            font_style: "H5"
            size_hint_y: None
            height: dp(40)

        MDLabel:
            text: root.status
            theme_text_color: "Secondary"
            halign: "center"
            size_hint_y: None
            height: dp(40)

        MDRaisedButton:
            text: "Stop Recording"
            size_hint: None, None
            size: dp(160), dp(50)
            pos_hint: {"center_x": 0.5}
            md_bg_color: 1, 0.3, 0, 1  
            on_release: root.stop_recording()
"""

class EntryScreen(Screen):
    pass

class ProfileScreen(Screen):
    start_command = ""
    stop_command = ""
    sen_number = ""

    def save_profile(self, start_command, stop_command, sen_number):
        if not start_command or not stop_command or not sen_number:
            Snackbar(text="Please fill all fields").open()
            return

        self.start_command = start_command
        self.stop_command = stop_command
        self.sen_number = sen_number

        try:
            main(start_command, stop_command, sen_number)
            Snackbar(text="Profile saved and backend started!").open()

            # Switch to RecordingScreen
            self.manager.get_screen("recording").status = "Waiting for command to start recording..."
            self.manager.current = "recording"
        except Exception as e:
            Snackbar(text=f"Error starting backend: {e}").open()

class RecordingScreen(Screen):
    status = StringProperty("Waiting for command to start recording...")

    def stop_recording(self):
        # Logic to stop the recording or handle backend interaction
        self.status = "Recording stopped!"
        Snackbar(text="Recording has been stopped.").open()

class StealthRec(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Orange"
        Window.size = (360, 640)  # Mobile screen size simulation
        return Builder.load_string(KV)

if __name__ == "__main__":
    StealthRec().run()
