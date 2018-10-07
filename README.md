# Relay
## University of Iowa Hackathon, 2018
We are Andrew Hancock, Jeremy Roghair, and Kellen O'Connor from Iowa State University.

# Inspiration
Have you ever noticed the steep learning curve required to get involved with programming? Despite the efforts of some of the nation's best educators, our society is missing out on the talents of many of the nation's youth due to the perceived challenge of getting involved in robotics.  While some competitions exist, such as FIRST Tech Challenge and FIRST Robotics Competition, many students don't have access to the resources required to start a team.

# Enter: Relay.

![alt text](https://raw.githubusercontent.com/jroghair/hackathon/master/relaypic.jpg)

We believe that getting youth involved with STEAM fields is of the utmost importance for the collective success of our planet.  Robotics is a fun and engaging way to get involved.  With Relay, teenagers have a simple way to interact with a myriad of components that are commonly used everywhere from agriculture to defense.

Relay is a collection of components that fit together to make a working system.  Whether your goal is to implement complex image analytics from a remote webcam through Google Cloud API or control an Arduino-based robot with a LiDAR, Relay is for you.  Configuration is performed through an easy to understand graphical user interface (a GUI for short).  Once the user configures *what* they want the system to do, they simply have to run Relay.

***Significance of the name***

The name Relay has multiple meanings.  The verb "relay" means "to receive and pass on".  Interpretted literally, our system is a way for all components of a system to share information with one another.  A relay is also an electrical device; a switch that is electronically controlled.  Based on the user's input to a relay, the system behaves differently.  See the similarity?

# How it works

The user of Relay has access to a GUI from which they can configure how components go together.  Under the hood, each component of the system runs on its own thread.  Each thread shares data via the Python Queue class.  By defining common data types early in the project, we were able to ensure compatibility amongst components.  One example is the Position data type.  Both the Point to Point robot navigation component and the Zed and IMU SLAM component rely on this data type.  Another example is the myriad of image processing plugins we have, including the IP webcam, HSV color conversion, the Google Cloud API annotator, and the MobileNet Single Shot Detector.  Other components include a lidar scanner and an Arduino/motor controller component.

# The Future of Relay

We firmly believe that Relay is a commercializable product.  As mentioned earlier, we've observed a lapse of widespread robotics education in the United States.  By licensing the software to schools and recommended hardware components, educators can provide a top-notch robotics curriculum, not limited in scope like other platforms.  For individual users, the GUI is a perfect starting point to understand how to put together a complicated system that utilizes cutting edge technology (deep learning, LiDAR, simultaneous localization and mapping, and more).  After a couple months with Relay, users may be ready to develop their own components and expand the functionality!

# Challenges we Faced

As with any immense project, there were plenty of hurdles to overcome.  Kellen struggled a lot with coming up with a scalable way to interface with sensors.  Once that was figured out early on, it made further component development significantly easier.  Andrew worked a lot on the embedded aspect of the robot - interfacing from a Python script to the Arduino through serial communcation.  Fitting that in with the rest of the Relay framework proved to be a challenge as well.  Jeremy worked extensively on learning a brand new GUI library, tkinter.  Learning the ins and outs of front end development with a previously unutilized library is a tough task.

# Our Accomplishments

We're very proud of what Relay is capable of.  We exceeded our goals for some basic components we wanted to create, and ended up building a whole robot to showcase what it's capable of.  The robot is capable of scanning the environment and navigating through a list of points.  It can also be commanded by a user to go just about anywhere.  Along the way, the user can put their phone camera on the robot to see what it sees from a first person view.



