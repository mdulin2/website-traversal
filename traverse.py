
import requests
import re
import time
import sys
#the list that is discovered
global full_list
#the hiearchy of the children
global map_dict
#the url associated with every child
global reference_dict
#the name of the overall child name count
global iteration
#how many total requests have been made
global resets

"""
ILY
This is a website mapper. It goes through and finds all of the links in the project!
It can get the links in no order or in a recursive tree.
Possibly add a login functionality here?
"""

"""
traverses a website that doesn't require authentication
Args:
    url: the url being tested!
    base: the base of the URL being tested on
    amount: the amount of traverses to make
    whos: True, include only the domains addresses. False otherwise
    name: the current nodes name on the reference_dict
"""
def call(url,base,amount,whos,name,depth):
    global iteration
    global resets
    amount +=1

    #don't want to overdo the amount of requests
    if(iteration % resets >= 150):
        time.sleep(0.500)
        resets+=1

    #the ending case/adds the link to the history, but doesn't follow the rabbit hole
    if(amount >= depth or base not in url):
        map_dict[name] = []
        reference_dict[name] = url
        return

    #getting the page
    source = str(url.encode('UTF-8'))
    r = requests.get(source)
    site = str(r.text.encode('UTF-8'))

    #regular expression for finding all links!
    match = re.findall(r'href=[\'"]?([^\'" >]+)', site)

    new_list = init_address(match,base)
    list_of_new = unique_address(new_list,whos,base)

    for item in list_of_new:
        iteration+=1

        #sets up the dictionary tree
        if(name not in map_dict):
            map_dict[name] = [iteration]
            reference_dict[iteration] = item
        elif(item):
            lst = map_dict[name]
            lst.append(iteration)
            map_dict[name] = lst
            reference_dict[iteration] = item

        #recursive call
        call(item,base,amount,whos,iteration,depth)

    if list_of_new == []:
        map_dict[name] = []
        reference_dict[name] = url

#matches intial addresses
def init_address(match,base):
    new_list = set()
    for post in match:
        if(post[0] == '/'):
            tmp = post
            new_list.add(base + tmp)
        elif(post[0]!= 'h'):
            new_list.add(base + "/"+  post)

        #could have a process to check for all things to check for...
        elif("instagram" in post):
            pass
        elif post != None:
            new_list.add(post)
    return new_list

#matches unique addresses
def unique_address(new_list,whos,base):
    #gets the unique addresses
    list_of_new = list()
    for post in new_list:
        if(whos):
            #only use links that are associated with the website
            if(base in post and post not in full_list):
                list_of_new.append(post)
                full_list.append(post)
        elif(post not in full_list):
            list_of_new.append(post)
            full_list.append(post)
    return list_of_new

#flattens the giant list
def flatten(container):
    for i in container:
        if isinstance(i, (list,tuple)):
            for j in flatten(i):
                yield j
        else:
            yield i

#recursively prints the map of a website
"""
Args:
    key: the current spot on the tree
    spot: the amount of depth in the tree
    mode: the type of display- 1 for tree numbers, anything else for URLs.
"""
def traverse_tree(key,spot,mode):
    tabs = ""
    for i in range(spot):
        tabs += '\t'

    for item in map_dict[key]:
        if(mode == 1):
            print tabs + reference_dict[item]
        else:
            print tabs + str(item)
        traverse_tree(item,spot+1,mode)

"""
Runs a full traverse of the website
Args:
    website(string): this is just a url for the site
    throughput(bool): True if just wanting the links on the website, False if you want all links
    depth(int): the depth that the tree will go
    website_base(int/string): if the base of the website is the same as the website being called it's 0.
                        any other string otherwise
"""
def run_traversal(website,throughput,depth, website_base = 0):
    global full_list,map_dict,reference_dict,iteration,resets
    full_list = list()
    map_dict = dict()
    reference_dict = dict()
    iteration = 0
    resets = 1

    if(website_base == 0):
        website_base = website
    call(website,website_base,0,throughput,0,depth)
    #traverse_tree(0,0,1)

"""
The recursive function for making the mapped page.
Args:
    child(int): the ID of the child node being called
    parent(int): the parent of which the child came from
Returns:
    totalString(html code): the entire main file, where all of the iFrames end up.
"""
def display_rec(child,parent):

    #ending case; no more children in line
    if(map_dict[child] == []):
        make_frame(child)
        return get_frame_code(parent,child)

    #breath first search iteration
    totalString = ""
    for spot in map_dict[child]:
        make_frame(spot)
        totalString += get_frame_code(child,spot)

    #the recursive call, breath first
    for item in map_dict[child]:
        totalString+= display_rec(item,child)
    return totalString

"""
Gets the code for the frame for the main file
Args:
    parent(int): the parent that called the name, or child
    name(int): the child node being called
Returns:
    html_doc_tmp(html code): The iFrame reference in the main file
"""
def get_frame_code(parent,name):

        html_doc_tmp = """
        Page of: %s Child of: %s
        <iframe src = "%s" width = "200" height = "200">
        </iframe>

       """ % (reference_dict[name],reference_dict[parent],str(name)+".html")
        return html_doc_tmp

"""
Create the html page for the iFrame
Args:
    name(int): the reference_dict ID of the URL
"""
def make_frame(name):

    #source = str(url.encode('UTF-8'))
    r = requests.get(reference_dict[name])
    site = str(r.text.encode('UTF-8'))
    f = open("visual/"+str(name)+ ".html",'w')
    f.write(site)
    f.close()

if __name__ == "__main__":
    global reference_dict
    run_traversal("https://moxie.org",True,3)
    #traverse_tree(0,0,1) # a full tree, indented traversal

    reference_dict[0] = "https://moxie.org"
    total_file = display_rec(0,0)
    f = open("visual/"+str("max")+ ".html",'w')
    f.write(total_file)
    f.close()
