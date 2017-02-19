#include <iostream>
#include "BitsStack.cpp"



int main() {
    std::cout << "Hello, World!" <<  std::endl;

    std::cout << "sizeof(valueType): "  << sizeof(valueType)<< std::endl;
    /*
    std::cout << "sizeof(valueType): "  << sizeof(valueType)<< std::endl;
    std::cout << "sizeof(unsigned short): "  << sizeof(unsigned short)<< std::endl;
    std::cout << "sizeof(bits_storage_t): "  << sizeof(bits_storage_t)<< std::endl;
    for (int i = 0; i < 8; ++i) {
        std::cout << "i:" << i << ", 1 << (i):"  << (1 << (i))<< std::endl;
    }
     */

    /*
    BitsStack s = BitsStack(16); // 16 bytes
    s.dump(NULL);
    valueType data1, data2;
    int maxTest = 8;
    fprintf(stdout, "--- sore ---------------------------------------\n");
    for (int i = 0; i < maxTest; ++i) {
        data1 = (unsigned short) i;
        data2 = (unsigned short) 2*i;
        fprintf(stdout, "#%d %2d, %2d\n", i, data1, data2);
        s.addToEnd(data1, 3);
        s.addToEnd(data2, 4);
    }

    fprintf(stdout, "--- load ---------------------------------------\n");
    ndxType bitIndex = s.getUsedBits() - 1;
    for (int i = 0; i < maxTest; ++i) {
        if (not s.readFromEndPosition(bitIndex, 4, data2)) {
            fprintf(stdout, "Error, data1\n");
        }
        bitIndex -= 3;
        if (not s.readFromEndPosition(bitIndex, 4, data1)) {
            fprintf(stdout, "Error, data2\n");
        }
        bitIndex -= 4;
        fprintf(stdout, "#%d %2d, %2d\n", i, data2, data1);
    }
    s.dump(NULL);

    /*
    bits_storage_t* dataPtr = (bits_storage_t*) malloc(512);
    BitsStack s1 = BitsStack(16, dataPtr);
    for (ndxType bitIndex = 1; bitIndex <= 25; ++bitIndex) {
        s1.setBit(bitIndex, ((bitIndex % 4) == 0));
        s1.dataPtr->usedBits += 1;
    }
    s1.dump(NULL);
    free(dataPtr);
    */
    return 0;
}