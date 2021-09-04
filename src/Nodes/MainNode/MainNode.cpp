#include "ros/ros.h"
#include "std_msgs/String.h"
#include "NodesManager.hpp"

#include <iostream>
#include <fstream>
#include <sstream>
#include <thread>
#include <vector>

int main(int argc, char **argv)
{
    ros::init(argc, argv, "Main");
    ros::NodeHandle nodeHandle;
    
    ROS_INFO("Starting MainNode");
    NodesManager nodesManager(nodeHandle);
    std::thread launcherThread([]()
        {
            ROS_INFO("Run roslaunch command");
            system("roslaunch manipulator manipLaunchTest.launch > /tmp/tmpManip.log");
            std::ifstream fstream("/tmp/tmpManip.log.");
            std::ostringstream stream; stream << fstream.rdbuf();
            ROS_INFO("%s", stream.str().c_str()); 
            ROS_INFO("Run roslaunch success");
        });
    nodesManager.addClients(
    {
        NodesManager::NodeInfo{manipulator::ValidateIKNode{}, nodeHandle.serviceClient<manipulator::ValidateIKNode>("/manipulator1/IKNodeValidator")},
        NodesManager::NodeInfo{manipulator::ValidateLMNode{}, nodeHandle.serviceClient<manipulator::ValidateLMNode>("/manipulator1/LMNodeValidator")},
        NodesManager::NodeInfo{manipulator::ValidateSKNode{}, nodeHandle.serviceClient<manipulator::ValidateSKNode>("/manipulator1/SKNodeValidator")},
        NodesManager::NodeInfo{manipulator::ValidateVisualNode{}, nodeHandle.serviceClient<manipulator::ValidateVisualNode>("/manipulator1/VisualNodeValidator")}
    }); 
    nodesManager.validateAllNodes();
        
    std::cout << "DUPA" << std::endl; 
    ROS_INFO("Ready for work!"); 
    while (ros::ok())
    {
    }           
    
    std::cout << "DUPA1" << std::endl; 

    std::cout << "Erase thread" << std::endl; 
    launcherThread.join();
    ROS_INFO("Thread erased!"); 
    return 0; 
}
