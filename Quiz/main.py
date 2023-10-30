# Importieren der Kivy-Komponenten und Module
from kivy.core.window import Window
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, NoTransition, Screen
from kivy.properties import ListProperty, StringProperty 
from kivy.core.text import LabelBase
from kivy.lang import Builder
import random
from kivy.uix.button import Button
from science import science_lowlevel, science_midlevel, science_highlevel #importieren der Frageliste
from informationtech import it_lowlevel, it_midlevel, it_highlevel #importieren der Frageliste
from history import history_lowlevel, history_midlevel, history_highlevel #importieren der Frageliste
from geography import geography_lowlevel, geography_midlevel, geography_highlevel #importieren der Frageliste
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout

# Festlegen der Fenstergröße
Window.size = (900,500)

# Laden der Kivy-Dateien
Builder.load_file("start.kv")
Builder.load_file("quiz.kv")
Builder.load_file("select_category.kv")
Builder.load_file("select_level.kv")
Builder.load_file("final_score.kv")

#  Klasse für Kategorieauswahl-Buttons
class CategoryButton(Button):
    bg_color = ListProperty([1, 1, 1, 1])

#  Klasse für Schwierigkeitsgrad-Auswahl-Buttons
class LevelButton(Button):
    bg_color = ListProperty([1, 1, 1, 1])

#Klasse für Antwort-Buttons im Quiz
class OptionButton(Button):
    answer_text = StringProperty("")
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
         #Aktualisieren des Texts des Buttons mit dem Wert von answer_text
        self.text = self.answer_text
        
# Startbildschirm
class StartScreen(Screen):
    pass
# Bildschirm für die Auswahl der Kategorie
class CategoryScreen(Screen):
    pass
# Bildschirm für die Auswahl des Schwierigkeitsgrads
class LevelScreen(Screen):
    pass

# Bildschirm für die Anzeige der Ergebnisse
class ScoreScreen(Screen):
    correct_count =0
    wrong_count=0
    
    def on_enter(self):
        app = App.get_running_app()
        self.correct_count=app.root.get_screen("quiz").correct_count
        self.wrong_count=app.root.get_screen("quiz").wrong_count
        self.incorrect_answer=app.root.get_screen("quiz").incorrect_answer
        self.ids.score_label.text = (f"Anzahl der richtigen Antworten: {self.correct_count} &"
        f"\nAnzahl der falschen Antworten: {self.wrong_count}"
        f"\nDie Ergebnisse lauten:\n" +'\n'.join(self.incorrect_answer))
        
# Quiz-Bildschirm   
class QuizScreen(Screen):
    current_question = 0 
    correct_count = 0
    wrong_count = 0
    incorrect_answer=[]
    
    
    def on_enter(self):
        self.correct_count = 0
        self.wrong_count = 0
        self.current_question = 1
        self.show_question()
        

    
    # Hier wird die Frage und die Antwortmöglichkeiten für das Quiz generiert
    def show_question(self):
        category = App.get_running_app().selected_category
        level = App.get_running_app().selected_level
        science = [] 
        informationtech = [] 
        geography = [] 
        history = [] 
        if category == "Wissenschaft" and level == "Leicht" :
            science = science_lowlevel
        elif category == "Wissenschaft" and level == "Mittel" :
            science = science_midlevel
        elif category == "Wissenschaft" and level == "Schwer" :
            science = science_highlevel

        elif category == "IT" and level == "Leicht":
            informationtech = it_lowlevel
        elif category == "IT" and level == "Mittel":
            informationtech = it_midlevel
        elif category == "IT" and level == "Schwer":
            informationtech =  it_highlevel

        elif category == "Geografie" and level == "Leicht":
            geography =  geography_lowlevel
        elif category == "Geografie" and level == "Mittel":
            geography =  geography_midlevel
        elif category == "Geografie" and level == "Schwer":
            geography =  geography_highlevel
      
        elif category == "Geschichte" and level == "Leicht":
            history =  history_lowlevel
        elif category == "Geschichte" and level == "Mittel":
            history =  history_midlevel    
        elif category == "Geschichte" and level == "Schwer":
            history =  history_highlevel  
        else:
            science = []# Wenn keine Kategorie ausgewählt wurde, leere Liste

        if science:
            #unpacking Tupel und Zufallsfunktion für die Auswahl der Frage
            question, *answers, correct_answer, hinweis = random.choice(science)
            #Fragelabel wird befüllt
            self.ids.question.text = question
            #Antwortbuttons werden geleert
            self.ids.option_layout.clear_widgets()
            #Antwortbuttons werden befüllt und funktion check_answer wird aufgerufen
            for answer in answers:
                buttontext = OptionButton(answer_text=answer, on_release=self.check_answer)
                self.ids.option_layout.add_widget(buttontext)
            self.correct_answer = correct_answer
            self.hinweis= hinweis
        elif informationtech:
            question, *answers, correct_answer, hinweis = random.choice(informationtech)
            self.ids.question.text = question
            self.ids.option_layout.clear_widgets()
            for answer in answers:
                buttontext = OptionButton(answer_text=answer, on_release=self.check_answer)
                self.ids.option_layout.add_widget(buttontext)
            self.correct_answer = correct_answer
            self.hinweis= hinweis
        elif geography:
            question, *answers, correct_answer, hinweis = random.choice(geography)
            self.ids.question.text = question
            self.ids.option_layout.clear_widgets()
            for answer in answers:
                buttontext = OptionButton(answer_text=answer, on_release=self.check_answer)
                self.ids.option_layout.add_widget(buttontext)
            self.correct_answer = correct_answer
            self.hinweis= hinweis
        elif history:
            question, *answers, correct_answer, hinweis = random.choice(history)
            self.ids.question.text = question
            self.ids.option_layout.clear_widgets()
            for answer in answers:
                buttontext = OptionButton(answer_text=answer, on_release=self.check_answer)
                self.ids.option_layout.add_widget(buttontext)
            self.correct_answer = correct_answer
            self.hinweis= hinweis
        else:
            # Falls keine Fragen für die ausgewählte Kategorie vorhanden sind, gehe zurück zur Kategorieauswahl
            self.manager.current = "select_category"
        self.current_question_text = (f"Frage: {self.current_question}/15")
        self.ids.currentquestion.text = self.current_question_text
 # Hier wird überprüft, ob die ausgewählte Antwort korrekt ist        
    def check_answer(self,answer):
        answer = App.get_running_app().selected_answer
        if answer == self.correct_answer:
            self.correct_count +=1
        else:
            self.wrong_count +=1
            self.incorrect_answer.append(f"\n" )
            self.incorrect_answer.append(f"Die Frage war: {self.ids.question.text}." )
            self.incorrect_answer.append(f"Deine Antwort war: {answer}." )
            self.incorrect_answer.append(f"Die richtige Antwort lautet: {self.correct_answer}.")
        self.current_question += 1
        if self.current_question >= 16:
            self.manager.get_screen("score").on_enter()
            self.manager.current = "score"
        else:
            self.show_question()
 # Hier wird ein Popup-Fenster mit einem Hinweis angezeigt
    def show_popup(self, hinweis):
        self.popup = Popup(title='Hinweis', content=BoxLayout(orientation='vertical'))
        layout = self.popup.content

        label = Label(text=self.hinweis)
        layout.add_widget(label)

        close_button = Button(text="Schließen", on_release=self.close_popup)
        layout.add_widget(close_button)

        self.popup.open()
# Hier wird das Popup-Fenster geschlossen
    def close_popup(self, instance):
        if self.popup:
            self.popup.dismiss()
# Hauptanwendungsklasse
class QuizApp(App): 

    def build(self):
        global screen_manager
        screen_manager = ScreenManager(transition=NoTransition())
        screen_manager.add_widget(StartScreen(name="start"))
        screen_manager.add_widget(CategoryScreen(name="select_category"))
        screen_manager.add_widget(LevelScreen(name="select_level"))
        screen_manager.add_widget(QuizScreen(name="quiz"))
        screen_manager.add_widget(ScoreScreen(name="score"))
        return screen_manager
    
    
    # Weitere Funktionen, um die Auswahl von Kategorie, Level und Antwort zu steuern        
    def select_quiz_category(self, category):
        self.selected_category = category
        screen_manager.current = "select_level"

    def select_quiz_level(self, level):
        self.selected_level = level
        screen_manager.current = "quiz"

    def select_quiz_answer(self, answer):
        self.selected_answer = answer
#App verlassen
    def exit_app(self):
        self.stop()

if __name__ == "__main__":
    #Hier wird de Schriftart registriert
    LabelBase.register(name="ADLaM_Display", fn_regular="C:\\Quiz\\ADLaM_Display\\ADLaMDisplay-Regular.ttf") #Pfad hier anpassen 
    QuizApp().run()                                    