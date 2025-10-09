def find_error(error_lst, error_type, error_desc):
    for line in error_lst:       
       existing_type  = line.get("type")
       if line.get("type") == error_type:
            line["count"] += 1
            line["examples"].append(error_desc)
            return True 
    return False   
               
               

def parse_log(path):
    error_lst = []
    result = {"errors": error_lst}
    with open(path, "r") as f:
        for line in f:
            error_lst = result.get("errors", [])
            if 'ERROR' in line:
                parts = line.split("ERROR", 1)  # only split once
                words = parts[1].strip().split(" ", 1)
                error_type = words[0]  
                if error_type[-1] == ":":    # trim colon
                    error_type = error_type[:-1]
                if len(words) > 1:
                    error_desc = words[1]
                else:
                    error_desc = ""
                    
                error_exist = find_error(error_lst, error_type, error_desc)
                if not error_exist:  
                    # make a new dict each time
                    error_dict = {
                        "type": error_type,
                        "count": 1,
                        "examples": [error_desc]
                    }
                    error_lst.append(error_dict)

        return result             


#path = "./logs/sample.log"  
#parse_log(path)   
