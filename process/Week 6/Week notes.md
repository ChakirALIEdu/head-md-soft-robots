# Notes of the direction of the project

Theo Jansen wood sculpture
Faire des chaînes de longueures progressives
Pas changer d'objets


In general, it feels like the project is headed in an interesting direction. I'm not discontent with it. I'm feeling streamlined and focused.


# PLEASE CHECK IMG file for videos
## Shape of the object

The prototype research shown to Douglas, Alexia, Laure and Pierre semmed to have had them satisfied. 
The shape of the object may remain the same, though adjustments can be made to help with its modularity (rounded/padded base)
I may also research ways to truly attack to the cables. I did add some extrusions that would keep the cone from moving along the parallel axis of the cable, 
but something to truly latch on to it, so the rotation can truly remain, may be researched further

Below, you can see the different sizes and shapes of the object, as well as a 3D model ready for impression (changed the topology to have the shape be easly cutted and folded back together)

![image](img/1%20(1).png)
![image](img/1%20(2).png)
Moving on, I did research on the object's interactions. In that form and those input output systems, the object is fine, but it does lack a scenario, or perhaps an animalistic/interactive aspect that gives it the same flavor as living animals.

With that being said, I conconcted a video showing different interactions for the object. Instead of only reacting to proximity, ti reacts to movements done around the cables


For example, pulling the cable would make it shiver, plugging cables or addding more to an extension chord may excite them. They can huddle up together, hit the ground, "wag their tail", excite
As such, the cable paralinkers (or quiltish? quiblish? name pending) behave like a colony of animals, glued on to cables like those bigourneaux animals.

![image](img/1%20(1).jpg)
![image](img/1%20(2).jpg)
The interactions do a lot, and will help in the creation of a more itneresting scenario for the soft robot. It is also all feasible, and just adds to the project. (Feasability notwithstanding. i highly doubt feasability was the point, though it shall remain a problematic I'll be aware of, as a reflex)

## Electronics


The mechnanism of the object would be simple. I decided not to go with ultrasonic sensors or motion sensors, as those would react to anything.
Instead, I am opting for a raspberry pi setup, with an usb camera. I already tested it last friday, and the rig works.

Simply put, the raspberry pi will be connected elsewhere and hold an USB camera. That camera will run a simple python code, using motion sensor libraries. 
It cuts the camera input into 6 regions, and detects movements in those 6 regions.
When those regions detect movement, they send data in from of 1 or 0 to the arduino.


The arduino, connected to the raspberry pi via an USB cable, receives the input and will then move the servos according to which part of the camera's image mvoed first.


Essentially, the electronics part of the project will involve a raspberry pi, an usb camera, an arduino, micro servos, and maybe microprocessors. The rig is fairly simple

What's left to do is creating modules to hold each parts of the project. I will not be altering the raspberry pi much (it's not "part" of the project or doesn't ultimately need to be included)

But the object in the end could be a 3D printed module, with then the paper cone being attacked to it. 
It would be possible to change the shape of the cones however I please? Creating different sizes and  shapes and heights. I could also add frills or spikes which could further expand the boundary of the robot.

# Pnteresting Notes


## Thoughts


I am content. Though, I lack time to fully document all of this.

# Reviews from teachers
Fine. Excitement.