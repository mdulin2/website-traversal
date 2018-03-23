from lib.google_search_results import GoogleSearchResults
def map_site_helper(url,link_list,count,iterations):
    if(count == iterations):
        return link_list
    new_url = url
    query = GoogleSearchResults({"q": url,"num":20})
    json_results = query.get_json()
    print json_results
    for item in json_results["organic_results"]:
        new_url += " -" + item['link']
        link_list.append(item['link'])
    return map_site_helper(new_url,link_list,count+1,iterations)


def map_site(url,iterations):
    return map_site_helper(url,[],1,iterations)
#print json_results

link_list = map_site("site:zagweb.gonzaga.edu",3)
for item in link_list:
    print item
