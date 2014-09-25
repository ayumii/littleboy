
#include <avr/io.h>

#define echoPin A0 // Echo Pin
#define trigPin A1 // Trigger Pin

/**void setup() {
  // initialize serial communication:
  Serial.begin(9600);
} **/

void loop()
{
 
  long duration, inches, cm;

  // The ultrasound is triggered by a HIGH pulse of 2 or more microseconds.
  // Give a short LOW pulse beforehand to ensure a clean HIGH pulse:
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);

  digitalWrite(trigPin, HIGH);
  delayMicroseconds(5);
  
  digitalWrite(trigPin, LOW);
  
  duration = pulseIn(echoPin, HIGH);
  
  // The same pin is used to read the signal from the ultrasound: a HIGH
  // pulse whose duration is the time (in microseconds) from the sending
  // of the ping to the reception of its echo off of an object.
  //pinMode(pingPin, INPUT);
  //duration = pulseIn(pingPin, HIGH);

  // convert the time into a distance
  inches = microsecondsToInches(duration);
  cm = microsecondsToCentimeters(duration);
  
  cout<<inches<<" inches  ";
  cout<<cm<<" cm  ";

  
  delay(100);
}

long microsecondsToInches(long microseconds)
{
  // According to Parallax's datasheet, there are
  // 73.746 microseconds per inch (i.e. sound travels at 1130 feet per
  // second).  This gives the distance travelled by the ping, outbound
  // and return, so we divide by 2 to get the distance of the obstacle.

  return microseconds / 74 / 2;
}

long microsecondsToCentimeters(long microseconds)
{
  // The speed of sound is 340 m/s or 29 microseconds per centimeter.
  // The ping travels out and back, so to find the distance of the
  // object we take half of the distance travelled.
  return microseconds / 29 / 2;
}


int main(void)
{
	while(1)
	{
		//TODO:: Please write your application code
		loop();
	}
}