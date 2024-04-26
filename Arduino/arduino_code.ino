#include <Servo.h>

Servo servoDoor;
Servo servoParcel;

const int SERVO_DOOR_PIN = 9;
const int SERVO_PARCEL_PIN = 10;
const int BUZZER_PIN = 8;

char serialInput;

bool doorIsOpen = false;
bool doorIsClosedPerm = false;
bool parcelIsExpected = true;

void unlockDoor()
{
	if(!doorIsOpen && !doorIsClosedPerm)
	{
		for(int deg = 0 ; deg <= 90 ; deg += 10)
		{
			servoDoor.write(deg);
			delay(10);
		}
		
		doorIsOpen = true;
	}
}

void lockDoor()
{
	if(doorIsOpen)
	{
		for(int deg = 90 ; deg >= 0 ; deg -= 10)
		{
			servoDoor.write(deg);
			delay(10);
		}
		
		doorIsOpen = false;
	}
}

void unlockParcelBox()
{
	if(parcelIsExpected)
	{
		for(int deg = 0 ; deg <= 90 ; deg += 10)
		{
			servoParcel.write(deg);
			delay(10);
		}
		
		delay(5000);
		
		for(int deg = 90 ; deg >= 0 ; deg -= 10)
		{
			servoParcel.write(deg);
			delay(10);
		}
	}
}

void activateBuzzer()
{
	digitalWrite(BUZZER_PIN, HIGH);
	delay(3000);
	digitalWrite(BUZZER_PIN, LOW);
}

void setup()
{
	servoDoor.attach(SERVO_DOOR_PIN);
	servoParcel.attach(SERVO_PARCEL_PIN);
	
	pinMode(BUZZER_PIN, OUTPUT);
	
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
				activateBuzzer();
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
}
