import yaml


if __name__ == '__main__':

    with open('rendered_wano.yml') as file:
        wano_file = yaml.full_load(file)

    with open("dft_half_results.yml",'w') as out:
        yaml.dump(wano_file, out,default_flow_style=False)    
