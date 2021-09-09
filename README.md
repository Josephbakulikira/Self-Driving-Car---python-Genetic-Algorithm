# Self Driving Car python
---
Not Finished Yet
---
## YOUTUBE CHANNEL
 Subscribe for support : http://www.youtube.com/channel/UCjPk9YDheKst1FlAf_KSpyA?sub_confirmation=1

---
### Requirements
      pygame : pip install pygame
      pickle : pip install pickle-mixin
---
### Controls
    - "R" to show boundary lines
    - "F" to show wireframe mode
    - "Q" to change the Theme
    - "Esc" to quit without saving the tracks modification
    - "Enter (Return) or P " to the parameter panel
    - "WASD or Arrows keys" to control the car
 
---
### Bugs
For a much better ai of self driving car , you should try to get maybe four output for brake, accelerate, left and right 
instead of just left and right as i did. Although this might take a lot of time to train but it definetly the better way to do it.

     -The car control still need a little bit of work.
     -The AI only decide if it will go right or left, to get a much better ai should decide by itself when to accelerate , when to brake and so on
      if you have a time and find a solution you can make a pull request.
---
![Screenshot (41)](https://user-images.githubusercontent.com/48150537/129870366-2266d4bc-8d0d-4bf2-85aa-fd1de656b1b2.png)
![Screenshot (40)](https://user-images.githubusercontent.com/48150537/129870374-83b75d29-653d-4921-b849-0b64013ecd78.png)
---

 If you want a track with a higher resolution and a higher control point , you can change this parameters in the constants file
 ![Screenshot (20)](https://user-images.githubusercontent.com/48150537/128978353-8ddea85c-c251-4166-b340-9864da70dfd8.png)
 
 Also When you load your saved data try to check if the N_points and spline_resolution are the same with the variables of the saved tracks, 
 if they are not the same this might  cause the saved track to look weird , to solve that issue you just have to change the n_points and 
 spline resolution in the constants file to the value store the   SavedTrack["variables"], ... 
 if you have a time to solve that issue you can always make a pull request .
 ---
![Screenshot (23)](https://user-images.githubusercontent.com/48150537/128980799-61a1bbcf-256c-4d9f-809e-4e5dc0f0503e.png)
![Screenshot (21)](https://user-images.githubusercontent.com/48150537/128980922-f169e580-9038-46e2-9044-a2a186e24df3.png)
![Screenshot (22)](https://user-images.githubusercontent.com/48150537/128980925-1dc6ddb8-75a8-4e1e-b467-245d5270a145.png)
![Screenshot (24)](https://user-images.githubusercontent.com/48150537/128980800-4fc8ff33-d194-461f-9463-0689408447d9.png)
---
#### sorry for the 🍝 code , enjoy✌️
