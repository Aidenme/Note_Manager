import re

sudo_list = [
['link_line', 'BM.1', 'Variable assignment'],
['dropdown_ul', 'BM.2', 'Numbers'],
['link_line', 'BM.2.1', 'Number Data Types'],
['end_dropdown_ul']
]

class HTMLFile:
    def __init__(self, html_filename):
        self.html_filename = html_filename
        self.html_file = self.set_html_file(self.html_filename)
        self.contents = self.get_contents(self.html_file)

    def set_html_file(self, html_filename):
        the_file = []
        global html_file
        with open(html_filename) as f:
            for line in f:
                the_file.append(line.rstrip())
        return the_file

    def print_html_file(self, html_list):
        for item in html_list:
            print(item)

    def get_contents(self, html_list):
        html_contents = []
        content_start_string = '<ul class="contents">'
        content_end_string = '</ul><!--End contents-->'
        start_index = None
        end_index = None
        for index, item in enumerate(html_list):
            if content_start_string in item:
                start_index = index + 1
            if content_end_string in item:
                end_index = index - 1
                break
        html_contents = html_list[start_index:(end_index + 1)]
        return html_contents

def write_html_file(html_list):
    with open("New_Html.html", mode='a') as y:
        for line in html_list:
            y.write(line + '\n')

def convert_sudo_to_html(sudo_list):
    html_list = []
    html_list.append('<ul class="contents">')
    for item in sudo_list:
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
    return html_list

def convert_contents_to_sudo(html_list):
    sudo_list = []
    id_regex_pattern = 'href="#BM(?:[.][1-9]*)*"'
    content_regex_pattern = '>([ a-zA-Z1-9.]*)</a>'
    for line in html_list:
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

    return sudo_list

html_file = HTMLFile("Python2.html")
contents = html_file.contents)
contents_sudo = convert_contents_to_sudo(contents)
html_contents = convert_sudo_to_html(contents_sudo)
write_html_file(html_contents)
