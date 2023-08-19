
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pprint
from bs4 import BeautifulSoup


driver = webdriver.Chrome()
driver.get("https://linkedin.com/uas/login")
sleep(2)
driver.find_element(By.XPATH, "//*[@id='username']").send_keys("surya@klizos.com")
driver.find_element(By.XPATH, "//*[@id='password']").send_keys("Surya@2201")
driver.find_element(By.XPATH, "//*[@id='organic-div']/form/div[3]/button").click()
sleep(10)

url='https://www.linkedin.com/in/subhadeep-banerjee/'
#url='https://www.linkedin.com/in/supriyapatra/'
#url='https://www.linkedin.com/in/reya-ghosh-a19542173/'
#url='https://www.linkedin.com/in/sourav-sarkar-85a981158/'
#url='https://www.linkedin.com/in/shreyosi-roy-615972147/'
#url='https://www.linkedin.com/in/priyanka-sen-a7484815a/'

driver.get(url)
sleep(2)

source = driver.page_source
#print(source)
soup=BeautifulSoup(source,'html.parser')
#print(soup)

#detail
dic={}
detail=soup.find('div',class_="mt2 relative")
name=detail.find('h1',class_='text-heading-xlarge inline t-24 v-align-middle break-words').text
name=name.strip('\n')
dic['name']=name
print('name:'+name)
highlights=detail.find('div',class_='text-body-medium break-words').text.strip()
print("highlights:"+highlights)
dic['highlights']=highlights

curr_company=detail.find("button","pv-text-details__right-panel-item-link text-align-left")
if curr_company == None:
    pass
else:
    curr_company = curr_company.text.strip()
    print('current_company:'+curr_company)
    dic['current_company']=curr_company

#Location

location=detail.find('span',class_='text-body-small inline t-black--light break-words')
if location == None:
    pass 
else:
    location = location.text.strip()
    if ',' in location:
        location=location.split(',')
        loc={'city':location[0],"state":location[1],'country':location[2]}
        print(loc)
        dic['location']=loc
    else:
        print(location)
        dic['location']=location

#connectioon and Followers
confol=soup.find('ul',class_='pv-top-card--list pv-top-card--list-bullet')
connfoll=confol.find_all('li')
i=len(connfoll)
if i==2:
    con_fol=confol.find_all("span",class_='t-bold')
    follower=con_fol[0].text
    connection=con_fol[1].text
else:
    foll=soup.find('p',class_='pvs-header__subtitle pvs-header__optional-link text-body-small')
    follower=foll.find('span',class_='visually-hidden').text
    follower=follower.strip(" followers")
    conn=soup.find("li",class_='text-body-small')
    connection=conn.find('span',class_='t-bold').text.strip()  
print('follower:' +follower.replace(',',''))
print('connection:'+connection)
dic['follower']=(follower.replace(',',''))
dic['connection']=(connection)


#profile
prof=soup.find('div',class_="pv-top-card__non-self-photo-wrapper ml0")
profile=prof.find("img",'pv-top-card-profile-picture__image pv-top-card-profile-picture__image--show evi-image ember-view')
if (profile==None):
    print(None)
else:    
    profile=profile['src']
    print("profile_link: "+profile)
    dic['display_photo']=profile
    

#banner
bann=soup.find('div',class_='profile-background-image__image-container')
if (bann==None):
    print(None)
else:    
    banner=bann.find('img',class_='profile-background-image__image relative full-width full-height')
    banner=banner['src']
    print("banner_link: "+banner)
    dic['banner']=banner


all_info=soup.find_all(class_='artdeco-card ember-view relative break-words pb3 mt2')
key=[]
value=[]
wh_info=['about','experience','education','skills','projects','publications','languages','licenses_and_certifications', 'volunteering_experience','courses', 'honors_and_awards','organizations']
len(all_info)

for i in all_info:
    name=i.find('div',class_="pv-profile-card__anchor") 
    na=name['id']
    if na in wh_info:
        key.append(na)
        value.append(i)
        

#About Section
def about1(i):
    About=i.find('div',class_="pv-shared-text-with-see-more full-width t-14 t-normal t-black display-flex align-items-center")
    about=About.find('span',class_="visually-hidden").text.replace("\n","")
    return about

for i in key:
    if i=="about":
        ind=key.index('about')
        about=about1(value[ind])
        if len(expe)==0:
            print(None)
        else:
            dic["about"]= about
        break
    else:
        about= None   
print(about)


#Experience Section 
def experience(i):
    footer=(i.find("div",class_='pvs-list__footer-wrapper'))
    if (footer==None):
        all_exp=i.find('ul',class_='pvs-list')
        li_tag=all_exp.find_all('li',class_= 'artdeco-list__item pvs-list__item--line-separated pvs-list__item--one-column')
        exp=experience2(li_tag) 
    else:
        a_tag=footer.find('a')
        a_tag=a_tag['href']
        driver.get(a_tag)
        sleep(2)
        source_exp= driver.page_source
        soup_exp=BeautifulSoup(source_exp,'html.parser')
        ul_exp=soup_exp.find('ul',class_='pvs-list')
        li_exp=ul_exp.find_all('li',class_= 'pvs-list__paged-list-item artdeco-list__item pvs-list__item--line-separated pvs-list__item--one-column')
        #print(li_exp)
        exp=experience2(li_exp)
        
    return exp
    
def experience2(li_tag2):    
    experience_dict={}
    num=0
    for li in li_tag2:
        num=num+1
        exp_dict={}
        job_detail=li.find('div',class_="display-flex flex-row justify-space-between")
        span=li.find_all("div",class_="display-flex flex-wrap align-items-center full-height")  
        if len(span)>1:
            company=job_detail.find('div',class_="display-flex full-width")
            if company==None:
                company_name=None
            else:    
                company_name=company.find('span',class_="visually-hidden").text
                
            exp_dict['company_name']=company_name
            #print(company_name)
            time=job_detail.find('span',class_="t-14 t-normal")
            if time==None:
                period=None
            else:    
                period=time.find('span',class_="visually-hidden").text
            exp_dict['time_peroid']=period
            #print(period)
            
            loc=job_detail.find('span',class_="t-14 t-normal t-black--light")
            if loc==None:
                location=None
            else:    
                location=loc.find('span',class_="visually-hidden").text
            exp_dict['location']=location
            #print(location)
            experience_dict["job_"+str(num)]=exp_dict   
            outer=li.find('div',class_='pvs-list__outer-container')
            outer_li=outer.find_all('li',class_='pvs-list__item--one-column')
            #print(len(outer_li))
            num1=0
            for j in outer_li:
                des_dict={}
                outer_info=j.find('div',class_="display-flex flex-row justify-space-between")
                if outer_info==None:
                    pass
                else:
                    dest_info=outer_info.find('div',class_='display-flex align-items-center mr1 hoverable-link-text t-bold')
                    if dest_info==None:
                        pass
                    else:
                        dest=dest_info.find('span',class_="visually-hidden").text.strip()
                        num1=num1+1
                        des_dict['designation']=dest
                        #print(num1)
                        #print(dest)
                    time=outer_info.find("span",class_='t-14 t-normal t-black--light')
                    if time==None:
                        pass
                    else:
                        time_hid=time.find('span',class_="visually-hidden").text.strip()
                        des_dict['period']=time_hid
                        #print(time_hid)
                    exp_dict["degination_"+str(num1)]=des_dict
            experience_dict["job_"+str(num)]=exp_dict    

  
        else:
            #detail=job_detail.find_all('span',class_="visually-hidden")
            #print(len(detail))
            job_degin=job_detail.find("div",class_='display-flex')
            degin=job_degin.find('span',class_='visually-hidden').text.strip()
            #print(degin)
            exp_dict["desgination"]=degin
            
            company_name=job_detail.find('span',class_='t-14 t-normal')
            #print(company_name)
            company=company_name.find('span',class_='visually-hidden').text.strip()
            exp_dict["company"]=company
            #print(company)
            
            loc_period=job_detail.find_all('span',class_='t-14 t-normal t-black--light')
            if len(loc_period)==1:
                time=loc_period[0].find('span',class_='visually-hidden').text.strip()
                location=None
            else:
                time_loc=loc_period[0].find('span',class_='visually-hidden').text.strip()
                time=time_loc
                time_loc=loc_period[1].find('span',class_='visually-hidden').text.strip()
                location=time_loc
                
            
            
            exp_dict["time"]=time
            exp_dict['location']=location

            outer2=li.find('div',class_='pvs-list__outer-container')
            if outer2==None:
                exp_dict['skill']=None
                exp_dict['Description']=None
            else:

                outer_li=outer2.find_all("li",class_='pvs-list__item--one-column')

                if(len(outer_li))==1:
                    outer_li_hid=outer_li[0].find('span',class_="visually-hidden")
                    strong_outer_li_hid=outer_li_hid.find("strong")
                    if strong_outer_li_hid==None:
                        description=outer_li_hid.text.strip()
                        exp_dict['Description']=description.replace("\n","")
                        exp_dict['skill']=None
                    else:
                        skill=description=outer_li_hid.text.strip()
                        exp_dict['description']=None
                        exp_dict['skill']=skill

                elif(len(outer_li)==2):
                    outer_li_hid=outer_li[0].find('span',class_="visually-hidden")
                    strong_outer_li_hid=outer_li_hid.find("strong")
                    if strong_outer_li_hid==None:
                        description=outer_li_hid.text.strip()
                        exp_dict['description']=description.replace("\n","")
                        exp_dict['skill']=None
                    else:
                        skill=outer_li_hid.text.strip()
                        exp_dict['skill']=skill
                        exp_dict['description']=None

                    outer_li_hid=outer_li[1].find('span',class_="visually-hidden")
                    strong_outer_li_hid=outer_li_hid.find("strong")
                    if strong_outer_li_hid==None:
                         pass
                    else:

                        skill=outer_li_hid.text.strip()
                        exp_dict['skill']=skill

                else:

                    outer_li_hid=outer_li[0].find('span',class_="visually-hidden")
                    strong_outer_li_hid=outer_li_hid.find("strong")
                    if strong_outer_li_hid==None:

                        description=outer_li_hid.text.strip()
                        exp_dict['description']=description.replace("\n","")
                        exp_dict['skill']=None
                    else:

                        skill=outer_li_hid.text.strip()
                        exp_dict["description"]=None
                        exp_dict['skill']=skill

                    outer_li_hid=outer_li[2].find('span',class_="visually-hidden")
                    strong_outer_li_hid=outer_li_hid.find("strong")
                    if strong_outer_li_hid==None:
                          pass
                    else:
                        skill=outer_li_hid.text.strip()
                        exp_dict['skill']=skill

            experience_dict["job_"+str(num)]=exp_dict         
    return experience_dict    
          
                 
for i in key:
    if i=="experience":
        ind=key.index('experience')
        expe=experience(value[ind])
        if len(expe)==0:
            print(None)
        else:
            dic["experience"]= expe 
        break
    else:
        expe= None   
print(expe)

#Education Section 
def education(i):
    edu={}
    num=0
    
    footer=i.find('div',class_='pvs-list__footer-wrapper')
    if footer is None:
        all_edu=i.find('ul',class_='pvs-list')
        li_tag=all_edu.find_all('li',class_= 'artdeco-list__item pvs-list__item--line-separated pvs-list__item--one-column')
    else:
        a_tag=footer.find('a')
        a_tag=a_tag['href']
        #print(a_tag)
        driver.get(a_tag)
        sleep(5)
        source_skill = driver.page_source
        #print(source_skill)
        soup_skill=BeautifulSoup(source_skill,'html.parser')
        ul_skill=soup_skill.find('ul',class_='pvs-list')
        li_tag=ul_skill.find_all('li',class_= 'pvs-list__paged-list-item artdeco-list__item pvs-list__item--line-separated pvs-list__item--one-column')
        print(len(li_tag))
        
    for li in li_tag:
        num=num+1
        dic1={}
        info=li.find('div',class_="display-flex flex-row justify-space-between")   
        school=info.find("div",class_='display-flex flex-wrap align-items-center full-height')
        school_name=school.find('span',class_="visually-hidden").text
        dic1['college/school']=school_name
        #print(school_name)
        degree=info.find("span",class_='t-14 t-normal')
        degree_name=degree.find('span',class_="visually-hidden").text
        #print(degree_name)
        dic1['degree']=degree_name
        year=info.find("span",class_='t-14 t-normal t-black--light')
        year_name=year.find('span',class_="visually-hidden").text
        #print(year_name)
        dic1['year']=year_name
        outer=li.find("div",class_='pvs-list__outer-container')
        if outer == None:
            skill=None  
        else:
            visually_hidden=outer.find('span',class_='visually-hidden')
            if visually_hidden is None:
                skill=None
            else:
                skill=visually_hidden.text().strip()
        dic1['skill']=skill
        edu['education_'+str(num)]=dic1
    return edu

for i in key:
    if i=="education":
            ind=key.index('education')
            educ=education(value[ind])
            if len(educ)==0:
                print(None)
            else:
                dic["education"]= educ
            break
    else:
        educ= None   
print(educ)

#Skills Section
def skills(i):
    skill={}
    all_skills=i.find('ul',class_='pvs-list')
    footer=i.find('div',class_='pvs-list__footer-wrapper')
    #print(footer)
    num=0
    if footer==None:
        li_tag=all_skills.find_all('li',class_= 'artdeco-list__item pvs-list__item--line-separated pvs-list__item--one-column')
        for li in li_tag:
            num=num+1
            info=li.find('div',class_="display-flex flex-row justify-space-between")
            #print(info)
            skills=info.find('span',class_='visually-hidden').text
            skill['skill_'+str(num)]=skills
        
    else:
        a_tag=footer.find('a')
        a_tag=a_tag['href']
        #print(a_tag)
        driver.get(a_tag)
        sleep(5)
        source_skill = driver.page_source
        #print(source_skill)
        soup_skill=BeautifulSoup(source_skill,'html.parser')
        ul_skill=soup_skill.find('ul',class_='pvs-list')
        li_tag=ul_skill.find_all('li',class_= 'pvs-list__paged-list-item artdeco-list__item pvs-list__item--line-separated pvs-list__item--one-column')
        
        
        print(len(li_tag))
        for li in li_tag:
            
            num=num+1
            info=li.find('div',class_="display-flex flex-row justify-space-between")
            #info=li.find('div',class_="display-flex flex-wrap align-items-center full-height")
            skills=info.find('span',class_='visually-hidden').text
            skill['skill_'+str(num)]=skills
            
            
    return skill
for i in key:
    if i=="skills":
            ind=key.index('skills')
            skill=skills(value[ind])
            if len(skill)==0:
                print(None)
            else:
                dic["skills"]=skill
            break
    else:
        skill= None   
print(skill)

#Courses Section 
def courses(i):
    all_course=i.find('ul',class_='pvs-list')
    footer=i.find('div',class_='pvs-list__footer-wrapper')
    #print(footer)
    course={}
    num=0
    if footer==None:
        li_tag=all_course.find_all('li',class_= 'artdeco-list__item pvs-list__item--line-separated pvs-list__item--one-column')
        list1=[]
        for li in li_tag:
            num=num+1
            info=li.find('div',class_="display-flex flex-row justify-space-between")
            #print(info)
            courses=info.find('span',class_='visually-hidden').text
            course['course_'+str(num)]=courses
    else:
        a_tag=footer.find('a')
        a_tag=a_tag['href']
        #print(a_tag)
        driver.get(a_tag)
        sleep(2)
        source_courses = driver.page_source
        soup_courses=BeautifulSoup(source_courses,'html.parser')
        ul_courses=soup_courses.find('ul',class_='pvs-list')
        li_courses=ul_courses.find_all('li',class_= 'pvs-list__paged-list-item artdeco-list__item pvs-list__item--line-separated pvs-list__item--one-column')
        list1=[]
        for li in li_courses:
            num=num+1
            info=li.find('div',class_="display-flex flex-row justify-space-between")
            #print(info)
            courses=info.find('span',class_='visually-hidden').text
            course['course_'+str(num)]=courses
            
    return course


for i in key:
    if i=="courses":
        ind=key.index('courses')
        course=courses(value[ind])
        if len(course)==0:
            print(None)
        else:
            dic["courses"]= course
        break
    else:
        course= None   
print(course)


#Languages Section 

def languages(i):
    all_languages=i.find('ul',class_='pvs-list')
    footer=i.find('div',class_='pvs-list__footer-wrapper')
    #print(footer)
    langu_dict={}
    num=0
    if footer==None:
        li_tag=all_languages.find_all('li',class_= 'artdeco-list__item pvs-list__item--line-separated pvs-list__item--one-column')
        #print(li_tag)
        for li in li_tag:
            num=num+1
            lan_dict={}
            info=li.find('div',class_="display-flex align-items-center mr1 t-bold")
            languages=info.find('span',class_='visually-hidden')
            lan=languages.text
            lan_dict['language_name']=lan
            level=li.find('span',class_='t-14 t-normal t-black--light')
            level_lan=level.find('span',class_='visually-hidden').text
            lan_dict['Knowing_level']=level_lan
            langu_dict['language_'+str(num)]=lan_dict
        
    else:
        a_tag=footer.find('a')
        a_tag=a_tag['href']
        driver.get(a_tag)
        sleep(2)
        source_languages = driver.page_source
        soup_languages=BeautifulSoup(source_languages,'html.parser')
        ul_languages=soup_languages.find('ul',class_='pvs-list')
        li_languages=ul_languages.find_all('li',class_= 'pvs-list__paged-list-item artdeco-list__item pvs-list__item--line-separated pvs-list__item--one-column')

        for li in li_languages:
            num=num+1
            lan_dict={}
            info=li.find('div',class_="display-flex align-items-center mr1 t-bold")
            languages=info.find('span',class_='visually-hidden')
            lan=languages.text
            lan_dict['language_name']=lan
            level=li.find('span',class_='t-14 t-normal t-black--light')
            level_lan=level.find('span',class_='visually-hidden').text
            lan_dict['Knowing_level']=level_lan
            langu_dict['language_'+str(num)]=lan_dict
            
            
    return langu_dict

for i in key:
    if i=="languages":
        ind=key.index('languages')
        language=languages(value[ind])
        if len(language)==0:
            print(None)
        else:
            dic["languages"]= language
       
        break
    else:
        language= None 
        
print(language)

# lisence Section 

def lisence(i):
    all_licenses=i.find('ul',class_='pvs-list')
    footer=i.find('div',class_='pvs-list__footer-wrapper')
    #print(footer)
    lisence_dict={}
    num=0
    if footer==None:
        li_tag=all_licenses.find_all('li',class_= 'artdeco-list__item pvs-list__item--line-separated pvs-list__item--one-column')
        for li in li_tag:
            num=num+1
            lis_dic={}
            info=li.find('div',class_="display-flex flex-row justify-space-between")
            tittle=info.find('div',class_='display-flex full-width')
            licenses_tittle=tittle.find('span',class_='visually-hidden').text
            lis_dic['tittle']=licenses_tittle
            lisence_comp=info.find('span',class_='t-14 t-normal')
            if lisence_comp==None:
                lis_company=None
            else:
                lis_company=lisence_comp.find('span','visually-hidden').text
            lis_dic['company']=lis_company
            lisence_date=info.find('span',class_='t-14 t-normal t-black--light')
            if lisence_date==None:
                lis_date=None
            else:
                lis_date=lisence_date.find('span','visually-hidden').text
            lis_dic['time']=lis_date
            lisence_dict['certificate_'+str(num)]=lis_dic        

    else:
        a_tag=footer.find('a')
        a_tag=a_tag['href']
        #print(a_tag)
        driver.get(a_tag)
        sleep(2)
        source_licenses = driver.page_source
        #print(source_skill)
        soup_licenses=BeautifulSoup(source_licenses,'html.parser')
        ul_licenses=soup_licenses.find('ul',class_='pvs-list')
        li_tag=ul_licenses.find_all('li',class_= 'pvs-list__paged-list-item artdeco-list__item pvs-list__item--line-separated pvs-list__item--one-column')
        list1=[]
        for li in li_tag:
            num=num+1
            lis_dic={}
            info=li.find('div',class_="display-flex flex-row justify-space-between")
            #print(info)
            tittle=info.find('div',class_='display-flex full-width')
            licenses_tittle=tittle.find('span',class_='visually-hidden').text
            #print(licenses_tittle)
            lisence_comp=info.find('span',class_='t-14 t-normal')
            if lisence_comp==None:
                lis_company=None
            else:
                lis_company=lisence_comp.find('span','visually-hidden').text
            lis_dic['company']=lis_company
            lisence_date=info.find('span',class_='t-14 t-normal t-black--light')
            if lisence_date==None:
                lis_date=None
            else:
                lis_date=lisence_date.find('span','visually-hidden').text
            lis_dic['time']=lis_date
            lisence_dict['certificate_'+str(num)]=lis_dic 

    return lisence_dict
for i in key:
    if i=="licenses_and_certifications":
            ind=key.index('licenses_and_certifications')
            licenses=lisence(value[ind])
            if len(licenses)==0:
                print(None)
            else:
                dic["licenses_and_certifications"]=licenses

            break
    else:
        licenses= None 
        
print(licenses)        

# voluntering section 
def volutering(i):
    all_volut=i.find('ul',class_='pvs-list')
    footer=i.find('div',class_='pvs-list__footer-wrapper')
    #print(footer)
    volentring_dict={}
    num=0
    if footer==None:
        li_tag=all_volut.find_all('li',class_= 'artdeco-list__item pvs-list__item--line-separated pvs-list__item--one-column')
        for li in li_tag:
            num=num+1
            volut_dic={}
            info=li.find('div',class_="display-flex flex-column full-width align-self-center")
            #print(info)
            tittle=info.find('div',class_='display-flex full-width')
            volut_tittle=tittle.find('span',class_='visually-hidden').text
            print(volut_tittle)
            volut_comp=info.find('span',class_='t-14 t-normal')
            if volut_comp==None:
                volut_company=None
            else:
                volut_company=volut_comp.find('span','visually-hidden').text
            volut_dic['voluterring_company']=volut_company    
            volut_date=info.find('span',class_='t-14 t-normal t-black--light')
            if volut_date==None:
                volut_date=None
            else:
                volut_date=volut_date.find('span','visually-hidden').text
            volut_dic['voluterring_date']=volut_date
            outer=info.find("div",class_='pvs-list__outer-container')
            if outer==None:
                about=None
            else:
                about=outer.find('span',class_='visually-hidden').text
            volut_dic['voluterring_about']=about 
            volentring_dict['volentring_'+str(num)]=volut_dic

    else:
        a_tag=footer.find('a')
        a_tag=a_tag['href']
        #print(a_tag)
        driver.get(a_tag)
        sleep(2)
        source_volut = driver.page_source
        #print(source_skill)
        soup_volut=BeautifulSoup(source_volut,'html.parser')
        ul_volut=soup_volut.find('ul',class_='pvs-list')
        li_tag=ul_volut.find_all('li',class_= 'pvs-list__paged-list-item artdeco-list__item pvs-list__item--line-separated pvs-list__item--one-column')
        for li in li_tag:
            volut_dic={}
            num=num+1
            info=li.find('div',class_="display-flex flex-column full-width align-self-center")
            #print(info)
            tittle=info.find('div',class_='display-flex full-width')
            volut_tittle=tittle.find('span',class_='visually-hidden').text
            #print(volut_tittle)
            volut_comp=info.find('span',class_='t-14 t-normal')
            if volut_comp==None:
                volut_company=None
            else:
                volut_company=volut_comp.find('span','visually-hidden').text
            volut_dic['voluterring_company']=volut_company    
            volut_date=info.find('span',class_='t-14 t-normal t-black--light')
            if volut_date==None:
                volut_date=None
            else:
                volut_date=volut_date.find('span','visually-hidden').text
            volut_dic['voluterring_date']=volut_date    
            outer=info.find("div",class_='pvs-list__outer-container')
            if outer==None:
                about=None
            else:
                about=outer.find('span',class_='visually-hidden').text
            volut_dic['voluterring_about']=about 
            volentring_dict['volentring_'+str(num)]=volut_dic
                                
    return volentring_dict

for i in key: 
    if i=="volunteering_experience":
        ind=key.index('volunteering_experience')
        volunteering=volutering(value[ind])
        if len(volunteering)==0:
            print(None)
        else:
            dic["volunteering_experience"]=volunteering
        break
    else:
        volunteering=None
        
print(volunteering)
        

#projects 
def project(i):
    all_projects=i.find('ul',class_='pvs-list')
    footer=i.find('div',class_='pvs-list__footer-wrapper')
    #print(footer)
    project_dict={}
    num=0
    if footer==None:
        li_tag=all_projects.find_all('li',class_= 'artdeco-list__item pvs-list__item--line-separated pvs-list__item--one-column')
        for li in li_tag:
            num=num+1
            proj_dict={}
            info=li.find('div',class_="display-flex flex-row justify-space-between")
            tittle=info.find('div',class_='display-flex full-width')
            projects_tittle=tittle.find('span',class_='visually-hidden').text
            proj_dict['Tittle']=projects_tittle 
            projects_date=info.find('span',class_='t-14 t-normal')
            if projects_date==None:
                proj_date=None
            else:
                proj_date=projects_date.find('span','visually-hidden').text
            proj_dict['date']=proj_date    
            outer=li.find("div",class_='pvs-list__outer-container')
            if outer==None:
                about=None
            else:
                outer_outer=outer.find('div',class_='pvs-list__outer-container')
                about=outer_outer.find('span',class_='visually-hidden').text
            proj_dict['about project']=about
            project_dict['project_'+str(num)]=proj_dict

    else:
        a_tag=footer.find('a')
        a_tag=a_tag['href']
        #print(a_tag)
        driver.get(a_tag)
        sleep(2)
        source_projects= driver.page_source
        #print(source_skill)
        soup_projects=BeautifulSoup(source_projects,'html.parser')
        ul_projects=soup_projects.find('ul',class_='pvs-list')
        li_tag=ul_projects.find_all('li',class_= 'pvs-list__paged-list-item artdeco-list__item pvs-list__item--line-separated pvs-list__item--one-column')
    
        for li in li_tag:
            num=num+1
            proj_dict={}
            info=li.find('div',class_="display-flex flex-row justify-space-between")
            tittle=info.find('div',class_='display-flex full-width')
            projects_tittle=tittle.find('span',class_='visually-hidden').text
            proj_dict['Tittle']=projects_tittle 
            projects_date=info.find('span',class_='t-14 t-normal')
            if projects_date==None:
                proj_date=None
            else:
                proj_date=projects_date.find('span','visually-hidden').text
            proj_dict['date']=proj_date    
            outer=li.find("div",class_='pvs-list__outer-container')
            if outer==None:
                about=None
            else:
                outer_outer=outer.find('div',class_='pvs-list__outer-container')
                about=outer_outer.find('span',class_='visually-hidden').text
            proj_dict['about project']=about
            project_dict['project_'+str(num)]=proj_dict
    return project_dict             
 
for i in key:   
    if i=="projects":
        ind=key.index('projects')
        projects=project(value[ind]) 
        print(projects)
        if len(projects)==0:
            print(None)
        else:
            dic["projects"]=projects
        break
    else:
        projects=None
        
print(projects)


#Honors And Award Section 
def Award(i):
    all_awards=i.find('ul',class_='pvs-list')
    footer=i.find('div',class_='pvs-list__footer-wrapper')
    #print(footer)
    langu_dict={}
    num=0
    if footer==None:
        li_tag=all_awards.find_all('li',class_= 'artdeco-list__item pvs-list__item--line-separated pvs-list__item--one-column')
        #print(li_tag)
        for li in li_tag:
            num=num+1
            lan_dict={}
            info=li.find('div',class_="display-flex align-items-center mr1 t-bold")
            awards=info.find('span',class_='visually-hidden')
            lan=awards.text
            lan_dict['award_name']=lan
            company=li.find('span',class_='t-14 t-normal')
            company_name=company.find('span',class_='visually-hidden').text
            lan_dict['issued_by']=company_name
            '''
            outer=li.find('div',class_='pvs-list__outer-container')
            if outer==None:
                pass
            else:
                outer_li=outer.find_all("li",class_='pvs-list__item--one-column')
            for j in outer:
                img=j.find('li',class_='pvs-list__item--with-top-padding pvs-list__item--one-column')
                
                if img==None:
                    des_text=None
                else:
                    des=img.find('div',class_='pv-shared-text-with-see-more full-width t-14 t-normal t-black display-flex align-items-center')
                    des_text=des.find('span',class_='visually-hidden').text
                    
                lan_dict['description']=des_text
                
'''
            langu_dict['award_'+str(num)]=lan_dict


    else:
        a_tag=footer.find('a')
        a_tag=a_tag['href']
        driver.get(a_tag)
        sleep(2)
        source_awards = driver.page_source
        soup_awards=BeautifulSoup(source_awards,'html.parser')
        ul_awards=soup_awards.find('ul',class_='pvs-list')
        li_awards=ul_awards.find_all('li',class_= 'pvs-list__paged-list-item artdeco-list__item pvs-list__item--line-separated pvs-list__item--one-column')

        for li in li_awards:
            num=num+1
            lan_dict={}
            info=li.find('div',class_="display-flex align-items-center mr1 t-bold")
            awards=info.find('span',class_='visually-hidden')
            lan=awards.text
            lan_dict['award_name']=lan
            company=li.find('span',class_='t-14 t-normal')
            comp=level.find('span',class_='visually-hidden').text
            lan_dict['issued_by']=comp
            
            '''
            outer=li.find('div',class_='pvs-list__outer-container')
            if outer==None:
                pass
            else:
                outer_li=outer.find_all("li",class_='pvs-list__item--one-column')
            for i in outer_li:
                img=i.find('img')
                if img==None:
                    des=i.find('div',class_='display-flex align-items-center t-14 t-normal t-black')
                    des_text=des.find('span',class_='visually-hidden').text
                    
                else:
                    des_text=None
                lan_dict['description']=des_text
                '''
            langu_dict['awards_'+str(num)]=lan_dict
            
            
    return langu_dict

for i in key:
    if i=="honors_and_awards":
        ind=key.index('honors_and_awards')
        award=Award(value[ind])
        if len(award)==0:
            print(None)
        else:
            dic["honors_and_awards"]= award
        break

    else:
        award= None 
        
print(award)

pprint.pprint(dic)


from pymongo import MongoClient

client = MongoClient()

db = client['Linkedin']

data = db['profile_data']

data.insert_one(dic)

