# ANYEXAM
Anyexam is an educational solution to improve the education system by making computer-based tests easy and friendly either for organization recruitment or school assessments.




## For Developer
To start the app 
$ flask --app api run


To generate an initial migration:

$ flask --app api db migrate
The migration script needs to be reviewed and edited, as Alembic currently does not detect every change you make to your models. In particular, Alembic is currently unable to detect indexes. Once finalized, the migration script also needs to be added to version control.

Then you can apply the migration to the database:

$ flask --app api db upgrade
Then each time the database models change repeat the `migrate` and `upgrade` commands.

To sync the database in another system just refresh the migrations folder from source control and run the `upgrade `command.

## Documentation
This is the API documentaion of anyexam backend server. The base url is `http://localhost:5000/api/v1`

### Home Route
home                    GET      / or /api or /api/v1


### Authentication 
Authentication routes handle the authentication process of the api. Each user is expected to create an account using the signup endpoint and also be authorized using signin endpoint in order to access some of the premium features of the API.

#### Signin
* auth.signin POST     /api/v1/auth/signin
    ##### Authorization - Bearer Token

##### Body raw (json)
    {
        "email": "admin3@testing.com",
        "password": "Password1"
    }

#### Signup
* auth.signup             POST     /api/v1/auth/signup

##### Body raw (json)
    {
        "firstname": "John",
        "lastname": "Doe",
        "email": "admin3@testing.com",
        "organization": "abcgroup",
        "position": "staff",
        "password": "Password1",
        "answer": "Correct"
    }

#### Reset Password
* auth.reset_password     PUT      /api/v1/auth/reset-password/<id>

##### Body raw (json)
    {
        "new_password": "NewPassword1",
        "answer": "Correct"
    }

#### Candidate Login
* auth.user_login         POST     /api/v1/auth/user-login
##### Body raw (json)
    {
        "email": "candidate1@testing.com
        "token": "c9577bcf"
        "firstname": "Jane"
        "lastname" = "Doe"
    }

### Admin
These routes handle retrieval, modification and deletion of the admin api. Information about an admin can be accessed using these routes. However, there are some routes that requires user authentication to have full access to its features

#### Update Admin
* admin.update_admin      PUT      /api/v1/admins/
    ##### Authorization - Bearer Token
##### Body raw (json)
    {
        "firstname": "Jonathan"
    }

#### Get all Admins
* admin.view_all_admins   GET      /api/v1/admins/

#### Get all Exams by Admin
* admin.get_all_my_exams  GET      /api/v1/admins/myexams
    ##### Authorization - Bearer Token

#### Get a single Admin details
* admin.get_one_admin     GET      /api/v1/admins/<admin_id>

#### Delete an Admin
* admin.delete_admin      DELETE   /api/v1/admins/<admin_id>


### Examination Routes
The examination routes handles all exam related endpoints. It grants the user(admin) the priviledge to set examination guidelines.

* exam.exam_condition     POST     /api/v1/admins/exams/
    ##### Authorization - Bearer Token
##### Body raw (json)
    {
        "title": "Chemical Analysis",
        "exam_type": "first semester",
        "duration": 25,
        "result": "visible",
        "no_of_questions": 30
    }
* exam.get_all_exam       GET      /api/v1/admins/exams/

* exam.get_exam           GET      /api/v1/admins/exams/<exam_id>

* exam.update_exam        PUT      /api/v1/admins/exams/<exam_id>
    ##### Authorization - Bearer Token
##### Body raw (json)
    {
        "title": "Introduction to Python Programming",
    }

* exam.generate_exam_token GET    /api/v1/admins/exams/generate_token/<exam_id>
    ##### Authorization - Bearer Token


### Quiz Routes
This routes handles the question bank where all questions are stored. Of course, It requires authentication to access. Here questions can be uploaded only as a .csv file.

* quiz.delete_question_bank  DELETE   /api/v1/quiz/questionbank/<exam_id>/         

* quiz.load_question_bank    GET      /api/v1/quiz/questionbank/<exam_id>          

* quiz.start_exam            POST     /api/v1/quiz/start                           

* quiz.upload_question       POST     /api/v1/quiz/upload/<exam_id>


### Result Routes
The result routes handles the examination scores of candidate that took the exam.
* exam.get_results          GET      /api/v1/admins/exams/results 

* exam.get_result           GET      /api/v1/admins/exams/results/<result_id> 

* exam.get_result_by_exam   GET      /api/v1/admins/exams/<exam_id>/results 
