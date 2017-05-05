def parse_paths(paths_taken, matched_dict):
    for path in paths_taken:
        if len(path[0]) == 4:
            
            for node in path[0]:
                if node[0] == 'w':
                    try:
                        matched_dict[path[0][path[0].index(node) - 1]].append(node)
                    except KeyError:
                        matched_dict[path[0][path[0].index(node) - 1]] = [node]
        # elif len(path[0]) == 6:
        #     first_path = True
        #     for node in path[0]:
        #         index_of_node = path[0].index(node)
        #         previous_node_in_path = path[0][index_of_node - 1]
        #
        #         if node[0] == 'w' and first_path:
        #             try:
        #                 matched_dict[previous_node_in_path].append(node)
        #                 first_path = False
        #             except KeyError:
        #                 matched_dict[previous_node_in_path] = [node]
        #                 first_path = False
        #         elif node[0] == 'w':
        #             try:
        #                 matched_dict[previous_node_in_path].remove(path[0][index_of_node - 2])
        #                 matched_dict[previous_node_in_path].append(node)
        #             except KeyError:
        #                 matched_dict[previous_node_in_path].remove(path[0][path[0].index(node) - 2])
        #                 matched_dict[previous_node_in_path] = [node]

        else:
            # for x in range(0, len(path), 1):
            #     try:
            #         first=path[x]
            #         second=path[x+1]
            #         if first != 's' and second != 't':
            #             if second[0] == 'w':
            #                 matched_dict[first].append(second)
            #             elif second[0] == 't':
            #                 matched_dict[second].remove(first)
            #     except:
            #         pass

            for node_index in range(len(path)-1):

                node = path[node_index]
                next_node = path[node_index+1]
              
                print(node)
                if node[0] == 't' and node[1] == 'a':
                    if matched_dict[node]:
                        matched_dict[node].append(next_node)
                    else:
                        matched_dict[node] = [next_node]

                if node[0] == 'w':
                    if next_node[0] == 't' and next_node[1] == 'a':
                        matched_dict[next_node].remove(node)
                        print("removeed")
                        print(node)

    return matched_dict


def clean_path(paths_taken):

    paths_taken1 = []
    for path in paths_taken:
        if path[1] > 0:
            paths_taken1.append(path)

    return paths_taken1

def parse_paths2(paths_taken, matched_dict):
    paths_taken=clean_path(paths_taken)
    for path in paths_taken:


        if len(path[0]) == 4:
            for node in path[0]:
                if node[0] == 'w':
                    try:
                        matched_dict[path[0][path[0].index(node) - 1]].append(node)
                    except KeyError:
                        matched_dict[path[0][path[0].index(node) - 1]] = [node]
        # elif len(path[0]) == 6:
        #     first_path = True
        #     for node in path[0]:
        #         index_of_node = path[0].index(node)
        #         previous_node_in_path = path[0][index_of_node - 1]

        #         if node[0] == 'w' and first_path:
        #             try:
        #                 matched_dict[previous_node_in_path].append(node)
        #                 first_path = False
        #             except KeyError:
        #                 matched_dict[previous_node_in_path] = [node]
        #                 first_path = False
        #         elif node[0] == 'w':
        #             try:
        #                 matched_dict[previous_node_in_path].remove(path[0][index_of_node - 2])
        #                 print("Removed: "+path[0][index_of_node - 2])
        #                 matched_dict[previous_node_in_path].append(node)
        #             except KeyError:
        #                 matched_dict[previous_node_in_path].remove(path[0][path[0].index(node) - 2])
        #                 print("Removed: "+path[0][index_of_node - 2])
        #                 matched_dict[previous_node_in_path] = [node]

        else:
            for node_index in range(len(path)):
                try:
                    node = path[node_index]
                    next_node = path[node_index+1]
                    previous_node = path[node_index-1]

                    if node[0] == 't' and node[1] == 'a':
                        if matched_dict[node]:
                            matched_dict[node].append(next_node)
                        else:
                            matched_dict[node] = [next_node]
                    if node[0] == 'w':
                       # print("RRR")
                        if next_node[0] == 't' and next_node[1] == 'a':
                           
                            matched_dict[next_node].remove(node)

                except IndexError:
                    pass


    return matched_dict

