#include "NodesManager.hpp"

#include <boost/variant.hpp>

void NodesManager::addClients(std::vector<NodeInfo>&& nodesClients)
{
    this->nodesClients = nodesClients;
}

void NodesManager::validateAllNodes()
{
    for (auto& node : nodesClients)
    {
        auto& srv = node.srvType;
        bool isServiceStarted = false;

        node.action();
        ROS_INFO("wait for service: %s", node.srvClient.getService().c_str());
        node.srvClient.waitForExistence();
        switch(srv.which())
        {
            case 0:{
                manipulator::ValidateIKNode service;
                isServiceStarted = node.srvClient.call(service);
                break;}
            case 1:{
                manipulator::ValidateLMNode service;
                isServiceStarted = node.srvClient.call(service);
                break;}
            case 2:{
                manipulator::ValidateSKNode service;
                isServiceStarted = node.srvClient.call(service);
                break;}
            case 3:{
                manipulator::ValidateVisualNode service;
                isServiceStarted = node.srvClient.call(service);
                break;}
            default:
                ROS_ERROR("No such service!");
        }

        ROS_INFO("Service: %s started: %s", node.srvClient.getService().c_str(), isServiceStarted ? "true" : "false");
    }
}
