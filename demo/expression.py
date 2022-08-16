from typing import List


class Expression:
    def __init__(self, names: List[str], code: str, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self.names = []
        self.code = []
        self_input_counter = 0
        self.ids = {id(self)}
        self.input_id_dict = {}
        # flatten first for existing Expression
        for name, arg in zip(names, args):
            arg_id = id(arg)
            if arg_id in self.input_id_dict:
                normalized_name = self.input_id_dict[arg_id][0]
                code = code.replace(name, normalized_name)
                continue
            normalized_name = f"##{id(self)}##input_{self_input_counter}"
            self_input_counter += 1
            self.input_id_dict[arg_id] = (normalized_name, arg)
            if isinstance(arg, Expression):
                code = code.replace(name, normalized_name)
                self.ids = set(list(self.ids) + list(arg.ids))
                arg_code = "\n".join(arg.code)
                for arg_name, arg_arg in zip(arg.names, arg.args):
                    if id(arg_arg) not in self.input_id_dict:
                        self_input_name = f"##{id(self)}##input_{self_input_counter}"
                        self_input_counter += 1
                        self.names.append(self_input_name)
                        self.input_id_dict[id(arg_arg)] = (self_input_name, arg_arg)
                    else:
                        self_input_name = self.input_id_dict[id(arg_arg)][0]
                    arg_code = arg_code.replace(arg_name, self_input_name)
                arg_code = arg_code.split("\n")
                arg_code[-1] = arg_code[-1].replace("return ", f"{normalized_name} = ")
                self.code.extend(arg_code)
            else:
                self.names.append(normalized_name)
                code = code.replace(name, normalized_name)
        self.code.extend(code.split("\n"))
        # self.export()

    def export(self):
        print("this is export:")
        names = self.names.copy()
        code = self.code.copy()
        for _id in self.ids:
            for i in range(len(names)):
                names[i] = names[i].replace(f"##{_id}##", "")
            for i in range(len(code)):
                code[i] = code[i].replace(f"##{_id}##", "")
        print(names)
        print("\n".join(code))
