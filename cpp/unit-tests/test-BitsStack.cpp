#include "catch.hpp"
#include "BitsStack.cpp"
#include <math.h>

TEST_CASE( "BitsStack tests" ) {

    unsigned short coutOfBytes = 16;

    SECTION( "init by zeros" ) {
        BitsStack s(coutOfBytes); // 16 bytes

        REQUIRE( s.getUsedBits() == 0 );

        for (unsigned short i = 0; i < 8 * coutOfBytes; ++i) {
            s.addToEnd(0, 1);
        }

        boolean result, success;
        for (unsigned short i = 0; i < 8 * coutOfBytes; ++i) {
            success = s.getBit(i, result);
            REQUIRE( success == true);
            REQUIRE( result == 0);
        }
    }

    SECTION( "init by 1" ) {

        boolean result, success;
        BitsStack s(coutOfBytes); // 16 bytes


        REQUIRE( s.getUsedBits() == 0 );
        REQUIRE( s.getAllocatedBytes() == coutOfBytes);

        for (unsigned short i = 0; i < 8 * coutOfBytes; ++i) {
            success = s.addToEnd(1, 1);
            REQUIRE( success == true);
        }

        // s.dump(NULL);


        for (unsigned short i = 0; i < 8 * coutOfBytes; ++i) {
            success = s.getBit(i, result);
            REQUIRE( success == true);
            REQUIRE( result == 1);
        }
    }

    SECTION( "add exact data" ) {

        boolean success;
        valueType result;

        struct data_type
        {
            unsigned short value;
            ndxType useBits;
        };

        data_type data[] = {
                {value:3, useBits:2},
                {value:8, useBits:4},
                {value:8, useBits:5},
                {value:127, useBits:8},
                {value:30, useBits:5},
                {value:(valueType) pow(2, 15), useBits:16},
                {value:145, useBits:8},
                {value:145, useBits:9},
                {value:145, useBits:20 },
        };

        ndxType countOfItems = sizeof(data) / sizeof(data_type);
        int countOfBits = 0;
        for (unsigned short i = 0; i < countOfItems; ++i) {
            countOfBits += data[i].useBits;
        }
        ndxType countObBytes = countOfBits / 8;
        if (countOfBits % 8) {
            countObBytes += 1;
        }
        printf("countOfItems:%d, countOfBits:%d countObBytes:%d\n", countOfItems, countOfBits, countObBytes);


        BitsStack s(countObBytes);

        // store data
        for (unsigned short i = 0; i < countOfItems; ++i) {
            success = s.addToEnd(data[i].value, data[i].useBits);
            REQUIRE( success == true);
        }


        // read data and test them
        ndxType bitIndex = s.getUsedBits() - 1;
        for (short i = countOfItems - 1; i >=0 ; --i) {
            success = s.readFromEndPosition(bitIndex, data[i].useBits, result);
            bitIndex -= data[i].useBits;
            printf("#%d, %d = %d (%d)\n", i, result, data[i].value, data[i].useBits);
            REQUIRE(success == true);
            REQUIRE(result == data[i].value);

        }

    }

}
