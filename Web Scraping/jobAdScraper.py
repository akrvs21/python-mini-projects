import time as tm
import urllib.error
import urllib.parse
import urllib.request
from bs4 import BeautifulSoup

def find_jobs():
    # print("What to exclude ?")
    # unfamiliar_skills = input('>')
    # print('Filtering out...')

    f = urllib.request.urlopen("https://www.monster.com/jobs/search/?q=python&where=usa&jobid=222743833")
    soup = BeautifulSoup(f, 'lxml')
    jobList = soup.find_all('section', class_="card-content")
    jobList = jobList[1:len(jobList)]
    count = 0
    print(jobList)
    print(len(jobList))
    for index,job in enumerate(jobList):
        if 'apas-ad' in job.get('class'):
            continue
        else:
            time = job.find('time').text
            rec_time = ''
            if time[0] == 'P':
                rec_time = time
                time = 0
            else:
                time = int(time[0:2])

            if time <= 3 or rec_time == 'Posted today':
                count += 1
                with open(f'posts/{rec_time if time == 0 else str(time) + " days ago"}.txt','w') as f:
                    title = job.find('h2', class_="title").a.text.strip()
                    company = job.find('div', class_="company").span.text.strip()
                    location = job.find('div', class_="location").span.text.strip()
                    f.write(f"Title: {title}\n")
                    f.write(f"Company: {company}\n")
                    f.write(f"Location: {location}\n")
                    f.write(f"Published date: {rec_time if time == 0 else str(time) + ' days ago'}")
                    print(f"File {count} saved")

if __name__ == "__main__":
    while True:
        print('Scraping....')
        find_jobs()
        print('Done!')
        time_wait = 10
        tm.sleep(time_wait * 60)
        print(f'Refreshed after {time_wait} minutes.')