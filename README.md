<h1 align = "center">
  
<img src = "https://github.com/Omanshu209/Securo-IoT/assets/114089324/46b3fcf6-4743-4736-9047-dcfc68fd1823" align = "left" height = 75>
</img>
Securo
<img src = "https://github.com/Omanshu209/Securo-IoT/assets/114089324/46b3fcf6-4743-4736-9047-dcfc68fd1823" align = "right" height = 75>
</img>

</h1>

<!-- ![IMG_20240430_220036](https://github.com/Omanshu209/Securo/assets/114089324/1b1eac7a-3e82-452f-8958-99c4051f9485)
![IMG_20240430_215654](https://github.com/Omanshu209/Securo/assets/114089324/7ffacae7-c7b7-46f0-8727-b15dcd60b207) -->

![](https://github.com/Omanshu209/Securo-IoT/assets/114089324/524968c7-f212-482d-93c6-7298a844aef0)

## Components

```
1) Arduino Uno --------------------|
2) Breadboard  --------------------|  
3) HC-SR04 Ultrasonic Sensor ------|---> 1 (each)
4) Buzzer      --------------------|

5) LEDs (Green) -------------------|
6) LEDs (Red)   -------------------|---> 2 (each)
7) Servo Motors -------------------|

8) Jumper Wires
```

## Circuit

```
                            |--- VCC  ---> 5v  (Arduino)
                            |
                            |--- ECHO ---> 6   (Arduino)
                            |
HC-SR04 Ultrasonic Sensor --|
                            |
                            |--- TRIG ---> 7   (Arduino)
                            |
                            |--- GND  ---> GND (Arduino)



                    |---- + ---> 4   (Arduino)
                    |            
LED (Door, Green) --|
                    |
                    |-- - -----> GND (Arduino)



         |---- + ---> 8   (Arduino)
         |
Buzzer --|
         |
         |-- - -----> GND (Arduino)



                        |---- + ---> 12  (Arduino)
                        |            
LED (Parcel Box, Red) --|
                        |
                        |-- - -----> GND (Arduino)



                     |---> 5v  (Arduino)
                     |
Servo Motor (Door) --|---> 9   (Arduino)
                     |
                     |---> GND (Arduino)



                          |---- + ---> 11  (Arduino)
                          |            
LED (Parcel Box, Green) --|
                          |
                          |-- - -----> GND (Arduino)



                           |---> 5v  (Arduino)
                           |
Servo Motor (Parcel Box) --|---> 10  (Arduino)
                           |
                           |---> GND (Arduino)



                  |---- + ---> 5   (Arduino)
                  |            
LED (Door, Red) --|
                  |
                  |-- - -----> GND (Arduino)
```
