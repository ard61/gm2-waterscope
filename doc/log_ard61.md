# GM2 log - Antoine

### Thursday 11 May

Morning meeting - met with all the participants. Understood - more or less - what the current hardware and software does. 

Currently, there is:
* A Raspberry Pi 3, with software and a GUI that can scan the whole microscope table
* A custom motors board to control the motors
* An Arduino to control sensors and LEDs

Discussed what we would be working on: there was a multitude of proposals - sigh ... cf my notes for all of that

We finally did converge - I think? - to streaming the camera output to a web-page, and being able to control the microscope through a web-interface (hence not worrying anymore about the internal workings inside the Raspberry Pi).

And agreed to a further meeting on Saturday 3:30pm BST. Not sure what we will discuss there: we're expecting a demo of the current kit, and an introduction to the software? It would be helpful if we could finalise in broad terms what we will be working on. 


### Monday 15 May

Converged on the features we'll want at the end of the project, and fleshed out the different components we'll need to achieve them. We decided that our end-goal, to be able to control the microscope and view its output from an external device, can be split off into two groups, one focusing on the interface between the Raspberry Pi and the motors & sensors, the other focusing on the interface between the Raspberry Pi and the external device. 

The precise goals were documented in [here](https://docs.google.com/document/d/1QzkXOdFrkiqjfj2YdRiPwxmbORR5bd-4i0nzOWeweW4)

Since the project proposal is due on Thursday, we have also discussed how we would proceed for that presentation. After consulting with Alexandre Kabla, the only written document will be on costing and parts needed - all the other items on the list will be delivered orally. 

Fergus gave us a Raspberry Pi camera we'll use - many thanks to him!

Followed the tutorial [here](https://frillip.com/using-your-raspberry-pi-3-as-a-wifi-access-point-with-hostapd/) and configured the Raspberry Pi as a WiFi hotspot.

We agreed on how to split off the project proposal presentation. 

*	Kai Song and William will present the context, the problem that we're solving, and describe the solution that we plan to deliver, and it's meant to be used. 

*	Akhass will give a presentation of the technical plans to build the hardware - RPi interface.

*	I'll be explaining the design of the Raspberry Pi - External Device interface, as a step towards our feature of being able to view and control the microscope from the external device (also including contingency plans such as what happens if there are latency/bandwidth issues with streaming video). 

	Definitely I want to talk about our AGILE approach to getting features out, and also propose a rough design based on my internship experience last year (things might turn out slightly different as I investigate Flask/streaming). 

	I will also present a mockup of the website which will help us get feedback for our design - which I've started [here](https://app.moqups.com/ard61/7ybYBf96FC/view). 

	I'm planning to do all of this before we meet on Wednesday to rehearse for our Thursday presentation and gather feedback.


William's done the risk assessment sheet, awesome! And he'll do the costing sheet too. 
Kai Song got the Raspberry Pi camera to work, using the raspistill and raspivid tools. 

#### So, the next things to do for me are:

Prepare my part of the project proposal:
*	get familiar with the different intermediate targets / maybe flesh them out a bit more, think where they could fail, think about the time each would take.