#include <Servo.h>

Servo servoDoor;
Servo servoParcel;

const int SERVO_DOOR_PIN = 9;
const int SERVO_PARCEL_PIN = 10;
const int BUZZER_PIN = 8;
const int ECHO_PIN = 6;
const int TRIGGER_PIN = 7;
const int LED_DOOR_GREEN_PIN = 4;
const int LED_DOOR_RED_PIN = 5;
const int LED_PARCEL_GREEN_PIN = 11;
const int LED_PARCEL_RED_PIN = 12;

char serialInput;
long time, distance;

bool doorIsOpen = false;
bool doorIsClosedPerm = false;
bool parcelIsExpected = true;

void unlockDoor()
{
  if(!doorIsOpen && !doorIsClosedPerm)
  {
    for(int deg = 0 ; deg <= 90 ; deg += 1)
    {
      servoDoor.write(deg);
      delay(10);
    }
    
    digitalWrite(LED_DOOR_GREEN_PIN, HIGH);
    digitalWrite(LED_DOOR_RED_PIN, LOW);
    doorIsOpen = true;
  }
}

void lockDoor()
{
  if(doorIsOpen)
  {
    for(int deg = 90 ; deg >= 0 ; deg -= 1)
    {
      servoDoor.write(deg);
      delay(10);
    }
    
    digitalWrite(LED_DOOR_GREEN_PIN, LOW);
    digitalWrite(LED_DOOR_RED_PIN, HIGH);
    doorIsOpen = false;
  }
}

void unlockParcelBox()
{
  if(parcelIsExpected)
  {
    for(int deg = 0 ; deg <= 90 ; deg += 1)
    {
      servoParcel.write(deg);
      delay(10);
    }
    
    digitalWrite(LED_PARCEL_GREEN_PIN, HIGH);
    digitalWrite(LED_PARCEL_RED_PIN, LOW);
    
    delay(5000);
    
    for(int deg = 90 ; deg >= 0 ; deg -= 1)
    {
      servoParcel.write(deg);
      delay(10);
    }
    
    digitalWrite(LED_PARCEL_GREEN_PIN, LOW);
    digitalWrite(LED_PARCEL_RED_PIN, HIGH);
  }
}

void activateBuzzer(int duration)
{
  digitalWrite(BUZZER_PIN, HIGH);
  delay(duration);
  digitalWrite(BUZZER_PIN, LOW);
}

int measureDoorDistance()
{
  digitalWrite(TRIGGER_PIN, LOW);
  delayMicroseconds(2);
  
  digitalWrite(TRIGGER_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIGGER_PIN, LOW);
  
  time = pulseIn(ECHO_PIN, HIGH);
  distance = time * 0.0343 / 2; // Unit -> centimeters
  return distance;
}

void setup()
{
  servoDoor.attach(SERVO_DOOR_PIN);
  servoParcel.attach(SERVO_PARCEL_PIN);
  
  pinMode(BUZZER_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);
  pinMode(TRIGGER_PIN, OUTPUT);
  pinMode(LED_DOOR_GREEN_PIN, OUTPUT);
  pinMode(LED_DOOR_RED_PIN, OUTPUT);
  pinMode(LED_PARCEL_GREEN_PIN, OUTPUT);
  pinMode(LED_PARCEL_RED_PIN, OUTPUT);

  digitalWrite(LED_DOOR_RED_PIN, HIGH);
  digitalWrite(LED_PARCEL_RED_PIN, HIGH);

  servoDoor.write(0);
  servoParcel.write(0);
  
  Serial.begin(9600);
}

void loop()
{
  if(Serial.available())
  {
    serialInput = Serial.read();
    
    switch(serialInput)
    {
      case '0':
        lockDoor();
        break;
      
      case '1':
        unlockDoor();
        break;
      
      case '2':
        lockDoor();
        break;
      
      case '3':
        activateBuzzer(3000);
        break;
      
      case '4':
        doorIsClosedPerm = !doorIsClosedPerm;
        break;
      
      case '5':
        parcelIsExpected = !parcelIsExpected;
        break;
      
      case '6':
        doorIsClosedPerm = !doorIsClosedPerm;
        parcelIsExpected = !parcelIsExpected;
        break;
      
      case '7':
        unlockDoor();
        delay(5000);
        lockDoor();
        break;
      
      case '8':
        unlockParcelBox();
        break;
    }
  }
  
  distance = measureDoorDistance();
  if(distance <= 7 && !doorIsOpen && distance != 0)
    activateBuzzer(100);
}
