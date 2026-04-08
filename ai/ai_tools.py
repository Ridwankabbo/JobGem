from langchain_core.tools import tool
from user.models import UserProfile, SocialLinks, Resumes, Company, WorkedCompanies, Certificates, ExtreFields
from jobpost.models import JobPost, Applications
import json
from django.db.models import Q


@tool
def search_jobs(querry:str):
    """ 
    Search for job postes in database.
    Search for products using fuzzy matching. Handles typos (e.g., 'frout' -> 'fruit') and plurals (e.g., 'jobs' -> 'job') and (synonyms like mobile and phoner are basically same).
    Use this when the user asks to see job post, find posts, or searches for a specific posts.
    Input should be a search string like '"python/Django/java/Spring boot /php/ Laravel/ wordpress/ shopify" developer'.
    Ignore all capital and small letter mismatch. 
    """
    
    words = querry.split()
    
    jobs_post_filter = Q()
    
    for word in words:
        if len(word)<2 : continue
        jobs_post_filter &= (
            Q(title__icontains=word) | 
            Q(description__icontains=word) |
            Q(requirements__icontains=word)
        )
        
    jobs = JobPost.objects.filter(jobs_post_filter).difference()
    
    results = []
    for job in jobs:
        results.append({
            "id":job.id,
            "title":job.title,
            "requirements":job.requirements,
            "experience": job.experience,
            "location":job.location,
            "status": job.status,
            "dedline" : job.dedline
            
        })
    
    return json.dumps(results)


@tool
def applay_job(user_id:int, job_id:int):
    
    ''' 
        Use this when a user explicitly says they want to buy or order an item.
        Requires the job_id (int) and the user_id (int).
    '''
    
    try:
        job = JobPost.objects.get(id=job_id)
        
        Applications.objects.create(
            seeker = user_id,
            job = job
        )
        return f"Job applied successfully"
    except JobPost.DoesNotExist:
        return "This post Doesn't exist"
    except Exception as e:
        return f"error: {str(e)}"
    
    
    
    