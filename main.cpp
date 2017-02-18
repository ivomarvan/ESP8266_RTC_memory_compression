#include <iostream>
#include "BitsStorage.cpp"

int main() {
    std::cout << "Hello, World!" << std::endl;
    /*
    std::cout << "sizeof(byte): "  << sizeof(byte)<< std::endl;
    std::cout << "sizeof(unsigned short): "  << sizeof(unsigned short)<< std::endl;
    std::cout << "sizeof(bits_storage_t): "  << sizeof(bits_storage_t)<< std::endl;
    for (int i = 0; i < 8; ++i) {
        std::cout << "i:" << i << ", 1 << (i):"  << (1 << (i))<< std::endl;
    }
     */
    BitsStorage s = BitsStorage(16);
    for (ndxType bitIndex = 0; bitIndex <= 25; ++bitIndex) {
        s.setBit(bitIndex, ((bitIndex % 3) == 0));
        s.dataPtr->usedBits += 1;
    }
    s.dump(NULL);
    return 0;
}