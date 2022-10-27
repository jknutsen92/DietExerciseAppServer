- [x] Refactor and cleanup models.py
- [x] Refactor and cleanup models.js
  - [x] Update user code in dashboard.js

<br>

- [ ] Implement and test APIs for web server
  - [ ] Create User
  - [ ] Update User
  - [ ] Get Users
  - [ ] Get User 
  - [ ] Create FoodConsumed
  - [ ] Delete FoodConsumed
  - [ ] Get FoodConsumed
  - [ ] Create exercise
  - [ ] Delete exercise
  - [ ] Get exercises
   
<br>

- [ ] Test all models in models.py
  - [ ] Macros
  - [ ] FoodConsumed
  - [ ] ExerciseDone
  - [ ] GenderEnum
  - [ ] NewUserInfo

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