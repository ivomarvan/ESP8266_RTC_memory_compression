#include "BitsStack.h"

// --- class BitsStack ---------------------------------------------------------------------------
/**
 * Constructor for case, when object allocate his own memory. (Usualy for tests.)
 */
BitsStack::BitsStack(ndxType countOfBytes) {
    _dataPtr = (bits_storage_t *)malloc(sizeof(bits_storage_t) + countOfBytes * sizeof(byte));
    _allocatedBytes = countOfBytes;
    _selfAllocated = true;
    _dataPtr->usedBits = 0;
    _maxBitIndex = 8 * _allocatedBytes - 1;
}


/**
 * Constructor for case, when object use already allocated memory (or some physical memory)
 */
BitsStack::BitsStack(ndxType lengthOfMemoryInBytes, bits_storage_t* memPtr) {
    _dataPtr = memPtr;
    _allocatedBytes = lengthOfMemoryInBytes - sizeof(bits_storage_t);
    _selfAllocated = false;
    _dataPtr->usedBits = 0;
    _maxBitIndex = 8 * _allocatedBytes - 1;
};

/**
 * Destructor.
 */
BitsStack::~BitsStack() {
    if (_selfAllocated) {
        free(_dataPtr);
    }
}


/**
 * Set bit by index. Do not care about index range.
 */
void BitsStack::_setBit(ndxType bitIndex, boolean bit) {
    if (bit) {
        _dataPtr->array[BYTE_IN_ARRAY(bitIndex)] |= MASKED_BIT(bitIndex);
    } else {
        _dataPtr->array[BYTE_IN_ARRAY(bitIndex)] &= ~ MASKED_BIT(bitIndex);
    }
}


/**
 * Return  value of bit given by by index. Do not care about index range.
 */
boolean BitsStack::BitsStack::_getBit(ndxType bitIndex) {
    return ((_dataPtr->array[BYTE_IN_ARRAY(bitIndex)] & MASKED_BIT(bitIndex)) != 0);
}


ndxType BitsStack::getUsedBits() {
    return _dataPtr->usedBits;
}

ndxType BitsStack::getAllocatedBytes() {
    return _allocatedBytes;
}

/**
 * If index is in good range return true and set bit by index.
 * Else return false and do nothing.
 */
boolean BitsStack::setBit(ndxType bitIndex, boolean bit) {
    if (bitIndex > _dataPtr->usedBits) { // min index is 0 allways, ndxType is unsigned
        return false;
    }
    _setBit(bitIndex, bit);
    return true;
}

/**
 * If index is in good range return true and set result by bit on index.
 * Else return false and result is undefined.
 */
boolean BitsStack::getBit(ndxType bitIndex, boolean& result) {
    if (bitIndex > _dataPtr->usedBits) { // min index is 0 allways, ndxType is unsigned
        return false;
    }
    result = _getBit(bitIndex);
    return true;
}

/**
 * If storage is full, return false a do nothing.
 * Else add one bit on the end of storage.
 */
boolean BitsStack::addBitToEnd(boolean bit) {
    if (_dataPtr->usedBits - 1 <= _maxBitIndex) {
        _setBit(_dataPtr->usedBits, bit);
        _dataPtr->usedBits += 1;
        return true;
    }
    return false;
}

/**
 * Add bits from data to the end of storage. Use countOfValidBits bits from least significant.
 */
boolean BitsStack::addToEnd(valueType data, ndxType countOfValidBits) {
    if (countOfValidBits > sizeof(valueType) * 8) {
        return false;
    }
    if (_dataPtr->usedBits + countOfValidBits - 1 > _maxBitIndex ) {
        return false;
    }
    mapValueTypeToBytes map;
    map.asValueType = data;
    ndxType bitIndexInData;
    boolean bit;


    for (int i = 0; i < countOfValidBits; ++i) {
        bitIndexInData = (ndxType) i;
        bit = map.asBytes[BYTE_IN_ARRAY(bitIndexInData)] & MASKED_BIT(bitIndexInData);
        addBitToEnd(bit);
        /*
        printf(
                "\t#%2d: bitIndexInData=%2d, (_dataPtr->usedBits-1)=%2d, bit=%d\n",
                i, bitIndexInData, (_dataPtr->usedBits-1), (int) bit
        );
        */
    }
    return true;
}

/**
 * Read data from storage to result. Return success.
 * The endIndex point to last bit which we want read.
 */
boolean BitsStack::readFromEndPosition(
        ndxType endIndex,
        ndxType countOfValidBits,
        valueType& result
) {
    if (endIndex >= _dataPtr->usedBits) {
        return false;
    }
    mapValueTypeToBytes map;
    ndxType storageBitIndex, bitIndexInData;
    boolean bit;
    map.asValueType = 0;
    for (int i = countOfValidBits - 1; i >= 0; --i) {
        storageBitIndex = endIndex - (ndxType) i;
        bit = _getBit(storageBitIndex);
        bitIndexInData = countOfValidBits - (ndxType) i - 1;
        /*
        printf(
            "\t#%2d: storageBitIndex=%2d, bitIndexInData=%2d, bit=%d\n",
            i, storageBitIndex, bitIndexInData, (int) bit
        );
        */
        if (bit) {
            map.asBytes[BYTE_IN_ARRAY(bitIndexInData)] |= MASKED_BIT(bitIndexInData);
        } else {
            map.asBytes[BYTE_IN_ARRAY(bitIndexInData)] &= ~ MASKED_BIT(bitIndexInData);
        }
    }
    result = map.asValueType;
    return true;
}

void BitsStack::dump(FILE *outFile) {
    if (outFile == NULL) {
        outFile = stdout;
    }
    fprintf(outFile, "allocatedBytes: %d\n", _allocatedBytes);
    fprintf(outFile, "usedBits: %d\n", _dataPtr->usedBits);
    if (_dataPtr->usedBits <= 0) {
        return;
    }
    // output by bytes
    ndxType lastBitIndex = _dataPtr->usedBits - 1;
    ndxType lastByte = BYTE_IN_ARRAY(lastBitIndex);
    for (ndxType byteIndex = 0; byteIndex <= lastByte; ++byteIndex) {
        fprintf(outFile, "#%d byte: ", byteIndex);
        ndxType lastBit;
        if (byteIndex == lastByte) {
            lastBit = BIT_IN_BYTE(lastBitIndex);
        } else {
            lastBit = 7;
        }

        ndxType longBiteIndex;
        for (ndxType bitIndex = 0; bitIndex <= lastBit; ++bitIndex) {
            longBiteIndex = 8 * byteIndex + bitIndex;
            if (_getBit(longBiteIndex)) {
                fprintf(outFile, "1");
            } else {
                fprintf(outFile, "0");
            }
            if (bitIndex == 3) {
                fprintf(outFile, " ");
            }
        }

        fprintf(outFile, " [bin-reversed], %02X [hex], %d [dec]\n", _dataPtr->array[byteIndex], _dataPtr->array[byteIndex]);
    }
}

/**
 * Add bits from storageToAdd to the current storage
 */
 /*
boolean BitsStack::addToEnd(BitsStack& storageToAdd) {

}*/