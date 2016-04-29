#EV3Server

##Setup

After downloading the repostitory, move the folder ev3server (if it is
not named this, rename it) into the /home/robot folder. I generally
use a program like cyberduck to SFTP into the ev3 that way I can just
drag and drop the files. After doing this ssh into the ev3 in order to move
the index.html and service file. The root user is robot and the password is
maker. Then follow these steps.
```
cd /home/robot/ev3server/
sudo mv index.html /
sudo mv ev3server.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable ev3server.service
```

We navigate to where the files are, and move the index.html
and ev3server.service file. The .service file will make it so
that the server runs on boot. 

You can then reboot the ev3 and after several moments the server will begin.
Navigate to the ip address located on the top of the ev3 screen in your
preferred web browser and the EV3's webpage should be there. You
can then control the speed and on time of the motors.