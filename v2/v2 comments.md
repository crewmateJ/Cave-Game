Had some feedback that the data wasn't saving for larger cohorts of animals that had been playing for a while, here's what to do if you get this issue:
  - download v2 folder, and save it in the original Cave Game folder
  - run v2_main.py instead of main.py --> make sure you are located in the v2 folder when running it

Basically what happened is the data was poorly stored in the last version, and the max width for a csv row was reached (32,767 characters).
Now it stores each coordinate (x, y) in its own cell.

Thanks to those who gave feedback :)
