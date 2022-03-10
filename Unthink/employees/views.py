from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest
from .models import Employee
import datetime
import json

# Create your views here.
def mapDict(results):
    """
    input : results 
    output : type <dict>
    functionality : Called via a map function which will fetch the empcode,dept and score and store in form of dict
    """
    return {'employee_code':results.empcode,'department': results.dept,'score': results.score}

def getAllData():
    """
    input :  
    output : type <list>
    functionality : Fetch data from DB in following sceanrio 
                   - Entries with DEPT = Unthink
                   - Entries within last 14 days and DEPT != Unthink
                   - Entries beyond last 14 days and DEPT != Unthink
    """    
    getUnthink = Employee.objects.filter(dept__contains = 'Unthink')
    #getUnthinkList = [{'employee_code':i.empcode,'department': i.dept,'score': i.score} for i in getUnthink]
    getUnthinkList = list(map(mapDict, getUnthink))
    #Calculating date 2weeks back from current date 
    today = datetime.datetime.now()
    backDate = datetime.timedelta(days = 14) 
    backD = today - backDate
    withInbackD = Employee.objects.exclude(dept__contains = 'Unthink').filter(createdate__gte = backD)
    #getwithInList = [{'employee_code':i.empcode,'department': i.dept,'score': i.score} for i in withInbackD]
    getwithInList = list(map(mapDict, withInbackD))

    getScoreSorted = Employee.objects.exclude(dept__contains = 'Unthink').filter(createdate__lt = backD).order_by('-score')
    #getScoreSortedList = [{'employee_code':i.empcode,'department': i.dept,'score': i.score} for i in getScoreSorted]
    getScoreSortedList = list(map(mapDict, getScoreSorted))
    #Inserting Data in to the final list
    stUnthink = 4
    for unthink in range(0,len(getUnthinkList),2):
        try:
            getScoreSortedList.insert(stUnthink, getUnthinkList[unthink])
            getScoreSortedList.insert(stUnthink+1, getUnthinkList[unthink+1])
            stUnthink = stUnthink + 6
        except IndexError:
            return HttpResponseBadRequest("Oops!! Seems Like Unthink is not in order 2 range")
    stwithInList = 6
    for inrange in range(0,len(getwithInList),2):
        try:
            getScoreSortedList.insert(stwithInList, getwithInList[inrange])
            getScoreSortedList.insert(stwithInList+1, getwithInList[inrange+1])
            stwithInList = stwithInList + 8
        except IndexError:
            return HttpResponseBadRequest("Oops!! Seems Like Last 14 days is not in order of 2 range")
            
    return getScoreSortedList

def employ(request):
    """
    input : request
    output : HttpResponse, HttpResponseBadRequest
    Functionality : If chunk is provided in the URL 
                    then process the output accordingly, 
                    if all the data is required the response is provided in that fashion
    """
    urlRequest = request.GET
    getSortedList = {'employees':[]}
    getSortedList['employees'] = getAllData()
    try:
        chunk = int(urlRequest['chunk'])
        final_result = getSortedList['employees'][(chunk*20)-20:(chunk*20)-1]
        if not final_result:
            return HttpResponseBadRequest("Oops!!! Chunk is too large.")
        return HttpResponse(json.dumps({'employees' : final_result}))
    except:
        return HttpResponse(json.dumps(getSortedList))
