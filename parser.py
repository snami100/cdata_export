import xml.etree.ElementTree as Et
import os
import pathlib


file_name = "_No_Translate.txt"


def get_cdata(root, xml_document, tree, state):
    line_number = 0
    for pageGrp in root.findall('pageGrp'):
        for data in pageGrp.iter('data'):
            tag = data.get("key").split(":")[2]
            if tag == "bodytext":
                data_type = data.text
                data_type = type(data_type)
                if data_type == str:
                    line_number += 1
                    if state == 0:
                        copy_content(data, line_number)  # copy the content of the cdata rows into a txt file
                    if state == 1:
                        replace_content(tree, xml_document, data,
                                        line_number)  # replace the cdata rows with the file names
                    if state == 2:
                        print('Copy former content to its places')
                        txt_string = paste_former_content(line_number)  # paste the former content into the xml again
                        data.text = txt_string
    if state == 2:
        tree.write(xml_document, encoding="UTF-8", xml_declaration=True,
                   method="xml")  # only use this when using data.text = paste_former_content.... !


def copy_content(data, line_number):
    file_open = open('txt_files/' + str(line_number) + file_name, "w", encoding="UTF-8")
    file_open.write(data.text)
    file_open.close()


def replace_content(tree, xml_document, data, line_number):
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
            file_append.write(']]>')
            file_append.close()
            line_number += 1
        except:
            print('No File - exit')
            return False


def replace_lt_gt(xml_document):
    with open(xml_document, 'r', encoding='UTF-8') as file_r:
        file_data = file_r.read()
        file_r.close()
        file_data = file_data.replace('&lt;', '<')
    with open(xml_document, 'w', encoding='UTF-8') as file_w:
        file_w.write(file_data)
        file_w.close()

    with open(xml_document, 'r', encoding='UTF-8') as file_r:
        file_data = file_r.read()
        file_r.close()
        file_data = file_data.replace('&gt;', '>')
    with open(xml_document, 'w', encoding='UTF-8') as file_w:
        file_w.write(file_data)
        file_w.close()


def main(xml_document):
    try:
        if(xml_document == None):
            xml_document = input("Bitte geben Sie den Namen der XML-Datei an: ")
            xml_document = str(xml_document)
            if len(xml_document) == 0:
                print('Bitte überprüfen Sie Ihre Eingabe')
                main(None)
            data_check = xml_document
            data_check = pathlib.Path(data_check).suffix
            if '.xml"' != data_check:
                exit()
            if xml_document[0] == '"':
                xml_document = xml_document[1:]
                xml_document = xml_document[:-1]
    except:
        print("\nBitte versuchen Sie es erneut.")

    with open(xml_document, 'r', encoding='utf-8') as xml_file:
        tree = Et.parse(xml_file)

    root = tree.getroot()
    path = os.getcwd()
    try:
        files_dir = path + '/txt_files'
        files_dir = str(files_dir)
        os.mkdir(files_dir)
    except:
        print('Creation of directory failed.')
    print("\n1 - Kopiere Inhalt der CDATA-Zeilen in neue TXT-Files und ersetze diese Zeilen durch die Dateinamen"
          "\n2 - Kopiert nun den Inhalt der durch '1' Erstellten TXT-Files zurück an die ursprüngliche Position. (Bitte nur ausführen wenn zuvor einmal die 1 ausgeführt wurde)"
          "\n3 - Führt 1 und 2 zusammen aus."
          "\n0 - Programm beenden")
    input_num = input("\nBitte geben Sie nun Ihre Auswahl an: ")
    input_num = int(input_num)

    if input_num == 1:
        print('\nOption 1 wurde ausgewählt\n')
        get_cdata(root, xml_document, tree, state=0)  # state = 0 --> Copy CDATA Content to txt Files
        get_cdata(root, xml_document, tree, state=1)  # state = 1 --> Replace CDATA Content with the Filenames
        refine_txt_files()  # add CDATA brackets to TXT Files

        last_state = input("\nMoechten Sie zurück zur Auswahl oder das Programm verlassen?\n0 - Programm verlassen\n1 - zurück zur Auswahl\n")
        last_state = int(last_state)
        if last_state == 1:
            main(xml_document)

    if input_num == 2:
        print('\nOption 2 wurde ausgewählt\n')
        get_cdata(root, xml_document, tree, state=2)  # copy TXT Inputs to its former position again
        replace_lt_gt(xml_document)  # replace &lt; with < and &gt; with >

    if input_num == 3:  # do both
        print('\nOption 1  und 2 wurde ausgewählt\n')
        get_cdata(root, xml_document, tree, state=0)
        get_cdata(root, xml_document, tree, state=1)
        refine_txt_files()
        get_cdata(root, xml_document, tree, state=2)
        replace_lt_gt(xml_document)

    if input_num == 0:
        print("Beende das Programm")
        exit()


main(None)
