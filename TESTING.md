# Pecise Calibration - Testing

[Back to README.md](README.md)

## Chrome Developer Tools

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