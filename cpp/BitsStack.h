#ifndef COMPRESSED_MEM_BITS_STACK_H
#define COMPRESSED_MEM_BITS_STACK_H

/****************************************************************************
 * access to bits
 ****************************************************************************/
/* position of byte in array where bit is */
#define BYTE_IN_ARRAY(bit) ((bit) / 8)

/* position of bit in selected byte */
#define BIT_IN_BYTE(bit) ((bit) % 8)

/* mask for bit */
#define MASKED_BIT(bit) ((byte) (1 << BIT_IN_BYTE(bit)))

/***************************************************************************
*                            TYPE DEFINITIONS
***************************************************************************/

#ifndef uint8_t
typedef unsigned char uint8_t;
#endif


#ifndef byte
typedef uint8_t byte;
#endif

#ifndef boolean
typedef bool boolean;
#endif

typedef unsigned short ndxType;
typedef unsigned int valueType;

struct bits_storage_t
{
    ndxType usedBits;             /* number of actual used bits in array */
    byte array[];                 /* array of bytes containing bits, first bit is used as flag  selfAlocated */
};

typedef union mapValueTypeToBytes {
    valueType  asValueType;
    byte asBytes[sizeof(valueType)];
} mapValueTypeToBytes;

/*
 * Represents memory, where it is stored compressed information.
 * It can be used already allocated memory or memory  allocates by the object (two types of constructors)
 */
class BitsStack {
    protected:
        bits_storage_t* _dataPtr;       /* point to compresed memory */
        boolean _selfAllocated;         /* Who allocate memory? Me or someone else? */
        ndxType _allocatedBytes;        /* number of bytes used for storage */
        ndxType _maxBitIndex;          /* maximum index for bits (minimum is 0) */
        void _setBit(ndxType bitIndex, boolean bit);
        boolean _getBit(ndxType bitIndex);
    public:

        BitsStack(ndxType countOfBytes);
        BitsStack(ndxType lengthOfMemoryInBytes, bits_storage_t* dataPtr);
        virtual ~BitsStack();
        ndxType getUsedBits();
        ndxType getAllocatedBytes();
        void dump(FILE *outFile=NULL);
        boolean setBit(ndxType bitIndex, boolean bit);
        boolean getBit(ndxType bitIndex, boolean& result);
        boolean addBitToEnd(boolean bit);
        boolean addToEnd(valueType data, ndxType countOfValidBits);
        boolean readFromEndPosition(ndxType endIndex, ndxType countOfValidBits, valueType& result);
};

#endif //COMPRESSED_MEM_BITS_STACK_H
