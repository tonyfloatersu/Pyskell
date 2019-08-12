class Inference:
    def __init__(self):
        self.__next_type_var_id = 0

    def new_type_var_name(self):
        name = 'tv_' + str(self.__next_type_var_id)
        self.__next_type_var_id += 1
        return name
