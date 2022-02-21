
# Exam Portal
Secure  Exam Platform a Great Alternative for Google Forms  made by *Django Web Framework* and channel

LINK : https://myonlinengineering.pythonanywhere.com
 ***
## Features 
- Separate Login,Register For **Student Teacher HODs**
- They Have their Own DashBoard To monitor their statistics
- Permission are Given So Everything is verified 

###  Student 
 - They can See Which Test Teacher has Added and they can enroll in course (with Permission of teachers)
 - They can given the test by **turning On Camera** and the question will be shuffle with **timer added**
 - they can bookmark and **list the question** and **click the option to save** and **report the question** if any 
 - They Can Also See The Answers (*if teacher set **show result** to True*)
 - Get Spam Message on **Student Dashboard** if Teacher Report them as a suspect so they have to **give test again**

###  Teacher  
 - After Registering as a Teacher HOD Will verify and then they can **Access their Dashboard** 
 - They Create Edit Delete Update **Test** and **add Question** and some actions with test
 - They can see Student Result and **Pictures to student** During Exams and can *report them as a spam*
 - they can verify Student of their class and edit their profile can unverified  also

 ### HOD(Head Of Department)
 - He/She can Verify Teacher and Create Subject And See All Test and Teacher Profile
  - He can verify and unverified Teachers and See Reported Students
 

***
## What Technology Used

### FrontEnd
 - HTML5
 - CSS
 - JavaScript
 - Bootstrap snippets
 - Jquery 

###  Backend

 - Django Python Web Framework
 - MySQL for Database
 - Sendgrid Email API for sending Emails
***

## Getting started
###   Requirements
 - Python 3.6+
 - pip
 - virtualenv 

###  Installation
```bash
# Clone the repository
git clone https://github.com/Abhishek-Gawade-programmer/exam-portal

# Enter into the directory
cd exam-portal/

# Create virtual environment 
virtualenv env

# Activate virtual environment 
source env/bin/activate

# Install the dependencies
pip install -r requirements.txt

# Check migrations.
python manage.py makemigrations

# Apply migrations.
python manage.py migrate

#Starting the application
python manage.py runserver

```
###  Configuration
Create `.env` file in cwd and add the following
```conf
#Email Settings
EMAIL_BACKEND=''
EMAIL_HOST_USER=''
EMAIL_HOST_PASSWORD=''

```
