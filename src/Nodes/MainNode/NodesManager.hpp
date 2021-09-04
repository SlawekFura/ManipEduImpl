#include "INodesManager.hpp"

class NodesManager : public INodesManager
{
public:
    NodesManager(ros::NodeHandle handle) : nodeHandle(handle){};
    using INodesManager::NodeInfo; 
    using INodesManager::NodeAction; 
    void addClients(std::vector<NodeInfo>&&) override;
    void validateAllNodes() override;
private:
    std::vector<NodeInfo> nodesClients;
    const ros::NodeHandle& nodeHandle;
};  
