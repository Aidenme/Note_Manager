html_file_list = []
sudo_list = []

def write_html_file(html_list):
    with open("New_Html.html", mode='a') as y:
        for line in html_list:
            y.write(line + '\n')

def set_html_list():
    the_file = []
    global html_file_list
    with open("Python2.html") as f:
        for line in f:
            the_file.append(line.rstrip())

    html_file_list = the_file

def print_html_file_list(html_list):
    for item in html_list:
        print(item)

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

def convert_html_to_sudo(html_list):
    sudo_list = []
    for line in html_list:
        type = None
        id = None
        content = None
        trimmed_line = line.strip()
        if 'class="subcontents"' in trimmed_line:
            type = 'dropdown_ul'
            sudo_list.append(['dropdown_ul', ])
#full_content_list = ['Some Item', ['category_name: d1', 'item', 'item', 'item', ['category_name: d2', 'item', 'item']]]
#test_id_gen_list = ['1',['1', '2', ['1', '2', '3', '4'], '4', '5'], '3', '4', ['1', '2', '3', ['1', '2', '3'], '5'], '5', '6']
#print(add_dot(test_id_gen_list))
set_html_list()
print_html_file_list(get_contents_from_html(html_file_list))
convert_html_to_sudo(html_file_list)

sudo_list = [
['link_line', 'BM.1', 'Variable assignment'],
['dropdown_ul', 'BM.2', 'Numbers'],
['link_line', 'BM.2.1', 'Number Data Types'],
['end_dropdown_ul']
]

#print_html_file_list(convert_sudo_to_html(sudo_list))
#write_html_file(convert_sudo_to_html(sudo_list))
