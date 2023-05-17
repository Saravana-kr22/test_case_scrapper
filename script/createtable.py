def create_df(table):
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
                            for r in range(1, span_size):
                                data[i].insert(j+1, '')
                        # Apply rowspans to data
                        for span in row_spans:
                            i, j, span_size = span
                            for r in range(1, span_size):
                                data[i+r].insert(j, '')

                        # Convert the data into a pandas dataframe
                        df = pd.DataFrame(data[1:], columns=data[0])

                        # Replace any None values with an empty string
                        df = df.fillna('')
                        # convert the dataframe to dict
                        data_dict = {}
                        # convert the dataframe to dict
                        data_dict = df.to_dict('list')
                        print(data_dict)
                        return(data_dict)
