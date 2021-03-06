#include <stdio.h>
#include <stdlib.h>

int getIndex(int row, int col, int numCol)
{
    return row * numCol + col;
}
void cfun(const void * indatav, int rowcount, int colcount, void * outdatav, int R) {
//    void cfun(const double * indata, int rowcount, int colcount, double * outdata) {
    const double * indata = (double *) indatav;
    double * outdata = (double *) outdatav;
    int row,col;

    short pixel7,pixel6,pixel5,pixel4,pixel3,pixel2,pixel1,pixel0;
    for (row = R; row < rowcount-R ; ++row) {

        for(col = R ; col <  colcount-R ; ++col)
        {

            int index = row*colcount+col;
            double center_point = indata[index];;
            pixel7 = (indata[getIndex(row - R , col , colcount)] > center_point)? 1 : 0 ;
            pixel6 = (indata[getIndex(row - R , col-R , colcount)] > center_point)? 1 : 0 ;
            pixel5 = (indata[getIndex(row, col- R , colcount)] > center_point)? 1 : 0 ;
            pixel4 = (indata[getIndex(row + R , col- R , colcount)] > center_point)? 1 : 0 ;
            pixel3 = (indata[getIndex(row + R , col , colcount)] > center_point)? 1 : 0 ;
            pixel2 = (indata[getIndex(row + R , col+R , colcount)] > center_point)? 1 : 0 ;
            pixel1 = (indata[getIndex(row  , col+R , colcount)] > center_point)? 1 : 0 ;
            pixel0 = (indata[getIndex(row -R , col+R , colcount)] > center_point)? 1 : 0 ;


            center_point = pixel7 * 128 + pixel6 * 64 + pixel5 * 32 + pixel4 * 16 + \
                            pixel3 * 8 + pixel2 * 4 + pixel1 * 2 + pixel0 * 1;

            outdata[index] = center_point;
        }

    }

}


