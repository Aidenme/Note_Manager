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
        '''Uses the head HTML of a contentunit with HTML to determine what value is_dropdown should be.'''
        dropdown_patt = re.compile('<li class="dropdown">')
        if dropdown_patt.search(self.head_html):
            self.is_dropdown = True
        else:
            self.is_dropdown = False

    def set_head_html(self, name, id):
        '''Generates the html for the head part of a contentunit. This only runs if there is not yet any HTML
        defined (a.k.a. when a new contentunit is created). The head type is determined by the value of is_dropdown,
         which is a parameter set when the contentunit is created.'''
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
    '''Takes the html that makes up the contents and converts it to a list of contentsunits. This MUST take only the html
    in the contents div on a notes website page. html in this correct format should get spit out from an html file by
    get_contents_html()'''
    contentsunits_list = []
    for line in html_contents_lines:
        content = convert_to_contentunit(line)
        if content:
            contentsunits_list.append(content)
    return contentsunits_list

def get_dot_number(id, dot):
    split_id = id.split('.')
    if dot == 0:
        bm_cleaned = split_id[0].replace("BM", "")
        return int(bm_cleaned)
    else:
        return int(split_id[dot])

def calc_search_id(some_id):
    calc_id = some_id.replace("BM", "").split('.')
    new_end_num = int(calc_id[-1]) - 1
    if new_end_num == 0:
        calc_id = calc_id[:-1]
    else:
        calc_id[-1] = str(new_end_num)
    return "BM" + '.'.join(calc_id)

def place_contentunit(contentsunits_list, contentunit):
    '''Takes a contentunit and properly places it in a contentsunits_list before returning the list.'''
    i = 0
    split_val = 0
    search_results = []
    units_list_ids = []
    for line in contentsunits_list:
        units_list_ids.append(line.id)
        if line.id == contentunit.id:
            print("Error, ID already in use! Please use a different ID.")
            break
        else:
            search_id = calc_search_id(contentunit.id)
            if search_id in line.id:
                search_results.append(line.id)
            else:
                continue
    print(search_results)
    print(units_list_ids)
    print(units_list_ids.index(search_results[-1]))

def unused_place_contentunit(contentsunits_list, contentunit):
    '''Takes a contentunit and properly places it in a contentsunits_list before returning the list.'''
    i = 0
    split_val = 0
    for line in contentsunits_list:
        if line.id == contentunit.id:
            print("Error, ID already in use! Please use a different ID.")
            break
        else:
            simple_line_id = line.id.replace("BM", "").split('.')
            simple_contentunit_id = contentunit.id.replace("BM", "").split('.')
            if simple_line_id[:-1] == simple_contentunit_id[:-1]:
                print("All but last match at line " + str(i))
                if int(simple_line_id[-1]) == (int(simple_contentunit_id[-1]) - 1):
                    print("Line position should be " + str(i + 1))
                else:
                    i = i + 1
            else:
                i = i + 1

def add_contentunit(contentsunits_list, contentunit):
    '''Takes the entire contentsunits list and adds a contentunit to it. This works to ensure the new contentunit has the
    correct is_dropdown value, which is determined by the ids of neighboring contentunits. It also makes sure the contentunit
    is placed in the correct place in the list.'''
    contentsunits_list = place_contentunit(contentsunits_list, contentunit)


def start_menu():
    print("--------------------Welcome to Contents Generator!--------------------\n")
    print("Please choose an option below")
    print("A - Add a content entry     B - Delete a content entry     C - Quit\n")
    print("CURRENT CONTENTS:")
    for index, contentunit in enumerate(contentsunits_list):
        print(str(index) + (len(contentunit.spaces) * " ") + contentunit.id + " - " + contentunit.name)

    choice = input()
    if choice == 'a':
        print("You chose A")
        add_contentunit(contentsunits_list, create_new_contentunit())
        start_menu()
    elif choice == 'b':
        print("You chose B")
        start_menu()
    elif choice == 'c':
        print("Thanks for using the generator! <3")
        exit()


contentsunits_list = contentunits_from_html(get_contents_html('Python.html'))
start_menu()
