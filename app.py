"""
    Todo App 
    app done with flet and sqlite and without forgetting our awesome friend python
"""

# modules
import flet
from flet import *
from datetime import datetime as dt
import sqlite3 as sql

# Okay, so the UI(User Interface) is done, now fore the final part, we can implement a database to store the tasks
# We can create a class for this
class Database:
    def ConnectToDatabase():
        try:
            # First we should verify if the database file wheter exists or not. then make some analyses and so on connect to the database but it can be done letter 
            db = sql.connect('todo.db')
            c = db.cursor()
            c.execute("""
                      CREATE TABLE IF NOT EXISTS tb_tasks (
                          id_task INTEGER PRIMARY KEY,
                          task VARCHAR(255) NOT NULL,
                          date DATE
                      )
                      """)
            return db
        except Exception as e:
            print(e)
    
    def ReadDatabase(db):
        c = db.cursor()
        # Make sure to name the columns and not select * from ...
        c.execute("SELECT * FROM tb_tasks")
        records = c.fetchall()
        return records
    
    def InsertDatabase(db, values):
        c = db.cursor()
        # Also make sure to use ? for the inputs for security purposes
        c.execute("INSERT INTO tb_tasks (task, date) VALUES (?, ?)", values)
        db.commit()

    def DeleteDatabase(db, value):
        c = db.cursor()
        # Quick note: Here we're assuming that no two task description are the same and as a result we are deleting based on task
        # An ideal app would not do this but instead delete based on the actual immutable database ID. but for the sake of the tutorial and length, we will do it this way 
        c.execute("DELETE FROM tb_tasks WHERE task = ?", value)
        db.commit()
    
    def UpdateDatabase(db, values):
        c = db.cursor()
        # c.execute("UPDATE tb_tasks SET task =  {t}, date = {d} WHERE task = {t}".format(t=values[2], d=values[1]))
        c.execute("UPDATE tb_tasks SET task = ?, date = ? WHERE task = ?", values)
        db.commit()
        
# Now that we have all CRUD function, we can start using the app ...

# Let's create the form class first so we can get some data 
class FormContainer (UserControl):
    # At this point, we can pass in  a function from the main() so we can expand. Minimize the form 
    # Go back to the FormContainer() and add an argument as such 
    def __init__(self, func):
        self.func = func
        super().__init__()
    
    def build(self):
        return Container(
            width=280,
            height=80,
            bgcolor="bluegrey500",
            opacity=0, # change later => change this to 0 and reverse to be 1 when called.
            border_radius=40,
            margin=margin.only(left=-20, right=-20),
            animate=animation.Animation(400, "decelarate"),
            animate_opacity=200,
            padding=padding.only(top=45, bottom=45),
            content=Column(
                horizontal_alignment=CrossAxisAlignment.CENTER,
                controls=[
                    TextField(
                        height= 48,
                        width=255,
                        filled=True,
                        color="black",
                        text_size=12,
                        border_color="transparent",
                        hint_text="Description...",
                        hint_style=TextStyle(size=11, color="black"),
                        on_submit=self.func # pass the function here
                    ),
                    IconButton(
                        content=Text("Add Task"),
                        width=255, 
                        height=44,
                        style=ButtonStyle(
                            bgcolor={"":"blck"},
                            shape={
                                "": RoundedRectangleBorder(radius=8)
                            }
                        ),
                        on_click= self.func # pass the function here
                    )
                ]
            )
        )
        
# Now, we need a class to generate a task when the user adds one 
class CreateTask(UserControl):
    def __init__(self, task: str, date: str, func1, func2):
        # Create two instances arguments so we can pass in the delete function and edit function when we create an instance of it
        self.task = task
        self.date = date
        self.func1 = func1
        self.func2 = func2
        super().__init__()
    
    def TaskDeleteEdit(self, name, color, func):
        return IconButton(
            icon=name,
            width=30,
            icon_size=18,
            icon_color=color,
            opacity=0,
            animate_opacity=200,
            # To use it, we need to keep it in our delete and edit iconbuttons 
            on_click=lambda e: func(self.GetContainerInstance())
        )
    
    # We need a final thing from here, and that is the instance itself
    # We need the instance identifier so that we can delete it needs to be deleted
    def GetContainerInstance(self):
        return self # We return the self instance
    
    
    def ShowIcons(self, e):
        if e.data == "true":
            # these are the indexes of each icon 
            (
            e.control.content.controls[1].controls[0].opacity,
            e.control.content.controls[1].controls[1].opacity
            ) = (1, 1)
            
            e.control.content.update()
        else:
            (
            e.control.content.controls[1].controls[0].opacity,
            e.control.content.controls[1].controls[1].opacity
            ) = (0, 0)
            
            e.control.content.update()
        
    def build(self):
        return Container(
            width=280,
            height=60,
            border=border.all(0.85, "white54"),
            border_radius=8,
            # Let's show the icons when we hover over them
            on_hover=lambda e: self.ShowIcons(e),
            clip_behavior=ClipBehavior.HARD_EDGE,
            padding=10,
            content=Row(
                alignment=MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    Column(
                        spacing=1,
                        alignment=MainAxisAlignment.CENTER,
                        controls=[
                            Text(value=self.task, size=10),
                            Text(value=self.date, size=9, color="white54")
                        ]
                    ),
                    # Icons delete and edit 
                    Row(   
                        spacing=0,
                        alignment=MainAxisAlignment.CENTER,
                        controls=[
                            self.TaskDeleteEdit(
                                icons.DELETE_ROUNDED, 
                                "red500",
                                self.func1
                            ),
                            self.TaskDeleteEdit(
                                icons.EDIT_ROUNDED, 
                                "green500",
                                self.func2
                            ),
                        ]
                    )
                ]
            )
        )


def main(page: Page):
    page.vertical_alignment = alignment.center
    page.horizontal_alignment = alignment.center
    
    page.bgcolor = "#cccccc"
    page.title = "ToDo App done by Monji Oilíta using Flet of Python and Sqlite3"
    page.name
    
    def AddTaskToScreen(e):
        # Now, everytime the user adds a task, we need to fetch the data and output it to the main column
        # there are two data we need: the task and the date 
        #
        datetime = dt.now().strftime("%b %d %Y %I:%M")
        
        # We can use the db here for starters... 
        # First, open a connection to the database 
        db = Database.ConnectToDatabase()
        Database.InsertDatabase(db, (
            form.content.controls[0].value, datetime
        ))
        db.close()
        
        # we could also place the Database funcions within if statment... 
        
        # now recall that we set the form container to form variable. we can use this row to see if there's any content in the textfield 
        if form.content.controls[0].value:
            _main_column_.controls.append(
                # Here we can create an instance of CreateTask() class 
                CreateTask(
                    form.content.controls[0].value,
                    datetime,
                    # now the instances takes two more arguments when called...
                    DeleteFunction,
                    UpdateFunction
                )
            )
            _main_column_.update()
            
            # We can recall the show.hide functon for the form here 
            CreateToDoTask(e)
        else:
            db.close() #Make sure it closes even if there is no user input
    
    def DeleteFunction(e):
        # now the delete of task within the db 
        db = Database.ConnectToDatabase()
        Database.DeleteDatabase(
            db, (e.controls[0].content.controls[0].controls[0].value, )
        )
        # we passed it as (value,) because it needs to be a tuple data type   
        db.close() 
        # delete working 
        
        # Wehn we want to delete, recall that these instances are int the list => so that means we can simply remove them when we want to 
        
        # let's show what e is 
        # so the instance is passed on as e
        _main_column_.controls.remove(e)
        _main_column_.update()   
    
    def UpdateFunction(e):
        # The update needs a little bit more work...
        # We want to update from the form, so we need to pass whatever the user had from the instance back to the form, then change the functions and pass it back again 
        #
        form.height, form.opacity = 200, 1 # Show the form
        (
            form.content.controls[0].value,
            # Here we are changing the button function and name
            # We need to change it from add task to update and so on
            form.content.controls[1].content.value,
            form.content.controls[1].on_click, 
            form.content.controls[1].on_submit
        ) = (
            e.controls[0].content.controls[0].controls[0].value, # this is the instance value of the task
            "Update",
            lambda _: FinalizeUpdate(e),
            lambda _: FinalizeUpdate(e),
        )
        form.update()
    
    def FinalizeUpdate(e):
         # Now finally, we can update the db as well 
        db = Database.ConnectToDatabase()
        Database.UpdateDatabase(
            db,
            (
                # first we need to get the data we want to change
                form.content.controls[0].value,
                dt.now().strftime("%b %d %Y %I:%M"),
                # second, we insert the data to check against (the value this query should look for)
                e.controls[0].content.controls[0].controls[0].value, 
            )
        )
        
        # we can simply reverse the values from above... 
        e.controls[0].content.controls[0].controls[0].value = form.content.controls[
         0
        ].value
        e.controls[0].content.update()
        CreateToDoTask(e)
        
    
    # Function to show/hide form container 
    def CreateToDoTask(e):
        # when we click ADD IconButton 
        if form.height  != 200:
            form.height, form.opacity = 200, 1
            form.update()
        else:
            form.height, form.opacity = 80, 0
            # we can remove the values from the textField too ...
            form.content.controls[0].value = None
            form.content.controls[1].content.value = "Add Text"
            form.content.controls[1].on_click = lambda e: AddTaskToScreen(e)
            form.update()
    
    _main_column_ = Column(
        scroll='hidden',
        expand=True,
        alignment=MainAxisAlignment.START,
        controls=[
            Row(
                alignment=MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    Text("To-Do items", size=18, weight="bold"),
                    IconButton(
                        icons.ADD_CIRCLE_ROUNDED,
                        icon_size=18,
                        on_click= lambda e: CreateToDoTask(e)
                    )
                ]
            ),
            Divider(height=8, color="white24")
        ]
    )
    
    # 
    page.add(
        Container(
            width=1500,
            height=800,
            margin=10,
            bgcolor="bluegrey900",
            alignment=alignment.center,
            content=Row(
                alignment=MainAxisAlignment.CENTER,
                vertical_alignment=CrossAxisAlignment.CENTER,
                controls=[
                    # main container 
                    Container(
                        width=280, 
                        height=600, 
                        bgcolor="#0f0f0f",
                        border_radius=40,
                        border=border.all(0.5, "white"),
                        padding=padding.only(top=35, left=20, right=20),
                        clip_behavior=ClipBehavior.HARD_EDGE,
                        content=Column(
                            alignment=MainAxisAlignment.CENTER,
                            expand= True,
                            controls=[
                                # main column here
                                _main_column_,
                                # Form Class here
                                # pass in the argument for the form class here 
                                FormContainer(lambda e: AddTaskToScreen(e))
                            ]
                        )
                    )
                ]
            )
        )
    )
    
    page.update()
    
    # the form container index is a follows. We can set the long element idnex as a variable so it can be called faster and easier 
    form = page.controls[0].content.controls[0].content.controls[1].controls[0]
    # now we can call form whenever we want to do something with it 
    
    # Now to display it, we need to read the database 
    # Another note: Flet keeps on refreshing when we call the database functions,
    # this could be from my code or from flet itself, but it should be addressed ...
    
    # open connection
    db = Database.ConnectToDatabase()
    # now remember that the readdatabase() function returns the records
    # Note: return is a tuple data type 
    # Note: we may want to display the records in reverse order, meaning the new records first followed by rhe oldest last...
    # using [::-1] reverses a tuple 
    # using [:-1] reverses a list 
    for task in Database.ReadDatabase(db)[::-1]:
        # let's see if the tasks are being saved 
        # lets add these to the screen now 
        _main_column_.controls.append(
            # Same process as before: we create an instance of this class 
            CreateTask(
                task[1],
                task[2],
                DeleteFunction,
                UpdateFunction,
            )
        )
        _main_column_.update()

if __name__ == "__main__":
    flet.app(target=main)
    
# so other changes can be made but the foundnations are working well...
