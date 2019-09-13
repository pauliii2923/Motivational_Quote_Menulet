import time
import rumps
import threading
import peewee
import random
import subprocess
from rumps import MenuItem

def ifdo(x,y):
  if x():
    y()

class Peewee:
  create_database=lambda self,name: peewee.SqliteDatabase(name)
  create_table=lambda self,x: x.create_table()
  drop_table=lambda self,x: x.drop_table()
  fields=lambda self: {"foreignkey":peewee.ForeignKeyField,"manytomany":peewee.ManyToManyField,"primarykey":peewee.PrimaryKeyField,"autofield":peewee.AutoField,"char":peewee.CharField,"int":peewee.IntegerField,"float":peewee.FloatField,"bigint":peewee.BigIntegerField,"datetime":peewee.DateTimeField,"blob":peewee.BlobField,}

db = Peewee().create_database("Motivational_Quote_Menulet.db")
class Quote(peewee.Model):
  id,quote=Peewee().fields()["primarykey"](),Peewee().fields()["char"]()
  class Meta:
    database = db


ifdo(lambda:Quote.__name__.lower() not in db.get_tables(),Peewee().create_table(Quote))

dialog_prompt = lambda prompt:subprocess.check_output("""osascript -e 'tell application (path to frontmost application as text)' -e 'with timeout of 30000 seconds -- wait 500 minutes' -e 'display dialog "%s" default answer "" buttons {"OK"}' -e 'end timeout' -e 'end tell'"""%prompt,shell=True).decode()[:-1].split("text returned:")[1]


class Motivational_Quote_Menulet:
  def __init__(self):
    import rumps
    from rumps import MenuItem
    self.app = rumps.App("Motivational Quote Menulet",quit_button=None)
    self.set_menu()
    infiniterange=int(10e100)
    threading.Thread(target=lambda:[[setattr(self.app,"title",random.choice([i.quote for i in Quote.select()] or ["Default Motivational Quote"])),time.sleep(60)] for i in range(infiniterange)]).start()
    self.app.run()

  def set_menu(self):
    self.app.menu.clear()
    self.app.menu = [MenuItem("Add Quote",callback=lambda _=None:[Quote(quote=dialog_prompt("Please enter in your quote!")).save(),self.set_menu()] )]
