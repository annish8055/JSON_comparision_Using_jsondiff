import os 
import csv
import json
from jsondiff import diff

path = './jsonfiles'
files = []

#createing CSV comparision result to display on the web page
def data_set_creator():
    #json objet to store pass fail result and additional information
    result ={}
    create_file_list()
    #Reading the files recived from the directory. Can be improved later
    with open(files[0]) as json_file:  
        file_data_1 = json.load(json_file)
    with open(files[1]) as json_file:  
        file_data_2 = json.load(json_file)
    f= open("./output/data.csv","w")
    if(file_data_1 == file_data_2):
        result['line1'] = "No mismatch"
        result['line2'] = 100
        result['line3'] = "Complete match"
        result['line3C'] = "green"            
    else:
        result['line1'] = "Mismatch in files"
        result['line3'] = "Incomplete match"
        result['line3C'] = "red" 

        mismatch_attribures_file1 = diff(file_data_1,file_data_2)
        f.write(files[0] + " --> Mismatched values \n")
        for key,value in mismatch_attribures_file1.items():
            val = "Key: "+str(key)+" , "+"values: "+str(value).replace(",",";")
            val = val.replace("{insert:","{")
            val = val.replace("delete:","other_file_issue_number:")
            f.write(val+"\n")
        file1_mismatch_percent = ((len(file_data_1.keys())-len(mismatch_attribures_file1.keys()))/(len(file_data_1.keys())))*100
        mismatch_attribures_file2 = diff(file_data_2,file_data_1)
        f.write(files[1] + " --> Mismatched values \n")
        for key,value in mismatch_attribures_file2.items():
            val = "Key: "+str(key)+" , "+"values: "+str(value).replace(",",";")
            val = val.replace("{insert:","{")
            val = val.replace("delete:","other_file_issue_number:")
            f.write(val+"\n")
        file2_mismatch_percent = ((len(file_data_2.keys())-len(mismatch_attribures_file2.keys()))/(len(file_data_2.keys())))*100
        
        result['line2'] = round((file1_mismatch_percent+file2_mismatch_percent)/2)
    f.close()
    #creating the final data csv whiching going to be used to display in HTML
    f= open("./output/data.csv","r")
    fhand = open('./output/data.js', 'w')
    fhand.write("myData = [\n")
    #f1= open("./output/data_fin.csv","w")
    for line in f.readlines():
        if line.strip() == '':
            continue
        output = "{"+"x1:"+'"'+line.replace('"','').strip('\n')+'"'+"},\n"
        fhand.write(output)
    fhand.write("\n];\n")
    fhand.close()
    #creating the json file for he HTML page
    outputdetails = open("./output/file.js",'w')
    outputdetails.write("extradata = ")
    outputdetails.write(json.dumps(result))
    outputdetails.close
    

#Function is being used to go through a complete folder and add CSV file path to the file global variable
def create_file_list():
    for r, d, f in os.walk(path):
        for file in f:
            if '.json' in file:
                files.append(os.path.join(r, file))

#main function
if __name__ == "__main__":
    data_set_creator()