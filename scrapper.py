from bs4 import BeautifulSoup
import pandas as pd
import openpyxl
import datetime

today = datetime.date.today().strftime('%Y-%m-%d')

filename = f"test_plan_change_{today}.xlsx"

workbook = openpyxl.Workbook()

#function to scrap testcase
def scrap( file, sheet ):
    with open (file) as f:
        soup = BeautifulSoup(f, 'html.parser')

    new_sheet = workbook.create_sheet(sheet)
    #list of clusters
    h1_texts = [h1_tag.text for h1_tag in soup.find_all('h1', {'id': True})]
    print (h1_texts)
    # list of testprocedure's containing testcase
    test_tags = soup.select('h5[id^="_test_procedure"]')

    p = 2

    for test_tag in test_tags:
        h4_tag = test_tag.find_previous('h4')
        head= h4_tag.text
        index = test_tags.index(test_tag)
        print (index)
        
        table = test_tag.find_next('table')

        if table:
            rows = table.find_all('tr')
            data = []
            col_spans = []
            row_spans = []
            # to find the rowspan and colspan
            for i, row in enumerate(rows):
                cells = row.find_all(['th', 'td'])
                row_data = []
                for j, cell in enumerate(cells):
                    if cell.has_attr('colspan'):
                        col_spans.append((i, j, int(cell['colspan'])))
                    if cell.has_attr('rowspan'):
                        row_spans.append((i, j, int(cell['rowspan'])))
                    row_data.append(cell.get_text(strip=True))
                data.append(row_data)
            # Apply colspans to data
            for span in col_spans:
                i, j, span_size = span
                for k in range(1, span_size):
                    data[i].insert(j+1, '')
            # Apply rowspans to data
            for span in row_spans:
                i, j, span_size = span
                for k in range(1, span_size):
                    data[i+k].insert(j, '')

            # Convert the data into a pandas dataframe
            df = pd.DataFrame(data[1:], columns=data[0])

            # Replace any None values with an empty string
            df = df.fillna('')
            # convert the dataframe to dict
            data_dict = {}
            # convert the dataframe to dict
            data_dict = df.to_dict('list')
            print(data_dict)

            # list to stroe the col of testcase
            list_a = []
            list_b = []
            list_c = []
            list_d = []
            list_e = []

            for k, v in data_dict.items():
                if k == "#":
                    list_a = v
                elif k == "Ref":
                    list_b = v
                elif k == "PICS":
                    list_c = v
                elif k == "Test Step":
                    list_d = v
                elif k == "Expected Outcome":
                    list_e = v
            
            length = len(list_a)
            
            current =  p
            cell_head = 'B'+str(current)
            print(cell_head)
            new_sheet[cell_head] = head
            r = p+2
            col = 2
            # writing the headers of testcase
            for key in data_dict.keys():
                cell= new_sheet.cell(row=r, column=col, value=key)
                cell.font = openpyxl.styles.Font(bold=True)
                col += 1
                
            # writing the content of testcase
            for i in range(len(list_a)):
                new_sheet.cell(row=i+p+3, column=2, value=list_a[i])
                new_sheet.cell(row=i+p+3, column=3, value=list_b[i])
                new_sheet.cell(row=i+p+3, column=4, value=list_c[i])
                new_sheet.cell(row=i+p+3, column=5, value=list_d[i])
                new_sheet.cell(row=i+p+3, column=6, value=list_e[i])

            p = p + 4 + length
            
            workbook.save(filename) 
            print ("success for ",index)
        
        else:
            print ("fail")

if __name__ == '__main__':
    print("ready")
    appcluster = "path/to/file"
    index = "path/to/file"
    scrap(appcluster,"app_TC")
    scrap(index,'main_TC')
    workbook.save(filename)
