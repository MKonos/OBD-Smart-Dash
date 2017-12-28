/*************************************************************************
* Simple OBD Data Display
* Works with any Arduino board connected with SH1106 128*64 I2C OLED and
* Written by Michael Koutsostamatis <mkouts2@uic.edu>
*************************************************************************/

#include <Wire.h>
#include <OBD2UART.h>
#include <MicroLCD.h>
#include <LiquidCrystal.h>
#include <SoftwareSerial.h>

const int rs = 12, en = 11, d4 = 5, d5 = 4, d6 = 3, d7 = 2;
LiquidCrystal lcd(rs, en, d4, d5, d6, d7);

SoftwareSerial dataCom(9, 8);

int values[] = {0,0,0,0,0,0,0,0,0};

//LCD_SH1106 lcd;
COBD obd;

void reconnect()
{
  //lcd.clear();
  lcd.setCursor(0, 0);

  lcd.print("Reconnecting");
  //digitalWrite(SD_CS_PIN, LOW);
  
  for (uint16_t i = 0; !obd.init(); i++) 
  {
    if (i == 5) 
    {
      lcd.clear();
    }
    delay(3000);
  }
}

void updateArray(byte pid, int value)
{

  switch (pid) 
  {
    case PID_RPM:
      values[0] = value;
      break;
      
    case PID_THROTTLE:
      values[1] = value;
      break;
    
    case PID_SPEED:
      values[2] = value * 0.621371;
      break;
    
    case PID_COOLANT_TEMP:
      values[3] = value;
      break;

    case PID_INTAKE_TEMP:
      values[4] = value;
      break;

    case PID_ENGINE_OIL_TEMP:
      values[5] = value;
      break;

    case PID_MAF_FLOW:
      values[6] = value;
      break;

    case PID_ENGINE_TORQUE_PERCENTAGE:
      values[7] = value;
      break;
  }
}

void dispatchData(uint16_t *codes)
{
  char temp[8], dataString[8];
    
  lcd.print(values[0]);
  lcd.print("  ");
  lcd.print(values[1]);
  lcd.print("  ");
  lcd.print(values[2]);
  lcd.print("  ");
  lcd.print(values[3]);
  lcd.print("  ");

  

  itoa(values[0], temp, 10);
  strcpy(dataString, temp);
  strcat(dataString, ";");
  dataCom.write(dataString);

  itoa(values[1], temp, 10);
  strcpy(dataString, temp);
  strcat(dataString, ";");
  dataCom.write(dataString);

  itoa(values[2], temp, 10);
  strcpy(dataString, temp);
  strcat(dataString, ";");
  dataCom.write(dataString);

  itoa(values[3], temp, 10);
  strcpy(dataString, temp);
  strcat(dataString, ";");
  dataCom.write(dataString);

  itoa(values[4], temp, 10);
  strcpy(dataString, temp);
  strcat(dataString, ";");
  dataCom.write(dataString);

  itoa(values[5], temp, 10);
  strcpy(dataString, temp);
  strcat(dataString, ";");
  dataCom.write(dataString);

  itoa(values[6], temp, 10);
  strcpy(dataString, temp);
  strcat(dataString, ";");
  dataCom.write(dataString);

  itoa(values[7], temp, 10);
  strcpy(dataString, temp);
  strcat(dataString, ";");
  dataCom.write(dataString);

  itoa(codes[0], temp, 10);
  strcpy(dataString, temp);
  strcat(dataString, ";");
  dataCom.write(dataString);

  dataCom.write('\n');

/*
  values[0]++;
  values[1]++;
  values[2]++;
  values[3]++;
  values[4]++;
  values[5]++;
  values[6]++;
  values[7]++;
  codes[0]++;
  */
}

void initScreen()
{
  lcd.clear();
  lcd.setCursor(0, 1);
  
}

void setup()
{
  Serial.begin(9600);
  dataCom.begin(9600);

  lcd.begin(16, 2);
  lcd.println("OBD DISPLAY"); 

  delay(500);
  obd.begin();

  //lcd.setCursor(0, 0);
  lcd.println("Connecting...");
  
  //OBD
  
  while (!obd.init())
  {
    initScreen();
  }
  
  
  delay(100);
}

void loop()
{ 
  /*
  Engine
  PID_RPM – Engine RPM (rpm) 
  PID_ENGINE_LOAD – Calculated engine load (%)
  PID_COOLANT_TEMP – Engine coolant temperature (°C)
  PID_ENGINE_LOAD – Calculated Engine load (%)
  PID_ABSOLUTE_ENGINE_LOAD – Absolute Engine load (%)
  PID_TIMING_ADVANCE – Ignition timing advance (°)
  PID_ENGINE_OIL_TEMP – Engine oil temperature (°C)
  PID_ENGINE_TORQUE_PERCENTAGE – Engine torque percentage (%)
  PID_ENGINE_REF_TORQUE – Engine reference torque (Nm)
  
  Intake/Exhaust
  PID_INTAKE_TEMP – Intake temperature (°C)
  PID_INTAKE_PRESSURE – Intake manifold absolute pressure (kPa)
  PID_MAF_FLOW – MAF flow pressure (grams/s)
  PID_BAROMETRIC – Barometric pressure (kPa)
  
  Speed/Time
  PID_SPEED – Vehicle speed (km/h)
  PID_RUNTIME – Engine running time (second)
  PID_DISTANCE – Vehicle running distance (km)
  
  Driver
  PID_THROTTLE – Throttle position (%)
  PID_AMBIENT_TEMP – Ambient temperature (°C)
    
  Electric Systems
  PID_CONTROL_MODULE_VOLTAGE – vehicle control module voltage (V)
  PID_HYBRID_BATTERY_PERCENTAGE – Hybrid battery pack remaining life (%)
  */
   
  static byte pids[]= {PID_RPM, PID_THROTTLE, PID_SPEED, PID_COOLANT_TEMP, PID_INTAKE_TEMP, PID_MAF_FLOW};
    //static byte pids[]= {PID_RPM, PID_THROTTLE, PID_SPEED, PID_COOLANT_TEMP, PID_INTAKE_TEMP};
  uint16_t codes{0}; 
  byte maxCodes = 1;

  static byte index = 0;
  byte pid = pids[index];
  int value;

  //OBD
  
  //obd.readDTC(codes, maxCodes);
  
  // send a query to OBD adapter for specified OBD-II pid
  if (obd.readPID(pid, value)) {
      lcd.clear();
      updateArray(pid, value);
  }
  index = (index + 1) % sizeof(pids);
  
  
  dispatchData(codes);
    
  //OBD
  
  if (obd.errors >= 2) {
      reconnect();
      setup();
  }

  lcd.setCursor(0,0);

  //delay(100);
}
