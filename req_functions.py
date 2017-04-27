def parse_paths(paths_taken, matched_dict):
    for path in paths_taken:
        if len(path[0]) == 4:
            for node in path[0]:
                if node[0] == 'w':
                    try:
                        matched_dict[path[0][path[0].index(node) - 1]].append(node)
                    except KeyError:
                        matched_dict[path[0][path[0].index(node) - 1]] = [node]
        elif len(path[0]) == 6:
            first_path = True
            for node in path[0]:
                index_of_node = path[0].index(node)
                previous_node_in_path = path[0][index_of_node - 1]

                if node[0] == 'w' and first_path:
                    try:
                        matched_dict[previous_node_in_path].append(node)
                        first_path = False
                    except KeyError:
                        matched_dict[previous_node_in_path] = [node]
                        first_path = False
                elif node[0] == 'w':
                    try:
                        matched_dict[previous_node_in_path].remove(path[0][index_of_node - 2])
                        matched_dict[previous_node_in_path].append(node)
                    except KeyError:
                        matched_dict[previous_node_in_path].remove(path[0][path[0].index(node) - 2])
                        matched_dict[previous_node_in_path] = [node]
        else:
            raise TypeError('Returned type of path is not acceptable.')
    return matched_dict
