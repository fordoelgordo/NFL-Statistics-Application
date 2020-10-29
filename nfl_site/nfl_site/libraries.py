'''
Author: FSt. J
Comments: We'll use this .py file to maintain all of our user-defined functions for the project
          Note that functions within this code can be called using the following syntax
          from nfl_site.nfl_site.libraries import <my_function1>, <my_function2>, ... : for specific functions OR
          from nfl_site.nfl_site.libraries import * : for all functions
'''

'''
Author: FSt.J
Comments: Global function to convert  heigh in decimal inches to cleaner view
'''
def conv_height(h):
    ft = int(divmod(h,12)[0])
    inch = round(int(divmod(h,12)[1]),0)
    if h == 0 or h == "" or h == " ":
        return ""
    else:
        return str(ft)+"'"+str(inch)+"\""

def getIndexes(dfObj, value):
    ''' Get index positions of value in dataframe i.e. dfObj.'''
    listOfPos = list()
    # Get bool dataframe with True at positions where the given value exists
    result = dfObj.isin([value])
    # Get list of columns that contains the value
    seriesObj = result.any()
    columnNames = list(seriesObj[seriesObj == True].index)
    # Iterate over list of columns and fetch the rows indexes where value exists
    for col in columnNames:
        rows = list(result[col][result[col] == True].index)
        for row in rows:
            listOfPos.append((row, col))
    # Return a list of tuples indicating the positions of value in the dataframe
    return listOfPos