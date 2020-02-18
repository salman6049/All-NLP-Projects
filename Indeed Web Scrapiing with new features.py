# -*- coding: utf-8 -*-
"""
Created on Thu May 24 10:45:09 2018

@author: Salman Sigari - Indeed Web Scrapiing with new features as Employee status(Current, Former),..
"""
from bs4 import BeautifulSoup
from time import sleep
import requests 
#from requests import grt
from random import randint
from IPython.core.display import clear_output
from warnings import warn
from requests import *
from time import *


# Declaring the lists to store data in
rating = []
Reviewer_Position = []
Location = []
Date = []
Comment = []
pros = []
cons = []

## Extracted all job categories by NLP methods
Job_Categories = "Deputy,Director,Supervisor,ADMINISTRATOR,ADVISOR,ADVOCATE,Agent,ANALYST,ASSOCIATE,Accountant,Administrator,Analista,Leader,Investigator,Physician,Processer,Procurement,Programmer,REPRESENTATIVE,Reclutador,Recruiter,SPECIALIST,TECHNICIAN,Teamleider,Tester,Trainer,Técnico,Vendor,assistant,clasificador,medewerkster,expert,medewerker,operator,temsilcisi,trainee,workers,TRainer,TeamLead,President,Scrum,Sorter,Manager,Auditor,Auxiliary,Banker,COACH,Coordinator,LEADER,reclutador,Reviewer"
Job_Categories = Job_Categories.lower().split(',')


#Preparing the Monitoring of the loop as it's still going
start_time = time()
requests = 0

# Get the Container
#

# For every page in the interval 0-400

pages = [str(i) for i in list(range(0,5,20))]

for page in pages:
    response = get('https://www.indeed.com/cmp/Conduent/reviews?fcountry=ALL&start=' + page)# make a get request
    #sleep(randint(0,1))# pause the loop
    
#Monitoring the request
    requests += 1
    elapsed_time = time() - start_time
    print('Request:{}; Frequency: {} requests/s'.format(requests, requests/elapsed_time))
    clear_output(wait = True)
## Throw a warning for non-200 status codes   
    if response.status_code !=200:
        warn('Request: {}; Status code: {}'.format(requests, response.status_code))

## Break the loop if the number of requests is greater than expected   
#    if requests >400:
#        warn('Number of request greater than expected.')
#        break

    
# parse the contents 
    page_html = BeautifulSoup(response.text, 'html.parser')
# Select all the Reviewers
    
    big_box = page_html.find_all('div', attrs = {'class' : 'cmp-review-container'})

# for every reviewr 
    for reviewer in big_box:
        # if the review was not empty
        #if review.find('span', class_={'class' : 'cmp-review-text'}) is not None:
            
            # Get Rating
            rating_ = reviewer.div.find('span', attrs = {'class' : 'cmp-Rating-on'})
            rating.append(rating_)
            Rating = []
            for r in rating:
                text = str(r)
                x= text.partition(':')[-1].rpartition(';')[0]
                Rating.append(x)            
            
#            
            # get position
            reviewer_position = reviewer.find('span', attrs = {'class' : 'cmp-reviewer-job-title'}).text
            Reviewer_Position.append(reviewer_position)
            Employee_Status = []
            Job_Category = []
            for i in Reviewer_Position:
                text = str(i)
                a = text.partition('(')[-1].rpartition(')')[0]
                Employee_Status.append(a)
            

#            for i in Reviewer_Position:
#                text = str(i)
#                #b = text.lower()
#                for j in Job_Categories:
#                    if j in text:
#                        Job_Category.append(j)
            for i in Job_Categories:
                for j in Reviewer_Position:
                    if i in j:
                        Job_Category.append(i)
                    else: Job_Category.append('Others')
                            

                        
                
                    
            # Get location 
            location = reviewer.find('span', attrs = {'class' : 'cmp-reviewer-job-location'}).text
            Location.append(location)
            City = []           
            State = []
            for i in Location:
                text = str(i)
                b = text.split(',',1)[0]
                c = text.split(',',1)[1:]
                City.append(b)
                State.append(''.join(c))
                
        
            
            #Get Date
            date = reviewer.find('span', attrs = {'class' : 'cmp-review-date-created'}).text
            Date.append(date)
            # Get Comment
            comment = reviewer.find('span', attrs = {'class' : 'cmp-review-text'}).text
            Comment.append(comment)
            #Get Pros
            pros_ = reviewer.find('div', {'class' : 'cmp-review-pro-text'})#.replace('<div class="cmp-review-con-text">','','</div>','' )
            pros.append(pros_)
            Pros = []
            for i in pros:
                text = str(i)
                x= text.partition('>')[-1].rpartition('<')[0]
                Pros.append(x)
                
            
            #get Cons
            cons_ = reviewer.find('div', {'class' : 'cmp-review-con-text'})
            cons.append(cons_)
            Cons = []
            for j in cons:
                text = str(j)
                y= text.partition('>')[-1].rpartition('<')[0]
                Cons.append(y)



#Indeed_review['cons'] = Indeed_review['Cons']  

# define a dictionary and store all list throught a structured form
Indeed_review = pd.DataFrame({'Rating' : Rating,
                              'Reviewer_Position' : Reviewer_Position,
                              'Location' : Location,
                              'Date' : Date,
                              'Comment' : Comment,
                              'pros' : Pros,
                              'cons' : Cons,
                              'Employee_Status' : Employee_Status,
                              'City' : City,
                              'State' : State,
                              'Job_category' : Job_Category})
    
cleanedIndeed_review = Indeed_review[15:][Indeed_review[15:].Comment.str.contains('Conduent Inc is still a company in its infancy')== False]   # Get rid of Duplications   

All_Indeed_Review = Indeed_review[:15].append(cleanedIndeed_review) # append the cleaned data frame to the 1st part
All_Indeed_Review = All_Indeed_Review.reset_index(drop = True) # fix the indexes for all rows
#Indeed_review = Indeed_review.reset_index(drop = True)
 #Indeed_review
#
#
#
#Pros =[]
#Cons = []
#
#for i in Indeed_review['pros']:
#    text = str(i)
#    x= text.partition('>')[-1].rpartition('<')[0]
#    Pros.append(x) 
##Indeed_review['pros'] = Indeed_review['Pros']   
#
#for j in Indeed_review['cons']:
#    text = str(j)
#    y= text.partition('>')[-1].rpartition('<')[0]
#    Cons.append(y)  

All_Indeed_Review.to_csv('C:/Test_1.csv') 

