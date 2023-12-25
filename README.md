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
POST     /api/v1/auth/signin
##### Authorization
Bearer Token

##### Body raw (json)
    {
        "email": "admin3@testing.com",
        "password": "Password1"
    }

#### Signup
auth.signup             POST     /api/v1/auth/signup

#### Reset Password
auth.reset_password     PUT      /api/v1/auth/reset-password/<id>

#### Candidate Login
auth.user_login         POST     /api/v1/auth/user-login

### Admin

#### Update Admin
admin.update_admin      PUT      /api/v1/admins/

#### Get all Admins
admin.view_all_admins   GET      /api/v1/admins/

#### Get all Exams by Admin
admin.get_all_my_exams  GET      /api/v1/admins/myexams

#### Get a single Admin details
admin.get_one_admin     GET      /api/v1/admins/<admin_id>

#### Delete an Admin
admin.delete_admin      DELETE   /api/v1/admins/<admin_id>


### Examination Routes
exam.exam_condition     POST     /api/v1/admins/exams/
exam.get_all_exam       GET      /api/v1/admins/exams/
exam.get_exam           GET      /api/v1/admins/exams/<exam_id>
exam.update_exam        PUT      /api/v1/admins/exams/<exam_id>

