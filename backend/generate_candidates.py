
import json
import random
from faker import Faker
from datetime import datetime, timedelta

fake = Faker("en_IN")
random.seed(42)

SKILLS = ["Python","Java","C++","JavaScript","TypeScript","React","Node.js","FastAPI","Django","Flask","SQL","PostgreSQL","MongoDB","Docker","Kubernetes","AWS","Azure","GCP","Git","Linux","TensorFlow","PyTorch","Pandas","NumPy"]
COMPANIES=["Google","Microsoft","Amazon","Meta","Flipkart","Swiggy","Zomato","Infosys","TCS","Wipro","Adobe","Oracle","NVIDIA","Atlassian"]
LOCS=["Bangalore","Hyderabad","Pune","Delhi","Mumbai","Chennai","Noida"]
IND=["Technology","FinTech","E-commerce","AI"]
DEGREES=["B.Tech","M.Tech","B.E.","MCA"]

def rand_date(days):
    return (datetime.now()-timedelta(days=random.randint(0,days))).strftime("%Y-%m-%d")

N = 20000
with open("candidates.jsonl","w",encoding="utf-8") as f:
    for i in range(1,N+1):
        yoe=random.randint(0,15)
        comp=random.choice(COMPANIES)
        title=random.choice(["Software Engineer","Backend Engineer","ML Engineer","Frontend Engineer","Data Engineer"])
        data={
            "candidate_id":f"cand_{i:06d}",
            "anonymized_name":fake.name(),
            "profile":{
                "headline":title,
                "summary":fake.text(180),
                "location":random.choice(LOCS),
                "country":"India",
                "years_of_experience":yoe,
                "current_title":title,
                "current_company":comp,
                "current_company_size":random.choice(["1-50","51-200","201-1000","1000+"]),
                "current_industry":random.choice(IND)
            },
            "redrob_signals":{
                "open_to_work_flag":random.choice([True,False]),
                "willing_to_relocate":random.choice([True,False]),
                "preferred_work_mode":random.choice(["remote","hybrid","onsite","flexible"]),
                "notice_period_days":random.choice([0,15,30,60,90]),
                "expected_salary_min_lpa":random.randint(5,35),
                "expected_salary_max_lpa":random.randint(36,60),
                "github_activity_score":random.randint(0,100),
                "profile_completeness_score":round(random.uniform(0.6,1.0),2),
                "linkedin_connected":True,
                "verified_email":True,
                "verified_phone":random.choice([True,False]),
                "last_active_date":rand_date(120),
                "signup_date":rand_date(1200)
            },
            "skills":[
                {
                    "name":s,
                    "proficiency":random.choice(["beginner","intermediate","advanced","expert"]),
                    "endorsements":random.randint(0,150),
                    "duration_months":random.randint(6,120)
                } for s in random.sample(SKILLS, random.randint(4,8))
            ],
            "education":[{
                "institution":random.choice(["MIT Manipal","IIT Delhi","IIT Bombay","NIT Trichy","BITS Pilani","VIT"]),
                "degree":random.choice(DEGREES),
                "field_of_study":"Computer Science",
                "start_year":2014+random.randint(0,8),
                "end_year":2018+random.randint(0,8),
                "grade":str(round(random.uniform(7.0,9.9),2)),
                "tier":random.choice(["tier1","tier2"])
            }],
            "career_history":[{
                "company":comp,
                "title":title,
                "start_date":"2022-01-01",
                "end_date":None,
                "duration_months":yoe*12,
                "is_current":True,
                "industry":"Technology",
                "company_size":"1000+",
                "description":fake.text(120)
            }]
        }
        f.write(json.dumps(data, ensure_ascii=False)+"\n")
print(f"Generated {N} candidates -> candidates.jsonl")

