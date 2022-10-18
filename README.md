# Coen424_assignment 1

## About this Assignment
This assignment aims to practice the concepts, and techniques for data models and the communications for resources represented by data models.

The data set is from a Github project, under the directory of Workload Data.
https://github.com/haniehalipour/Online-Machine-Learning-for-Cloud-Resource-Provisioning-of-Microservice-Backend-Systems

I started by creating a server file where I made all the processing logic regarding the aassignment. I then proceeded to create a client.py file where I made all the inputs the user needs to put in the terminal to send the request.
Once the 2 files were ready, I made a TCP socket, connected them and got the data sending from client to server and back to the client. 

##Usage
Create 2 terminals (I suggest using split terminal if you are using Visual Studio Code or an editor that has its own terminal)
On both terminal, cd into the src directory Use: cd src
Start by running the server.py first by doing: python server.py
On the server terminal, you should see:

        Socket Successfuly created!
        Socket successfully connected to port 666
        Socket is listening

Only after the server is running, on the second terminal, start the client by: python client.py
On the client terminal you should see: 

        Please enter an ID for your request:

On the server terminal, you should be able to see your client connection as below:

        Connection received from ('127.0.0.1', 23716) 
        
        Note. The IP address and port may differ for you
Now you are set, you can start inputting the data you wish to request from the server.

## How it works?
Once the user has put in all inputs, based on the last input from the user where they choose which format they wish to receive the data, the data is serialzied in either protoco format or JSON format. 
On the server side, when it receives the data it processes the data and send the requested data back in the same format as the user has requested. The data is also being saved in files from the server side and the client side so the user can view the data being requested and sent from both sides.
