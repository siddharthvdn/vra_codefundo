# Sahaay : Co-Ordinating rescue/relief operations among relief camps

## Issues to be tackled
Recent floods in the states of Kerala and Nagaland have highlighted a major issue with the present disaster management systems : **resource allocation and the resultant deficit**.
Most of the time, the deficit isn't caused by the actual unavailability of the resources with the disaster management teams. In fact, in the event of the Kerala floods, a huge amount of resources in one relief camp were observed to be discarded(especially clothes), even when some people in other relief camps needed them very badly. The main issue here is the lack of **co-ordination** between the relief camps and the **lack efficient transfer** of resources between the camps. 

We tackle this problem with the reasonable assumption that the camps are well equipped with mobile/computing devices with internet and GPS connectivity, and if they are not reachable by any technical means, it is unable to include them in the coordination process.

## Solution

We propose an application to solve the problem. An instance of the application is deployed in each of the relief camp. 

  - Each relief camp admin will continuously update the resource-status at their respective camp. 
  - The status data will include the resource ID (the kind of resource, e.g: clothes, water, etc), whether it is in surplus and how much, or if it is deficit and how much is required.
  - A centralized server will collect this information and make decisions on efficiently transferring(the 'efficiently' will be elaborated soon) the resources from one camp to another.
  - Once a decision is made, say a command 'Transfer N units of resource R from camp A to camp B'(which is an output of a backend algorithm) is spit out, the corresponding instructions are sent to the respective camps. The instruction to the camp A will be to lock away N units of resource R for a representative from camp B to collect them.

## Additional Features

  - Relief camps can gather local information and update the severity of the disaster. This can help us generate a heatmap which conveys the impact of the disaster at various places and allow transport teams to choose the best route to get from one place to another.

