import xml.etree.ElementTree as ET

xml_document = "systecnet_catxml_de-de_to_en-GB_280121-113333.xml"
with open(xml_document, 'r', encoding='utf-8') as xml_file:
    tree = ET.parse(xml_file)
root = tree.getroot()
file_name = "_No_Translate.txt"


def get_cdata(state):
    line_number = 0
    for pageGrp in root.findall('pageGrp'):
        for data in pageGrp.iter('data'):
            tag = data.get("key").split(":")[2]
            if (tag == "bodytext"):
                data_type = data.text
                data_type = type(data_type)
                if data_type == str:
                    line_number += 1
                    if state == 0:
                        copy_content(data, line_number)  # copy the content of the cdata rows into a txt file
                    if state == 1:
                        replace_content(data, line_number)  # replace the cdata rows with the file names
                    if state == 2:
                        print('Copy former content to its places')
                        txt_string = paste_former_content(line_number)  # paste the former content into the xml again
                        data.text = txt_string
    if state == 2:
        tree.write(xml_document, encoding="UTF-8", xml_declaration=True, method="xml")  # only use this when using data.text = paste_former_content.... !


def copy_content(data, line_number):
    file_open = open('txt_files/' + str(line_number) + file_name, "w", encoding="UTF-8")
    file_open.write(data.text)
    file_open.close()



def replace_content(data, line_number):
    data.text = str(line_number) + file_name
    tree.write(xml_document, encoding="UTF-8", xml_declaration=True)


def paste_former_content(line_number):

    with open('txt_files/' + str(line_number) + file_name, 'r', encoding="UTF-8") as file:
        html_string = file.read()
    return html_string


def refine_txt_files():
    line_number = 1

    while True:
        try:
            file = open('txt_files/' + str(line_number) + file_name, 'r+')
            print('file open')
            content = file.read()
            file.seek(0, 0)
            file.write('<![CDATA[' + content)
            file.close()

            file_append = open('txt_files/' + str(line_number) + file_name, 'a')
            file_append.write(']]')
            file_append.close()
            line_number += 1
        except:
            print('No File - exit')
            return False


def replace_lt_gt():
    file_name = 'systecnet_catxml_de-de_to_en-GB_280121-113333.xml'
    with open(file_name, 'r', encoding='UTF-8') as file_r:
        file_data = file_r.read()
    file_r.close()
    file_data = file_data.replace('&lt;', '<')
    with open(file_name, 'w', encoding='UTF-8') as file_w:
        file_w.write(file_data)
    file_w.close()

    with open(file_name, 'r', encoding='UTF-8') as file_r:
        file_data = file_r.read()
    file_r.close()
    file_data = file_data.replace('&gt;', '>')
    with open(file_name, 'w', encoding='UTF-8') as file_w:
        file_w.write(file_data)
    file_w.close()


def main():
    get_cdata(state=0)  # state = 0 --> Copy CDATA Content to txt Files
    get_cdata(state=1)  # state = 1 --> Replace CDATA Content with the Filenames
    refine_txt_files()  # add CDATA brackets to TXT Files
    get_cdata(state=2)  # copy TXT Inputs to its former position again
    replace_lt_gt()  # replace &lt; with < and &gt; with >


main()