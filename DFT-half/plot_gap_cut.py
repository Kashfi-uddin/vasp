import yaml
import matplotlib.pyplot as plt


if __name__ == '__main__':

    with open('Table-dict.yml') as file:
        table_file = yaml.full_load(file)

    x = list(table_file['Cut'])
    x = [float(var) for var in x]
    y = list(table_file['gap'])
   
    plt.plot(x,y,'-o')
    plt.xlabel("Cut",fontsize='13')	#adds a label in the x axis
    plt.ylabel("Gap",fontsize='13')
    plt.text(6.5,1.1,"KPOINTS(8,8,8)", ha='right', fontsize='13')
    plt.text(6.5,1.0,"SOC-MAPbI3-cubic", ha='right', fontsize='13')
    plt.show()