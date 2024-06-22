from bs4 import BeautifulSoup
import requests

file = open('scrape.html', 'r')
content = file.read()
file.close()
#html_text = requests.get('https://www.sanfoundry.com/1000-data-structure-questions-answers/').text
# print(html_text)
soup = BeautifulSoup(content, 'lxml')
#question = soup.find('div', class_="entry-content")
#questions = question.find('p')
c_choice = soup.find_all('div', class_="collapseomatic_content")

question_limit = 10

list_p = []
paragraph = soup.find_all('p')
i = 0
for para in paragraph:
    if para != "":
        # print(para.text)
        soup = BeautifulSoup(para.text, 'lxml')
        html = soup.find('p', class_="")
        # print(html)
        if i != 0:
            if html != None and html.string[0].isdigit():
                # print(html)
                list_p.append(html.string)
        i += 1

        if i > question_limit:
            # print(html.string)
            break
    # if html != None and html.string[0].isdigit():
    #    print(html.string)
        # print(html_list)
# print(list_p)

dict = {}

for i in list_p:
    # rint()
    # break
    index = list_p.index(i)
    strip = i.split('\n')
    if strip[0].startswith('23'):
        list_p[index] = list_p[index] + '\n' + list_p[index + 1]
        del list_p[index + 1]
    if strip[0].startswith('36'):
        list_p[index] = list_p[index] + '\n' + list_p[index + 1]
        del list_p[index + 1]
    if strip[0].startswith('30'):
        list_p[index] = list_p[index] + '\n' + list_p[index + 1]
        del list_p[index + 1]
    # for j in strip:
    #    if j[0].startswith('23'):
     #       print(j)

c_choice_clean = []
for choice in c_choice:
    strip = choice.text.split('\n')
    # print(strip)
    for i in strip:
        if i.startswith("Answer"):
            c_choice_clean.append(i[8])

for i in list_p:
    strip = i.split('\n')
    index = list_p.index(i)
    #strip = strip[4]
    #print(strip, index)
    #print(strip, index)
    try:
        dict[strip[0]] = [[strip[1], None], [strip[2], None], [strip[3], None], [strip[4], None]]
    except:
        print(strip)
    for j in range(1, 5):
        if strip[j][0] == c_choice_clean[index]:
            #print(strip[0], c_choice_clean[index])
            dict[strip[0]][j-1][1] = True
        else:
            dict[strip[0]][j-1][1] = False

# print(dict)


# print(c_choice_clean)
