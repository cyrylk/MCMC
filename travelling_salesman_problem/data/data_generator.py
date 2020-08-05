import xml.etree.ElementTree as ET
tree = ET.parse('burma14.xml')
rooot = tree.getroot()


def get_problem_size(root):
    name = root.find("name").text
    for i in range(len(name)):
        try:
            return int(name[i:], 10)
        except ValueError:
            pass


def generate_initial_dictionary(size):
    return {i: {j: float("inf") for j in range(size) if j != i} for i in range(size)}


def get_graph_from_root(root, dictionary):
    graph = root.find("graph")
    current_vertex = 0
    for vertex in graph.findall("vertex"):
        for edge in vertex.findall("edge"):
            dictionary[current_vertex][int(edge.text)] = float(edge.get("cost"))
        current_vertex += 1


def get_data_from_file(filename):
    tree = ET.parse(filename)
    root = tree.getroot()
    size = get_problem_size(root)
    dictionary = generate_initial_dictionary(size)
    get_graph_from_root(root, dictionary)
    return dictionary


print(get_data_from_file("burma14.xml"))





