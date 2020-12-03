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
        self.html_file = self.get_html_file(html_filename)
        self.html_dict_list = self.get_html_dict_list(self.html_file)

    def get_html_file(self, html_filename):
        the_file = []
        with open(html_filename) as f:
            for line in f:
                the_file.append(line)
        return the_file

    def print_html_file(self):
        for item in self.html_file:
            print(item)

    def get_html_dict_list(self, html_file):
        html_dict_list = []
        for index, line in enumerate(html_file):
            html_dict_line = {'raw_string' : line.strip(), 'line_index' : index + 1, 'contents_id' : self.get_contents_id(line), 'content' : self.get_content_from_line(line), 'spaces' : len(line) - len(line.lstrip()), 'type' : None}
            html_dict_line['type'] = self.get_type(html_dict_line)
            html_dict_list.append(html_dict_line)
        return html_dict_list

    def get_contents_id(self, line):
        contents_id = self.get_href_from_line(line)
        if contents_id == 'No href':
            contents_id = self.get_id_from_line(line)
        return contents_id

    def get_id_from_line(self, line):
        id_search_pattern = 'id="BM(?:[.][1-9]*)*"'
        id_search = re.findall(id_search_pattern, line)
        if id_search == []:
            id = 'No ID'
        else:
            id = id_search[0]
        return id

    def get_href_from_line(self, line):
        href_search_pattern = 'href="#BM(?:[.][1-9]*)*"'
        regex_href = re.findall(href_search_pattern, line)
        if regex_href == []:
            href = 'No href'
        else:
            href = regex_href[0]
        return href

    def get_content_from_line(self, line):
        content_regex_pattern = '>([ a-zA-Z1-9.]*)</'
        regex_content = re.findall(content_regex_pattern, line)
        if regex_content == []:
            content = 'No Content'
        else:
            content = regex_content[0]
        return content

    def get_type(self, dict_line):
        if dict_line['contents_id'] != 'No ID':
            type = 'linked_contents'
        else:
            type = None
        return type

    def insert_contents(self, contents):
        self.html_file[self.contents_start_index:self.contents_end_index + 1] = contents

    def get_html_body_contents(self, html_file):
        deep_list = []
        section_classes = ['class="linked_sub"', 'class="linked_sec"']
        for line in html_file:
            if any(x in line for x in section_classes):
                deep_list.append(line.strip())
        self.html_body_contents = deep_list

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

    def print_html_dict_list(self):
        for line in self.html_dict_list:
            print(line)

class Contents:
    def __init__(self, html_file):
        self.contents_indexes = self.get_contents_indexes(html_file)
        self.top_links = self.get_top_links(html_file, self.contents_indexes)
        self.body_links = None
        self.all_links = None
        self.ref_id = 0

    def get_top_links(self, html_file, content_indexes):
        top_links = []
        content_start_string = '<ul class="contents">'
        content_end_string = '</ul><!--End contents-->'
        start_index = None
        end_index = None
        for dict in html_file.html_dict_list[content_indexes[0]:content_indexes[1]]:
            if dict['type'] == 'linked_contents':
                top_links.append(dict)
        return top_links

    def get_contents_indexes(self, html_file):
        content_start_string = '<ul class="contents">'
        content_end_string = '</ul><!--End contents-->'
        start_index = None
        end_index = None
        for dict in html_file.html_dict_list:
            if dict['raw_string'] == content_start_string:
                start_index = dict['line_index']
            if dict['raw_string'] == content_end_string:
                end_index = dict['line_index']
                break
        return (start_index, end_index)

    def get_html_from_top_contents(self):
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
        self.html_top_contents = html_list

    def set_top_contents(self):
        sudo_list = []
        id_regex_pattern = 'href="#BM(?:[.][1-9]*)*"'
        content_regex_pattern = '>([ a-zA-Z1-9.]*)</a>'
        for line in self.html_top_contents:
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
            sudo_list.append({'type' : type , 'id' : id, 'content' : content , 'ref_id' : str(self.ref_id)})
            self.ref_id += 1
        self.top_contents = sudo_list

    def set_contents_from_clist(self, contents_list):
        self.top_contents = contents_list
        self.convert_contents_list_to_html()

    def set_body_contents(self):
        sudo_list = []
        id_regex_pattern = 'id="BM(?:[.][1-9]*)*"'
        content_regex_pattern = '>([: a-zA-Z1-9.]*)</h'
        for line in self.html_body_contents:
            try:
                id = re.findall(id_regex_pattern, line)[0]
            except:
                id = 'No id'
            try:
                content = re.findall(content_regex_pattern, line)[0]
            except:
                content = 'No content'
            sudo_list.append({'id' : id, 'content' : content, 'type' : 'sec_link', 'ref_id' : str(self.ref_id)})
            self.ref_id += 1
        self.body_contents = sudo_list

    def set_top_contents_links_only(self):
        for line in self.top_contents:
            if line['type'] == 'dropdown_ul' or line['type'] == 'link_line':
                self.top_contents_links_only.append(line)

    def set_link_list(self):
        full_list = []
        for item in self.top_contents_links_only:
            full_list.append(item)
        for item in self.body_contents:
            full_list.append(item)

    def print_top_links(self):
        for line in self.top_links:
            print(line)

    def print_html_contents(self):
        for line in self.html_top_contents:
            print(line)

    def print_html_body_contents(self):
        for line in self.html_body_contents:
            print(line)

    def print_deep_list(self):
        for line in self.body_contents:
            print(line)

class Display:
    def __init__(self, html_file, contents_file):
        self.html_file = html_file
        self.contents_file = contents_file
        self.display = []
        self.add_display_menu()

    def run(self):
        input = self.get_user_input()
        if input == 'c':
            self.change_line_id()
        elif input == 'x':
            exit()
        self.get_user_input()

    def change_line_id(self):
        ref_id = self.get_user_input("Select a ref id")
        for item in self.contents_file.link_list:
            if item['ref_id'] == ref_id:
                pass

    def display_the_lists(self, top_contents, body_contents):
        list_display = []
        clean_top_contents = []
        clean_body_contents = []
        list_difference = abs(len(top_contents) - len(body_contents))

        for x, line in enumerate(top_contents):
            top_contents[x] = self.clean_content_dict(line)
        for x, line in enumerate(body_contents):
            body_contents[x] = self.clean_content_dict(line)

        #In theory these lists should be the same length at all times, but if they aren't blank spaces will be added to the end of the list
        if len(top_contents) >= len(body_contents):
            body_contents.extend([' '] * list_difference)
        else:
            top_contents.extend([' '] * list_difference)
        i = 0
        while i < len(top_contents):
            self.display.append(top_contents[i].ljust(100) + body_contents[i].ljust(100))
            i += 1

    def add_display_menu(self):
        self.display.append("Welcome to Contents Manager! What would you like to do?")
        self.display.append("a - Add a new link")
        self.display.append("c - Change an ID")
        self.display.append("x - Exit")

    def print_display(self):
        for line in self.display:
            print(line)

    def clean_content_dict(self, content_dict):
        if content_dict['type'] == 'sec_link':
            return content_dict['ref_id'] + " - " + content_dict['id'][4:-1] + " - " + content_dict['content']
        elif content_dict['type'] == 'link_line' or 'dropdown_ul':
            return content_dict['ref_id'] + " - " + content_dict['id'][7:-1] + " - " + content_dict['content']
        else:
            return "Wrong type for clean_content_dict()"

    def get_user_input(self, input_message="Make a selection"):
        input = raw_input(input_message)
        return input

html_file = HTMLFile("Python2.html")
contents = Contents(html_file)
#html_file.print_html_dict_list()
contents.print_top_links()
writer = HTMLWriter("New_Html.html")
