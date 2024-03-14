#include <iostream>
#include <sys/stat.h>
#include <sys/types.h>
#include <ctime>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <filesystem>
namespace fs = std::filesystem;


    //  // Check if the file exists
    // std::ifstream outfileexist(outfilename);
    // if (outfileexist.good()) {
    //     outfileexist.close(); // Close the file if it exists

    //     // Delete the file
    //     if (std::remove(outfilename.Data()) != 0) {
    //         std::cerr << "Error deleting file!" << std::endl;
    //         return 1;
    //     } else {
    //         std::cout << "File deleted successfully!" << std::endl;
    //     }
    // } else {
    //     std::cout << "File does not exist." << std::endl;
    // }

void moveFilesToNewFolder(const std::string& sourceFolderPath, const std::string& destinationFolderPath) {
    try {
        // Create the destination directory if it doesn't exist
        if (!fs::exists(destinationFolderPath)) {
            fs::create_directories(destinationFolderPath);
        }

        // Iterate over files in the source directory
        for (const auto& entry : fs::directory_iterator(sourceFolderPath)) {
            if (entry.is_regular_file()) {
                // Get the filename and construct the destination path
                fs::path sourcePath = entry.path();
                fs::path destinationPath = destinationFolderPath + "/" + sourcePath.filename().string();

                // Move the file to the destination directory
                fs::rename(sourcePath, destinationPath);

                std::cout << "Moved file: " << sourcePath << " to: " << destinationPath << std::endl;
            }
        }
    } catch (const std::exception& e) {
        std::cerr << "Error: " << e.what() << std::endl;
    }
}
bool directoryExists(const char* path) {
    struct stat info;
    return stat(path, &info) == 0 && (info.st_mode & S_IFDIR);
}

bool createDirectory(const char* path) {
    std::cout << "----------------" <<std::endl;
    mkdir(path, S_IRWXU | S_IRWXG | S_IROTH | S_IXOTH);
    return 0;
    // return mkdir(path, S_IRWXU | S_IRWXG | S_IROTH | S_IXOTH) == 0;
}

std::string getCurrentTime() {
    std::cout << "============++++++++++" << std::endl;
    std::time_t t = std::time(nullptr);
    char buffer[20];
    std::strftime(buffer, sizeof(buffer), "%Y%m%d%H%M%S", std::localtime(&t));
    return std::string(buffer);
}
// int Checkpath() {
int Createpath (const char *folderName ){
    // const char *folderName = "../../Result/CB22/test";
    std::cout << folderName << std::endl;
    std::filesystem::path path(folderName);
    if (!std::filesystem::exists(path)) {
        if (!std::filesystem::create_directories(path)) {
            std::cerr << "Failed to create the directory!" << std::endl;
            return EXIT_FAILURE;
        }
        std::cout << "Directory created successfully." << std::endl;
    } else {
        std::cout << "Directory already exists." << std::endl;
        if (directoryExists(folderName)) {
        std::cout << "=================" << std::endl;
        // Directory exists, create a new directory with a unique name

        std::string newFolderName = folderName + getCurrentTime();
        std::cout << newFolderName << std::endl;
        if (createDirectory(newFolderName.c_str()))
        {
            std::cerr << "Failed to create the new directory." << std::endl;
            return EXIT_FAILURE;
        }

        // Here, you need to move the contents of the original directory to the new one
        // and then remove the original directory.

        std::cerr << "Directory renamed successfully." << std::endl;
        moveFilesToNewFolder(folderName, newFolderName);
     }
    }

    return EXIT_SUCCESS;
}
