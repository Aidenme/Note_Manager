html_list = []
content_li_list = []
def write_html_file(html_list):
    with open("New_Html.html", mode='a') as y:
        for line in html_list:
            y.write(line + '\n')

def set_html_list():
    the_file = []
    with open("Python.html") as f:
        for line in f:
            the_file.append(line)

def generate_contents(contents_li_items):
    contents = []
    contents.append('<ul class="contents">')
    for item in contents_li_items:
        contents.append('<li>')
        if isinstance(item, list):
            for list_item in temp_gen_dropdown(item):
                contents.append(list_item)
        else:
            contents.append(item)
        contents.append('</li>')
    contents.append('</ul>')
    print(contents)
    return contents

def add_html(sub_html_list):
    for line in sub_html_list:
        html_list.append(line)

def temp_gen_dropdown(content_list):
    dropdown_ul = []
    dropdown_ul.append('<a>' + content_list[0] + '</a>')
    dropdown_ul.append('<ul>')
    for item in content_list[1:]:
        dropdown_ul.append('<li>')
        if isinstance(item, list):
            for list_item in temp_gen_dropdown(item):
                dropdown_ul.append(list_item)
        else:
            dropdown_ul.append(item)
        dropdown_ul.append('</li>')
    dropdown_ul.append('</ul>')
    return dropdown_ul

def generate_dropdown_ul(id, content, items):
    dropdown_ul = []
    dropdown_ul.append('<a href="#' + id + '" id="' + id + 'Link">' + content + '</a><div id="' + id + 'but" class="twirl_button" onclick="reveal(\'' + id + 'sub\', \'' + id + 'but\')">&#8658;</div>')
    dropdown_ul.append('<ul id="' + id + 'sub" class="subcontents" style="display:none;">')
    for item in items:
        dropdown_ul.append('<li>' + item + '</li>')
    dropdown_ul.append('</ul>')
    return dropdown_ul

def generate_link(content):
    return content

def generate_id_list(content_list):
    id_list = []
    item_count = 1
    for item in content_list:
        id_list.append(str(item_count))
        item_count += 1

    return id_list

#content_li_list.append(generate_dropdown_ul('BM2', 'Lists', ['dogs', 'cats']))
full_list = ['Some Item', ['categor_name', 'item', 'item', 'item', ['another', 'please']]]
print(generate_id_list(full_list))

#add_html(generate_contents(full_list))
#write_html_file(html_list)
