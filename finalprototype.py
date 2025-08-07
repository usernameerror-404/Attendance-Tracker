import json
import os

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView


class MyApp(App):
    def build(self):
        self.data_file_to_save = "attendance_data.json"
        self.reload_memory()

        root = ScrollView()
        self.layout = GridLayout(cols=2, spacing=10, padding=10, size_hint_y=None)
        self.layout.bind(minimum_height=self.layout.setter('height'))

        self.attendance = {}  # store subject attendance info
        self.history = []     # for undo feature

        # Add all subjects (with proper settings)
        self.add_subject("Operating System (UCS 303)", lecture=True, practical=True)
        self.add_subject("Object Oriented Programming (UAI301)", lecture=True, practical=True)
        self.add_subject("Data Structures (UCS301)", lecture=True, practical=True)
        self.add_subject("Numerical Linear Algebra (UMA021)", lecture=True, practical=True)
        self.add_subject("Engineering Drawing Project 1 (UTA016)", lecture=True, practical=True)
        self.add_subject("Experimental Learning (UAI302)", lecture=False, practical=True)
        self.add_subject("Evolutionary Psychology (UHU050)", lecture=True, practical=False)

        # Add Undo Button
        self.layout.add_widget(Label(text="Undo Last Action:", size_hint_y=None, height=40))
        self.layout.add_widget(Button(text="Undo", on_press=self.undo_history, size_hint_y=None, height=40))

        root.add_widget(self.layout)
        return root

    def add_subject(self, name, lecture, practical):
        self.attendance[name] = self.saved_data.get(name, {
            'lectures_attended': 0,
            'total_lectures': 0,
            'practicals_attended': 0,
            'total_practicals': 0
        })

        # Subject Heading
        self.layout.add_widget(Label(text=f"[b]{name}[/b]", markup=True,
                                     font_size=18, size_hint_y=None, height=50))
        self.layout.add_widget(Label(size_hint_y=None, height=10))

        # Lecture Buttons
        if lecture:
            self.layout.add_widget(Label(text="Lecture:", size_hint_y=None, height=30))
            self.layout.add_widget(Label(size_hint_y=None, height=10))
            self.layout.add_widget(Button(text="Present", size_hint_y=None, height=40,
                                          on_press=lambda x, s=name: self.mark(s, "lecture", True)))
            self.layout.add_widget(Button(text="Absent", size_hint_y=None, height=40,
                                          on_press=lambda x, s=name: self.mark(s, "lecture", False)))

        # Practical Buttons
        if practical:
            self.layout.add_widget(Label(text="Practical:", size_hint_y=None, height=30))
            self.layout.add_widget(Label(size_hint_y=None, height=10))
            self.layout.add_widget(Button(text="Present", size_hint_y=None, height=40,
                                          on_press=lambda x, s=name: self.mark(s, "practical", True)))
            self.layout.add_widget(Button(text="Absent", size_hint_y=None, height=40,
                                          on_press=lambda x, s=name: self.mark(s, "practical", False)))

        # Labels to show attendance info
        self.attendance[name]['lecture_label'] = Label(text="Lectures Attended: 0 / 0",
                                                       size_hint_y=None, height=30)
        self.attendance[name]['practical_label'] = Label(text="Practicals Attended: 0 / 0",
                                                         size_hint_y=None, height=30)
        self.attendance[name]['percentage_label'] = Label(text="Attendance Percentage: 0.00%",
                                                          size_hint_y=None, height=30)

        self.layout.add_widget(self.attendance[name]['lecture_label'])
        self.layout.add_widget(self.attendance[name]['practical_label'])
        self.layout.add_widget(self.attendance[name]['percentage_label'])
        self.layout.add_widget(Label(size_hint_y=None, height=20))

        self.update_labels(name)

    def mark(self, subject, class_type, present):
        data = self.attendance[subject]

        if class_type == 'lecture':
            data['total_lectures'] += 1
            if present:
                data['lectures_attended'] += 1

        elif class_type == 'practical':
            data['total_practicals'] += 2
            if present:
                data['practicals_attended'] += 2

        self.history.append((subject, class_type, present))
        self.update_labels(subject)
        self.save_memory()

    def update_labels(self, subject):
        data = self.attendance[subject]

        data['lecture_label'].text = f"Lectures Attended: {data['lectures_attended']} / {data['total_lectures']}"
        data['practical_label'].text = f"Practicals Attended: {data['practicals_attended']} / {data['total_practicals']}"

        total_attended = data['lectures_attended'] + data['practicals_attended']
        total_classes = data['total_lectures'] + data['total_practicals']

        percentage = (total_attended / total_classes * 100) if total_classes else 0
        data['percentage_label'].text = f"Attendance Percentage: {percentage:.2f}%"

    def undo_history(self, instance):
        if not self.history:
            return

        subject, class_type, present = self.history.pop()
        data = self.attendance[subject]

        if class_type == 'lecture':
            data['total_lectures'] -= 1
            if present:
                data['lectures_attended'] -= 1

        elif class_type == 'practical':
            data['total_practicals'] -= 2
            if present:
                data['practicals_attended'] -= 2

        self.update_labels(subject)
        self.save_memory()

    def save_memory(self):
        data_to_save = {
            subject: {
                'lectures_attended': data['lectures_attended'],
                'total_lectures': data['total_lectures'],
                'practicals_attended': data['practicals_attended'],
                'total_practicals': data['total_practicals']
            }
            for subject, data in self.attendance.items()
        }
        with open(self.data_file_to_save, 'w') as f:
            json.dump(data_to_save, f)

    def reload_memory(self):
        if os.path.exists(self.data_file_to_save):
            with open(self.data_file_to_save, 'r') as f:
                self.saved_data = json.load(f)
        else:
            self.saved_data = {}


if __name__ == "__main__":
    MyApp().run()
