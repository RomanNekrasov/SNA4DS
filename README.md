# SNA4DS

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li><a href="#getting-started">Getting Started</a></li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#authors">Contact</a></li>
  </ol>
</details>

## About The Project
Examine the presence and structure of echo chambers within YouTube comment sections, focusing on channels producing far right-wing content.

### Built With
[![Python 3.11](https://img.shields.io/badge/Python-3.11-3776AB)](https://www.python.org/downloads/)
![R 4.3.1](https://img.shields.io/badge/R-4.3.1-3776AB)

### Project Structure
Folder structure, stack.
I do not now how yet, keep python and r in different folders and start from there?

## Getting Started
### Using venv:
1. Clone the repository into a specific directory: `git clone https://github.com/RomanNekrasov/SNA4DS.git`
2. Enter project directory: `cd SNA4DS`
3. Create a virtual environment: `python -m venv envsna`
4. Activate virtual environment: `windows: envsna\Scripts\activate or mac: source envsna/bin/activate`
5. Install needed packages just with pip: `pip install package`
6. If you use external dependencies share them with: `pip freeze > requirements.txt`
7. Other can than install packages: `pip install requirements.txt`

### Using R:
We should all have similar R enviroments already.

### Add to gitignore
Different IDE's use files we do not want in our repo. Add your own to the .gitignore file  
E.g. for pycharm: https://github.com/github/gitignore/blob/main/Global/JetBrains.gitignore

## Usage
### Using Constants
Constants are used for all variables that are used multiple times and/or over multiple files  
Capitalize them.
1. personal constants: everytime you need a variable that's personal and where other team memebers have their personal version of it e.g. google drive path for data or a personal API key put it in the personal constant file. This file is in the gitignore so it is not updated. Reference the personal constant in the normal constant file so people know to put a new constant in the personal file. Look at the files first for an example for the drive path. 
2. constant file: Put in constants to use and make personal constants global.
3. Import using: `import constants as c`
4. Use the constant in the code where needed with: `c.CONSTANT`
5. Use a name that exactly describes the constant, do this for all variables actually.

### Using branches
You can not commit directly to main.  
If you work on something new or change some existing make a branch first.  
You are able to merge the brange yourself but if you do some collabarative work it's better to let a peer check it.  
Use proper names for branches.

## Authors
- Andy Huang
- Huub van de Voort 
- Oumaima Lemhour
- Roman Nekrasov
- Tom Teurlings
