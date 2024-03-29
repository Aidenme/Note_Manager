import re

class ContentUnit:
    def __init__(self, name=None, id=None, head_html=None, is_dropdown=False):
        self.name = name
        self.id = id
        self.spaces = "0"
        self.head_html = head_html
        self.is_dropdown = is_dropdown

        self.set_spaces_from_id(self.id)
        self.set_head_html(self.name, self.id)

    def __str__(self):
        return self.spaces + self.name + " - " + self.id

    def print_content(self):
        '''Prints a contentunit's id and name in a nice and organized way. This is used to make the current contents easy to read and understand
        without having to read through html lines.'''
        print(self.spaces + self.name + " - " + self.id)

    def print_html(self):
        '''Prints the html code that makes up the head html of a contentunit'''
        print(self.head_html)

    def set_spaces_from_id(self, id, base_spaces=4, space_multiplier=4, space_char=" "):
        '''Based on an id the tab level of an html line is determined and set. This is only to make the created html lines easier to read
         in the actual html file.'''
        space_count = base_spaces + (self.id.count(".") * space_multiplier)
        self.spaces = space_count * space_char

    def get_space_count_from_html(self):
        '''This determines the tab level of an html line based on the tab level stored in the actual html code. When importing the contents
        this information is stored in order to maintain the tab level of the original contents so when regenerating the contents
        set_spaces_from_id doesn't need to run again.'''
        space_patt = re.compile('(\s+)<li><a href')
        space_results = space_patt.search(self.head_html)
        if space_results:
            return len(space_results.group(1))
        else:
            return 0

    def set_dropdown(self):
        '''Uses the head HTML of a contentunit with HTML to determine what value is_dropdown should be. This runs if a newly created ContentUnit
         is passed html in the creation stage. If that HTML draws a dropdown is_dropdown needs to be "True" if not it needs to be "False"'''
        dropdown_patt = re.compile('<li class="dropdown">')
        if dropdown_patt.search(self.head_html):
            self.is_dropdown = True
        else:
            self.is_dropdown = False

    def set_head_html(self, name, id):
        '''Generates the html for the head part of a contentunit. This will run by default when a new contentunit is created.
        The head type is determined by the class variable "is_dropdown". It can either be html that generates a dropdown or html that
        allows the contentunit head to fit neatly in a list of contents.'''
        if self.is_dropdown == False:
            self.head_html = self.spaces + '<li><a href="#' + id + '">' + name + '</a></li>'
        else:
            self.head_html = self.spaces + '<li class="dropdown"><a href="#' + id + '">' + name + '</a><div id="' + id + 'but" class="twirl_button" onclick="reveal(\'' + id + 'sub\', \'' + id + 'but\')">&#8658;</div><ul id="' + id + 'sub" class="subcontents" style="display:none;">'

class Contents:
    def __init__(self, contents_dict):
        self.html_contents = contents_dict['contents']
        self.notefile_start = contents_dict['start_index']
        self.notefile_end = contents_dict['end_index']
        self.contents = None

        self.convert_from_html(self.html_contents)
        print("Contents Initialized")

    def __getitem__(self, index):
        if index == len(self.contents):
            raise IndexError
        else:
            return self.contents[index]

    def convert_from_html(self, html_contents):
        '''Takes the lines of html that make up the contents and converts it to a list of contentsunits. This MUST take only the html lines
        in the "contents" div in a note html file. get_contents_html searches and returns those lines from a full html file so run that
        first on an html file to get lines that can actually be converted.'''
        contentsunits_list = []
        for line in html_contents:
            content = self.convert_to_contentunit(line)
            if content:
                contentsunits_list.append(content)
        self.contents = contentsunits_list

    def convert_to_contentunit(self, html_line):
        '''When importing an html file with contents the html generating each contents entry needs to be converted to a contentunit object for
        easy processing and storage in the contentunits_list global variable.'''
        search_patt = re.compile('<a href="#(BM(?:\d+\.|\d)+)">([\w\s\&\(\)]+)</a>')
        search_results = search_patt.search(html_line)
        if search_results:
            return ContentUnit(id=search_results.group(1), name=search_results.group(2))

    def calc_search_id(self, some_id):
        '''Takes a contentunit id and returns the id that is expected to come before it in the contents. Once that is determined it is easy to search for
        that id (see function find_id_placement) and then insert the new contentunit beneath it (see function add_contentunit).'''
        calc_id = some_id.replace("BM", "").split('.')
        new_end_num = int(calc_id[-1]) - 1
        if new_end_num == 0:
            calc_id = calc_id[:-1]
        else:
            calc_id[-1] = str(new_end_num)

        return "BM" + '.'.join(calc_id)

    def find_id_placement(self, contentsunits_list, new_id):
        '''Takes a list of contentunits and looks at their ids compared to a new id to determine where that new id should be placed in the contents'''
        search_results = []
        units_list_ids = []
        for line in contentsunits_list:
            units_list_ids.append(line.id)
            if line.id == new_id:
                print("Error, ID already in use! Please use a different ID.")
                break
            else:
                search_id = self.calc_search_id(new_id)
                #This if statements includes length because if it didn't a search id like "BM1" would find
                #everything that starts with BM1 like BM10 or BM11
                if search_id in line.id and len(search_id) == len(line.id):
                    search_results.append(line.id)
                else:
                    continue

        return units_list_ids.index(search_results[-1])

    def add_contentunit(self, id, name):
        '''Takes the entire contentsunits list and adds a contentunit to it. This works to ensure the new contentunit has the
        correct is_dropdown value, which is determined by the ids of neighboring contentunits. It also makes sure the contentunit
        is placed in the correct place in the list.'''
        new_contentunit = ContentUnit(id=id, name=name)
        self.contents.insert((self.find_id_placement(self.contents, new_contentunit.id) + 1), new_contentunit)
        self.convert_to_html(self.contents)

    def generate_dropdowns(self, contents_list):
        '''After creating Content Units with an id that allows them to be properly placed, Content Units that need a dropdown (which
        is based on their id) need to have their is_dropdown variable set and the proper html generated'''
        print("generate_dropdowns ran")
        for i, contentunit in enumerate(contents_list):
            if i + 1 == len(contents_list):
                break
            else:
                #A contentunit must have subcontents if the contentunit id in the line below it is longer than the id in the current contentunit.
                if len(contentunit.id) < len(contents_list[i + 1].id) and contentunit.is_dropdown == False:
                    print("If ran for: " + contentunit.id)
                    contentunit.is_dropdown = True
                    contentunit.set_head_html(contentunit.name, contentunit.id)
        self.contents = contents_list

    def get_last_subcontent_id(self, content_id):
        '''Finds the last id in a dropdown's sublist of contentunit ids. This is used to determine the index in which to insert closing tags
        </ul></li> by putting it under the found id.'''
        subcontent_ids = []
        #define regex pattern as "string that starts with content_id"
        patt = re.compile("(?:" + str(content_id) + "\.\d+)$")
        #Add everything that passes the pattern to the subcontent_ids list
        for content in self.contents:
            match = patt.search(content.id)
            if match:
                subcontent_ids.append(content.id)
            else:
                continue
        #print("Tags go under: " + subcontent_ids[-1])
        return subcontent_ids[-1]

    def convert_to_html(self, contents):
        contents_strings = []
        self.generate_dropdowns(self.contents)

        for i in range(len(self.contents)):
            contents_strings.append(self.contents[i].head_html + '\n')
            current_periods = self.contents[i].id.count(".")
            try:
                next_periods = self.contents[i + 1].id.count(".")
            except:
                self.html_contents = contents_strings
                return
            if current_periods > next_periods:
                closing_count = current_periods - next_periods
                contents_strings.append('</ul></li>\n' * closing_count)

class NoteFile:
    def __init__(self, filename):
        self.note_interface = NoteFileInterface(filename)
        self.contents = Contents(self.note_interface.get_contents())
        print("NoteFile Initialized")

    def add_contents(self):
        '''Prompts the user to enter the information needed to create a new contentunit and returns a complete contentunit'''
        id = input("Please enter an ID")
        name = input("Please enter a name")
        self.contents.add_contentunit(id, name)
        self.note_interface.set_contents(self.contents)
        self.note_interface.save_to_html()

class NoteFileInterface:
    def __init__(self, filename):
        self.filename = filename
        self.html = None

        self.import_file(self.filename)
        print("NoteFileInterface Initialized")

    def import_file(self, filename):
        note_file = open(filename, 'r')
        self.html = note_file.readlines()
        note_file.close()

    def get_contents(self, html=None, start_line='<!--Start contents-->', end_line='<!--End contents-->'):
        '''Searches an html file for the ul that makes up the contents on the top of the page. Once found this will return all the html lines in the
        ul as a dictionary containing "contents": the lines of html, "start_index": the line on which the contents start and "end_index": the line on
        which the contents end.'''
        if html == None:
            html = self.html
        html_contents_dict = {'contents' : [], 'start_index' : None, 'end_index' : None}
        for index, line in enumerate(html):
            if start_line in line:
                html_contents_dict['start_index'] = index
            if end_line in line:
                html_contents_dict['end_index'] = index
                break
        html_contents_dict['contents'] = html[html_contents_dict['start_index']:html_contents_dict['end_index']]

        return html_contents_dict

    def save_to_html(self):
        note_file = open(self.filename, 'w')
        for line in self.html:
            note_file.write(line)
        note_file.close()

    def set_contents(self, contents):
        self.html[contents.notefile_start + 1:contents.notefile_end] = contents.html_contents


def start_menu():
    #global contentsunits_list
    print("--------------------Welcome to Contents Generator!--------------------\n")
    print("Please choose an option below")
    print("A - Add a content entry     B - Delete a content entry      C - Quit\n")
    print("CURRENT CONTENTS:")
    for index, contentunit in enumerate(note_file.contents):
        print(str(index) + (len(contentunit.spaces) * " ") + contentunit.id + " - " + contentunit.name)

    choice = input()
    if choice == 'a':
        note_file.add_contents()
        print("New content entry added!")
        start_menu()
    elif choice == 'b':
        print("You Chose B")
        start_menu()
    elif choice == 'c':
        print("Thank you for using content generator! <3 <3")
        exit()

note_file = NoteFile('Python.html')
start_menu()
