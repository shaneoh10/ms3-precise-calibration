# Website for Precise Calibration

![Precise Calibration](assets/mockups/precise-calibration-mockup.png)

## Code Institute Milestone Project 3 : Data Centric Development

Precise Calibration is a fictional company that provides calibration services for process instrumentation equipment. Some examples of this equipment would be pressure or temperature sensors in a pharmaceutical plant or oil refinery that require regular routine calibration for reasons of regulatory compliance. The website will feature a landing page with information about the company and its services with the goal of acquiring new customers. It will also contain a secure application for employees where they will be able to log in and keep track of work that is due for completionto ensure jobs are completed on time. This application will allow employees to make use of a database and CRUD operations to keep the calibration management system up to date.

A link to the live website can be found [here.](https://precise-calibration-ms3.herokuapp.com/)

## Table of Contents

- [User Experience (UX)](#ux)
- [Database Schema](#database-schema)
- [Features](#features)

## UX

### Strategy

The website for precise calibration will be designed with two sets of users in mind. First there are the potential customers of the services that precise calibration have to offer. These potential customers will be interested in viewing what services can be provided and how it may benefit them from a business perspective. Potential customers may be owners of a small business or they may be managers or supervisors in a larger business that requires regular routine instrument calibration services. The landing page be easy to navigate and will have a professional feel to it with all information clearly presented so as not to cause any confusion to potential customers.

The other set of users are the employees of precise calibration. Each employee will register their own personal login credentials to gain access to the calibration management application on the website. The purpose of this application is to reduce time filling out paperwork and sending emails as all information will be automatically updated to the database where a supervisor will be able to view the completed work and close out tasks. This application will contain a list of all instruments that are due for calibration and some information regarding the instrument (due date, tag id, location, instrument type). When an instrument has been calibrated employees will be able to mark the job as complete and if it has passed or failed and this information is then updated on the database. All information regarding instruments (due-date, location, tag-id etc.) needs to be clearly displayed and all buttons for CRUD functionality will need to be clearly labelled. At no point when using the application should employees feel confused or lost as this could lead to user input errors which would affect the efficiency of the application. 

The website will be designed for both mobile and desktop but will be targeted more towards desktop / laptop users as they are the norm in a professional setting and it is much easier to read and input information on a larger screen.

#### As a potential customer I want to:
- view the website on various devices (mobile, tablet, desktop)
- be able to instinctively navigate the website to efficiently find the information required
- be able to contact Precise Calibration with any queries about the services they are offering
- be easily directed to any social media channels to connect / network with Precise Calibration 

#### As an employee I want to:
- easily register an account
- be able to log in and log out without difficulty
- be able to search for specific instruments
- update the status of an instrument when calibration is complete (Pass / Fail)
- add new instruments to the calibration list as required
- remove instruments from the application when calibration is complete and closed out

### Scope

After analysing the user stories, I have decided to use the following features as my initial minimum scope.
- Responsive design
- Landing page with company information (services, contact info, social media)
- Employee account registration
- Log In / Log Out functionality for registered employees
- Calibrations Due section listing all instruments currently due for calibration with search functionality
- Calibrations Complete section visible by users with supervisor level access where they can review completed tasks
- CRUD functionality throughout the app 

### Structure

I did some research on websites belonging to companies that provide similar engineering and calibration services and I found that some websites did not look very appealing and looked a bit out dated. There were a few others with a more modern design which I found much more professional and eye-catching so I chose to go with a similar design for my landing page.

I also did some research on instrument calibration tracking software to get an idea of what employees may be used to working with. I found that with a lot of these applications that although the information fields used are common to my own application, the user interface was very basic and outdated. I decided to go with a more modern looking design that still keeps the same functionality as these other applications but with a cleaner and more legible presentation so as to avoid employees getting lost or confused.

Both the landing page and the employee application are designed to be easy to navigate, with all information presented in a clean manner so that users will have a familiar and enjoyable experience.

I have structured the website with:
- A brand logo on the top left of the page and a navbar to the right whic is common to most websites
- A collapsible navbar with a hamburger icon for smaller screen sizes
- Navbar common to all pages - items displayed on navbar depending on access level (supervisor access)
- Main content written with MaterializeCSS for structure and responsive design
- Landing Page, Register and Log In pages accessible by all users of the website
- Calibrations Due and Calibrations Sign Off pages accessible by all logged in employees
- Add, Edit and Completed Calibrations pages accessible by employees with supervisor access

### Skeleton 

I designed wireframes for desktop, tablet and mobile using Balsamiq. These wireframes can be viewed [here.](https://github.com/shaneoh10/precise-calibration-ms3/tree/master/assets/wireframes)

### Surface

#### Colours
I decided to go with a neutral color palette for the website to keep it looking professional and so as not to distract the users while they are reading through or inputting information. I used brighter green and red colours for the Pass/Fail indicators on the dashboard page so that they will stand out to the users. The main buttons are blue for positive interactions (Log in, upload etc.) and red for negative interactions (cancel, delete etc.). This makes it easier for users to distinguish between which type of action they are trying to take while using the application and it also provides a good contrast from the neutral colour palette of the rest of the website.
- #F8F9FA - Cultured (off-white) 
- #E9ECEF - Cultured (off-white)
- #ADB5BD - Wild Blue Yonder
- #495057 - Davys Grey
- #343A40 - Gunmental

#### Typography
I chose 'Fira Sans Condensed' as the main font for the project as it is easy to ready and gives the website a competent and professional feel to it.

## Database Schema

I am using MongoDB, which is a NoSQL database for this project. There are two entitites stored in the database which are user data and calibration data. The user data contains information like the user's name which is used when signing off a calibration and also the user's login details which are used to access the application and determine the access level granted. The calibration data includes instrument type, instrument location, due date, instrument tag id etc. which is all added to the databse by users. There is also a collection with calibration totals which is automatically incremented up or down on the database depending on the type of action carried out by the user.

### Database Structure
The database contains four collections:
- users
- cals_due
- cals_complete
- cal_totals

#### Users 

| MongoDB users Collection |
| -------- |
|![Users](assets/images/users.png)|

- This collection holds all of the user data

|  Key  |  Data Type | Notes |
| ------| ---------- | ----- |
|  `_id`  | Object Id  | This is automatically generated by MongoDB and is unique to each document. |
|  `first_name`  | String  | The first name of the user as entered on registration. This is used along with last_name when a user is signing off a clibration. Each completed calibration has a field containing the name of the user it was completed by. When a user logs in this is added to a session cookie `session["name"]` so it can be easily retrieved and attached to the calibration signoff form |
|  `last_name`  | String  | The last name of the user as entered on registration. This is used along with first_name when a user is signing off a clibration. Each completed calibration has a field containing the name of the user it was completed by. When a user logs in this is added to a session cookie `session["name"]` so it can be easily retrieved and attached to the calibration signoff form | 
|  `username`  | String  | The username chosen by the user upon registration. This username is required when the user wants to log in to access the application. When the user logs in this username is assigned to a session cookie `session["user"]` and the level of access granted is based on the data that is attached to that username on the DB |
|  `password`  | String  | This is the pasword chosen by the user upon registration. This password is required along with the username when logging in to the application. The password is hashed by werkzeug for secure password storage |
|  `is_supervisor`  | Boolean | This is either true or false depending on whether a user is a supervisor or not. This value is added to a session cookie `session["is_supervisor"]` so that it can easily be checked by the application. Supervisor access is required to view certain pages and to edit/delete certain documents. The application will check if this value is true or false and grant access appropriately. The value of is_supervisor is automatically assigned as false and can only be changed by logging in to the database on MongoDB.com as a form of protection for the application |


#### Calibrations Due

| MongoDB cals_due Collection |
| -------- |
|![Calibrations Due](assets/images/cals_due.png)|

- This collection contains the data on calibrations that are due for completion

|  Key  |  Data Type | Notes |
| ------| ---------- | ----- |
|  `_id`  | Object Id  | This is automatically generated by MongoDB and is unique to each document. |
|  `tag_id`  | String  | This is the tag id of the instrument which is local to the site that the instrument is located on. This tag is used as an identifier for the instrument that is to be worked on |
|  `inst_type`  | String  | This is the type of instrument that is to be worked on. Generally the instrument type is the same as the varible which it measures (Flow, Temperature, Pressure etc.) |
|  `location`  | String  | The location of the instrument that is to be worked on. The site address is entered in this field |
|  `due_date`  | String  | This is by which the requested work has to be completed. On the application this is converted to a datetime object and compared against a delta of 7 days which in turn will notify users that the work is nearing due date |


#### Calibrations Complete

| MongoDB cals_complete Collection |
| -------- |
|![Calibrations Complete](assets/images/cals_complete.png)|

- This collection contains the data on calibrations that have been signed off but are still on the database awaiting review to be closed out

|  Key  |  Data Type | Notes |
| ------| ---------- | ----- |
|  `_id`  | Object Id  | This is automatically generated by MongoDB and is unique to each document. |
|  `tag_id`  | String  | This is the tag id of the instrument which is local to the site that the instrument is located on. This tag is used as an identifier for the instrument that is to be worked on |
|  `inst_type`  | String  | This is the type of instrument that is to be worked on. Generally the instrument type is the same as the varible which it measures (Flow, Temperature, Pressure etc.) |
|  `location`  | String  | The location of the instrument that is to be worked on. The site address is entered in this field |
|  `due_date`  | String  | This is by which the requested work has to be completed. On the application this is converted to a datetime object and compared against a delta of 7 days which in turn will notify users that the work is nearing due date |
|  `signoff_user`  | String  | The name of the user that was logged in and signed off the calibration as complete. This data is taken from a session cookie `session["name"]` which is created with the users first and last name upon login |
|  `signoff_date`  | String  | The date that the user signd off the calibration as complete. The datetime python library is used to get the current date and it is converted to a string before being uploaded to the database |
|  `pass_or_fail`  | String  | This is the result of the calibration work carried out by the user. The user checks either the Pass or Fail radio button when completing the calibration signoff form |


#### Calibrations Totals

| MongoDB cal_totals Collection |
| -------- |
|![Calibration Totals](assets/images/cal_totals.png)|

- This collection contains the total number for calibrations stored on the database for various data points

|  Key  |  Data Type | Notes |
| ------| ---------- | ----- |
|  `_id`  | Object Id  | This is automatically generated by MongoDB and is unique to each document. |
|  `total_open`  | Int  | The total number of calibrations that are active on the system (have not been closed out yet). This is the total of cals_due + cals_complete and is incremented as required when any changes are made to the database, for example, deleting a calibration or closing out a completed calibration |
|  `total_due`  | Int  | This is the total number of calibrations due that are on the system. This total is incremented as required when any changes are made to the DB, for example, deleting a calibration or signing off a calibration as complete |
|  `total_pass`  | Int  | The cumulative total number of instruments that have passed a calibration. This number is incremented each time a calibration is signed off as a pass |
|  `total_fail`  | Int  | The cumulative total number of instruments that have failed a calibration. This number is incremented each time a calibration is signed off as a fail |

### Database Relationships

Each collection in the database is in some way linked to another collection. This image represents the relationships between each of the collections.

![Database Relationships](assets/images/db_relationships.jpg)

## Features 

The website features a main landing page which is accessible to all users and it has a calibration management application which is only accessible by logging in to the system. There are two access levels for users of the calibration management application which are standard level and supervisor level. Some features are only available to standard users (calibration signoff) and some features are only available to supervisor users (add new, delete, edit). All new accounts created are automatically set as standard user accounts and for security reasons can only be changed to supervisor level by modifying the user data directly on the database at MongoDB.com. This ensures that users can not create a supervisor level account and manipulate the stored data, which could be disastrous from a business point of view. The following credentials can be used to view the application with supervisor level permissions.
- Username: supervisor
- Password: supervisor

### Across all pages: 
- The navbar will be visible at the top of the page across all pages of the website. The navbar has the Precise Calibration logo on the left and there are multiple navigation items on the right-hand side: Home, About, Contact, Register, Log In, Log Out, New Cal, Cals Due, Dashboard. These navigation items are not always displayed on the navbar, they are dependant on whether a user is logged in or not, the user's access level and what page the user is on. The navbar collapses into a hamburger icon on smaller screens and the navbar pops out from the side of the screen.

### Home Page: 