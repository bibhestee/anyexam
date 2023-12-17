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