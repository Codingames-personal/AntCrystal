# Tools for the CodinGames platform

CodinGame platform require to have a script with all of the code on it of course this is not really helpfull for coding, testing and debugging.
That why I am trying to create this environment.

## Structure

When a repertory is made for CodinGame, it will have to clone this one firstly.

You will find here this repertories :
* src : it contains the differents main objects of your code
* tests : it contains the tests of your code
* core : a folder that is made for the management of the environmenet


### manage.py

This file will be the one to use to manage your project. It is inspired from the django librairy.
It will have the following command :

* merge : merge all the files that are required (not tests by exemples) and create the script main.py

### cgignore

This file contains the script that you do not want in merge 

### cgfolder

This file contains the name of the folder that you want to merge

## How does it works

You have to put the order of your script at the top of its with the keyword "order :" :

```py
# author : Blopausore ,... order : 1
```

Then you can merge it with :
```bash
python manage.py merge
```
