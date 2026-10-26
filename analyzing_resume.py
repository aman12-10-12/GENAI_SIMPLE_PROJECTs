import pymupdf
import os
from dotenv import load_dotenv
from groq import Groq
from pydantic import BaseModel, ValidationError, Field
import json
from typing import Literal


load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")

if not groq_api_key:
    raise ValueError("GROQ_API_KEY is missing")

client = Groq(api_key=groq_api_key)

model = "openai/gpt-oss-120b"

# opening the document and getting the text into resume_text
doc = None
resume_text = ""
try:
    doc = pymupdf.open("Aman_Raj.pdf")

    for page in doc:
        resume_text += page.get_text() + "\n"

except FileNotFoundError:
    print("Error: PDF file not found!")

except pymupdf.EmptyFileError:
    print("Error: PDF file is empty!")

except pymupdf.FileDataError:
    print("Error: Invalid or corrupted PDF file!")

except Exception as e:
    print(f"Unexpected error: {e}")

finally:
    if doc is not None:
        doc.close()


# job description for testing

job_description = """
Job Title: Full Stack Developer (MERN Stack)
Location: Bengaluru, Karnataka, India
Job Type: Full-Time
Experience Required: 0-2 Years
Education: B.E./B.Tech in Computer Science, IT, or related field

Job Summary:
We are looking for a skilled Full Stack Developer with hands-on experience
in building scalable web applications using React.js, Node.js, Express.js,
and MongoDB.

The ideal candidate should have strong knowledge of frontend development,
backend API development, database management, authentication, cloud
deployment, and software engineering principles.

Key Responsibilities:
1. Develop responsive web applications using React.js, JavaScript,
   HTML5, CSS3, and Vite.

2. Build scalable backend services using Node.js and Express.js.

3. Design, develop, and integrate RESTful APIs.

4. Implement authentication and authorization using JWT, cookies,
   Bcrypt, and role-based access control.

5. Design MongoDB and MySQL database schemas and optimize queries.

6. Implement real-time communication using WebSockets and Socket.IO.

7. Deploy applications using AWS EC2, ECS, Docker, and Nginx.

8. Implement CI/CD pipelines using GitHub Actions.

9. Write unit and integration tests using Jest.

10. Participate in code reviews, debugging, and Agile development.

Required Technical Skills:
- JavaScript (ES6+)
- React.js
- React Hooks
- Context API
- HTML5
- CSS3
- Node.js
- Express.js
- RESTful APIs
- MongoDB
- Mongoose
- MySQL
- SQL
- JWT Authentication
- Bcrypt
- Git
- GitHub
- Postman
- Database Schema Design
- CRUD Operations
- Data Structures and Algorithms
- Object-Oriented Programming
- DBMS
- Operating Systems
- Computer Networks

Preferred Skills:
- AWS EC2, ECS, ECR, IAM, ALB
- Docker
- Nginx
- Linux
- GitHub Actions
- CI/CD
- Socket.IO
- WebSockets
- Microservices
- PostgreSQL
- Jest
- Unit Testing
- Integration Testing
- TypeScript
- Redis
- Cloudflare
- AWS SES
- Python
- Gemini API
- AI/ML API Integration

Qualifications:
- Bachelor's degree in Computer Science, Software Engineering,
  Information Technology, or related field.
- 0-2 years of experience in full-stack development.
- Fresh graduates with strong projects are encouraged to apply.
- Strong understanding of software development principles.
- Experience building and deploying full-stack applications.

Preferred Project Experience:
- Developed full-stack applications using MERN stack.
- Implemented secure JWT authentication.
- Built REST APIs using Node.js and Express.js.
- Worked with MongoDB and MySQL databases.
- Deployed applications on AWS.
- Used Docker for containerization.
- Implemented real-time chat using Socket.IO.
- Optimized database queries and indexing.
- Integrated third-party APIs.
- Implemented automated testing.

Soft Skills:
- Problem Solving
- Analytical Thinking
- Communication
- Team Collaboration
- Leadership
- Adaptability
- Attention to Detail
- Debugging
- Time Management

ATS Keywords:
Full Stack Developer, MERN Stack, Software Engineer,
JavaScript, React.js, Node.js, Express.js, MongoDB,
MySQL, SQL, REST API, JWT, Authentication, Authorization,
Mongoose, CRUD, Database Indexing, Query Optimization,
Socket.IO, WebSockets, AWS, EC2, ECS, Docker, Nginx,
CI/CD, GitHub Actions, Git, GitHub, Jest, Unit Testing,
Integration Testing, Agile, Scrum, Data Structures,
Algorithms, OOP, DBMS, Microservices, Cloud Deployment.
"""

class Eligibility(BaseModel):
    candidate_name: str

    matched_skills: list[str] = Field(
        description="Skills present in both the resume and job description"
    )

    unmatched_skills: list[str] = Field(
        description="Skills required by the job description but missing from the resume"
    )

    matching_score: int = Field(
        ge=0,
        le=100,
        description="Resume matching score between 0 and 100"
    )

    eligibility_status: Literal["Highly Eligible", "Moderately Eligible", "Not Eligible"]

    feedback: str = Field(
        description="Brief explanation of the candidate's suitability for the job"
    )

schema = Eligibility.model_json_schema()

response_format = {
    "type": "json_object"
}

import json

schema = Eligibility.model_json_schema()

import json

schema = Eligibility.model_json_schema()

system_prompt = f"""
You are an expert ATS resume evaluator specializing in
software engineering recruitment.

Your task is to compare a candidate's resume against a
job description and return an accurate eligibility report.

INSTRUCTIONS:

1. Extract the candidate's full name from the resume.
   If unavailable, use "Unknown".

2. Identify all required and preferred technical skills
   from the job description.

3. Compare each skill against the entire resume,
   including technical skills, projects, and experience.

4. MATCHED SKILLS:
   - Include skills explicitly mentioned in the resume.
   - Include skills clearly demonstrated through projects.
   - Recognize equivalent terminology.
   - Avoid duplicate skills.

5. UNMATCHED SKILLS:
   - Include required or preferred skills not demonstrated
     in the resume.
   - Do not invent missing skills.
   - Do not assume knowledge of related technologies.
   - Do not omit missing preferred skills.

6. MATCHING SCORE:

   Required Match Percentage =
   (Matched Required Skills / Total Required Skills) * 100

   Preferred Match Percentage =
   (Matched Preferred Skills / Total Preferred Skills) * 100

   Final Score =
   (Required Match Percentage * 0.70) +
   (Preferred Match Percentage * 0.30)

   If only one category has skills, use that category
   with 100% weight. If neither has skills, score 0.

   Round the final score to an integer between 0 and 100.

7. ELIGIBILITY STATUS:
   - 80-100: Highly Eligible
   - 50-79: Moderately Eligible
   - 0-49: Not Eligible

8. FEEDBACK:
   - Summarize the candidate's strengths.
   - Identify important missing skills.
   - Mention relevant project experience.
   - Keep feedback under 100 words.

IMPORTANT RULES:
- Evaluate every required and preferred skill.
- Each skill must appear in exactly one matching category.
- Do not count duplicate skills.
- Do not invent candidate experience.
- Return only valid JSON.
- Follow the provided schema exactly.
- Do not include Markdown or additional explanations.

JSON SCHEMA:
{json.dumps(schema)}
"""

user_prompt = f"""
Evaluate the following candidate resume against the provided
job description.

CANDIDATE RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description}

Perform a complete skill-by-skill evaluation.

Return the final eligibility report strictly in the
specified JSON format.
"""

system_message = {
    "role" : "system",
    "content" : system_prompt
}

user_message = {
    "role" : "user",
    "content" : user_prompt
}

messages = [system_message, user_message]

response = client.chat.completions.create(
    model=model,
    messages=messages,
    response_format=response_format,
    temperature=0,
    max_completion_tokens=4096
)

main_answer = response.choices[0].message.content

# Validate using Pydantic
try:
    result = Eligibility.model_validate_json(main_answer)

    print(
        json.dumps(
            result.model_dump(),
            indent=4,
            ensure_ascii=False
        )
    )

except ValidationError as e:
    print("Validation Error:", e)
