# -------------------------------------------------------
# Overview
# --------------
#
# Building on what we learned last week, we are going to
# create a new 'Character' class that works with the
# upgraded character editor that I have made for you.
# -------------------------------------------------------
import csv


"""
--------------------------------------------------------
 Challenge 1
--------------

Create the empty class itself using the 'class' keyword,
followed by a space, then the name of the class 
(in this case Character). Then finish with a colon :
and press enter
---------------------------------------------------------
"""


""" 
--------------------------------------------------------
Challenge 2
--------------

Define the classes constructor, or __init__ function.
It must take a parameter for the file_path and store it in a
class variable.

Define four more class variables called 'name',
'strength', 'dexterity' and 'intelligence' and
give them sensible default values (e.g. 0 or "none")

HINTS
--------
 - Recall that class functions must pass the 'self' 
   keyword as the first parameter.
 - A class variable is created by starting the variable
   name with 'self' followed by a full stop. e.g.

       'self.my_class_variable'
--------------------------------------------------------
"""

"""
--------------------------------------------------------
Challenge 3
------------
Define two more class functions called 'load' and 'save'.
make these functions load data to our
class variables and save it to a file.

Then see if it all works by running the 'character_creator'
python file!
       
HELPFUL HINTS:

- Use the debugger! If you run the character creator the
  errors you get should help you figure out what you
  still need to add to your character class.
- If you get stuck on how to make a class look at the
  code for almost any of our past projects.
- If you get stuck on the loading and saving functions
  look at last weeks code (I've provided a solution to last 
  weeks challenges in this project).
- You can save and load the character data however you
  like, including using the csv library.
- Use int() and str() to change numbers into strings
  and back again. You will need to do this for the
  characters stat numbers because we save the numbers
  as strings in text files.
-------------------------------------------------------
"""

"""
-------------------------------------------------------
What is a class? - A brief explanation
------------------
We have briefly covered classes before but perhaps you
could use a refresher. A class definition is like the
blueprint or description of a new type of (often)
more complicated variable.

Usually it is composed of several of the built-in data
types (strings, integers, etc) and some functions that
operate on that data.

Organising your code into classes can make it easier to
understand and work with when a program gets larger.

When you create an 'instance' of your class and assign it
a variable it is sometimes called an 'object'. This is
where the name object oriented programming comes from.

I like to think of it the process like IKEA furniture -
there is one Billy bookcase design (this is like the class),
and it is composed of lots of simpler pieces like screws
and lengths of wood (these are like the simple data types).
There are millions of actual Billy bookcases in homes
around the world from that single design (these are like
the objects)
----------------------------------------------------------
"""
