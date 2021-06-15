# Website for Precise Calibration

## Code Institute Milestone Project 3 : Data Centric Development

Precise Calibration is a fictional company that provides calibration services for process instrumentation equipment. Some examples of this equipment would be pressure or temperature sensors in a pharmaceutical plant or oil refinery that require regular routine calibration for reasons of regulatory compliance. The website will feature a landing page with information about the company and its services with the goal of acquiring new customers. It will also contain a secure application for employees where they will be able to log in and keep track of work that is due for completionto ensure jobs are completed on time. This application will allow employees to make use of a database and CRUD operations to keep the calibration management system up to date.

A link to the live website can be found [here.](https://precise-calibration-ms3.herokuapp.com/)

## Table of Contents

- [User Experience (UX)](#ux)

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