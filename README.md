# Course-Recommender

Qualichain H2020 Course Recommendation Module

### Docker Installation

In order to install Course recommender use Docker and docker-compose.

`docker-compose up -d --build`

You can access Course Recommender from port `5000`

### Local Installation
1. Install Requirements: `pip install -r requirements.txt`
2. go to /app/views/ folder using this command: `cd /app/views`
3. and then  execute this command: `python -m flask run`

### Join Courses and Skills tables

Initially before running Course Recommendation module you should execute the following command
in orded to have a merged table that contains Courses and Skills.

`docker exec python join_tables_skill_courses.py`

### Recommendation API example usage

**Recommendations combining ElasticSearch and clustering Functionalities**
```http request
POST /recommend HTTP/1.1
Host: localhost:5000
Content-Type: application/json

{"source":{
   "PersonURI":"http://somewhere/JohnSmith",
   "Label":"CV1",
   "targetSector":"IT",
   "expectedSalary":"40K",
   "Description":"It is a test CV",
   "skills":[
      {
         "label":"Java",
         "proficiencyLevel":"basic",
         "SkillComment":"java programming language"
},
      {
         "label":"SQL",
         "proficiencyLevel":"basic",
         "SkillComment":"sql"
      	
      },
           {
         "label":"Python",
         "proficiencyLevel":"basic",
         "SkillComment":"python"
      	
      }
      
],
   "workHistory":[
      {
         "position":"developer",
         "from":"2019-01-01",
         "to":"2020-01-01",
         "employer":"QualiChain"
}


],
   "Education":[
      {
         "title":"informatic engineering",
         "from":"2015-09-01",
         "to":"2019-01-01",
         "organisation":"a",
         "description":"a"


}


]
},
"source_type": "cv",
"recommendation_type": "courses"}

```

**Recommendations using ElasticSearch Functionalities**
```http request
POST /recommend_elk HTTP/1.1
Host: localhost:5000
Content-Type: application/json

{"source":{
   "PersonURI":"http://somewhere/JohnSmith",
   "Label":"CV1",
   "targetSector":"IT",
   "expectedSalary":"40K",
   "Description":"It is a test CV",
   "skills":[
      {
         "label":"Java",
         "proficiencyLevel":"basic",
         "SkillComment":"java programming language"
},
      {
         "label":"SQL",
         "proficiencyLevel":"basic",
         "SkillComment":"sql"
      	
      },
           {
         "label":"Python",
         "proficiencyLevel":"basic",
         "SkillComment":"python"
      	
      }
      
],
   "workHistory":[
      {
         "position":"developer",
         "from":"2019-01-01",
         "to":"2020-01-01",
         "employer":"QualiChain"
}


],
   "Education":[
      {
         "title":"informatic engineering",
         "from":"2015-09-01",
         "to":"2019-01-01",
         "organisation":"a",
         "description":"a"


}


]
},
"source_type": "cv",
"recommendation_type": "courses"}

```

**Recommendations using Clustering**

```http request
POST /get_recommended_skills HTTP/1.1
Host: 127.0.0.1:5000
Content-Type: application/json

{
	"Skills":
	[{"SkillLabel":"Java"}, {"SkillLabel":"SQL"}]	
}
```

```http request
POST /get_recommended_courses HTTP/1.1
Host: 127.0.0.1:5000
Content-Type: application/json

{
	"Skills":
	[{"SkillLabel":"Java"}, {"SkillLabel":"SQL"}]	
}
```