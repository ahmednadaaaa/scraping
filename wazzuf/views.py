import requests
from bs4 import BeautifulSoup
from django.shortcuts import render, redirect

def search_page(request):
    # Get the search query from the form
    search_query = request.GET.get('searchname', '').strip()
    
    if search_query:
        return redirect('scrape_jobs_search', search_job=search_query, page_num=0)
    
    return render(request, 'index.html')


def scrape_jobs(request, search_job="", page_num=0):
    search_query = request.GET.get('searchname', search_job)

    url1 = f"https://wuzzuf.net/search/jobs/?a=hpb&q={search_query}&start={page_num}"
    url2 = f"https://eg.indeed.com/jobs?q={search_query}&start={page_num}"
    url3 = f"https://www.linkedin.com/jobs/search/?currentJobId=3949748195&keywords={search_query}&origin=JOBS_HOME_SEARCH_BUTTON&refresh=true&start={page_num}"
    
    result1 = requests.get(url1).content
    result2 = requests.get(url2).content
    result3 = requests.get(url3).content
    
    soup1 = BeautifulSoup(result1, "lxml")
    soup2 = BeautifulSoup(result2, "lxml")
    soup3 = BeautifulSoup(result3, "lxml")

    job_titles1 = soup1.find_all("h2", {"class": "css-m604qf"})
    company_names1 = soup1.find_all("div", {"class": "css-d7j1kk"})
    location_names1 = soup1.find_all("span", {"class": "css-5wys0k"})
    job_skills1 = soup1.find_all("div", {"class": "css-y4udm8"})
    
    job_titles2 = soup2.find_all("h2", {"class": "jobTitle css-198pbd eu4oa1w0"})
    company_names2 = soup2.find_all("div", {"class": "css-1qv0295 e37uo190"})
    location_names2 = soup2.find_all("div", {"class": "text-location"})
    job_skills2 = soup2.find_all("div", {"class": "css-9446fg eu4oa1w0"})
    
    job_titles3 = soup3.find_all("div", {"class": "full-width artdeco-entity-lockup__title ember-view"})
    company_names3 = soup3.find_all("div", {"class": "artdeco-entity-lockup__subtitle ember-view"})
    location_names3 = soup3.find_all("div", {"class": "artdeco-entity-lockup__caption ember-view"})
    job_skills3 = soup3.find_all("div", {"class": "job-details-module__content"})
    
    jobs = []

    for i in range(min(len(job_titles1), len(company_names1), len(location_names1), len(job_skills1))):
        jobs.append({
            "title": job_titles1[i].text.strip(),
            "company": company_names1[i].text.strip(),
            "location": location_names1[i].text.strip(),
            "skills": job_skills1[i].text.strip(),
            "platform": "Wuzzuf"
        })
    
    for i in range(min(len(job_titles2), len(company_names2), len(location_names2), len(job_skills2))):
        jobs.append({
            "title": job_titles2[i].text.strip(),
            "company": company_names2[i].text.strip(),
            "location": location_names2[i].text.strip(),
            "skills": job_skills2[i].text.strip(),
            "platform": "Indeed"
        })
    
    for i in range(min(len(job_titles3), len(company_names3), len(location_names3), len(job_skills3))):
        jobs.append({
            "title": job_titles3[i].text.strip(),
            "company": company_names3[i].text.strip(),
            "location": location_names3[i].text.strip(),
            "skills": job_skills3[i].text.strip(),
            "platform": "LinkedIn"
        })

    prev_page_num = page_num - 1 if page_num > 0 else 0
    next_page_num = page_num + 1

    context = {
        'jobs': jobs,
        'search_job': search_query,
        'page_num': page_num,
        'prev_page_num': prev_page_num,
        'next_page_num': next_page_num,
    }
    
    return render(request, 'scraping/job_list.html', context)