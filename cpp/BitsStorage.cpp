#include "BitsStorage.h"

// --- class BitsStorage ---------------------------------------------------------------------------
// constructor for case, when object allocate his own memory
BitsStorage::BitsStorage(ndxType countOfBytes) {
    dataPtr = (bits_storage_t *)malloc(sizeof(bits_storage_t) + countOfBytes * sizeof(byte));
    dataPtr->allocatedBytes = countOfBytes;
    dataPtr->usedBits = 1;

}

// constructor for case, when object use already allocated memory (or some physical memory)
BitsStorage::BitsStorage(ndxType lengthOfMemoryInBytes, bits_storage_t* memPtr) {
    dataPtr = memPtr;
    dataPtr->allocatedBytes = lengthOfMemoryInBytes - sizeof(bits_storage_t);
    dataPtr->usedBits = 1;
};

BitsStorage::~BitsStorage() {
    //if (dataPtr->selfAlocated) {
        free(dataPtr);
    //    free(dataPtr);
    //}
}

/**
 * Set bit by index.
 */
void BitsStorage::setBit(ndxType bitIndex, boolean bit) {
    if (bit) {
        dataPtr->array[BYTE_IN_ARRAY(bitIndex)] |= MASKED_BIT(bitIndex);
    } else {
        dataPtr->array[BYTE_IN_ARRAY(bitIndex)] &= ~ MASKED_BIT(bitIndex);
    }
}

/**
 * Return  value of bit given by by index.
 */
boolean BitsStorage::BitsStorage::getBit(ndxType bitIndex) {
    return ((dataPtr->array[BYTE_IN_ARRAY(bitIndex)] & MASKED_BIT(bitIndex)) != 0);
}


unsigned  short BitsStorage::getUsedBits() {
    return dataPtr->usedBits;
}

void BitsStorage::dump(FILE *outFile) {
    if (outFile == NULL) {
        outFile = stdout;
    }

    fprintf(outFile, "allocatedBytes: %d\n", dataPtr->allocatedBytes);
    fprintf(outFile, "usedBits: %d\n", dataPtr->usedBits);
    // output by bytes
    ndxType lastByte = BYTE_IN_ARRAY(dataPtr->usedBits);
    for (ndxType byteIndex = 0; byteIndex <= lastByte; ++byteIndex) {
        fprintf(outFile, "#%d byte: ", byteIndex);
        ndxType lastBit;
        if (byteIndex == lastByte) {
            lastBit = BIT_IN_BYTE(dataPtr->usedBits);
        } else {
            lastBit = 7;
        }

        ndxType longBiteIndex;
        for (ndxType bitIndex = 0; bitIndex <= lastBit; ++bitIndex) {
            longBiteIndex = 8 * byteIndex + bitIndex;
            if (getBit(longBiteIndex)) {
                fprintf(outFile, "1");
            } else {
                fprintf(outFile, "0");
            }
        }

        fprintf(outFile, " [bin-reversed], %02X [hex], %d [dec]\n", dataPtr->array[byteIndex], dataPtr->array[byteIndex]);
    }
}

