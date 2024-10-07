import re, os, yaml

def clean_num(srt_var):
    alphanumeric_filter = filter(str.isalnum, srt_var)
    alphanumeric_string = "".join(alphanumeric_filter)
    return alphanumeric_string
def clean_tuple(my_list):
    my_list = [clean_num(i) for i in my_list]
    my_list = list(filter(None, my_list))
    my_list = [int(i) for i in my_list]
    my_list =  tuple(my_list)
    return my_list

def read_elements(filename):
    with open(filename) as f:
        Var1 = f.read().splitlines()
        Var2 = Var1[5]
    Chem_elem_temp = re.split("\s+", Var2)
    Chem_elem = [string for string in Chem_elem_temp if string != ""]

    print(Chem_elem)
    return Chem_elem

def gen_potcar(var_elements, element):
    var_path = "potpaw_PBE.54/"
    var_pot_GW = "_GW/POTCAR"
    pot_var = ""
    for i in var_elements:
        if i == "Pb" or i == "Sb" and i != element:
            pot_var = pot_var + var_path + i + "_d" + var_pot_GW + " "
        elif i == "Cs" or i == "K" or i == "Rb" or i == "Na" or i == "Nb" or i == "Ba" or i == "Mo" and i != element:
            pot_var = pot_var + var_path + i + "_sv" + var_pot_GW + " "
        elif i == element:
            pot_var = pot_var + ' POTCARcut '
        else:
            pot_var = pot_var + var_path + i + var_pot_GW + " "
    
    os.system("cat " + pot_var + " > POTCAR_final")
    
    print("POTCAR generate for:", var_elements)
    
#if __name__ == '__main__':

    # with open('rendered_wano.yml') as file:
    #     wano_file = yaml.full_load(file)

    # element = wano_file["Element"]

    # potcar_elements = read_elements("POSCAR")
    # gen_potcar(potcar_elements,element)