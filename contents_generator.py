import re

class ContentUnit:
    def __init__(self, name=None, id=None, head_html=None):
        self.name = name
        self.id = id
        self.head_html = head_html
        self.is_dropdown = self.get_dropdown()
        self.spaces = self.get_spaces_from_id()

    def print_content(self):
        print(" " * self.spaces + self.name + " - " + self.id)

    def print_html(self):
        print(self.head_html)

    def get_spaces_from_id(self, base_spaces=6, space_multiplier=2):
        print("get_spaces_from_id ran")
        return base_spaces + (self.id.count(".") * space_multiplier)

    def get_space_count_from_html(self):
        space_patt = re.compile('(\s+)<li><a href')
        space_results = space_patt.search(self.head_html)
        if space_results:
            return len(space_results.group(1))
        else:
            return 0

    def get_dropdown(self):
        dropdown_patt = re.compile('<li class="dropdown">')
        if dropdown_patt.search(self.head_html):
            return True
        else:
            return False

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
    return ContentUnit(id=id, name=name, head_html=create_head_html(id, name))

def create_head_html(id, name, dropdown=False):
    if dropdown == False:
        head_html = '<li><a href="#' + id + '">' + name + '</a></li>'
    else:
        head_html = '<li class="dropdown"><a href="#' + id + '">' + name + '</a><div id="BM2but" class="twirl_button" onclick="reveal(\'' + id + 'sub\', \'' + id + 'but\')">&#8658;</div><ul id="' + id + 'sub" class="subcontents" style="display:none;">'
    return head_html

print("Welcome to Contents Generator!")
html_contents_lines = get_contents_html('Python.html')
contentsunits_list = []
for line in html_contents_lines:
    content = convert_to_contentunit(line)
    if content:
        contentsunits_list.append(content)

contentsunits_list.append(create_new_contentunit())

for content in contentsunits_list:
    print(content.head_html)
    print(content.is_dropdown)
