#ifndef BITSMEMORY_H
#define BITSMEMORY_H

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

struct bits_storage_t
{
    ndxType allocatedBytes;       /* number of bytes used for storage */
    ndxType usedBits;             /* number of actual used bits in array */
    byte array[];                        /* array of bytes containing bits, first bit is used as flag  selfAlocated */
};


/*
 * Represents memory, where it is stored compressed information.
 * It can be used already allocated memory or memory  allocates by the object (two types of constructors)
 */
class BitsStorage {
    protected:

    public:
        bits_storage_t* dataPtr;
        BitsStorage(ndxType countOfBytes);
        BitsStorage(ndxType lengthOfMemoryInBytes, bits_storage_t* dataPtr);
        virtual ~BitsStorage();
        ndxType getUsedBits();
        void setBit(ndxType bitIndex, boolean bit);
        boolean getBit(ndxType bitIndex);
        void dump(FILE *outFile);
};




#endif //BITSMEMORY_H
