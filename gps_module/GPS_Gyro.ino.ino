// This code shows how to listen to the GPS module in an interrupt
// which allows the program to have more 'freedom' - just parse
// when a new NMEA sentence is available! Then access data when
// desired.

#include <SoftwareSerial.h>
#include <Wire.h>
#include <Adafruit_GPS.h>
#include <Adafruit_MMA8451.h>
#include <Adafruit_Sensor.h>

SoftwareSerial mySerial(3, 2); // (RX, TX)
SoftwareSerial OBDSerial(5, 4);

// GPS
Adafruit_GPS GPS(&mySerial);

// Gyro/Accel
Adafruit_MMA8451 mma = Adafruit_MMA8451();



// Set GPSECHO to 'false' to turn off echoing the GPS data to the Serial console
// Set to 'true' if you want to debug and listen to the raw GPS sentences. 
#define GPSECHO  false

// this keeps track of whether we're using the interrupt
// off by default!
boolean usingInterrupt = false;
void useInterrupt(boolean); // Func prototype keeps Arduino 0023 happy

void gpsSetup()
{
  // 9600 NMEA is the default baud rate for Adafruit MTK GPS's- some use 4800
  GPS.begin(9600);
  
  // uncomment this line to turn on RMC (recommended minimum) and GGA (fix data) including altitude
  GPS.sendCommand(PMTK_SET_NMEA_OUTPUT_RMCGGA);
  // uncomment this line to turn on only the "minimum recommended" data
  //GPS.sendCommand(PMTK_SET_NMEA_OUTPUT_RMCONLY);
  // For parsing data, we don't suggest using anything but either RMC only or RMC+GGA since
  // the parser doesn't care about other sentences at this time
  
  // Set the update rate
  GPS.sendCommand(PMTK_SET_NMEA_UPDATE_1HZ);   // 1 Hz update rate
  // For the parsing code to work nicely and have time to sort thru the data, and
  // print it out we don't suggest using anything higher than 1 Hz

  // Request updates on antenna status, comment out to keep quiet
  GPS.sendCommand(PGCMD_ANTENNA);

  // the nice thing about this code is you can have a timer0 interrupt go off
  // every 1 millisecond, and read data from the GPS for you. that makes the
  // loop code a heck of a lot easier!
  useInterrupt(true);
}

void gyroSetup() {  

  if (! mma.begin()) {
    Serial.println("Couldnt start gyro");
    while (1);
  }
  Serial.println("MMA8451 found!");
  
  mma.setRange(MMA8451_RANGE_2_G);
  
  Serial.print("Range = "); Serial.print(2 << mma.getRange());  
  Serial.println("G");
}

void setup()  
{
  Serial.begin(9600);
  
  gpsSetup();
  gyroSetup();

  
  delay(1000);
  
  // Ask for firmware version
  mySerial.println(PMTK_Q_RELEASE);
}


// Interrupt is called once a millisecond, looks for any new GPS data, and stores it
SIGNAL(TIMER0_COMPA_vect) {
  char c = GPS.read();
  // if you want to debug, this is a good time to do it!
#ifdef UDR0
  if (GPSECHO)
    if (c) UDR0 = c;  
    // writing direct to UDR0 is much much faster than Serial.print 
    // but only one character can be written at a time. 
#endif
}

void useInterrupt(boolean v) {
  if (v) {
    // Timer0 is already used for millis() - we'll just interrupt somewhere
    // in the middle and call the "Compare A" function above
    OCR0A = 0xAF;
    TIMSK0 |= _BV(OCIE0A);
    usingInterrupt = true;
  } else {
    // do not call the interrupt function COMPA anymore
    TIMSK0 &= ~_BV(OCIE0A);
    usingInterrupt = false;
  }
}

//
// Set up data string to send
//
char dataString[128];
char lat[16], lon[16];


uint32_t timer = millis();
bool doGPS() {
  // in case you are not using the interrupt above, you'll
  // need to 'hand query' the GPS, not suggested :(
  if (! usingInterrupt) {
    // read data from the GPS in the 'main loop'
    char c = GPS.read();
    // if you want to debug, this is a good time to do it!
    if (GPSECHO)
      if (c) Serial.print(c);
  }
  
  // if a sentence is received, we can check the checksum, parse it...
  if (GPS.newNMEAreceived()) {
    // a tricky thing here is if we print the NMEA sentence, or data
    // we end up not listening and catching other sentences! 
    // so be very wary if using OUTPUT_ALLDATA and trytng to print out data
    //Serial.println(GPS.lastNMEA());   // this also sets the newNMEAreceived() flag to false
  
    if (!GPS.parse(GPS.lastNMEA()))   // this also sets the newNMEAreceived() flag to false
      return;  // we can fail to parse a sentence in which case we should just wait for another
  }

  // if millis() or timer wraps around, we'll just reset it
  if (timer > millis())  timer = millis();

  // approximately every 2 seconds or so, print out the current stats
  if (millis() - timer > 2000) { 
    timer = millis(); // reset the timer

    //strcpy(dataString, GPS.hour);
    //char temp[16]; 

    dtostrf(41.8658728, 4, 4, lat);
    dtostrf(-87.6461332, 4, 4, lon);

    return true;
  }
  return false;
}

void doGyro() {
  // Read the 'raw' data in 14-bit counts
  mma.read();

  char temp[8];

  /* Get a new sensor event */ 
  sensors_event_t event; 
  mma.getEvent(&event);

  /* Store the results (acceleration is measured in m/s^2) */

  dtostrf(event.acceleration.x, 4, 4, temp);
  strcat(dataString, temp);
  strcat(dataString, ";");

  dtostrf(event.acceleration.y, 4, 4, temp);
  strcat(dataString, temp);
  strcat(dataString, ";");

  dtostrf(event.acceleration.z, 4, 4, temp);
  strcat(dataString, temp);
  strcat(dataString, ";");
}

void loop()                     // run over and over again
{
  for (int i = 0; i < sizeof(dataString); i++) 
    dataString[0] = '\0';

  doGPS();
  strcat(dataString, lat);
  strcat(dataString, ";");

  strcat(dataString, lon);
  strcat(dataString, ";");
  
  doGyro();
  
  //Serial.write('<');

  int size = sizeof(dataString);
  for (int i = 0; i < size; i++) {
    Serial.write(dataString[i]);
  }

  //Serial.write('>');
  Serial.write('\n');
}





















