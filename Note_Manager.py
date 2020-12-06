import re

class HTMLWriter:
    def __init__(self, filename):
        self.file_to_write = None
        self.filename = filename

    def write_html_file(self, html_file):
        with open(self.filename, mode='a') as y:
            for line in html_file.html_file:
                y.write(line + '\n')

    def write_htmlfile_dict_list(self, html_file):
        with open(self.filename, mode='a') as y:
            for line in html_file.html_dict_list:
                y.write((line['spaces'] * ' ') + line['raw_string'] + '\n')

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
            html_dict_line = {'raw_string' : line.strip(), 'line_index' : index + 1, 'contents_id' : self.get_contents_id(line), 'content' : self.get_content_from_line(line), 'spaces' : len(line) - len(line.lstrip()), 'type' : None, 'paired' : False}
            html_dict_line['type'] = self.set_type(html_dict_line)
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
            id = id_search[0][4:-1]
        return id

    def get_href_from_line(self, line):
        href_search_pattern = 'href="#BM(?:[.][1-9]*)*"'
        regex_href = re.findall(href_search_pattern, line)
        if regex_href == []:
            href = 'No href'
        else:
            href = regex_href[0][7:-1]
        return href

    def get_content_from_line(self, line):
        content_regex_pattern = '>([ a-zA-Z1-9.]*)</'
        regex_content = re.findall(content_regex_pattern, line)
        if regex_content == []:
            content = 'No Content'
        else:
            content = regex_content[0]
        return content

    def set_type(self, dict_line):
        if dict_line['contents_id'] != 'No ID':
            if 'href="#BM' in dict_line['raw_string']:
                type = 'top_contents_link'
            else:
                type = 'body_contents_link'
        else:
            type = None
        return type

    def print_html_dict_list(self):
        for line in self.html_dict_list:
            print(line)

class Contents:
    def __init__(self, html_file):
        self.contents_indexes = self.get_contents_indexes(html_file)
        self.top_links = self.get_top_links(html_file, self.contents_indexes)
        self.body_links = self.get_body_links(html_file, self.contents_indexes[1])
        self.top_body_pairs = self.pair_links(self.top_links, self.body_links)

    def get_top_links(self, html_file, content_indexes):
        top_links = []
        content_start_string = '<ul class="contents">'
        content_end_string = '</ul><!--End contents-->'
        start_index = None
        end_index = None
        for dict in html_file.html_dict_list[content_indexes[0]:content_indexes[1]]:
            if dict['type'] == 'top_contents_link':
                top_links.append(dict)
        return top_links

    def get_body_links(self, html_file, search_start_index):
        body_links = []
        for dict in html_file.html_dict_list[search_start_index:]:
            if dict['type'] == 'body_contents_link':
                body_links.append(dict)
        return body_links

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

    def pair_links(self, top_links, body_links):
        pair_links = []
        for top_line in top_links:
            search_id = top_line['contents_id']
            for body_line in body_links:
                if body_line['contents_id'] == search_id:
                    pair_links.append({ 'top_link' : top_line, 'body_link' : body_line})
        return pair_links

    def print_top_links(self):
        for line in self.top_links:
            print(line)

    def print_body_links(self):
        for line in self.body_links:
            print(line)

    def print_top_body_pairs(self):
        for line in self.top_body_pairs:
            print(line)

class ContentManager:
    def __init__(self, html_file, contents_file):
        self.html_file = html_file
        self.contents_file = contents_file

    def run(self):
        self.print_menu()
        self.display_the_lists(self.contents_file.top_links, self.contents_file.body_links)
        input = self.get_user_input()
        if input == 'c':
            self.change_line_id()
        elif input == 'x':
            exit()
        self.get_user_input()

    def print_menu(self):
        print("Welcome to Contents Manager! What would you like to do?")
        print("a - Add a new link")
        print("c - Change an ID")
        print("x - Exit")

    def display_the_lists(self, top_contents, body_contents):
        list_display = []
        clean_top_contents = []
        clean_body_contents = []
        list_difference = abs(len(top_contents) - len(body_contents))

        for x, line in enumerate(top_contents):
            top_contents[x] = str(line['line_index']) + " - " + line['contents_id'] + " - " + line['content']
        for x, line in enumerate(body_contents):
            body_contents[x] = str(line['line_index']) + " - " + line['contents_id'] + " - " + line['content']

        #In theory these lists should be the same length at all times, but if they aren't blank spaces will be added to the end of the list
        if len(top_contents) >= len(body_contents):
            body_contents.extend([' '] * list_difference)
        else:
            top_contents.extend([' '] * list_difference)
        i = 0
        while i < len(top_contents):
            print(top_contents[i].ljust(100) + body_contents[i].ljust(100))
            i += 1

    def get_user_input(self, input_message="Make a selection"):
        input = raw_input(input_message)
        return input

    def simplify_id(self, contents_id):
        regex_pattern = 'BM(?:[.][1-9]*)*'
        re_result = re.findall(regex_pattern, contents_id)
        if re_result != []:
            return re_result[0]
        else:
            return "Could not simplify"


html_file = HTMLFile("Python2.html")
contents = Contents(html_file)
contents.print_top_body_pairs()
#content_mod = ContentManager(html_file, contents)
#content_mod.run()
#writer = HTMLWriter("New_Html.html")
