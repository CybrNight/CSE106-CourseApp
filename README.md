# CSE106-Project

Code for CSE106 course registration app project

## Setup
### Clone repo and install requirements
```bash
    git clone https://github.com/CybrNight/CSE106-CourseApp.git .
    pip install -r requirements.txt
```

### Setup database model with default data
```python
    from project import *
    rebuild()
```
### Run flask app
```bash
    flask --app project run
```

