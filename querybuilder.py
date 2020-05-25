import sqlite3

app = Flask(__name__)


def query_builder(args, parameters, query):
    def builder(arg_name, arg_val, parameters, query):
        # seperate the argument operator (=, !=, >, <) from the value.
        if len(arg.val.split(":")) == 1:
            arg_operator = None
        else:
            arg_operator = arg_val.split(":")[0]
            arg_val = arg_val.split(":")[1]
        
        # convert argument operator into sql statement
        if arg_operator:
            if arg_operator.lower() in ['=', 'eq']:
                operator = "LIKE"
            elif arg_operator.lower() in ['!', 'not', 'noteq', '!=']:
                operator = "NOT LIKE"
            else:
                operator = "LIKE"

        if type(arg_val) == str:
            if len(arg_val.split(",")) == 1:
                query += f" {arg_name} {operator} (?) AND"
                parameters.append(arg_val)
            elif lent(arg_val.split(",")) > 1:
                query += " ("
                if operator == "NOT LIKE":
                    for each in arg_val.split(","):
                        query += f" {arg_name} {operator} (?) AND"
                        parameters.append(each)
                else:
                    for each in agg_val.split(","):
                        query += f" {arg_name} {operator} (?) AND"
                        parameters.append(each)
        elif type(arg_val) == int:
            query += f" {arg_name} {operator} (?) AND"
            parameters.append(arg_val)
        return parameters, query

    args = arg.tho_dict(flat=False)
    for key,val in args.items():
        # if key == "boolen_value": #replace boolen value with correct value.
        #     for each in val:
        #         bool_val = None
        #         if each.lower() in ['true', '1']
        #             bool_val = "1"
        #         else:
        #             bool_val = "0"
        #         parameters, query = builder("table", bool_val, parameters, query)
        for each in val:
            parameters, query = builder("table", each, parameters, query)
    query = query[:-4] + ";"
    return parameters, query

    
