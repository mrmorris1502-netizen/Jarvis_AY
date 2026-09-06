#Pydroid run kivy

from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Color, Line, Ellipse, Rectangle
from kivy.metrics import dp
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

import threading
import datetime
import re
import webbrowser
import math


# =========================================================
# SETTINGS
# =========================================================

API_KEY = "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"
MODEL = "gpt-5.6-luna"


# =========================================================
# HUD GRAPHICS
# =========================================================

class HUDBackground(Widget):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.angle = 0

        self.bind(
            size=self.draw_hud,
            pos=self.draw_hud
        )

        Clock.schedule_interval(
            self.animate,
            1 / 30
        )

        Clock.schedule_once(
            self.draw_hud,
            0.2
        )

    def animate(self, dt):

        self.angle += 1

        if self.angle >= 360:
            self.angle = 0

        self.draw_hud()

    def draw_hud(self, *args):

        self.canvas.clear()

        w = self.width
        h = self.height

        cx = w / 2
        cy = h * 0.56

        with self.canvas:

            # =================================================
            # BACKGROUND
            # =================================================

            Color(
                0.005,
                0.012,
                0.02,
                1
            )

            Rectangle(
                pos=(0, 0),
                size=(w, h)
            )

            # =================================================
            # GRID
            # =================================================

            Color(
                0.02,
                0.18,
                0.25,
                0.35
            )

            for x in range(
                0,
                int(w),
                35
            ):

                Line(
                    points=[
                        x, 0,
                        x, h
                    ],
                    width=0.4
                )

            for y in range(
                0,
                int(h),
                35
            ):

                Line(
                    points=[
                        0, y,
                        w, y
                    ],
                    width=0.4
                )

            # =================================================
            # OUTER BORDER
            # =================================================

            Color(
                0.05,
                0.65,
                0.95,
                0.8
            )

            Line(
                rectangle=(
                    dp(15),
                    dp(15),
                    w - dp(30),
                    h - dp(30)
                ),
                width=1.2
            )

            # =================================================
            # TOP LINE
            # =================================================

            Color(
                1,
                0.2,
                0.05,
                0.8
            )

            Line(
                points=[
                    dp(25),
                    h - dp(55),
                    w - dp(25),
                    h - dp(55)
                ],
                width=1
            )

            # =================================================
            # LEFT PANEL
            # =================================================

            Color(
                0.05,
                0.55,
                0.8,
                0.75
            )

            Line(
                rectangle=(
                    dp(25),
                    h - dp(285),
                    dp(180),
                    dp(145)
                ),
                width=1
            )

            # =================================================
            # RIGHT PANEL
            # =================================================

            Line(
                rectangle=(
                    w - dp(205),
                    h - dp(285),
                    dp(180),
                    dp(145)
                ),
                width=1
            )

            # =================================================
            # CENTRAL REACTOR
            # =================================================

            Color(
                0.05,
                0.55,
                0.9,
                0.7
            )

            Line(
                circle=(
                    cx,
                    cy,
                    dp(175)
                ),
                width=1.5
            )

            Color(
                1,
                0.18,
                0.03,
                0.9
            )

            Line(
                circle=(
                    cx,
                    cy,
                    dp(125)
                ),
                width=3
            )

            Color(
                0.05,
                0.75,
                1,
                0.8
            )

            Line(
                circle=(
                    cx,
                    cy,
                    dp(145)
                ),
                width=2
            )

            # =================================================
            # ROTATING ARC
            # =================================================

            Color(
                1,
                0.25,
                0.05,
                1
            )

            Line(
                circle=(
                    cx,
                    cy,
                    dp(158),
                    self.angle,
                    self.angle + 65
                ),
                width=dp(5)
            )

            Color(
                0.1,
                0.8,
                1,
                1
            )

            Line(
                circle=(
                    cx,
                    cy,
                    dp(138),
                    -self.angle,
                    -self.angle + 55
                ),
                width=dp(4)
            )

            # =================================================
            # CORE GLOW
            # =================================================

            Color(
                1,
                0.15,
                0.02,
                0.25
            )

            Ellipse(
                pos=(
                    cx - dp(62),
                    cy - dp(62)
                ),
                size=(
                    dp(124),
                    dp(124)
                )
            )

            Color(
                1,
                0.2,
                0.03,
                1
            )

            Ellipse(
                pos=(
                    cx - dp(42),
                    cy - dp(42)
                ),
                size=(
                    dp(84),
                    dp(84)
                )
            )

            Color(
                0.02,
                0.06,
                0.1,
                1
            )

            Ellipse(
                pos=(
                    cx - dp(31),
                    cy - dp(31)
                ),
                size=(
                    dp(62),
                    dp(62)
                )
            )

            # =================================================
            # CORE CROSSHAIR
            # =================================================

            Color(
                0.1,
                0.75,
                1,
                0.7
            )

            Line(
                points=[
                    cx - dp(25),
                    cy,
                    cx + dp(25),
                    cy
                ],
                width=1
            )

            Line(
                points=[
                    cx,
                    cy - dp(25),
                    cx,
                    cy + dp(25)
                ],
                width=1
            )

            # =================================================
            # SIDE CONNECTION LINES
            # =================================================

            Color(
                0.1,
                0.65,
                0.9,
                0.6
            )

            Line(
                points=[
                    dp(205),
                    cy,
                    cx - dp(175),
                    cy
                ],
                width=1
            )

            Line(
                points=[
                    cx + dp(175),
                    cy,
                    w - dp(205),
                    cy
                ],
                width=1
            )

            # =================================================
            # BOTTOM DATA BARS
            # =================================================

            for i in range(9):

                height1 = dp(
                    8 + (i % 5) * 7
                )

                height2 = dp(
                    10 + ((8 - i) % 5) * 6
                )

                Color(
                    0.05,
                    0.65,
                    0.9,
                    0.85
                )

                Rectangle(
                    pos=(
                        dp(25) + i * dp(35),
                        dp(42)
                    ),
                    size=(
                        dp(25),
                        height1
                    )
                )

                Color(
                    1,
                    0.2,
                    0.04,
                    0.85
                )

                Rectangle(
                    pos=(
                        w - dp(340) + i * dp(35),
                        dp(42)
                    ),
                    size=(
                        dp(25),
                        height2
                    )
                )


# =========================================================
# JARVIS APP
# =========================================================

class JarvisApp(App):

    def build(self):

        Window.softinput_mode = "resize"

        self.memory = []

        self.personality = "professional"

        root = FloatLayout()

        # =================================================
        # HUD
        # =================================================

        hud = HUDBackground(
            size_hint=(1, 1)
        )

        root.add_widget(hud)

        # =================================================
        # TITLE
        # =================================================

        title = Label(
            text="J.A.R.V.I.S",
            font_size=30,
            bold=True,
            color=(
                0.1,
                0.8,
                1,
                1
            ),
            size_hint=(None, None),
            size=(
                dp(220),
                dp(50)
            ),
            pos_hint={
                "x": 0.04,
                "top": 0.96
            }
        )

        root.add_widget(title)

        # =================================================
        # ONLINE
        # =================================================

        online = Label(
            text="● ONLINE",
            font_size=13,
            color=(
                0.2,
                1,
                0.4,
                1
            ),
            size_hint=(None, None),
            size=(
                dp(120),
                dp(35)
            ),
            pos_hint={
                "right": 0.96,
                "top": 0.96
            }
        )

        root.add_widget(online)

        # =================================================
        # CLOCK
        # =================================================

        self.clock_label = Label(
            text="00:00:00",
            font_size=21,
            bold=True,
            color=(
                1,
                0.3,
                0.08,
                1
            ),
            size_hint=(None, None),
            size=(
                dp(150),
                dp(40)
            ),
            pos_hint={
                "x": 0.06,
                "top": 0.84
            }
        )

        root.add_widget(
            self.clock_label
        )

        # =================================================
        # LEFT DATA
        # =================================================

        left = Label(
            text=(
                "SYSTEM DATA\n\n"
                "CORE       100%\n"
                "MEMORY     ACTIVE\n"
                "NETWORK    ONLINE\n"
                "VOICE      READY"
            ),
            font_size=10,
            color=(
                0.2,
                0.7,
                0.9,
                1
            ),
            halign="left",
            valign="top",
            size_hint=(None, None),
            size=(
                dp(165),
                dp(120)
            ),
            pos_hint={
                "x": 0.055,
                "top": 0.70
            }
        )

        root.add_widget(left)

        # =================================================
        # RIGHT DATA
        # =================================================

        right = Label(
            text=(
                "JARVIS STATUS\n\n"
                "AI         READY\n"
                "VOICE      READY\n"
                "CONTACTS   READY\n"
                "SECURITY   OK"
            ),
            font_size=10,
            color=(
                1,
                0.3,
                0.08,
                1
            ),
            halign="left",
            valign="top",
            size_hint=(None, None),
            size=(
                dp(165),
                dp(120)
            ),
            pos_hint={
                "right": 0.95,
                "top": 0.70
            }
        )

        root.add_widget(right)

        # =================================================
        # CENTER RESPONSE
        # =================================================

        self.response = Label(
            text="JARVIS\nREADY",
            font_size=17,
            bold=True,
            halign="center",
            valign="middle",
            color=(
                0.55,
                0.9,
                1,
                1
            ),
            size_hint=(0.30, 0.13),
            pos_hint={
                "x": 0.35,
                "y": 0.50
            }
        )

        self.response.bind(
            size=lambda instance, value:
            setattr(
                instance,
                "text_size",
                value
            )
        )

        root.add_widget(
            self.response
        )

        # =================================================
        # TYPE HERE BOX
        # CENTER OF HUD
        # =================================================

        self.input_box = TextInput(
            hint_text="TYPE HERE...",
            multiline=False,
            font_size=17,
            foreground_color=(
                0.4,
                0.9,
                1,
                1
            ),
            hint_text_color=(
                0.3,
                0.55,
                0.65,
                1
            ),
            background_color=(
                0.01,
                0.04,
                0.07,
                0.98
            ),
            cursor_color=(
                0.1,
                0.8,
                1,
                1
            ),
            padding=[
                dp(14),
                dp(12)
            ],
            size_hint=(0.62, None),
            height=dp(55),
            pos_hint={
                "x": 0.19,
                "y": 0.36
            }
        )

        self.input_box.bind(
            on_text_validate=self.enter_pressed
        )

        root.add_widget(
            self.input_box
        )

        # =================================================
        # EXECUTE BUTTON
        # =================================================

        self.execute_button = Button(
            text="EXECUTE",
            font_size=15,
            bold=True,
            color=(
                0.2,
                0.85,
                1,
                1
            ),
            background_color=(
                0.02,
                0.15,
                0.22,
                1
            ),
            size_hint=(0.20, None),
            height=dp(55),
            pos_hint={
                "x": 0.40,
                "y": 0.28
            }
        )

        self.execute_button.bind(
            on_press=self.process_command
        )

        root.add_widget(
            self.execute_button
        )

        # =================================================
        # STATUS
        # =================================================

        self.status = Label(
            text="SYSTEM READY",
            font_size=11,
            color=(
                1,
                0.25,
                0.07,
                1
            ),
            size_hint=(1, None),
            height=dp(30),
            pos_hint={
                "x": 0,
                "y": 0.17
            }
        )

        root.add_widget(
            self.status
        )

        # =================================================
        # CREATOR
        # =================================================

        creator = Label(
            text="CREATED BY ASWIN & YASHWANTH",
            font_size=9,
            color=(
                0.25,
                0.55,
                0.65,
                1
            ),
            size_hint=(1, None),
            height=dp(25),
            pos_hint={
                "x": 0,
                "y": 0.025
            }
        )

        root.add_widget(creator)

        # =================================================
        # CLOCK TIMER
        # =================================================

        Clock.schedule_interval(
            self.update_clock,
            1
        )

        return root

    # =====================================================
    # CLOCK
    # =====================================================

    def update_clock(self, dt):

        self.clock_label.text = (
            datetime.datetime.now().strftime(
                "%H:%M:%S"
            )
        )

    # =====================================================
    # EMOJI CLEANER
    # =====================================================

    def clean_emojis(self, text):

        replacements = {
            "😀": ":)",
            "😃": ":)",
            "😄": ":)",
            "😁": ":)",
            "😂": "haha",
            "🤣": "haha",
            "😊": ":)",
            "😍": "<3",
            "❤️": "<3",
            "❤": "<3",
            "👍": "[OK]",
            "👎": "[NO]",
            "🔥": "[FIRE]",
            "💥": "[BOOM]",
            "🚀": "[ROCKET]",
            "🎉": "[YAY]",
            "😎": "[COOL]",
            "🤖": "[ROBOT]",
            "💡": "[IDEA]"
        }

        for emoji, replacement in replacements.items():

            text = text.replace(
                emoji,
                replacement
            )

        return (
            text
            .encode(
                "ascii",
                "ignore"
            )
            .decode()
        )

    # =====================================================
    # VOICE
    # =====================================================

    def speak(self, text):

        try:

            from gtts import gTTS
            import pygame
            import os
            import time

            text = self.clean_emojis(text)

            filename = (
                "/storage/emulated/0/Download/"
                "jarvis_voice.mp3"
            )

            tts = gTTS(
                text=text,
                lang="en"
            )

            tts.save(filename)

            pygame.mixer.init()

            pygame.mixer.music.load(
                filename
            )

            pygame.mixer.music.play()

            while pygame.mixer.music.get_busy():

                time.sleep(0.1)

            pygame.mixer.quit()

            try:
                os.remove(filename)
            except:
                pass

        except Exception as e:

            print(
                "VOICE ERROR:",
                e
            )

    # =====================================================
    # CONTACT CALLING
    # =====================================================

    def call_contact(self, contact_name):

        try:

            from jnius import autoclass

            PythonActivity = autoclass(
                "org.kivy.android.PythonActivity"
            )

            Intent = autoclass(
                "android.content.Intent"
            )

            Uri = autoclass(
                "android.net.Uri"
            )

            ContactsContract = autoclass(
                "android.provider.ContactsContract"
            )

            Build = autoclass(
                "android.os.Build"
            )

            PackageManager = autoclass(
                "android.content.pm.PackageManager"
            )

            activity = (
                PythonActivity.mActivity
            )

            permission = (
                "android.permission.READ_CONTACTS"
            )

            if Build.VERSION.SDK_INT >= 23:

                result = (
                    activity.checkSelfPermission(
                        permission
                    )
                )

                if (
                    result
                    !=
                    PackageManager.PERMISSION_GRANTED
                ):

                    activity.requestPermissions(
                        [permission],
                        1001
                    )

                    return (
                        "Contacts permission is required. "
                        "Allow it and try again."
                    )

            resolver = (
                activity.getContentResolver()
            )

            uri = (
                ContactsContract
                .CommonDataKinds
                .Phone
                .CONTENT_URI
            )

            projection = [
                ContactsContract
                .CommonDataKinds
                .Phone
                .NUMBER,

                ContactsContract
                .CommonDataKinds
                .Phone
                .DISPLAY_NAME
            ]

            selection = (
                ContactsContract
                .CommonDataKinds
                .Phone
                .DISPLAY_NAME
                + " LIKE ?"
            )

            selection_args = [
                "%" + contact_name + "%"
            ]

            cursor = resolver.query(
                uri,
                projection,
                selection,
                selection_args,
                None
            )

            if cursor is None:

                return "Unable to access contacts."

            try:

                if cursor.moveToFirst():

                    number_index = (
                        cursor.getColumnIndex(
                            ContactsContract
                            .CommonDataKinds
                            .Phone
                            .NUMBER
                        )
                    )

                    name_index = (
                        cursor.getColumnIndex(
                            ContactsContract
                            .CommonDataKinds
                            .Phone
                            .DISPLAY_NAME
                        )
                    )

                    number = cursor.getString(
                        number_index
                    )

                    found_name = cursor.getString(
                        name_index
                    )

                    intent = Intent(
                        Intent.ACTION_DIAL
                    )

                    intent.setData(
                        Uri.parse(
                            "tel:" + number
                        )
                    )

                    activity.startActivity(
                        intent
                    )

                    return (
                        "Opening the dialer for "
                        + found_name
                        + "."
                    )

                return (
                    "I could not find "
                    + contact_name
                    + " in your contacts."
                )

            finally:

                cursor.close()

        except Exception as e:

            print(
                "CONTACT ERROR:",
                e
            )

            return (
                "I could not access that contact. "
                "Check Contacts permission."
            )

    # =====================================================
    # OPEN APPS
    # =====================================================

    def open_app(self, name):

        try:

            from jnius import autoclass

            PythonActivity = autoclass(
                "org.kivy.android.PythonActivity"
            )

            Intent = autoclass(
                "android.content.Intent"
            )

            Uri = autoclass(
                "android.net.Uri"
            )

            activity = (
                PythonActivity.mActivity
            )

            if name == "youtube":

                intent = Intent(
                    Intent.ACTION_VIEW
                )

                intent.setData(
                    Uri.parse(
                        "https://www.youtube.com"
                    )
                )

            elif name == "google":

                intent = Intent(
                    Intent.ACTION_VIEW
                )

                intent.setData(
                    Uri.parse(
                        "https://www.google.com"
                    )
                )

            elif name == "maps":

                intent = Intent(
                    Intent.ACTION_VIEW
                )

                intent.setData(
                    Uri.parse(
                        "geo:0,0?q="
                    )
                )

            elif name == "music":

                intent = Intent(
                    Intent.ACTION_VIEW
                )

                intent.setData(
                    Uri.parse(
                        "https://music.youtube.com"
                    )
                )

            elif name == "phone":

                intent = Intent(
                    Intent.ACTION_DIAL
                )

            elif name == "messages":

                intent = Intent(
                    Intent.ACTION_VIEW
                )

                intent.setType(
                    "vnd.android-dir/mms-sms"
                )

            elif name == "settings":

                intent = Intent(
                    "android.settings.SETTINGS"
                )

            else:

                return False

            activity.startActivity(
                intent
            )

            return True

        except Exception as e:

            print(
                "APP ERROR:",
                e
            )

            return False

    # =====================================================
    # PERSONALITY
    # =====================================================

    def personality_prompt(self):

        if self.personality == "friendly":

            return (
                "Be friendly and encouraging."
            )

        if self.personality == "funny":

            return (
                "Use light appropriate humor."
            )

        if self.personality == "stark":

            return (
                "Act like a futuristic high-tech "
                "AI assistant. Be confident and witty."
            )

        return (
            "Be professional, intelligent and concise."
        )

    # =====================================================
    # AI
    # =====================================================

    def ask_ai(self, question):

        try:

            from openai import OpenAI

            client = OpenAI(
                api_key=API_KEY
            )

            history = ""

            for user_text, ai_text in (
                self.memory[-10:]
            ):

                history += (
                    "User: "
                    + user_text
                    + "\n"
                    "JARVIS: "
                    + ai_text
                    + "\n"
                )

            response = client.responses.create(

                model=MODEL,

                input=(
                    "You are JARVIS, created by "
                    "Aswin and Yashwanth.\n"

                    +
                    self.personality_prompt()
                    +

                    "\nAnswer clearly.\n"
                    "For school questions, use simple "
                    "language.\n\n"

                    "Conversation memory:\n"
                    +
                    history
                    +

                    "\nUser: "
                    +
                    question
                )
            )

            answer = response.output_text

            if not answer:

                return (
                    "The AI returned an empty answer."
                )

            return answer

        except Exception as e:

            print(
                "========== AI ERROR =========="
            )

            print(
                str(e)
            )

            print(
                "=============================="
            )

            return (
                "AI connection failed. "
                "Check the Pydroid console."
            )

    # =====================================================
    # CALCULATOR
    # =====================================================

    def calculate(self, expression):

        try:

            expression = expression.replace(
                "x",
                "*"
            )

            expression = expression.replace(
                "÷",
                "/"
            )

            expression = expression.replace(
                "^",
                "**"
            )

            if not re.match(
                r"^[0-9+\-*/().%\s]+$",
                expression
            ):

                return None

            result = eval(
                expression,
                {
                    "__builtins__": {}
                },
                {}
            )

            return str(result)

        except:

            return None

    # =====================================================
    # FINISH ANSWER
    # =====================================================

    def finish_answer(
        self,
        question,
        answer
    ):

        self.memory.append(
            (
                question,
                answer
            )
        )

        self.memory = (
            self.memory[-10:]
        )

        clean = self.clean_emojis(
            answer
        )

        Clock.schedule_once(
            lambda dt:
            self.show_answer(clean)
        )

        threading.Thread(
            target=self.speak,
            args=(clean,),
            daemon=True
        ).start()

    def show_answer(self, answer):

        self.response.text = answer

        self.status.text = (
            "SYSTEM READY // AWAITING COMMAND"
        )

    # =====================================================
    # COMMAND PROCESSING
    # =====================================================

    def process_command(self, instance):

        question = (
            self.input_box.text.strip()
        )

        if not question:

            return

        self.input_box.text = ""

        self.input_box.focus = False

        self.status.text = (
            "PROCESSING // EXECUTING"
        )

        threading.Thread(
            target=self.handle_command,
            args=(question,),
            daemon=True
        ).start()

    def enter_pressed(self, instance):

        self.process_command(
            self.execute_button
        )

    # =====================================================
    # COMMAND HANDLER
    # =====================================================

    def handle_command(self, question):

        q = question.lower().strip()

        # -------------------------------------------------
        # CONTACT CALLING
        # -------------------------------------------------

        for prefix in [
            "call ",
            "phone ",
            "dial ",
            "ring "
        ]:

            if q.startswith(prefix):

                name = question[
                    len(prefix):
                ].strip()

                Clock.schedule_once(
                    lambda dt:
                    self.show_answer(
                        "SEARCHING CONTACT..."
                    )
                )

                answer = self.call_contact(
                    name
                )

                self.finish_answer(
                    question,
                    answer
                )

                return

        # -------------------------------------------------
        # PERSONALITY
        # -------------------------------------------------

        for prefix in [
            "personality ",
            "change personality ",
            "switch personality "
        ]:

            if q.startswith(prefix):

                mode = q[
                    len(prefix):
                ].strip()

                if mode in [
                    "professional",
                    "friendly",
                    "funny",
                    "stark"
                ]:

                    self.personality = mode

                    answer = (
                        mode.capitalize()
                        +
                        " personality activated."
                    )

                else:

                    answer = (
                        "Available personalities are "
                        "Professional, Friendly, "
                        "Funny and Stark."
                    )

                self.finish_answer(
                    question,
                    answer
                )

                return

        # -------------------------------------------------
        # HELLO
        # -------------------------------------------------

        if q in [
            "hello",
            "hi",
            "hey",
            "hello jarvis",
            "hi jarvis"
        ]:

            self.finish_answer(
                question,
                "Hello sir. How can I help you?"
            )

            return

        # -------------------------------------------------
        # NAME
        # -------------------------------------------------

        if "your name" in q:

            self.finish_answer(
                question,
                "My name is JARVIS."
            )

            return

        # -------------------------------------------------
        # CREATOR
        # -------------------------------------------------

        if (
            "who created you" in q
            or
            "who made you" in q
            or
            "your creator" in q
        ):

            self.finish_answer(
                question,
                "I was created by Aswin and Yashwanth."
            )

            return

        # -------------------------------------------------
        # HOW ARE YOU
        # -------------------------------------------------

        if "how are you" in q:

            self.finish_answer(
                question,
                "I am doing great, sir. "
                "All systems are ready."
            )

            return

        # -------------------------------------------------
        # TIME
        # -------------------------------------------------

        if (
            q == "time"
            or
            "what time" in q
        ):

            self.finish_answer(
                question,
                "The time is "
                +
                datetime.datetime.now().strftime(
                    "%I:%M %p"
                )
            )

            return

        # -------------------------------------------------
        # DATE
        # -------------------------------------------------

        if (
            "date" in q
            or
            "today" in q
        ):

            self.finish_answer(
                question,
                "Today is "
                +
                datetime.datetime.now().strftime(
                    "%A, %d %B %Y"
                )
            )

            return

        # -------------------------------------------------
        # THANKS
        # -------------------------------------------------

        if (
            "thanks" in q
            or
            "thank you" in q
        ):

            self.finish_answer(
                question,
                "You're welcome, sir."
            )

            return

        # -------------------------------------------------
        # CALCULATOR
        # -------------------------------------------------

        for word in [
            "calculate",
            "solve"
        ]:

            if q.startswith(word):

                expression = (
                    q[len(word):].strip()
                )

                result = self.calculate(
                    expression
                )

                if result is not None:

                    self.finish_answer(
                        question,
                        "The answer is "
                        + result
                    )

                    return

        # -------------------------------------------------
        # OPEN APP
        # -------------------------------------------------

        apps = [
            "youtube",
            "google",
            "maps",
            "music",
            "phone",
            "messages",
            "settings"
        ]

        if q.startswith("open "):

            app = q[5:].strip()

            if app in apps:

                success = self.open_app(
                    app
                )

                if success:

                    self.finish_answer(
                        question,
                        "Opening " + app + "."
                    )

                    return

        # -------------------------------------------------
        # GOOGLE SEARCH
        # -------------------------------------------------

        if q.startswith(
            "search google for "
        ):

            search_text = q[
                len("search google for "):
            ]

            url = (
                "https://www.google.com/search?q="
                +
                search_text.replace(
                    " ",
                    "+"
                )
            )

            webbrowser.open(url)

            self.finish_answer(
                question,
                "Searching Google for "
                + search_text
            )

            return

        # -------------------------------------------------
        # YOUTUBE SEARCH
        # -------------------------------------------------

        if q.startswith(
            "search youtube for "
        ):

            search_text = q[
                len("search youtube for "):
            ]

            url = (
                "https://www.youtube.com/results?search_query="
                +
                search_text.replace(
                    " ",
                    "+"
                )
            )

            webbrowser.open(url)

            self.finish_answer(
                question,
                "Searching YouTube for "
                + search_text
            )

            return

        # -------------------------------------------------
        # AI
        # -------------------------------------------------

        Clock.schedule_once(
            lambda dt:
            self.show_answer(
                "AI PROCESSING..."
            )
        )

        answer = self.ask_ai(
            question
        )

        self.finish_answer(
            question,
            answer
        )


# =========================================================
# RUN
# =========================================================

JarvisApp().run()