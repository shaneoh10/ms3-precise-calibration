# Pecise Calibration - Testing

[Back to README.md](README.md)

## Chrome Developer Tools

I used Chrome Developer Tools throughout the development of the project to assist with the design and layout of each page. This is a great tool to use when implementing or making changes to HTML and CSS code as it allows you to test various font sizes, margin, padding etc. before committing any changes to the project. I also found it very useful to help me find exactly which elements needed to be targeted in the DOM when making visual changes to the pages (JQuery effects, media queries etc.). I am satisfied with how the website turned out and I think it is clear and easy to read on mobile, tablet and desktop. Overall, I would have to say the best experience is on larger devices (desktop, laptop), which would be the intended device to use the application on in a real setting.

When testing the responsiveness of the website I encountered an issue with the positioning of the due-soon span on mobile devices. 

![crome-dev-1](assets/images/testing-images/chrome-dev-1.png)

As the primary use for the application is on larger screen sizes, I decided to implement a media query to set `display: none` on the due-soon span on mobile devices. The due-soon span will now only appear on devices with screen width of greater than 600px so that it does not interfere with the appearance of the page. I also had a similar issue on the dashboard with the pass/fail spans and implemented the same solution.

### Lighthouse 

I ran tests with lighthouse across all of the pages for both desktop and mobile. Below is an example of some of the errors that were found in these tests:

![lighthouse-1](assets/images/testing-images/lighthouse-1.png)

## Validation

### W3C Validator

#### HTML

I ran HTML validator tests throughout the development of project with the W3C Validator. See below some of the errors that were caught.

![W3C-html-1](assets/images/testing-images/W3C-html-1.png)
![W3C-html-2](assets/images/testing-images/W3C-html-2.png)

I investigated and refactored the code to fix these errors and on the final tests there were no errors found in the HTML across the website.

#### CSS

When testing the CSS with the validator the following errors and warnings were found.

![W3C-css-1](assets/images/testing-images/W3C-css-1.png)

These errors and warnings are found in the Materialize CDN and the Fontawesome CDN and are therefore out of my control. To bypass these CDN files and to get a more accurate result I tested my own CSS files by direct input into the validator and the following result was returned.

![W3C-css-2](assets/images/testing-images/W3C-css-2.png)

This test result shows that I was using an invalid value for the vertical-align property, which I promptly fixed. After fixing this error there were no more errors found in the CSS files.

### JSHint

I ran all the JavaScript code through JSHint and I found a few errors which I was able to easily resolve.

- There were multiple counts of 'missing semicolon' which was an easy fix
- There are multiple counts of undeclared variable which can be ignored. These variables are declared in external resources (JQuery, ScrollReveal, Materialize)
- There are multiple warnings which remain present in the files about the use of `let` and `const` in JS version ES6 as follows: `let' is available in ES6 (use 'esversion: 6') or Mozilla JS extensions (use moz).` I found an article on stack overflow [here](https://stackoverflow.com/questions/27441803/why-does-jshint-throw-a-warning-if-i-am-using-const) that advises by adding `/*jshint esversion: 6 */ ` at the top of the javascript files it would clear this error. I implemented this solution while testing in JSHint and the warnings were no longer present.

## Web Browser and Device Testing