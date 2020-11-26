import re

sudo_list = [
['link_line', 'BM.1', 'Variable assignment'],
['dropdown_ul', 'BM.2', 'Numbers'],
['link_line', 'BM.2.1', 'Number Data Types'],
['end_dropdown_ul']
]

class HTMLWriter:
    def __init__(self, filename):
        self.file_to_write = None
        self.filename = filename

    def write_html_file(self, html_file):
        with open(self.filename, mode='a') as y:
            for line in html_file.html_file:
                y.write(line + '\n')

class HTMLFile:
    def __init__(self, html_filename):
        self.html_filename = html_filename
        self.html_file = None
        self.contents = None
        self.contents_start_index = None
        self.contents_end_index = None
        self.html_deep_list = None
        self.set_html_file(self.html_filename)
        self.get_contents(self.html_file)
        self.get_html_deep_list(self.html_file)

    def set_html_file(self, html_filename):
        print("set_html_file ran")
        the_file = []
        global html_file
        with open(html_filename) as f:
            for line in f:
                the_file.append(line.rstrip())
        self.html_file = the_file

    def print_html_file(self):
        for item in self.html_file:
            print(item)

    def get_contents(self, html_list):
        html_contents = []
        content_start_string = '<ul class="contents">'
        content_end_string = '</ul><!--End contents-->'
        start_index = None
        end_index = None
        for index, item in enumerate(html_list):
            if content_start_string in item:
                print("if statement ran")
                self.contents_start_index = index
                start_index = index + 1
            if content_end_string in item:
                self.contents_end_index = index
                end_index = index - 1
                break
        html_contents = html_list[start_index:(end_index + 1)]
        self.contents = html_contents

    def insert_contents(self, contents):
        self.html_file[self.contents_start_index:self.contents_end_index + 1] = contents

    def get_html_deep_list(self, html_file):
        deep_list = []
        section_classes = ['class="linked_sub"', 'class="linked_sec"']
        for line in html_file:
            if any(x in line for x in section_classes):
                deep_list.append(line.strip())
        self.html_deep_list = deep_list

class Contents:
    def __init__(self, contents):
        self.html_contents = contents.contents
        self.contents_list = None
        self.html_deep_list = contents.html_deep_list
        self.deep_list = None
        self.full_list = None

        self.convert_html_to_contents_list()
        self.set_deep_list()
        self.set_full_list()

    def convert_contents_list_to_html(self):
        html_list = []
        html_list.append('<ul class="contents">')
        for item in self.contents_list:
            if item[0] == 'link_line':
                line = '<li><a href="#' + item[1] + '">' + item[2] + '</a></li>'
                html_list.append(line)
            elif item[0] == 'dropdown_ul':
                line = '<li><a href="#' + item[1] + '">' + item[2] + '</a><div id="'+ item[1] + 'but" class="twirl_button" onclick="reveal(\'' + item[1] + 'sub\', \'' + item[1] + 'but\')">&#8658;</div><ul id="' + item[1] + 'sub" class="subcontents" style="display:none;">'
                html_list.append(line)
            elif item[0] == 'end_dropdown_ul':
                line = '</ul></li>'
                html_list.append(line)
        html_list.append('</ul><!--End contents-->')
        self.html_contents = html_list

    def convert_html_to_contents_list(self):
        sudo_list = []
        id_regex_pattern = 'href="#BM(?:[.][1-9]*)*"'
        content_regex_pattern = '>([ a-zA-Z1-9.]*)</a>'
        for line in self.html_contents:
            try:
                id = re.findall(id_regex_pattern, line)[0]
            except:
                id = 'No id'
            try:
                content = re.findall(content_regex_pattern, line)[0]
            except:
                content = 'No content'
            type = 'link_line'
            trimmed_line = line.strip()
            if 'class="subcontents"' in trimmed_line:
                type = 'dropdown_ul'
            if '</ul></li>' in trimmed_line:
                type = 'end_dropdown_ul'

            if content == 'No content':
                sudo_list.append([type])
            else:
                sudo_list.append([type, id, content])
        self.contents_list = sudo_list

    def set_contents_from_clist(self, contents_list):
        self.contents_list = contents_list
        self.convert_contents_list_to_html()

    def set_deep_list(self):
        sudo_list = []
        id_regex_pattern = 'id="BM(?:[.][1-9]*)*"'
        content_regex_pattern = '>([ a-zA-Z1-9.]*)</h'
        for line in self.html_deep_list:
            try:
                id = re.findall(id_regex_pattern, line)[0]
            except:
                id = 'No id'
            try:
                content = re.findall(content_regex_pattern, line)[0]
            except:
                content = 'No content'
            sudo_list.append([id, content])
        self.deep_list = sudo_list

    def print_contents_list(self):
        if self.contents_list is not None:
            for line in self.contents_list:
                print(line)

    def print_html_contents(self):
        for line in self.html_contents:
            print(line)

    def print_html_deep_list(self):
        for line in self.html_deep_list:
            print(line)

    def print_deep_list(self):
        for line in self.deep_list:
            print(line)

html_file = HTMLFile("Python2.html")
writer = HTMLWriter("New_Html.html")
contents = Contents(html_file)
contents.print_deep_list()
#contents.set_contents_from_clist(sudo_list)
#html_file.insert_contents(contents.html_contents)
#writer.write_html_file(html_file)
