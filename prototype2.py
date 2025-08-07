from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label

class attendenceapp(App):
    def build(self):
        layout = GridLayout(cols=2 , spacing = 10, padding = 10)
        
        self.attended = 0
        self.total = 0
        
        self.lectures_attended = 0
        self.total_lectures = 0
        self.practicals_attended = 0
        self.total_practicals = 0
        
        self.history = []
        
        layout.add_widget(Label(text = "Attendence tracker", font_size = 50))
        layout.add_widget(Label(text = ""))
        
        
        #for lecture
        layout.add_widget(Label(text="Lecture:"))
        layout.add_widget(Label(text=""))
        layout.add_widget(Button(text="Present", on_press = self.lecture_present))
        layout.add_widget(Button(text="Absent", on_press=self.lecture_absent ))
        
        #for practical
        layout.add_widget(Label(text="Practical:"))
        layout.add_widget(Label(text=""))
        layout.add_widget(Button(text="Present", on_press = self.practical_present))
        layout.add_widget(Button(text="Absent", on_press = self.practical_absent))
        
        #undo button
        layout.add_widget(Label(text = "For Undo:"))
        layout.add_widget(Button(text="Undo", on_press = self.undo))
        layout.add_widget(Label(text=""))
        layout.add_widget(Label(text=""))
        
        #Class Details
        self.lectures_attended_label = Label(text="Lectures Attended: 0")
        self.total_lectures_label = Label(text="Total Lectures: 0")
        self.practicals_attended_label = Label(text="Practicals Attended: 0")
        self.total_practicals_label = Label(text="Total Practicals: 0")
        
        self.percent_label = Label(text="Attendence Percentage: 0.00%")
        
        layout.add_widget(self.lectures_attended_label)
        layout.add_widget(self.total_lectures_label)
        layout.add_widget(self.practicals_attended_label)
        layout.add_widget(self.total_practicals_label)
        
        layout.add_widget(self.percent_label)
        layout.add_widget(Label(text = ""))
        
        return layout
    
    #for updating the labels after each click
    def update_label(self):
        
        self.lectures_attended_label.text = f"Lectures Attended: {self.lectures_attended}"
        self.total_lectures_label.text = f"Total Classes: {self.total_lectures}"
        self.practicals_attended_label.text = f"Practicals Attended: {self.practicals_attended}"
        self.total_practicals_label.text = f"Total Practicals: {self.total_practicals}"
        
        percentage = self.attended/self.total * 100 if self.total !=0 else 0
        self.percent_label.text=f"Attendence Percentage: {percentage}%"
    
    #for lecture buttons    
    def lecture_present(self, instance):
        
        self.lectures_attended +=1
        self.total_lectures +=1
        
        self.attended +=1
        self.total +=1
        
        self.history.append(("Lecture" ,1, 1, 0, 0, 1, 1))
        self.update_label()
        
    def lecture_absent(self, instance):
        
        self.lectures_attended +=0
        self.total_lectures +=1
        
        self.attended +=0
        self.total +=1
        
        self.history.append(("Lecture" ,0, 1, 0, 0, 0, 1))
        self.update_label()
    
    #for practical buttons    
    def practical_present(self, instance):
        
        self.practicals_attended +=2
        self.total_practicals +=2
        
        self.attended +=2
        self.total +=2
        
        self.history.append(("Lecture" ,0, 0, 2, 2, 2, 2))
        self.update_label()
        
    def practical_absent(self, instance):
        
        self.practicals_attended +=0
        self.total_practicals +=2
        
        self.attended +=0
        self.total +=2
        
        self.history.append(("Lecture" ,0, 0, 0, 2, 0, 2))
        self.update_label()
        
    #for undo button
    def undo(self, instance):
        if self.history:
            last = self.history.pop()
            self.lectures_attended -=last[1]
            self.total_lectures -=last[2]
            self.practicals_attended -=last[3]
            self.total_practicals -=last[4]
            self.attended -=last[5]
            self.total -= last[6]
            #because ["Lecture", 1, 1, 0, 0, 1, 1] and
            #["Practicaql", 0, 0, 2, 2, 2, 2]
            self.update_label()
                     
if __name__ == "__main__":
    attendenceapp().run()
        
        
        
        
        
        
        