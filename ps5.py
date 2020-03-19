# 6.0001/6.00 Problem Set 5 - RSS Feed Filter
# Name: Tracey Mai
# Collaborators:
# Time:

import feedparser
import string
import time
import threading
from project_util import translate_html
from mtTkinter import *
from datetime import datetime
import pytz


#-----------------------------------------------------------------------

#======================
# Code for retrieving and parsing
# Google and Yahoo News feeds
# Do not change this code
#======================

def process(url):
    """
    Fetches news items from the rss url and parses them.
    Returns a list of NewsStory-s.
    """
    feed = feedparser.parse(url)
    entries = feed.entries
    ret = []
    for entry in entries:
        guid = entry.guid
        title = translate_html(entry.title)
        link = entry.link
        description = translate_html(entry.description)
        pubdate = translate_html(entry.published)

        try:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %Z")
            pubdate.replace(tzinfo=pytz.timezone("GMT"))
          #  pubdate = pubdate.astimezone(pytz.timezone('EST'))
          #  pubdate.replace(tzinfo=None)
        except ValueError:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %z")

        newsStory = NewsStory(guid, title, description, link, pubdate)
        ret.append(newsStory)
    return ret

#======================
# Data structure design
#======================

# Problem 1

# TODO: NewsStory
class NewsStory(object):
    def __init__(self, guid, title, description, link, pubdate):
        self.guid = guid
        self.title = title
        self.description = description
        self.link = link
        self.pubdate = pubdate
    def get_guid(self):
        return self.guid
    def get_title(self):
        return self.title
    def get_description(self):
        return self.description
    def get_link(self):
        return self.link
    def get_pubdate(self):
        return self.pubdate

#======================
# Triggers
#======================

class Trigger(object):
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        # DO NOT CHANGE THIS!
        raise NotImplementedError

# PHRASE TRIGGERS

# Problem 2
# TODO: PhraseTrigger
class PhraseTrigger(Trigger):
    def __init__(self, phrase):
        phrase = phrase.lower()
        self.phrase = phrase
    def is_phrase_in(self, text):
        phrase = self.phrase
        phrase = phrase.lower()
        text = text.lower()
        strip_text = string.punctuation + " "
        for char in text:
            if char in strip_text:
                text = text.replace(char, " ")
        text_list = text.split(" ")
        new_list = []
        for ele in text_list:
            if ele != '':
                new_list.append(ele)
        phrase_list = phrase.split()
        for ele in phrase_list:
            if ele not in new_list:
                return False
        text_phrase = " ".join(new_list)
        phrase = " ".join(phrase_list)
        if phrase in text_phrase:
            return True
        return False
        
        
# Problem 3
# TODO: TitleTrigger
class TitleTrigger(PhraseTrigger):
    def __init__(self, phrase):
        PhraseTrigger.__init__(self, phrase)
    def evaluate(self, news_item):
        title = news_item.get_title()
        trigger_or_not = self.is_phrase_in(title)
        return trigger_or_not
# Problem 4
# TODO: DescriptionTrigger
class DescriptionTrigger(PhraseTrigger):
    def __init__(self, phrase):
        PhraseTrigger.__init__(self, phrase)
    def evaluate(self, news_item):
        description = news_item.get_description()
        trigger_or_not = self.is_phrase_in(description)
        return trigger_or_not
# TIME TRIGGERS
# Problem 5
# TODO: TimeTrigger
# Constructor:
#        Input: Time has to be in EST and in the format of "%d %b %Y %H:%M:%S".
#        Convert time from string to a datetime before saving it as an attribute.
class TimeTrigger(Trigger):
    def __init__(self, est_string):
        time = datetime.strptime(est_string, "%d %b %Y %H:%M:%S")
        self.time = time


# Problem 6
# TODO: BeforeTrigger and AfterTrigger
class BeforeTrigger(TimeTrigger):
    def evaluate(self, news_story):
        try:
            condition = news_story.get_pubdate() < self.time
        except:
            self.time = self.time.replace(tzinfo = pytz.timezone("EST"))
            condition = news_story.get_pubdate() < self.time
        if condition:
            return True
        else:
            return False
        


class AfterTrigger(TimeTrigger):
     def evaluate(self, news_story):
        try:
            condition = news_story.get_pubdate() > self.time
        except:
            self.time = self.time.replace(tzinfo = pytz.timezone("EST"))
            condition = news_story.get_pubdate() > self.time
        if condition:
            return True
        else:
            return False


# COMPOSITE TRIGGERS

# Problem 7
# TODO: NotTrigger
class NotTrigger(Trigger):
    def __init__(self, another_trigger):
        self.another_trigger = another_trigger
    def evaluate(self, news_story):
        if not self.another_trigger.evaluate(news_story):
            return True
        else:
            return False
# Problem 8
# TODO: AndTrigger
class AndTrigger(Trigger):
    def __init__(self, trigger1, trigger2):
        self.trigger1 = trigger1
        self.trigger2 = trigger2
    def evaluate(self, news_story):
        if self.trigger1.evaluate(news_story) and self.trigger2.evaluate(news_story):
            return True
        else:
            return False

# Problem 9
# TODO: OrTrigger
class OrTrigger(Trigger):
    def __init__(self, trigger1, trigger2):
        self.trigger1 = trigger1
        self.trigger2 = trigger2
    def evaluate(self, news_story):
        if self.trigger1.evaluate(news_story) or self.trigger2.evaluate(news_story):
            return True
        else:
            return False

#======================
# Filtering
#======================

# Problem 10
def filter_stories(stories, triggerlist):
    """
    Takes in a list of NewsStory instances.

    Returns: a list of only the stories for which a trigger in triggerlist fires.
    """
    # TODO: Problem 10
    # This is a placeholder
    # (we're just returning all the stories, with no filtering)
    fired_stories = []
    for story in stories:
        for trigger in triggerlist:
            if trigger.evaluate(story):
                fired_stories.append(story)
    return fired_stories



#======================
# User-Specified Triggers
#======================
# Problem 11
def read_trigger_config(filename):
    """
    filename: the name of a trigger configuration file

    Returns: a list of trigger objects specified by the trigger configuration
        file.
    """
    # We give you the code to read in the file and eliminate blank lines and
    # comments. You don't need to know how it works for now!
    trigger_file = open(filename, 'r')
    lines = []
    for line in trigger_file:
        line = line.rstrip()
        if not (len(line) == 0 or line.startswith('//')):
            lines.append(line)

    # TODO: Problem 11
    # line is the list of lines that you need to parse and for which you need
    # to build triggers

    triggerlist = []
    triggerdict = {}
    for line in lines:
        if not line.startswith("ADD"): # line describes a trigger to be created
            ele_list = line.split(",")
            trigger = identify_trigger(ele_list, triggerdict)
            if ele_list[0] not in triggerdict:
                triggerdict[ele_list[0]] = trigger
        else: # line to add 2 specified triggers
            ele_list = line.split(",")
            for index in range(1, len(ele_list)):
                trigger_name = ele_list[index]
                triggerlist.append(triggerdict[trigger_name])
    return triggerdict
            
            
def identify_trigger(ele_list, triggerdict):
    type_of_trigger = ele_list[1]
    if type_of_trigger == "TITLE":
        return TitleTrigger(ele_list[2])
    elif type_of_trigger == "DESCRIPTION":
        return DescriptionTrigger(ele_list[2])
    elif type_of_trigger == "AFTER":
        return AfterTrigger(ele_list[2])
    elif type_of_trigger == "BEFORE":
        return BeforeTrigger(ele_list[2])
    elif type_of_trigger == "NOT":
        return NotTrigger(triggerdict[ele_list[2]])
    elif type_of_trigger == "AND":
        return AndTrigger(triggerdict[ele_list[2]], triggerdict[ele_list[3]])
    elif type_of_trigger == "OR":
        return OrTrigger(triggerdict[ele_list[2]], triggerdict[ele_list[3]])
    
    


SLEEPTIME = 120 #seconds -- how often we poll

def main_thread(master):
    # A sample trigger list - you might need to change the phrases to correspond
    # to what is currently in the news
    try:
        t1 = TitleTrigger("election")
        t2 = DescriptionTrigger("Trump")
        t3 = DescriptionTrigger("Clinton")
        t4 = AndTrigger(t2, t3)
        triggerlist = [t1, t4]

        # Problem 11
        # TODO: After implementing read_trigger_config, uncomment this line 
        # triggerlist = read_trigger_config('triggers.txt')
        
        # HELPER CODE - you don't need to understand this!
        # Draws the popup window that displays the filtered stories
        # Retrieves and filters the stories from the RSS feeds
        frame = Frame(master)
        frame.pack(side=BOTTOM)
        scrollbar = Scrollbar(master)
        scrollbar.pack(side=RIGHT,fill=Y)

        t = "Google & Yahoo Top News"
        title = StringVar()
        title.set(t)
        ttl = Label(master, textvariable=title, font=("Helvetica", 18))
        ttl.pack(side=TOP)
        cont = Text(master, font=("Helvetica",14), yscrollcommand=scrollbar.set)
        cont.pack(side=BOTTOM)
        cont.tag_config("title", justify='center')
        button = Button(frame, text="Exit", command=root.destroy)
        button.pack(side=BOTTOM)
        guidShown = []
        def get_cont(newstory):
            if newstory.get_guid() not in guidShown:
                cont.insert(END, newstory.get_title()+"\n", "title")
                cont.insert(END, "\n---------------------------------------------------------------\n", "title")
                cont.insert(END, newstory.get_description())
                cont.insert(END, "\n*********************************************************************\n", "title")
                guidShown.append(newstory.get_guid())

        while True:

            print("Polling . . .", end=' ')
            # Get stories from Google's Top Stories RSS news feed
            stories = process("http://news.google.com/news?output=rss")

            # Get stories from Yahoo's Top Stories RSS news feed
            stories.extend(process("http://news.yahoo.com/rss/topstories"))

            stories = filter_stories(stories, triggerlist)

            list(map(get_cont, stories))
            scrollbar.config(command=cont.yview)


            print("Sleeping...")
            time.sleep(SLEEPTIME)

    except Exception as e:
        print(e)


if __name__ == '__main__':
    root = Tk()
    root.title("Some RSS parser")
    t = threading.Thread(target=main_thread, args=(root,))
    t.start()
    root.mainloop()

