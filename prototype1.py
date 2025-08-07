from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label

class attendenceapp(App):
    def build(self):
        layout = GridLayout(cols=2 , spacing = 10, padding = 10)
        
        self.attended = 0
        self.total = 0
        
        self.lecture_attended = 0
        self.practicals_attended = 0
        
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
        self.attended_label = Label(text="Classes Attended: 0")
        self.total_label = Label(text="Total Classes: 0")
        self.percent_label = Label(text="Attendence Percentage: 0.00%")
        
        layout.add_widget(self.attended_label)
        layout.add_widget(self.total_label)
        layout.add_widget(self.percent_label)
        layout.add_widget(Label(text = ""))
        
        return layout
    
    #for updating the labels after each click
    def update_label(self):
        self.attended_label.text = f"Attended Classes: {self.attended}"
        self.total_label.text = f"Total Classes: {self.total}"
        percentage = self.attended/self.total * 100 if self.total !=0 else 0
        self.percent_label.text=f"Attendence Percentage: {percentage}%"
    
    #for lecture buttons    
    def lecture_present(self, instance):
        self.attended +=1
        self.total +=1
        self.history.append(("Lecture" ,1, 1))
        self.update_label()
    def lecture_absent(self, instance):
        self.attended +=0
        self.total +=1
        self.history.append(("Lecture", 0, 1))    
        self.update_label()
    
    #for practical buttons    
    def practical_present(self, instance):
        self.attended +=2
        self.total +=2
        self.history.append(("Lecture" ,2, 2))
        self.update_label()
    def practical_absent(self, instance):
        self.attended +=0
        self.total +=1
        self.history.append(("Lecture" ,0, 2))
        self.update_label()
        
    #for undo button
    def undo(self, instance):
        if self.history:
            last = self.history.pop()
            self.attended -=last[1]
            self.total -= last[2]
            #because ["Lecture", 1, 1]
            self.update_label()   
        
    
           
if __name__ == "__main__":
    attendenceapp().run()
        
        
        
        
        
        
        