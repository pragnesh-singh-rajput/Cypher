import requests  # Corrected the import statement
import random
import re

def scrape(newdata):
    yourquery = newdata

    if " " in yourquery:
        yourquery = yourquery.replace(" ", "+")
    url = "https://ahmia.fi/search/?g={}".format(yourquery)
    response = requests.get(url)  # Corrected the variable name
    content = response.text  # Corrected the attribute name
    regexquery = "\w+\.onion"
    minedata = re.findall(regexquery, content)

    n = random.randint(1, 9999)  # Corrected the method name

    filename = "sites{}.txt".format(str(n))
    print("Saving to ...", filename)
    minedata = list(dict.fromkeys(minedata))

    for k in minedata:
        with open(filename, "a") as newfile:
            k = k + "\n"
            newfile.write(k)
    print("All the files written to text file : ", filename)

    with open(filename) as input_file:  # Corrected the function name
        head = [next(input_file) for x in range(5)]
        contents = '\n'.join(map(str, head))  # Corrected the syntax
        print(contents)

newdata = input("[*]Please Enter Your Query: ")
scrape(newdata)

