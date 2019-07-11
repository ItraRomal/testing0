import bs4
import requests
import sys
import time

base_url = 'http://s3.eu-central-1.amazonaws.com/qa-web-test-task/'
no_links = list()
no_text = list()
no_href = list()

def get_next_page(page_num):
    return '{}{}.html'.format(base_url, page_num)


def link_check(url):
    # получаем html код страницы
    request = requests.get(url)

    soup = bs4.BeautifulSoup(request.content, 'html.parser')
    # not_links.append(request)
    links = soup.find_all('a')
    print(url)
    if not links:
        print(' IS FAILED WITH NO LINK')
        no_links.append(url)
    elif not links[0].text:
        print(' IS FAILED WITH NO TEXT')
        no_text.append(url)
    elif not links[0]['href']:
        print(' IS FAILED WITH NO HREF')
        no_href.append(url)
    else :
        print(' is Ok')


start_page_num = int(sys.argv[1])
final_page_num = int(sys.argv[2])
n = str(final_page_num - start_page_num)

while (start_page_num < final_page_num):
    url = get_next_page(start_page_num)
    link_check(url)
    start_page_num += 1

print("Job is done!")
print("You've checked " + n + " link(s)")
print("Do you wanna have a text file with a report? (y/n)")
agree = input()
if agree == 'y' or agree == 'Y':

    report_day = time.strftime("%Y%m%d")
    with open("report" + report_day + ".txt", "w") as file:

        print('FAILED WITH NO LINKS: ', file=file)
        print(no_links, file=file)
        print('FAILED WITH NO TEXT: ', file=file)
        print(no_text, file=file)
        print('FAILED WITH NO HREFS: ', file=file)
        print(no_href, file=file)

    print("Report has been saves as 'report" + report_day + ".txt'")

else:

    print('FAILED WITH NO LINKS')
    print(no_links)
    print('FAILED WITH NO TEXT')
    print(no_text)
    print('FAILED WITH NO HREFS')
    print(no_href)
