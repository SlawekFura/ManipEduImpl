#include "ros/ros.h"
#include "boost/variant.hpp"
#include "manipulator/ValidateIKNode.h"
#include "manipulator/ValidateLMNode.h"
#include "manipulator/ValidateSKNode.h"
#include "manipulator/ValidateVisualNode.h"
    
#include <string>
#include <vector>
#include <utility>
#include <typeinfo>
    
class INodesManager
{       
public: 
    using service = boost::variant<manipulator::ValidateIKNode,
                                   manipulator::ValidateLMNode,
                                   manipulator::ValidateSKNode,
                                   manipulator::ValidateVisualNode>;
    using NodeAction = std::function<void()>;
    struct NodeInfo
    {
        NodeInfo(service srv, ros::ServiceClient client, NodeAction act = [](){}) : srvType(srv), srvClient(client), action(act) {};
        service srvType;
        ros::ServiceClient srvClient;
        NodeAction action;
    };          
                
    virtual void validateAllNodes() = 0;
    virtual void addClients(std::vector<INodesManager::NodeInfo>&&) = 0;
};              
