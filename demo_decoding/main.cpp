#include <iostream>
#include <fstream>
#include <vector>

struct DemoHeader {
    char magic[8];      // Magic number or signature
    // char demo_guid[12];
    int32_t protocol;   // Protocol version
    char serverName[260];
    char clientName[260];
    char mapName[260];
    // Add more fields as needed
};

int main() {
    std::ifstream file("test.dem", std::ios::binary);

    if (!file.is_open()) {
        std::cerr << "Failed to open file!" << std::endl;
        return 1;
    }

    DemoHeader header;
    file.read(reinterpret_cast<char*>(&header), sizeof(DemoHeader));
    if (!file) {
        std::cerr << "Failed to read header!" << std::endl;
        return 1;
    }

    // Output header fields for verification
    std::cout << "Magic: " << std::string(header.magic, 8) << "\n";
    std::cout << "Protocol: " << header.protocol << "\n";
    std::cout << "Server Name: " << header.serverName << "\n";
    std::cout << "Client Name: " << header.clientName << "\n";
    std::cout << "Map Name: " << header.mapName << "\n";

    file.close();
    return 0;
}
