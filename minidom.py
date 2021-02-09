from xml.dom.minidom import parse, parseString

tree = parse("systecnet_catxml_de-de_to_en-GB_280121-113333.xml")
node = tree.documentElement
servers = tree.getElementsByTagName("pageGrp")

for server in servers:
    keys = server.getElementsByTagName("data")[0].childNode[0].data
    print(keys)
