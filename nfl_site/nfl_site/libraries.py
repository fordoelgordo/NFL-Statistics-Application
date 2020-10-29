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