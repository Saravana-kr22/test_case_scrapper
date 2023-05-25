from bs4 import BeautifulSoup
import re
from script.create_table import create_df


def dict_(h1_tags):
        
        wdata_dict = {}
        for i in range(len(h1_tags)-1):
            h1 = h1_tags[i].text
            sheet=h1.replace('Cluster Test Plan', '').replace(' ', '').replace('/', '')
            print(sheet)
            first_h1 = h1_tags[i]  # Select the first h1 tag in the pair
            second_h1 = h1_tags[i+1]  # Select the second h1 tag in the pair
            
            # Find all h5 tags after the first h1 tag with id starting with the value
            h5_tags = first_h1.find_all_next('h5', {'id': lambda x: x and x.startswith('_test_procedure')})  
            #print (h5_tags)
            
            #print (h4_tags.text)
            # list of testprocedure's containing testcase
            #test_tags = soup.select('h5[id^="_test_procedure"]')
            result = []

            # Find the h4 tag of the paeticular cluster
            for h5_tag in h5_tags:
                #print(h5_tag)
                if h5_tag.find_previous('h1') == first_h1:
                    if h5_tag.find_next('h1') == second_h1:
                        result.append(h5_tag)
            p = 2
            print (result)

            
            data_tables = []
            
            if result:
               
                heads = []
                for h5_tag in result:
                    h4_tag = h5_tag.find_previous('h4')
                    headt= h4_tag.text
                    heads.append(headt)
                    index = result.index(h5_tag)
                    print (index)

                    testcase1 = re.search(r'\[(.*?)\]',headt )
                    if testcase1:
                        matched_str = testcase1.group()  # Extract the matched substring
                        testcase = re.sub(r'\[|\]', '', matched_str)

                    table = h5_tag.find_next('table')
                    if table:

                        data_dict = create_df(table)
                        data_tables.append(data_dict)
                        wdata_dict[testcase] = data_dict
                    else: 
                        print("no table no table no table")

                

                    
            else:

                h5_tags = first_h1.find_all_next('h6', {'id': lambda x: x and x.startswith('_test_procedure')})  

                for h5_tag in h5_tags:
                #print(h5_tag)
                    if h5_tag.find_previous('h1') == first_h1:
                        if h5_tag.find_next('h1') == second_h1:
                            result.append(h5_tag)
                
                print (result)
                heads =[]
                for h5_tag in result:
                    h4_tag = h5_tag.find_previous('h5')
                    headt= h4_tag.text
                    heads.append(headt)
                    index = result.index(h5_tag)
                    print (index)

                    testcase1 = re.search(r'\[(.*?)\]',headt )
                    if testcase1:
                        matched_str = testcase1.group()  # Extract the matched substring
                        testcase = re.sub(r'\[|\]', '', matched_str)

                    table = h5_tag.find_next('table')

                    print(table)
                    if table:
                        data_dict = create_df(table)
                        data_tables.append(data_dict)
                        wdata_dict[testcase] = data_dict
                    else:
                        print("no table no table no table")
                    
            #print (data_tables)   
                
        return(wdata_dict)