import re

class ContentUnit:
    def __init__(self, name=None, id=None, head_html=None, is_dropdown=False):
        self.name = name
        self.id = id
        self.spaces = "0"
        self.head_html = head_html
        self.is_dropdown = is_dropdown

        self.set_spaces_from_id(self.id)
        if head_html == None:
            #Create the html line. The type depends on the is_dropdown value
            self.set_head_html(self.name, self.id)
        else:
            #Translate variables from the existing html line to create a complete contentunit
            self.set_dropdown()

    def print_content(self):
        print(self.spaces + self.name + " - " + self.id)

    def print_html(self):
        print(self.head_html)

    def set_spaces_from_id(self, id, base_spaces=0, space_multiplier=2, space_char=" "):
        space_count = base_spaces + (self.id.count(".") * space_multiplier)
        self.spaces = space_count * space_char

    def get_space_count_from_html(self):
        space_patt = re.compile('(\s+)<li><a href')
        space_results = space_patt.search(self.head_html)
        if space_results:
            return len(space_results.group(1))
        else:
            return 0

    def set_dropdown(self):
        '''Uses the head HTML of a contentunit with HTML to determine what value is_dropdown should be'''
        dropdown_patt = re.compile('<li class="dropdown">')
        if dropdown_patt.search(self.head_html):
            self.is_dropdown = True
        else:
            self.is_dropdown = False

    def set_head_html(self, name, id):
        '''Generates the html for the head part of a contentunit. This only runs if there is not yet any HTML defined. The head type is determined by the value of is_dropdown'''
        if self.is_dropdown == False:
            self.head_html = self.spaces + '<li><a href="#' + id + '">' + name + '</a></li>'
        else:
            self.head_html = self.spaces + '<li class="dropdown"><a href="#' + id + '">' + name + '</a><div id="BM2but" class="twirl_button" onclick="reveal(\'' + id + 'sub\', \'' + id + 'but\')">&#8658;</div><ul id="' + id + 'sub" class="subcontents" style="display:none;">'

def get_contents_html(filename, start_line='<!--Start contents-->', end_line='<!--End contents-->'):
    note_file = open(filename, 'r')
    content_end = False
    html_contents_lines = []
    x = 0
    in_contents = False
    while 1:
        line = note_file.readline()
        line = line[:-1]
        if start_line in line:
            in_contents = True
        if in_contents == True:
            html_contents_lines.append(line)
        if end_line in line:
            break
        if not line:
            break
    return html_contents_lines

def convert_to_contentunit(html_line):
    search_patt = re.compile('<a href="#(BM(?:\d+\.|\d)+)">([\w\s\&\(\)]+)</a>')
    search_results = search_patt.search(html_line)
    if search_results:
        return ContentUnit(id=search_results.group(1), name=search_results.group(2), head_html=html_line)

def create_new_contentunit():
    id = input("Please enter an ID")
    name = input("Please enter a name")
    return ContentUnit(id=id, name=name)

def contentunits_from_html(html_contents_lines):
    contentsunits_list = []
    for line in html_contents_lines:
        content = convert_to_contentunit(line)
        if content:
            contentsunits_list.append(content)
    return contentsunits_list

def start_menu():
    print("--------------------Welcome to Contents Generator!--------------------\n")
    print("Please choose an option below")
    print("A - Add a content entry     B - Delete a content entry     C - Quit\n")
    print("CURRENT CONTENTS:")
    for contentunit in contentsunits_list:
        print((len(contentunit.spaces) * " ") + contentunit.id + " - " + contentunit.name)

    choice = input()
    if choice == 'a':
        print("You chose A")
        start_menu()
    elif choice == 'b':
        print("You chose B")
        start_menu()
    elif choice == 'c':
        print("Thanks for using the generator! <3")
        exit()

contentsunits_list = contentunits_from_html(get_contents_html('Python.html'))


start_menu()
