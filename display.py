def get_type_of_element_dof(dof):
    element_dof = (dof - 1) % 6 + 1

    if element_dof > 3:
        node_dof = element_dof - 3
    else:
        node_dof = element_dof

    if node_dof == 1:
        return "dof_x"
    elif node_dof == 2:
        return "dof_z"
    elif node_dof == 3:
        return "dof_phi"
    else:
        raise Exception()


def get_point_of_element_by_dof(static_system, dof):
    element_id = (dof - 1) // 6 + 1
    element_dof = (dof - 1) % 6 + 1

    element = static_system.get_element(id=element_id)

    if element_dof > 3:
        p = element.p_k
        element_dof -= 3
    else:
        p = element.p_i

    return f"x={p[0]} z={p[1]}"


class Display:

    def prepare_static_system_for_display(static_system):
        display_info = {}

        for dof in static_system.get_essential_dofs():

            p_string = get_point_of_element_by_dof(static_system, dof)
            dof_type = get_type_of_element_dof(dof)

            if p_string not in display_info:
                display_info[p_string] = {
                    "dof_x": {},
                    "dof_z": {},
                    "dof_phi": {},
                }

            display_info[p_string][dof_type][dof] = {
                "dependencies": False,
                "restrained": dof in static_system.get_restrained_dofs(),
            }

        for boundary_condition in static_system.boundary_conditions.values():
            dof = boundary_condition[1]

            p_string = get_point_of_element_by_dof(static_system, dof)
            dof_type = get_type_of_element_dof(dof)

            display_info[p_string][dof_type][dof]["dependencies"] = True

        return display_info

    def get_dof_of_node(data):
        keys_list = list(data.keys())
        dependencies_list = [data[key]["dependencies"] for key in keys_list]
        restrained_list = [data[key]["restrained"] for key in keys_list]

        if len(data) == 1 or True not in dependencies_list:
            return keys_list[0]

        index_of_true = dependencies_list.index(True)

        return keys_list[index_of_true]

    def is_phi_of_node_restrained(data):
        keys_list = list(data.keys())
        dependencies_list = [data[key]["dependencies"] for key in keys_list]
        restrained_list = [data[key]["restrained"] for key in keys_list]

        if len(data) == 1:
            return restrained_list[0]

        if True not in dependencies_list:
            return False

        index_of_true = dependencies_list.index(True)

        return restrained_list[index_of_true]

    def should_place_moment_joint(static_system, dof):

        point_string = get_point_of_element_by_dof(static_system, dof)
        display_data = Display.prepare_static_system_for_display(static_system)

        if (
            Display.get_dof_of_node(display_data[point_string]["dof_phi"]) == dof
            or dof not in static_system.get_essential_dofs()
        ):
            return False

        return True
