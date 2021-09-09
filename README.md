# HandDetector

This piece of code has 2 parts to it: 
it detects the palm of a hand passed to it as a x-rayed picture and draws a red polygen around it.
it detects then the tips of the fingers in the same picture.
it also print a an excel file the coordinates of the detected palm/tips. 
it simply creates a small template polygen thats placed in the center of the palm and after proccesing the images (changes the brightness, normalize, apply blur, canny, etc.)
and then moves the coordinates of the polygen to the edges of the hand. its accuracy is ~85%. for the scond part it crops the palm part and start looking for the finger tips and marks them with a red dot, finally it prints the coordinates to an excel file
