#include <iostream>
#include <filesystem>

namespace fs = std::filesystem;

void handlePath(const std::string& pathStr ) {

    fs::path myPath(pathStr);

    if (fs::exists(myPath)) {
        if (fs::is_directory(myPath)) {
            std::cout << "Directory exists. Deleting..." << std::endl;
            fs::remove_all(myPath); // Delete directory and its contents
        } else {
            std::cout << "File exists, not a directory." << std::endl;
            return;
        }
    }

    std::cout << "Creating directory..." << std::endl;
    fs::create_directories(myPath); // Create directory recursively


  
}