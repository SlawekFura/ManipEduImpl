#include "ros/ros.h"
#include "std_msgs/String.h"
#include "NodesManager.hpp"
#include "manipulator/IKTask.h"
#include "manipulator/SKTask.h"
#include "manipulator/KinReqType.h"

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
            system("roslaunch manipulator manipLaunchTest.launch &> /tmp/tmpManip.log");
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
    
    //ros::NodeHandle n;
    //ros::ServiceClient client = n.serviceClient<manipulator::IKTask>("manipulator1/IKTask");
    //manipulator::IKTask srv;
    //manipulator::Point point;
    //point.X = std::vector<uint8_t>{1,2,3};
    //point.Y = std::vector<uint8_t>{4,5,6};
    //point.Z = std::vector<uint8_t>{7,8,9};
    //srv.request.points = std::vector<manipulator::Point>{point};
    //ROS_INFO("IKTask performing"); 
    //client.waitForExistence();

    //if (client.call(srv))
    //{
    //    ROS_INFO("Sum: %i", (int8_t)srv.response.numOfJoints);
    //}
    //else
    //{
    //    ROS_ERROR("Failed to call service IKTask");
    //    return 1;
    //}

    ros::NodeHandle n;
    ros::ServiceClient client = n.serviceClient<manipulator::SKTask>("manipulator1/SKTask");
    manipulator::SKTask srv;
    uint8_t reqType = manipulator::KinReqType::SK_PARAMS_REQ; 
    if (client.call(srv))
    {
        ROS_INFO("SKNode responded!");
    }
    else
    {
        ROS_ERROR("Failed to call service SKTask");
        return 1;
    }
    while (ros::ok()){}          
        
    std::cout << "DUPA1" << std::endl; 

    std::cout << "Erase thread" << std::endl; 
    launcherThread.join();
    ROS_INFO("Thread erased!"); 
    return 0; 
}
