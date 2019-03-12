
import pylab 
#from operator import itemgetter   # optional, if you use itemgetter when sorting

REGIONS = {'MENA':'Middle East and North Africa','EUR':'Europe',\
               'AFR':'Africa','NAC':'North America and Caribbean',\
               'SACA':'South and Central America',\
               'WP':'Western Pacific','SEA':'South East Asia'}

def open_file():
    '''
        This function will open a file and return an error if the file name is incorrect
    '''
    #Create a try and except error
    file_name = input("Please enter a file name: ")
    while True:
        #While this is true, we can open the file
        try:
            #try to open the file here
            file_open = open(file_name, encoding ="windows-1252")
            #We return the opened file
            return file_open
        #If this is false, We return an error and promt for a new file
        except:
            #if error, try again
            file_name = input("File not found. Please enter a valid file name: ")
    
    
def create_dictionary(fp):
    '''
        This function will read the open file and create a dictionary of the different
        data. The dictonary that it returns will contain dictionaries or dictionaries or lists of tuples.
    '''
    #Create an empty dictionary
    main_dict = {}
    #Strip the top line
    header = fp.readline()
    #Create a for each line in my file loop
    for line in fp:
        #Split each line at a comma
        line_list = line.strip().split(",")
        #The next following lines set values equal to certain values in lines
        country = line_list[1]
        region = line_list[2]
        age_group = line_list[3]
        gender = line_list[4]
        geographic_area = line_list[5]
        diabetes = int(float(line_list[6])*1000)
        population = int(float(line_list[7])*1000)
        #Here I create a tuple for some data
        tup = (gender, geographic_area, diabetes, population)
        #Create an if statement saying if my region is not yet in my dictionary, we create an empty dictionary for that region
        if region not in main_dict:
            main_dict[region]={}
        #Create an if statement saying if my country isnt in the dictionary I just created, then create an empty dictionary for that country
        if country not in main_dict[region]:
            main_dict[region][country] = {}
        #Create an if statement for the age group, if it is not in the the dictionary i just created, then i create an empty dict for that age group
        if age_group not in main_dict[region][country]:
            main_dict[region][country][age_group] = []
        #Here I create my main dictionary with all my data and appending my previously created tuple
        main_dict[region][country][age_group].append(tup)
    return main_dict

def get_country_total(data):
    '''
        This function will input an entire dictionary, interpret the data and return totals for each country
    '''
    #Create an empty dictionary
    total = {}
    #Create a for loop for country in data
    for country, v in data.items():
        #Set some initial values
        diab_tot = 0
        pop_tot = 0
        #Create another for loop for age in v
        for age in v.values():
            #Create a for loop for the tuple in my age
            for tup in age:
                #Add the totals up in  two values
                diab_tot += int(tup[2])
                pop_tot += int(tup[3])       
        #Create my dictionary
        total[country] = (diab_tot,pop_tot)
    #Return the dictionary
    return total
        
    
def display_table(data, region):
    '''
        This function will be inputed with two different dictionaries. It will print some data according to what region is asked
    '''
    #Here I print different things for the different regions
    if region == "MENA":
        print("{:>56s}".format("Diabetes Prevalence in Middle East and North Africa"))
    if region == "EUR": 
        print("{:>34s}".format("Diabetes Prevalence in Europe"))
    if region == "AFR": 
        print("{:>34s}".format("Diabetes Prevalence in Africa"))
    if region == "NAC": 
        print("{:>55s}".format("Diabetes Prevalence in North America and Caribbean"))
    if region == "SACA":
        print("{:>53s}".format("Diabetes Prevalence in South and Central America"))
    if region == "WP": 
        print("{:>43s}".format("Diabetes Prevalence in Western Pacific"))
    if region == "SEA":
        print("{:>43s}".format("Diabetes Prevalence in South East Asia"))
    #Print format for my columns
    print("{:<25s}{:>20s}{:>16s}".format('Country Name', 'Diabetes Prevalence', 'Population'))
    print('')
    #Initialize some values
    country = data.keys()
    country = sorted(country)
    #Make a for loop so I can print every single item
    total_diabetes = 0
    total_diabetes2 = 0
    for item in country:
        totals1 = data[item][0]
        totals2 = data[item][1]
        total_diabetes += totals1
        total_diabetes2 += totals2
        print("{:<25s}{:>20,d}{:>16,d}".format(item, totals1, totals2))
    print("")
    print("{:<25s}{:>20,d}{:>16,d}".format("TOTAL", total_diabetes, total_diabetes2))
        
        
    

def prepare_plot(data):
    '''
        This function will take in a dictionary for a specific region. It will return a dictionary with the data classfied by age and then by gender.
    '''
    #Create an empty dictionary
    main_dict = {}
    #Create a for country in data loop
    for country, v in data.items():
        #Craete a for age in v loop
        for age, item in v.items():
            #Create the second empty dictionary
            second_dict = {}
            #Create an if statement to say if my age isn't in my main_dict then we create a "MALE" and "FEMALE" and assign some values to them
            if age not in main_dict.keys():
                second_dict['MALE'] = item[1][2]
                second_dict['FEMALE'] = item[0][2]
                main_dict[age] = second_dict
            #Create an if statement, to say that if my age is in the dictionary, I just add some values to the already existing values
            elif age in main_dict.keys():
                main_dict[age]['MALE'] += item[1][2]
                main_dict[age]['FEMALE'] += item[0][2]
    #Return the main dictionary
    return main_dict
    
            
            
    
def plot_data(plot_type,data,title):
    '''
        This function plots the data. 
            1) Bar plot: Plots the diabetes prevalence of various age groups in
                         a specific region.
            2) Pie chart: Plots the diabetes prevalence by gender. 
    
        Parameters:
            plot_type (string): Indicates what plotting function is used.
            data (dict): Contains the dibetes prevalence of all the contries 
                         within a specific region.
            title (string): Plot title
            
        Returns: 
            None
            
    '''
    
    plot_type = plot_type.upper()
    
    categories = data.keys() # Have the list of age groups
    gender = ['FEMALE','MALE'] # List of the genders used in this dataset
    
    if plot_type == 'BAR':
        
        # List of population with diabetes per age group and gender
        female = [data[x][gender[0]] for x in categories]
        male = [data[x][gender[1]] for x in categories] 
        
        # Make the bar plots
        width = 0.35
        p1 = pylab.bar([x for x in range(len(categories))], female, width = width)
        p2 = pylab.bar([x + width for x in range(len(categories))], male, width = width)
        pylab.legend((p1[0],p2[0]),gender)
    
        pylab.title(title)
        pylab.xlabel('Age Group')
        pylab.ylabel('Population with Diabetes')
        
        # Place the tick between both bar plots
        pylab.xticks([x + width/2 for x in range(len(categories))], categories, rotation='vertical')
        pylab.show()
        # optionally save the plot to a file; file extension determines file type
        #pylab.savefig("plot_bar.png")
        
        
    elif plot_type == 'PIE':
        
        # total population with diabetes per gender
        male = sum([data[x][gender[1]] for x in categories])
        female = sum([data[x][gender[0]] for x in categories])
        
        pylab.title(title)
        pylab.pie([female,male],labels=gender,autopct='%1.1f%%')
        pylab.show()
        # optionally save the plot to a file; file extension determines file type
        #pylab.savefig("plot_pie.png")
        

def main():
    
    "\nDiabetes Prevalence Data in 2017"
    MENU = \
    '''
                Region Codes
    MENA: Middle East and North Africa
    EUR: Europe
    AFR: Africa
    NAC: North America and Caribbean
    SACA: South and Central America
    WP: Western Pacific
    SEA: South East Asia
    '''
    
    "Enter region code ('quit' to terminate): "
    "Do you want to visualize diabetes prevalence by age group and gender (yes/no)?: "
    "Error with the region key! Try another region"
    "Incorrect Input! Try Again!"
    #Call the open file function
    fp = open_file()
    #I call the create dictionary function here
    data = create_dictionary(fp)
    while True:
        print(MENU)
        #Ask for a certain region and make that upper case
        try:
            region = (input("Enter region code ('quit' to terminate): ")).upper()
            #If my region is QUIT then i end my program
            if region == "QUIT":
                break
            #I call the get country total function here
            data2 = get_country_total(data[region])
            #Display all my data here
            display_table(data2,region)
            #Ask if they want to plot the data
            plot_data2 = input("Do you want to visualize diabetes prevalence by age group and gender (yes/no)?:")
            #If they want to plot the data, i call the plot data function
            if plot_data2 == "yes":
                #Create some data to plot
                plot = prepare_plot(data[region])
                plot_data("PIE",plot,"Diabetes Prevalence in "+REGIONS[region]+" by age group and gender")
                plot_data("BAR",plot,"Diabetes Prevalence in "+REGIONS[region]+" by age group and gender")
        except KeyError:
            print("Error with the region key! Try another region")

    
    "Do you want to visualize diabetes prevalence by age group and gender (yes/no)?: "
    "Error with the region key! Try another region"
    "Incorrect Input! Try Again!"
   
    
   
###### Main Code ######
if __name__ == "__main__":
    main()