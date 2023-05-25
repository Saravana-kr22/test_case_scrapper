import pandas as pd
import openpyxl
from openpyxl.styles import Font



def cluster_dif(h1text1, h1text2,new_data_dicts_keys,old_data_dicts_keys,sheet1):

        added = []
        added = list(set(h1text1) - set(h1text2))
        print (added)
        removed = []
        removed = list(set(h1text2) - set(h1text1))
        print(removed)
        mod_tc = []
        

        if (len(new_data_dicts_keys) == len(old_data_dicts_keys)):
           
            for i in range(len(new_data_dicts_keys)):
                if new_data_dicts_keys[i] != old_data_dicts_keys[i]:
                    mod_tc.append((new_data_dicts_keys[i], old_data_dicts_keys[i]))

            if mod_tc:
                
                print(mod_tc)
                sheet1.append(["modification in the test case's"])
                sheet1.append([""])
                for fgc in range(len(mod_tc)):
                    sg = str(mod_tc[fgc])
                    sheet1.append([sg])
                    print("print")
                   


        else:
             
            added_tc = list(set(old_data_dicts_keys) - set(new_data_dicts_keys))
            removed_tc = list(set(new_data_dicts_keys) - set(old_data_dicts_keys))
        

            for i in range(min(len(new_data_dicts_keys), len(old_data_dicts_keys))):
                if new_data_dicts_keys[i] != old_data_dicts_keys[i]:
                    mod_tc.append((new_data_dicts_keys[i], old_data_dicts_keys[i]))
            
            print(added_tc)
            print(removed_tc)

            if added_tc:
                sheet1.append([""])
                
                sheet1.append(["Removed test case's"])
                
                for i in added_tc:
                    sheet1.append([i])
                    
                
            if removed_tc:
                sheet1.append([""])
                
                sheet1.append(["Newly added test case's"])
                
                for fg in removed_tc:
                    sheet1.append([fg])
                    

            if mod_tc:
                sheet1.append([""])
                
                print(mod_tc)
                sheet1.append(["Modification in the test case's"])
                
                for fgc in range(len(mod_tc)):
                    sg = str(mod_tc[fgc])
                    sheet1.append([sg])
                    



def tc_diff(new_data_dicts_keys,old_data_dicts_keys):
        mod_tc = []
        added_tc = []
        removed_tc = []

        if (len(new_data_dicts_keys) == len(old_data_dicts_keys)):
           
            for i in range(len(new_data_dicts_keys)):
                if new_data_dicts_keys[i] != old_data_dicts_keys[i]:
                    mod_tc.append((new_data_dicts_keys[i], old_data_dicts_keys[i]))

            if mod_tc:
                
                print("mod_tc is " + str(mod_tc))

                
                


        else:
             
            added_tc = list(set(old_data_dicts_keys) - set(new_data_dicts_keys))
            removed_tc = list(set(new_data_dicts_keys) - set(old_data_dicts_keys))
        

            for i in range(min(len(new_data_dicts_keys), len(old_data_dicts_keys))):
                if new_data_dicts_keys[i] != old_data_dicts_keys[i]:
                    mod_tc.append((new_data_dicts_keys[i], old_data_dicts_keys[i]))
            print("12323422")
            print(added_tc)
            print(removed_tc)

            
                
        
        print(new_data_dicts_keys)
        print ("this is diff")
        print(mod_tc)
        return (added_tc, removed_tc, mod_tc)


def dif_table(data):
        

        
        new_data_dicts_keys = data[0]
        old_data_dicts_keys = data[1]
        new_data_dicts = data[2]
        old_data_dicts = data[3]
        removed_tc = data[4]
        added_tc = data[5]
        mod_tc = data[6]

        sheet1 = data[7]
        next_row = sheet1.max_row + 2

        head = ['testcase','row','column','old value','new value']
        sheet1.append(head)

        appended_row = sheet1[next_row]

        # Make the entire row bold
        for cell in appended_row:
            cell.font = Font(bold=True)

        for i in range(max(len(new_data_dicts_keys), len(old_data_dicts_keys))):

                new_data_dicts_key = new_data_dicts_keys[i]
                old_data_dicts_key = old_data_dicts_keys[i]

                if new_data_dicts_key == old_data_dicts_key:
                    new_data_dict = new_data_dicts[new_data_dicts_keys[i]]
                    old_data_dict = old_data_dicts[old_data_dicts_keys[i]]
                elif new_data_dicts_keys[i] in removed_tc:
                    break
                elif new_data_dicts_keys[i] in added_tc:
                    break
                else:
                    
                    for g in mod_tc:
                        
                        if  new_data_dicts_keys[i] in mod_tc[g]:

                            pos = mod_tc[g].index(new_data_dicts_keys[i])
            
                            if pos:
                                new_data_dict = new_data_dicts[new_data_dicts_keys[i]]
                                old_data_dict = old_data_dicts[old_data_dicts_keys[i+g]]
                                   
                

            
                print (new_data_dict)
                print(old_data_dict)

                

                old_df = pd.DataFrame(old_data_dict)


                new_df = pd.DataFrame(new_data_dict)



                # Check if the dataframes are equal
                if old_df.shape == new_df.shape:
                    print("The dataframes are equal.")
                    
                    # Find the differences in cell values
                    diff_locations = []
                    for c in range(len(old_df.index)):
                        for j in range(len(old_df.columns)):
                            if old_df.iloc[c, j] != new_df.iloc[c, j]:
                                diff_locations.append((c, j))
                    
                    if diff_locations:
                        print("Cell value changes:")
                    
                        sheet1.append([""])
                        

                        for x in diff_locations:
                            
                            y, z = x
                            val = [new_data_dicts_key,y,z,old_df.iloc[y, z],new_df.iloc[y, z]]
                            sheet1.append(val)
    
                            print(f"Row: {i}, Column: {j}")
                            #print(f"Old Value: {old_df.iloc[i, j]}")
                            #print(f"New Value: {new_df.iloc[i, j]}")
                            

                    else:
                        print("No cell value changes.")
                else:
                    # Convert dataframes to nested lists
                    

                    old_list = old_df.iloc[:, 1:].values.tolist()
                    new_list = new_df.iloc[:, 1:].values.tolist()

                    # Compare the nested lists
                    added_rows = [row for row in new_list if row not in old_list]
                    removed_rows = [row for row in old_list if row not in new_list]

                    # Check if any rows were added or removed
                    if added_rows:
                        tcid = "added step in " + new_data_dicts_key
                        sheet1.append([tcid])
                        sheet1.append([""])
                        
                        
                        for c in added_rows:
                            sheet1.append([str(c)])
                            
                    else:
                        print("No rows added.")

                    if removed_rows:
                        tcid = "removed step in " + new_data_dicts_key
                        sheet1.append([tcid])
                        sheet1.append([""])
                        
                       
                        for c in removed_rows:
                            sheet1.append([str(c)])
                        
                    else:
                        print("No rows removed.")

                    

                