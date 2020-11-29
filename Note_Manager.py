import re

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
        self.html_contents = None
        self.contents_start_index = None
        self.contents_end_index = None
        self.html_deep_list = None
        self.set_html_file(self.html_filename)
        self.get_html_contents(self.html_file)
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

    def get_html_contents(self, html_list):
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
        self.html_contents = html_contents

    def insert_contents(self, contents):
        self.html_file[self.contents_start_index:self.contents_end_index + 1] = contents

    def get_html_deep_list(self, html_file):
        deep_list = []
        section_classes = ['class="linked_sub"', 'class="linked_sec"']
        for line in html_file:
            if any(x in line for x in section_classes):
                deep_list.append(line.strip())
        self.html_deep_list = deep_list

    def change_line(self, index, line_string):
        self.html_file[index] = line_string

    def change_line_id(self, index, new_id):
        line_to_change = self.html_file[index]
        #I've been treating id and href as the same thing, but different patterns need to be used to search for each of them:
        href_search_pattern = 'href="#BM(?:[.][1-9]*)*"'
        id_search_pattern = 'id="BM(?:[.][1-9]*)*"'
        #These are added to whatever results are returned from the regex to get the index of where the id, starting with BM actually starts.
        href_index_mod = 7
        id_index_mod = 4
        search_result = re.search(href_search_pattern, line_to_change)
        if search_result == None:
            search_result = re.search(id_search_pattern, line_to_change)
            span_indexes = search_result.span()
            search_indexes = [span_indexes[0] + id_index_mod, span_indexes[1] - 1]
        else:
            span_indexes = search_result.span()
            search_indexes = [span_indexes[0] + href_index_mod, span_indexes[1] - 1]
        left_string = line_to_change[:search_indexes[0]]
        right_string = line_to_change[search_indexes[1]:]
        modded_line = ''.join([left_string, new_id, right_string])
        self.html_file[index] = modded_line


class Contents:
    def __init__(self, html):
        self.html_contents = html.html_contents
        self.top_contents = None
        self.html_deep_list = html.html_deep_list
        self.deep_list = None
        self.full_list = None
        self.clean_contents_list = []

        self.convert_html_to_contents_list()
        self.set_deep_list()
        self.set_clean_contents_list()

    def convert_contents_list_to_html(self):
        html_list = []
        html_list.append('<ul class="contents">')
        for item in self.top_contents:
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
            sudo_list.append({'type' : type , 'id' : id, 'content' : content })
        self.top_contents = sudo_list

    def set_contents_from_clist(self, contents_list):
        self.top_contents = contents_list
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
            sudo_list.append({'id' : id, 'content' : content, 'type' : 'sec_link'})
        self.deep_list = sudo_list

    def set_clean_contents_list(self):
        for line in self.top_contents:
            if line['type'] == 'dropdown_ul' or line['type'] == 'link_line':
                self.clean_contents_list.append(line)

    def print_contents_list(self):
        if self.clean_contents_list is not None:
            for line in self.clean_contents_list:
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

class Display:
    def __init__(self):
        self.display = []
        self.add_display_menu()

    def display_the_lists(self, list_1, list_2):
        list_display = []
        short_list_strings = []

        if len(list_1) >= len(list_2):
            long_list = list_1
            short_list = list_2
        else:
            long_list = list_2
            short_list = list_1

        i = 0
        while i <= len(long_list):
            if i < len(short_list):
                short_string = self.clean_content_dict(short_list[i])
            else:
                short_string = " "
            short_list_strings.append(short_string)
            i += 1

        i = 0
        while i < len(long_list):
            self.display.append(self.clean_content_dict(long_list[i]).ljust(100) + short_list_strings[i].ljust(100))
            i += 1

    def add_display_menu(self):
        self.display.append("Welcome to Contents Manager! What would you like to do?")
        self.display.append("c - Change a line's ID (Not functioning)")

    def print_display(self):
        for line in self.display:
            print(line)

    def clean_content_dict(self, content_dict):
        if content_dict['type'] == 'sec_link':
            return content_dict['id'][4:-1] + " - " + content_dict['content']
        elif content_dict['type'] == 'link_line' or 'dropdown_ul':
            return content_dict['id'][7:-1] + " - " + content_dict['content']
        else:
            return "Wrong type for clean_content_dict()"



html_file = HTMLFile("Python2.html")
writer = HTMLWriter("New_Html.html")
contents = Contents(html_file)
display = Display()
display.display_the_lists(contents.deep_list, contents.clean_contents_list)
display.print_display()
#contents.set_contents_from_clist(sudo_list)
#html_file.insert_contents(contents.html_contents)
writer.write_html_file(html_file)
