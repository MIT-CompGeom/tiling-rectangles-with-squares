# Tiling Integer Rectangles with Integer Squares

Code for paper "When Can You Tile an Integer Rectangle with Integer Squares?"
by MIT CompGeom Group, Zachary Abel, Hugo A. Akitaya, Erik D. Demaine,
Adam C. Hesterberg, and Jayson Lynch

This software solves via brute force the problem of completely filling (tiling)
a rectangular board of given dimensions using nonoverlapping squares of
specified allowed sizes.

## Tilings

Here are the tilings found by the search up to 19×19
(drawn as SVGs by the code),
restricted to sizes where the numbers of rows and columns have a common divisor
*d*&nbsp;&gt;&nbsp;1; otherwise, it is easy to tile using *d*×*d* squares.

### 5×n

![5x6](output/5x6.svg)
![5x11](output/5x11.svg)
![5x12](output/5x12.svg)
![5x16](output/5x16.svg)
![5x17](output/5x17.svg)
![5x18](output/5x18.svg)

### 6×n

![6x7](output/6x7.svg)
![6x11](output/6x11.svg)
![6x13](output/6x13.svg)
![6x17](output/6x17.svg)
![6x19](output/6x19.svg)

### 7×n

![7x10](output/7x10.svg)
![7x12](output/7x12.svg)
![7x13](output/7x13.svg)
![7x16](output/7x16.svg)
![7x17](output/7x17.svg)
![7x18](output/7x18.svg)
![7x19](output/7x19.svg)

### 8×n

![8x15](output/8x15.svg)
![8x17](output/8x17.svg)
![8x19](output/8x19.svg)

### 9×n

![9x10](output/9x10.svg)
![9x13](output/9x13.svg)
![9x14](output/9x14.svg)
![9x16](output/9x16.svg)
![9x17](output/9x17.svg)
![9x19](output/9x19.svg)

### 10×n

![10x11](output/10x11.svg)
![10x13](output/10x13.svg)
![10x17](output/10x17.svg)
![10x19](output/10x19.svg)

### 11×n

![11x12](output/11x12.svg)
![11x13](output/11x13.svg)
![11x14](output/11x14.svg)
![11x15](output/11x15.svg)
![11x16](output/11x16.svg)
![11x17](output/11x17.svg)
![11x18](output/11x18.svg)
![11x19](output/11x19.svg)

### 12×n

![12x13](output/12x13.svg)
![12x17](output/12x17.svg)
![12x19](output/12x19.svg)

### 13×n

![13x14](output/13x14.svg)
![13x15](output/13x15.svg)
![13x16](output/13x16.svg)
![13x17](output/13x17.svg)
![13x18](output/13x18.svg)
![13x19](output/13x19.svg)

### 14×n

![14x15](output/14x15.svg)
![14x17](output/14x17.svg)
![14x19](output/14x19.svg)

### 15×n

![15x16](output/15x16.svg)
![15x17](output/15x17.svg)
![15x19](output/15x19.svg)

### 16×n

![16x17](output/16x17.svg)
![16x19](output/16x19.svg)

### 17×n

![17x18](output/17x18.svg)
![17x19](output/17x19.svg)

### 18×n

![18x19](output/18x19.svg)
