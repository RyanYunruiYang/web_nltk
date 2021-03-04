#Choate Honor Pledge: On my honor I have neither given nor received unauthorized help
#Sources: I've probably visited every site on the internet in the quest to figure out what's going wrong.

#Major Challenge: Everytime I renamed my file, a lot of things would go wrong. However, the first 
# time this happened was when I renamed this file to run.py, and I didn't terminate and reboot
#the local hosting of the website, so none of my edits were going through, and I spent 2 hours trying
#to figure out what was wrong. So, I systematically commented out the functions which weren't working
# until I was left with those that worked. At that point, I noticed that these were all old functions
# and realised that the code was probably not updating, so I thought to copy the code, delete the file
# and make a new file, but then I realised that it was a naming issue, reran the code on run.py instead 
# of the old main.py, and everything worked. 
import random
import string
import cherrypy
import os

from nltk_test import imaging, naive_comparison
#from sciwriting import highlight #old function that I wrote in sciwriting.py, cooler to do it with html though

first_per = ['we','i']

def listToString(s): #converts a list to string        
    str1 = ""  
    for ele in s:  
        str1 += ele   
    return str1  

class TextAnalysis(object):
    @cherrypy.expose
    def index(self):#part of cherrypy interface, tells the computer which html file is supposed
        #to be the landing and first page seen
        htmlStr = open("landing.html").read()
        return htmlStr

    @cherrypy.expose
    def text_comparison(self, text1, text2):#this is used to access and include the similarity score calculated from the nltk_test.py file
       x = naive_comparison(text1, text2)
       string2 = open("similarity2.html").read().format(similarity=x)
       return string2

    @cherrypy.expose #used in cherrypy to mark it as something you can put at the end of the url
    def generate(self): #This is used as a gateway to the html for the wordcloud text reception
        # cherrypy.session['saved_string'] = some_string
        
        string2 = open("generate2.html").read()#.format(my_name="[good/thought-provoking]")
        
        return string2
    
    @cherrypy.expose
    def wcloud_display(self,text_unclouded):#this is used to create the word cloud. The imaging() is a 
        #function from nltk_test.py, which creates a new image at a certain adress, and then
        #I display it
        imaging(text_unclouded)
        string_return = open("wcloud-display.html").read()#.format(my_name="[good/thought-provoking]")
        return string_return


    @cherrypy.expose
    def compare(self):#gateway to similarity score html
        string_return = open("compare2.html").read()   #.format(my_name="[good/thought-provoking]")
        return string_return
       
    @cherrypy.expose
    def highlight_pronoun(self):#gateway to pronoun html
       string_r = open("highlight_landing.html").read()#.format(highlighted_text = highlighted)
       return string_r 
    
    @cherrypy.expose
    def display_highlight(self, text_unhigh): #replace personal pronouns with html-highlighted copies 
       stringr = text_unhigh.replace(' I ','<span style="background-color:hotpink;"> I </span> ')
       stringr= stringr.replace(' we ','<span style="background-color:red;">we</span>')
       stringr= stringr.replace('We ','<span style="background-color:red;">We </span>')

       return stringr 


    # @cherrypy.expose
    # def display(self):
    #     return cherrypy.session['saved_string']

if __name__ == '__main__':#driver code to make website
    conf = {
        '/': {
            'tools.sessions.on': True,
            'tools.staticdir.root': os.path.abspath(os.getcwd())
        },
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': './public'
        }
    }
    cherrypy.quickstart(TextAnalysis(),'/',conf)
    # cherrypy.engine.start()
    # cherrypy.engine.block()
