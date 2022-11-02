- [x] Refactor and cleanup models.py
- [x] Refactor and cleanup models.js
  - [x] Update user code in dashboard.js

<br>

- [x] Implement Argon2 for password storage

<br>

- [x] Implement and test APIs for web server
  - [x] Create User
  - [x] Update User
  - [x] Get Users
  - [x] Get User 
  - [x] Create FoodConsumed
  - [x] Delete FoodConsumed
  - [x] Get FoodConsumed
  - [x] Create exercise
  - [x] Delete exercise
  - [x] Get exercises
   
<br>

- [x] Error handling on APIs
- [x] Status Codes on all responses

<br>

- [ ] Implement session management
- [ ] Update APIs to check user session for API authorization

<br>

- [ ] Test all models in models.py
  - [ ] Macros
  - [ ] FoodConsumed
  - [ ] ExerciseDone
  - [ ] GenderEnum
  - [ ] NewUserInfo

<br>

- [ ] Make sure that all datetimes/datetimes from the client are in UTC 

<br>

- [ ] Implement client-side API calling functions for calling app web server APIs
  - [ ] insertFoodConsumed(foodConsumed)
  - [ ] deleteFoodConsumed(id, foodId, timeConsumed)
  - [ ] getFoodConsumed(id, [foodId], [timeConsumed])

<br>
  
- [ ] Refactor dashboard page markup such that:
  - [ ] New item menu is outside main element
  - [ ] Modal dialog is outside main element

<br>

- [ ] Refactor app singleton object's DOM element object so that its structure matches the markup
  - [ ] Move newItem out of e.main into e
  - [ ] Move modalDialog out of e.main into e

<br>

- [ ] Test newItems list -> modalDialog -> dialogConfirm UI behavior