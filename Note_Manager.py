html_list = []
content_li_list = []
string_to_append = "BM"
index_count = 0
big_ol_list = []
list_depth = 0

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

def add_dot(the_list):
    global list_depth
    global index_count
    global string_to_append
    dot_list = []
    local_index = 0
    for item in the_list:
        local_index += 1
        if isinstance(item, list):
            index_count = local_index
            string_to_append = string_to_append + "." + str(index_count)
            dot_list.append(add_dot(item))
            string_to_append = string_to_append[0:-2]
        else:
            dot_list.append(string_to_append + "." + item)

    return(dot_list)


#content_li_list.append(generate_dropdown_ul('BM2', 'Lists', ['dogs', 'cats']))
#full_list = ['Some Item', ['category_name: d1', 'item', 'item', 'item', ['category_name: d2', 'item', 'item']]]
#print(generate_id_list(full_list))
test_list = ['1',['1', '2', ['1', '2', '3', '4'], '4', '5'], '3', '4', ['1', '2', '3', ['1', '2', '3'], '5'], '5', '6']
#deeper_breakdown(test_list)
print(add_dot(test_list))
print(big_ol_list)



#add_html(generate_contents(full_list))
#write_html_file(html_list)
