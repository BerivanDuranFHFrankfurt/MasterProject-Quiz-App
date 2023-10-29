# Importieren der erforderlichen Kivy-Module
from kivy.app import App
import random
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.utils import get_color_from_hex
from kivy.animation import Animation
from wissenschaft_quiz import wissenschaft_leicht, wissenschaft_mittel, wissenschaft_schwer
from it_quiz import it_leicht, it_mittel, it_schwer
from geografie_quiz import geo_leicht, geo_mittel, geo_schwer
from geschichte_quiz import geschichte_leicht, geschichte_mittel, geschichte_schwer
from kivy.clock import Clock
from kivy.properties import StringProperty
from kivy.uix.popup import Popup
# Definition von benutzerdefinierten Kivy-Widgets
class DifficultyButton(Button):
    pass

class CategoryButton(Button):
    pass

class ResultButton(Button):
    pass

class HintButton(Button):
    pass
class HintPopup(Popup):
    pass

class AntwortButton(Button):
    pass
# Definition der StartScreen-Klasse
class StartScreen(Screen):
    pass
# Definition der CategoryScreen-Klasse
class CategoryScreen(Screen):
    def set_category(self, category_name):
        self.manager.category = category_name
        
 
 
# Definition der DifficultyScreen-Klasse      
class DifficultyScreen(Screen):
    def set_difficulty(self, difficulty):
        self.manager.difficulty = difficulty
        self.manager.current = 'fragerunde'
    
# Definition der FragerundeScreen-Klasse

class FragerundeScreen(Screen):
    answer_buttons = [] 
    incorrect_answers = []  # Liste, um falsch beantwortete Fragen zu speichern
    current_question = None  # Hier werden wir die aktuelle Frage speichern
    question_count = 0
    correct_answers_count = 0  # Hinzugefügte Variable für die Anzahl der richtigen Antworten
    asked_questions = set() 
    timer_duration = 300  # Timer-Dauer in Sekunden (2 Minuten)
    remaining_time = StringProperty()  # Property zur Anzeige der verbleibenden Zeit
    current_question_label = StringProperty()
    
    
    def on_pre_enter(self, *args):
        # Diese Methode wird aufgerufen, bevor der Screen angezeigt wird
        # Hier können Sie die Fragen laden und das Label aktualisieren
        self.load_question()
        self.start_timer()
        self.update_hint_button()

    def show_hint(self):
        hint_popup = HintPopup(title='Hinweis', auto_dismiss=True)
        hint_popup.ids.hint_label.text = self.current_question_hint
        hint_popup.open()

    def update_hint_button(self):
        # Überprüfen Sie die ausgewählte Schwierigkeitsstufe und passen Sie den ?-Button an
        if self.manager.difficulty in ("Leicht", "Mittel"):
            self.ids.hinweis_button.opacity = 0  # Blenden Sie den ?-Button aus
            self.ids.hinweis_button.disabled = True
        else:
            self.ids.hinweis_button.opacity = 1  # Zeigen Sie den ?-Button an
            self.ids.hinweis_button.disabled = False    

    def start_timer(self):
        self.timer = Clock.schedule_interval(self.update_timer, 1)  # Jede Sekunde aktualisieren

    def update_timer(self, dt):
        # Berechnen Sie die verbleibende Zeit und aktualisieren Sie das Anzeige-Property
        self.timer_duration -= 1
        minutes = self.timer_duration // 60
        seconds = self.timer_duration % 60
        self.remaining_time = f"Verbleibende Zeit: {minutes:02}:{seconds:02}"

        if self.timer_duration <= 0:
            # Wenn die Zeit abgelaufen ist, beenden Sie die Quizrunde und zeigen Sie die Ergebnisansicht an
            self.timer.cancel()
            self.manager.remaining_time = self.remaining_time  # Speichern Sie die verbleibende Zeit in der Manager-Klasse
            self.manager.current = 'result'
            self.question_count = 15

    def load_question(self):
        if self.question_count >= 15:
            # Wenn 15 Fragen gestellt wurden, wechseln Sie zum Ergebnisbildschirm oder einer anderen geeigneten Aktion
            self.manager.current = 'result'
            self.question_count = 15
            return

        available_questions = None
        if self.manager.category == "Wissenschaft":
            if self.manager.difficulty == "Leicht":
                available_questions = wissenschaft_leicht
            elif self.manager.difficulty == "Mittel":
                available_questions = wissenschaft_mittel
            elif self.manager.difficulty == "Schwer":
                available_questions = wissenschaft_schwer
        elif self.manager.category == "IT":
            if self.manager.difficulty == "Leicht":
                available_questions = it_leicht
            elif self.manager.difficulty == "Mittel":
                available_questions = it_mittel
            elif self.manager.difficulty == "Schwer":
                available_questions = it_schwer
       
        elif self.manager.category == "Geografie":
            if self.manager.difficulty == "Leicht":
                available_questions = geo_leicht
            elif self.manager.difficulty == "Mittel":
                available_questions = geo_mittel
            elif self.manager.difficulty == "Schwer":
                available_questions = geo_schwer
        elif self.manager.category == "Geschichte":
            if self.manager.difficulty == "Leicht":
                available_questions = geschichte_leicht
            elif self.manager.difficulty == "Mittel":
                available_questions = geschichte_mittel
            elif self.manager.difficulty == "Schwer":
                available_questions = geschichte_schwer

        if available_questions:
            # Wählen Sie eine zufällige Frage aus den verfügbaren Fragen aus, die nicht bereits gestellt wurde
            while True:
                question_data = random.choice(available_questions)
                question_key = question_data["frage"]  # Verwenden Sie den Fragesatz als Schlüssel

                if question_key not in self.asked_questions:
                    break

            self.asked_questions.add(question_key)

            self.current_question = question_data
            self.current_question_label = f"Frage {self.question_count + 1}/15"  # Aktualisieren Sie das Frage-Label
            self.ids.question_label.text = question_data["frage"]
            self.ids.question_label.texture_update()
            
            self.current_question_hint = question_data.get("hinweis", "")  # Verwenden Sie "hinweis" als Schlüssel für den Hinweis

         # Zeigen Sie die Antwortmöglichkeiten in den Antwortbuttons an
        for i, antwort in enumerate(question_data["antworten"]):
            answer_button_id = f"answer_button_{i + 1}"  # Die ID des Antwortbuttons
            self.ids[answer_button_id].text = antwort

        self.question_count += 1

    def check_answer(self, selected_answer):
        # Überprüfen Sie die ausgewählte Antwort mit der richtigen Antwort
        if selected_answer == self.current_question["richtige_antwort"]:
            # Den geklickten Antwortbutton grün einfärben
            for i, antwort in enumerate(self.current_question["antworten"]):
                if antwort == selected_answer:
                    answer_button_id = f"answer_button_{i + 1}"
                    selected_button = self.ids[answer_button_id]
                    anim = Animation(background_color=get_color_from_hex("#00FF00"), duration=0.05)
                    anim.start(selected_button)

            self.correct_answers_count += 1
        else:
            # Den geklickten Antwortbutton rot einfärben
            for i, antwort in enumerate(self.current_question["antworten"]):
                if antwort == selected_answer:
                    answer_button_id = f"answer_button_{i + 1}"
                    selected_button = self.ids[answer_button_id]
                    anim = Animation(background_color=get_color_from_hex("#FF0000"), duration=0.05)
                    anim.start(selected_button)

            self.incorrect_question = {
                "frage": self.current_question["frage"],
                "falsche_antwort": selected_answer,
                "korrekte_antwort": self.current_question["richtige_antwort"]
            }
            self.incorrect_answers.append(self.incorrect_question)

        # Verzögerung von 1 Sekunde hinzufügen und dann load_question aufrufen
        
        Clock.schedule_once(lambda dt: self.reset_button_colors(), 0.25)
        Clock.schedule_once(lambda dt: self.load_question(), 0.45)
    def reset_button_colors(self):
        # Iteriere über alle Antwortbuttons und setze ihre Hintergrundfarben zurück
        for i in range(1, 5):  # Annahme: Es gibt 4 Antwortbuttons mit IDs answer_button_1 bis answer_button_4
            answer_button_id = f"answer_button_{i}"
            answer_button = self.ids[answer_button_id]
            anim = Animation(background_color=(1, 1, 1, 0), duration=0.30)  # Zurücksetzen auf Weiß
            anim.start(answer_button)
        
 


    def cancel_quiz(self):
        # Zurücksetzen der Fragezählung und der gestellten Fragen
        self.question_count = 0
        self.asked_questions = set()

        # Zurücksetzen der Timer-Dauer
        self.timer_duration = 300

        # Stoppen des laufenden Timers
        if hasattr(self, "timer"):
            self.timer.cancel()

        # Zurückkehren zum Startbildschirm
        self.manager.current = 'start'

# Definition der ResultScreen-Klasse

class ResultScreen(Screen):
    def on_pre_leave(self):
        # Zurücksetzen aller relevanten Daten
        fragerunde_screen = self.manager.get_screen("fragerunde")
        if fragerunde_screen:
            fragerunde_screen.correct_answers_count = 0
            fragerunde_screen.incorrect_answers = []
            fragerunde_screen.question_count = 0
            fragerunde_screen.asked_questions = set()
            fragerunde_screen.timer_duration = 300
            if hasattr(fragerunde_screen, "timer"):
                fragerunde_screen.timer.cancel()
            

    def on_enter(self):
 
        fragerunde_screen = self.manager.get_screen("fragerunde")
        if fragerunde_screen:
            self.ids.performance_summary_label.text = f'Korrekte Antworten: {fragerunde_screen.correct_answers_count}/{fragerunde_screen.question_count}'
            
            # Anzeigen der verbleibenden Zeit aus dem Manager
            self.ids.remaining_time_label.text = fragerunde_screen.remaining_time

            incorrect_answers_text = ""
            for i, question_data in enumerate(fragerunde_screen.incorrect_answers):
                incorrect_answers_text += f"Falsch beantwortete Frage {i + 1}:\n"
                incorrect_answers_text += f"{question_data['frage']}\n"
                incorrect_answers_text += f"Falsche Antwort: [color=b32821]{question_data['falsche_antwort']}[/color]\n"
                  # Verwenden Sie Markup, um die korrekte Antwort in Grün einzufärben
                incorrect_answers_text += f"Korrekte Antwort: [color=008800]{question_data['korrekte_antwort']}[/color]\n\n"
            
            self.ids.incorrect_answers_label.text = incorrect_answers_text

    def close_app(self):
        App.get_running_app().stop()

 # Definition der ResultScreen-Klasse
class QuizApp(App):
    category = ""
    difficulty = ""
    def build(self): 
        sm = ScreenManager()
        sm.add_widget(StartScreen(name='start'))
        sm.add_widget(CategoryScreen(name='category'))
        sm.add_widget(DifficultyScreen(name='difficulty'))
        sm.add_widget(FragerundeScreen(name='fragerunde'))  # Beachten Sie die Namensänderung hier
        sm.add_widget(ResultScreen(name='result'))
        return sm
    
    
if __name__ == '__main__':
    QuizApp().run() 